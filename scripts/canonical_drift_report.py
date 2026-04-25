#!/usr/bin/env python3
"""Generate Codex-ready fix plan for canonical URL drift products.

Reads STATE.json for full product details, diagnoses each drift product
by canonical HTTP code, and outputs concrete Vercel CLI commands.

Usage:
    python3 scripts/canonical_drift_report.py                # Markdown to stdout
    python3 scripts/canonical_drift_report.py --json          # JSON to stdout
    python3 scripts/canonical_drift_report.py --write         # Write to analysis/canonical_drift_plan.md
    python3 scripts/canonical_drift_report.py --apply-brief   # Write codex_task.md handoff
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

STATE_PATH = ROOT / "STATE.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
OUTPUT_PATH = ROOT / "analysis" / "canonical_drift_plan.md"
CODEX_TASK_PATH = ROOT / "analysis" / "codex_task.md"

DIAGNOSIS_MAP: dict[int, dict] = {
    200: {"label": "ok", "severity": "info", "fix": "No fix needed"},
    301: {"label": "permanent_redirect", "severity": "low", "fix": "Update vercel_url alias or accept redirect"},
    302: {"label": "temporary_redirect", "severity": "low", "fix": "Check Vercel project redirect rules"},
    307: {"label": "temporary_redirect", "severity": "low", "fix": "Alias redirect — redeploy canonical slug via: cd products/{slug} && vercel --prod --yes"},
    401: {"label": "sso_protection", "severity": "high", "fix": "Disable Vercel Authentication in project settings"},
    402: {"label": "billing_issue", "severity": "high", "fix": "Check Vercel billing — project may be suspended; redeploy: cd products/{slug} && vercel --prod --yes"},
    404: {"label": "not_found", "severity": "high", "fix": "Project not linked — link and deploy: cd products/{slug} && vercel link --yes && vercel --prod --yes"},
    500: {"label": "server_error", "severity": "high", "fix": "Check build logs — redeploy: cd products/{slug} && vercel --prod --yes"},
    502: {"label": "bad_gateway", "severity": "high", "fix": "Upstream error — redeploy: cd products/{slug} && vercel --prod --yes"},
    0: {"label": "timeout", "severity": "medium", "fix": "DNS or network issue — verify domain and retry"},
}

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def _normalize_url(val: str | None) -> str:
    if not val:
        return ""
    return str(val).strip().rstrip("/")


def load_drift_from_summary(summary_path: Path = SUMMARY_PATH) -> list[dict]:
    try:
        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

    drift_entries = summary.get("gaps", {}).get("canonical_url_drift", [])
    results: list[dict] = []
    for d in drift_entries:
        canonical_code = d.get("canonical_code", 0)
        diagnosis = DIAGNOSIS_MAP.get(canonical_code, {
            "label": f"error_{canonical_code}",
            "severity": "medium",
            "fix": f"Investigate HTTP {canonical_code} on canonical URL",
        })
        results.append({
            "slug": d.get("slug", ""),
            "name": d.get("slug", ""),
            "vercel_url": _normalize_url(d.get("url")),
            "ideal_vercel_url": _normalize_url(d.get("ideal_url")),
            "canonical_health_url": _normalize_url(d.get("canonical_url")),
            "canonical_health_code": canonical_code,
            "canonical_health_status": d.get("canonical_status", "unknown"),
            "last_health_code": d.get("health_code", 0),
            "checkout_url": "",
            "checkout_status": "unknown",
            "diagnosis_label": diagnosis["label"],
            "severity": diagnosis["severity"],
            "fix_command": diagnosis["fix"].format(slug=d.get("slug", "")),
        })

    results.sort(key=lambda r: SEVERITY_ORDER.get(r["severity"], 2))
    return results


def load_drift_products(state_path: Path = STATE_PATH) -> list[dict]:
    try:
        with open(state_path, encoding="utf-8") as f:
            state = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

    drift_slugs = state.get("canonical_url_drift_products", [])
    products = state.get("products", {}).get("active", [])
    slug_set = set(drift_slugs)

    results: list[dict] = []
    for p in products:
        slug = p.get("slug", "")
        if slug not in slug_set:
            continue
        canonical_code = p.get("canonical_health_code", 0)
        diagnosis = DIAGNOSIS_MAP.get(canonical_code, {
            "label": f"error_{canonical_code}",
            "severity": "medium",
            "fix": f"Investigate HTTP {canonical_code} on canonical URL",
        })

        results.append({
            "slug": slug,
            "name": p.get("name", slug),
            "vercel_url": _normalize_url(p.get("vercel_url")),
            "ideal_vercel_url": _normalize_url(p.get("ideal_vercel_url")),
            "canonical_health_url": _normalize_url(p.get("canonical_health_url")),
            "canonical_health_code": canonical_code,
            "canonical_health_status": p.get("canonical_health_status", "unknown"),
            "last_health_code": p.get("last_health_code", 0),
            "checkout_url": p.get("checkout_url", ""),
            "checkout_status": p.get("checkout_status", "unknown"),
            "diagnosis_label": diagnosis["label"],
            "severity": diagnosis["severity"],
            "fix_command": diagnosis["fix"].format(slug=slug),
        })

    results.sort(key=lambda r: SEVERITY_ORDER.get(r["severity"], 2))
    return results


def to_markdown(products: list[dict]) -> str:
    lines = [
        "# Canonical Drift Fix Plan",
        f"**Generated:** {_utc_now_iso()} UTC",
        f"**Total drift products:** {len(products)}",
        "",
    ]

    if not products:
        lines.append("No canonical drift products found.")
        return "\n".join(lines)

    high = sum(1 for p in products if p["severity"] == "high")
    medium = sum(1 for p in products if p["severity"] == "medium")
    low = sum(1 for p in products if p["severity"] == "low")

    lines.append(f"**Severity:** {high} high / {medium} medium / {low} low")
    lines.append("")

    lines.append("## Summary Table")
    lines.append("| # | Slug | Canonical Code | Diagnosis | Severity |")
    lines.append("|---|------|---------------|-----------|----------|")
    for i, p in enumerate(products, 1):
        lines.append(
            f"| {i} | {p['slug']} | {p['canonical_health_code']} | "
            f"{p['diagnosis_label']} | {p['severity']} |"
        )
    lines.append("")

    lines.append("## Detailed Fix Plan")
    for i, p in enumerate(products, 1):
        lines.append(f"### {i}. {p['name']} (`{p['slug']}`)")
        lines.append(f"- **Current URL:** `{p['vercel_url']}`")
        lines.append(f"- **Ideal URL:** `{p['ideal_vercel_url']}`")
        lines.append(f"- **Canonical probe:** `{p['canonical_health_url']}` → HTTP {p['canonical_health_code']}")
        lines.append(f"- **Fallback health:** HTTP {p['last_health_code']} (via alias)")
        lines.append(f"- **Diagnosis:** {p['diagnosis_label']}")
        lines.append(f"- **Fix:** `{p['fix_command']}`")
        if p.get("checkout_url"):
            lines.append(f"- **Checkout:** {p['checkout_status']} → `{p['checkout_url'][:60]}...`")
        lines.append("")

    lines.append("## Batch Fix Commands")
    lines.append("```bash")
    for p in products:
        if p["severity"] == "high":
            lines.append(f"# {p['slug']} (HTTP {p['canonical_health_code']})")
            lines.append(p["fix_command"])
            lines.append("")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def write_codex_task(products: list[dict], output_path: Path = CODEX_TASK_PATH) -> str:
    if not products:
        return "No drift products — codex_task.md not updated."

    high_products = [p for p in products if p.get("severity") == "high"]
    ts = _utc_now_iso()

    lines = [
        "# Codex Task — Canonical Drift Fix",
        f"**Generated by GLM:** {ts} UTC",
        f"**Priority:** HIGH — {len(high_products)} products with broken canonical URLs",
        "",
        "## Context",
        f"{len(products)} products have canonical URL drift. They are healthy via fallback aliases",
        "but their canonical Vercel URLs return non-200 codes. This affects SEO and discoverability.",
        "",
        "## Products to Fix",
    ]

    for p in products:
        lines.append(f"- **{p['slug']}** — HTTP {p['canonical_health_code']} ({p['diagnosis_label']}) → `{p['fix_command']}`")

    lines.append("")
    lines.append("## Steps")
    lines.append("1. For each product above, run the fix command")
    lines.append("2. Verify canonical URL returns HTTP 200 after fix")
    lines.append("3. Update STATE.json if vercel_url changed")
    lines.append("4. Run `python3 scripts/health_check.py` to verify")
    lines.append("")
    lines.append("## Acceptance Criteria")
    lines.append("- All 6 canonical URLs return HTTP 200")
    lines.append("- `canonical_url_drift` count in STATE_SUMMARY = 0")
    lines.append("- No fallback alias needed — canonical URL is the deployment URL")
    lines.append("")

    content = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return f"Written: {output_path}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Canonical drift fix plan generator")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--apply-brief", action="store_true", dest="apply_brief")
    parser.add_argument("--from-summary", action="store_true", dest="from_summary",
                        help="Load drift data from STATE_SUMMARY.json instead of STATE.json")
    args = parser.parse_args()

    if args.from_summary:
        products = load_drift_from_summary()
    else:
        products = load_drift_products()

    if args.as_json:
        print(json.dumps(products, indent=2, ensure_ascii=False))
    elif args.write:
        md = to_markdown(products)
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(md, encoding="utf-8")
        json_path = OUTPUT_PATH.with_suffix(".json")
        json_path.write_text(
            json.dumps(products, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Written: {OUTPUT_PATH} + {json_path}")
    elif args.apply_brief:
        result = write_codex_task(products)
        print(result)
    else:
        print(to_markdown(products))

    return 0


if __name__ == "__main__":
    sys.exit(main())
