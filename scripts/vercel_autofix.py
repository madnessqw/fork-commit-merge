#!/usr/bin/env python3
"""Automated diagnosis and fix suggestions for unhealthy Vercel products.

Reads STATE_SUMMARY.json, probes unhealthy / canonical-drift products,
inspects local product source files, and produces actionable fix plans
with concrete commands and file changes.

Usage:
    python3 scripts/vercel_autofix.py                    # full diagnosis
    python3 scripts/vercel_autofix.py --slug jwt         # single product
    python3 scripts/vercel_autofix.py --apply            # apply safe fixes
    python3 scripts/vercel_autofix.py --json             # machine-readable
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.retry_probe import probe_url
from scripts.summary_visibility import canonical_drift_entries
from scripts.unhealthy_triage import (
    TRIAGE_RULES,
    sort_by_severity,
    generate_triage,
    VERCEL_FIX_COMMANDS,
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


DIAGNOSIS_RULES = {
    401: {
        "root_cause": "Vercel Authentication / SSO Protection enabled",
        "file_check": "vercel.json",
        "fix_type": "vercel_settings",
        "auto_fixable": False,
        "fix_steps": [
            "Open Vercel dashboard → project Settings → Deployment Protection",
            "Disable 'Vercel Authentication'",
            "Redeploy: cd products/{slug} && vercel --prod --yes",
        ],
    },
    402: {
        "root_cause": "Deployment disabled (billing or plan limit)",
        "file_check": None,
        "fix_type": "billing",
        "auto_fixable": False,
        "fix_steps": [
            "Check Vercel billing status",
            "Verify project is not paused",
            "Redeploy if needed",
        ],
    },
    404: {
        "root_cause": "Project not deployed or wrong slug",
        "file_check": "vercel.json",
        "fix_type": "redeploy",
        "auto_fixable": True,
        "fix_steps": [
            "Verify project files exist locally",
            "Deploy: cd products/{slug} && vercel --prod --yes",
        ],
    },
    429: {
        "root_cause": "Rate limited by Vercel",
        "file_check": None,
        "fix_type": "wait",
        "auto_fixable": False,
        "fix_steps": ["Wait for rate limit to reset", "Reduce concurrent deployments"],
    },
    451: {
        "root_cause": "Geo-blocked by Vercel Firewall",
        "file_check": "vercel.json",
        "fix_type": "firewall",
        "auto_fixable": False,
        "fix_steps": [
            "Check Vercel Firewall rules → project Settings → Firewall",
            "Remove or modify geo-blocking rules",
            "Whitelist necessary regions",
        ],
    },
    500: {
        "root_cause": "Server error — build or runtime failure",
        "file_check": "api/",
        "fix_type": "code_fix",
        "auto_fixable": True,
        "fix_steps": [
            "Check Vercel deployment logs",
            "Inspect api/ directory for runtime errors",
            "Fix code and redeploy",
        ],
    },
    0: {
        "root_cause": "Connection timeout or DNS failure",
        "file_check": None,
        "fix_type": "network",
        "auto_fixable": False,
        "fix_steps": ["Verify DNS resolution", "Check network connectivity"],
    },
}


def _inspect_product_dir(slug: str) -> dict:
    product_dir = ROOT / "products" / slug
    if not product_dir.is_dir():
        return {"exists": False, "slug": slug}

    files = [f.name for f in product_dir.iterdir()]
    has_vercel_json = "vercel.json" in files
    has_package_json = "package.json" in files
    has_api_dir = (product_dir / "api").is_dir()
    has_index_html = "index.html" in files

    api_files = []
    if has_api_dir:
        api_files = [f.name for f in (product_dir / "api").iterdir() if f.is_file()]

    vercel_config = {}
    if has_vercel_json:
        try:
            vercel_config = json.loads((product_dir / "vercel.json").read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    has_builds = bool(vercel_config.get("builds"))
    has_routes = bool(vercel_config.get("routes"))
    has_rewrites = bool(vercel_config.get("rewrites"))
    uses_routes_not_rewrites = has_routes and not has_rewrites

    config_issues = []
    if uses_routes_not_rewrites:
        config_issues.append("uses_deprecated_routes")
    if has_builds and not has_api_dir:
        config_issues.append("builds_without_api")
    if not has_index_html and not has_api_dir:
        config_issues.append("no_entry_point")

    package_info = {}
    if has_package_json:
        try:
            pkg = json.loads((product_dir / "package.json").read_text(encoding="utf-8"))
            package_info = {
                "name": pkg.get("name", ""),
                "dependencies": list(pkg.get("dependencies", {}).keys()),
                "dev_dependencies": list(pkg.get("devDependencies", {}).keys()),
            }
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "exists": True,
        "slug": slug,
        "files": sorted(files),
        "has_vercel_json": has_vercel_json,
        "has_package_json": has_package_json,
        "has_api_dir": has_api_dir,
        "has_index_html": has_index_html,
        "api_files": sorted(api_files),
        "vercel_config": vercel_config,
        "config_issues": config_issues,
        "uses_deprecated_routes": uses_routes_not_rewrites,
        "package_info": package_info,
    }


def _check_api_health(slug: str, inspection: dict) -> dict:
    if not inspection.get("has_api_dir") or not inspection.get("api_files"):
        return {"has_health_endpoint": False}

    has_health = "health.js" in inspection.get("api_files", [])
    health_url = f"https://{slug}.vercel.app/api/health" if has_health else None
    health_result = None

    if health_url:
        probe = probe_url(health_url)
        health_result = {
            "url": health_url,
            "code": probe["code"],
            "healthy": probe["code"] == 200,
        }

    return {
        "has_health_endpoint": has_health,
        "health_check": health_result,
    }


def diagnose_product(slug: str, code: int, url: str) -> dict:
    rule = DIAGNOSIS_RULES.get(code, {
        "root_cause": f"Unknown error (HTTP {code})",
        "fix_type": "investigate",
        "auto_fixable": False,
        "fix_steps": ["Investigate manually"],
    })

    inspection = _inspect_product_dir(slug)
    api_health = _check_api_health(slug, inspection)

    config_fix = None
    if inspection.get("uses_deprecated_routes") and code in (500, 404):
        config_fix = {
            "type": "migrate_routes_to_rewrites",
            "description": "vercel.json uses deprecated 'routes' — migrate to 'rewrites'",
            "auto_apply": True,
        }

    fix_steps = [
        step.replace("{slug}", slug) for step in rule.get("fix_steps", [])
    ]

    return {
        "slug": slug,
        "http_code": code,
        "url": url,
        "root_cause": rule["root_cause"],
        "fix_type": rule["fix_type"],
        "auto_fixable": rule.get("auto_fixable", False),
        "fix_steps": fix_steps,
        "inspection": inspection,
        "api_health": api_health,
        "config_fix": config_fix,
        "diagnosed_at": _utc_now_iso(),
    }


def autofix_deprecated_routes(slug: str) -> dict | None:
    product_dir = ROOT / "products" / slug
    vercel_json_path = product_dir / "vercel.json"
    if not vercel_json_path.exists():
        return None

    try:
        config = json.loads(vercel_json_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    routes = config.get("routes", [])
    if not routes:
        return None

    rewrites = []
    for route in routes:
        src = route.get("src", route.get("source", ""))
        dest = route.get("dest", route.get("destination", ""))
        if src and dest:
            rewrites.append({"source": src, "destination": dest})

    if not rewrites:
        return None

    config.pop("routes", None)
    existing_rewrites = config.get("rewrites", [])
    config["rewrites"] = existing_rewrites + rewrites

    vercel_json_path.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "slug": slug,
        "fix": "migrated routes → rewrites in vercel.json",
        "routes_count": len(routes),
        "rewrites_count": len(config["rewrites"]),
    }


def run_autofix(
    summary_path: Path | None = None,
    slug_filter: str = "",
    apply: bool = False,
    dry_run: bool = False,
) -> list[dict]:
    if summary_path is None:
        summary_path = ROOT / "STATE_SUMMARY.json"

    with open(summary_path, encoding="utf-8") as f:
        summary = json.load(f)

    targets: list[dict] = []
    gaps = summary.get("gaps", {})

    for item in gaps.get("unhealthy_live", []):
        slug = item.get("slug", "")
        if slug_filter and slug_filter not in slug:
            continue
        targets.append({
            "slug": slug,
            "code": item.get("code", 0),
            "url": item.get("url", f"https://{slug}.vercel.app"),
        })

    for item in canonical_drift_entries(summary):
        slug = item.get("slug", "")
        if slug_filter and slug_filter not in slug:
            continue
        code = item.get("canonical_code", 0)
        targets.append({
            "slug": slug,
            "code": code,
            "url": item.get("ideal_url", f"https://{slug}.vercel.app"),
        })

    if not targets:
        return []

    results: list[dict] = []

    def _diagnose_one(target: dict) -> dict:
        slug = target["slug"]
        code = target.get("code", 0)
        url = target.get("url", f"https://{slug}.vercel.app")

        fresh_probe = probe_url(url)
        diagnosis = diagnose_product(slug, fresh_probe["code"], url)
        diagnosis["prior_code"] = code
        diagnosis["current_code"] = fresh_probe["code"]
        diagnosis["recovered"] = fresh_probe["code"] == 200 and code != 200

        config_fix = diagnosis.get("config_fix") or {}
        if dry_run and config_fix.get("auto_apply"):
            diagnosis["would_apply"] = {
                "slug": slug,
                "fix": "migrated routes → rewrites in vercel.json",
                "dry_run": True,
            }
        elif apply and config_fix.get("auto_apply"):
            fix_result = autofix_deprecated_routes(slug)
            if fix_result:
                diagnosis["applied_fix"] = fix_result

        return diagnosis

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(_diagnose_one, t): t for t in targets}
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda r: (0 if r.get("recovered") else 1, str(r["slug"])))
    return results


def format_report(results: list[dict], *, compact: bool = False) -> str:
    if not results:
        return "All products healthy — no autofix needed."

    lines = [
        "# Vercel AutoFix Report",
        f"**Generated:** {_utc_now_iso()}",
        f"**Diagnosed:** {len(results)}",
        "",
    ]

    recovered = sum(1 for r in results if r.get("recovered"))
    auto_fixable = sum(1 for r in results if r.get("auto_fixable"))
    applied = sum(1 for r in results if r.get("applied_fix"))
    would_apply = sum(1 for r in results if r.get("would_apply"))

    if compact:
        slugs_by_code: dict[str, list[str]] = {}
        for r in results:
            code = str(r.get("current_code", "?"))
            slugs_by_code.setdefault(code, []).append(r["slug"])
        lines.append(f"**Recovered:** {recovered} | **Fixable:** {auto_fixable} | **Would apply:** {would_apply}")
        lines.append("")
        for code in sorted(slugs_by_code):
            lines.append(f"- HTTP {code}: {', '.join(slugs_by_code[code])}")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"**Recovered:** {recovered} | **Auto-fixable:** {auto_fixable} | **Applied:** {applied}")
    lines.append("")

    for r in results:
        status_icon = "RECOVERED" if r.get("recovered") else f"HTTP {r.get('current_code', '?')}"
        lines.append(f"## {r['slug']} — {status_icon}")
        lines.append(f"- **Root cause:** {r.get('root_cause', 'unknown')}")
        lines.append(f"- **URL:** `{r.get('url', '')}`")
        lines.append(f"- **Prior code:** {r.get('prior_code', '?')} → **Current:** {r.get('current_code', '?')}")

        inspection = r.get("inspection", {})
        if inspection.get("exists"):
            issues = inspection.get("config_issues", [])
            if issues:
                lines.append(f"- **Config issues:** {', '.join(issues)}")
            if inspection.get("has_api_dir"):
                lines.append(f"- **API files:** {', '.join(inspection.get('api_files', []))}")

        api_h = r.get("api_health", {})
        if api_h.get("health_check"):
            hc = api_h["health_check"]
            lines.append(f"- **Health endpoint:** {hc['url']} → HTTP {hc['code']}")

        if r.get("applied_fix"):
            lines.append(f"- **Applied fix:** {r['applied_fix']['fix']}")
        if r.get("would_apply"):
            lines.append(f"- **Would apply (dry-run):** {r['would_apply']['fix']}")

        fix_steps = r.get("fix_steps", [])
        if fix_steps and not r.get("recovered"):
            lines.append("- **Fix steps:**")
            for step in fix_steps:
                lines.append(f"  1. {step}")

        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="AutoFix unhealthy Vercel products")
    parser.add_argument("--slug", default="", help="Filter by slug substring")
    parser.add_argument("--apply", action="store_true", help="Apply safe fixes")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run", help="Preview fixes without applying")
    parser.add_argument("--compact", action="store_true", help="Compact summary output")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--output", default="", help="Write report to file")
    args = parser.parse_args()

    results = run_autofix(slug_filter=args.slug, apply=args.apply, dry_run=args.dry_run)

    if args.as_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        report = format_report(results, compact=args.compact)
        print(report)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(report, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
