#!/usr/bin/env python3
"""
Triage report generator for unhealthy live products.

Reads STATE_SUMMARY.json, categorises each unhealthy item by HTTP code,
and produces a short remediation brief that downstream agents (GLM, Codex)
can act on immediately.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.summary_visibility import (
    canonical_drift_count,
    canonical_drift_entries as visible_canonical_drift_entries,
)

TRIAGE_RULES = {
    401: {
        "label": "sso_protection",
        "action": "Check Vercel project settings -> disable Vercel Authentication",
        "severity": "high",
    },
    402: {
        "label": "deployment_disabled",
        "action": "Redeploy via Vercel CLI or dashboard; check billing",
        "severity": "medium",
    },
    404: {
        "label": "not_found",
        "action": "Verify deployment exists; re-link Vercel project to correct slug",
        "severity": "medium",
    },
    429: {
        "label": "rate_limited",
        "action": "Check Vercel plan limits; reduce concurrent deployments or upgrade plan",
        "severity": "medium",
    },
    451: {
        "label": "geo_block",
        "action": "Check Vercel firewall/geo rules; may need region whitelist",
        "severity": "low",
    },
    500: {
        "label": "server_error",
        "action": "Check Vercel build/runtime logs; redeploy if transient",
        "severity": "high",
    },
    0: {
        "label": "timeout",
        "action": "Increase timeout or verify DNS resolution",
        "severity": "medium",
    },
}

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def _triage_entry(slug: str, code: int) -> dict:
    rule = TRIAGE_RULES.get(
        code,
        {
            "label": f"error_{code}",
            "action": "Investigate manually",
            "severity": "medium",
        },
    )
    return {
        "slug": slug,
        "http_code": code,
        "label": rule["label"],
        "suggested_action": rule["action"],
        "severity": rule.get("severity", "medium"),
    }


def sort_by_severity(entries: list[dict]) -> list[dict]:
    return sorted(
        entries, key=lambda e: SEVERITY_ORDER.get(e.get("severity", "medium"), 1)
    )


def _canonical_drift_items(summary: dict) -> list[dict]:
    gaps = summary.get("gaps", {})
    if isinstance(gaps, dict):
        for key in ("canonical_url_drift", "canonical_drift"):
            raw_entries = gaps.get(key)
            if isinstance(raw_entries, list):
                entries = [item for item in raw_entries if isinstance(item, dict)]
                if entries:
                    return entries

    return visible_canonical_drift_entries(summary)


def generate_triage(summary_path: Path | None = None) -> list[dict]:
    """Generate triage entries for unhealthy live products AND canonical-drift products.

    Canonical-drift products (alternate_healthy via fallback alias) are triaged
    based on the canonical URL HTTP code so they surface in remediation reports.
    """
    if summary_path is None:
        summary_path = ROOT / "STATE_SUMMARY.json"
    with open(summary_path, encoding="utf-8") as f:
        summary = json.load(f)

    gaps = summary.get("gaps", {})
    seen_slugs: set[str] = set()
    entries: list[dict] = []

    # 1) Direct unhealthy live products
    for item in gaps.get("unhealthy_live", []):
        code = item.get("code", 0)
        if isinstance(code, str) and code.isdigit():
            code = int(code)
        slug = item.get("slug", "unknown")
        seen_slugs.add(slug)
        entries.append(_triage_entry(slug, code))

    # 2) Canonical-drift products (healthy via fallback, broken at canonical)
    for item in _canonical_drift_items(summary):
        slug = item.get("slug", "unknown")
        if slug in seen_slugs:
            continue
        canonical_code = item.get("canonical_code", 0)
        if isinstance(canonical_code, str) and canonical_code.isdigit():
            canonical_code = int(canonical_code)
        entry = _triage_entry(slug, canonical_code)
        entry["label"] = f"canonical_drift/{entry['label']}"
        entry["severity"] = "medium"
        entry["suggested_action"] = (
            f"Canonical URL returns {canonical_code}; healthy via fallback alias. "
            "Redeploy canonical or update DNS/Vercel project slug."
        )
        seen_slugs.add(slug)
        entries.append(entry)

    return entries


def write_triage_report(entries: list[dict], output_path: Path | None = None) -> str:
    if output_path is None:
        output_path = ROOT / "analysis" / "unhealthy_triage.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sorted_entries = sort_by_severity(entries)
    lines = [
        f"# Unhealthy Live Triage Report",
        f"**Generated:** {_utc_now_iso()} UTC",
        f"**Count:** {len(sorted_entries)}",
        "",
        "| Slug | HTTP | Label | Severity | Quick Fix |",
        "|------|------|-------|----------|----------|",
    ]
    for e in sorted_entries:
        fix = quick_fix_suggestion(e)
        lines.append(
            f"| {e['slug']} | {e['http_code']} | {e['label']} | {e['severity']} | `{fix}` |"
        )
    lines.append("")
    if sorted_entries:
        high_count = sum(1 for e in sorted_entries if e.get("severity") == "high")
        med_count = sum(1 for e in sorted_entries if e.get("severity") == "medium")
        low_count = sum(1 for e in sorted_entries if e.get("severity") == "low")
        lines.append(
            f"**Severity breakdown:** {high_count} high / {med_count} medium / {low_count} low"
        )
        lines.append("")

    report = "\n".join(lines)
    output_path.write_text(report, encoding="utf-8")
    return report


CANONICAL_DRIFT_FIXES = {
    "error_500": "Redeploy via: cd products/{slug} && vercel --prod --yes",
    "not_found": "Link project: cd products/{slug} && vercel link --yes && vercel --prod --yes",
    "deployment_disabled": "Re-enable in Vercel dashboard → Settings → Deployment Protection → disable, then: cd products/{slug} && vercel --prod --yes",
    "ssoProtection": "vercel project inspect {slug} && disable Vercel Authentication in project settings",
}


def canonical_drift_fix_suggestions(
    summary_path: Path | None = None,
) -> list[dict]:
    """Generate concrete fix suggestions for canonical URL drift products.

    For each product whose canonical URL is broken but works via a fallback
    alias, produces a remediation command based on the canonical_status code.

    Returns a list of dicts with keys: slug, fallback_url, ideal_url,
    canonical_status, fix_command.
    """
    if summary_path is None:
        summary_path = ROOT / "STATE_SUMMARY.json"
    try:
        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

    drift_items = _canonical_drift_items(summary)
    suggestions: list[dict] = []

    for item in drift_items:
        slug = item.get("slug", "unknown")
        canonical_status = item.get("canonical_status", "unknown")
        template = CANONICAL_DRIFT_FIXES.get(canonical_status)
        fix_command = template.format(slug=slug) if template else (
            f"Investigate canonical URL for {slug}: "
            f"status={canonical_status}"
        )
        suggestions.append({
            "slug": slug,
            "fallback_url": item.get("url", ""),
            "ideal_url": item.get("ideal_url", ""),
            "canonical_status": canonical_status,
            "fix_command": fix_command,
        })

    suggestions.sort(key=lambda s: str(s["slug"]))
    return suggestions


VERCEL_FIX_COMMANDS = {
    401: "vercel project ls --yes 2>/dev/null && vercel inspect {slug} 2>/dev/null || echo 'Check Vercel dashboard → Settings → Authentication → Disable Vercel Authentication'",
    402: "vercel inspect {slug} 2>/dev/null || echo 'Check billing/deployment status in Vercel dashboard'",
    404: "cd products/{slug} && vercel --prod --yes 2>&1",
    429: "echo 'Rate limited — check Vercel plan limits at vercel.com/account/billing'",
    451: "echo 'Geo-block: check Vercel Firewall rules → vercel.com/dashboard → project → Settings → Firewall'",
    500: "cd products/{slug} && vercel logs --output json 2>/dev/null | tail -50 || echo 'Check Vercel dashboard → Deployments → Function Logs'",
    0: "echo 'Timeout — check DNS or increase timeout settings'",
}


def quick_fix_suggestion(entry: dict) -> str:
    """Return a concrete CLI command or action for a triage entry.

    If a Vercel CLI command template exists for the HTTP code, format it
    with the product slug.  Otherwise fall back to the generic
    ``suggested_action`` field.
    """
    code = entry.get("http_code", 0)
    slug = entry.get("slug", "unknown")
    template = VERCEL_FIX_COMMANDS.get(code)
    if template:
        return template.format(slug=slug)
    return entry.get("suggested_action", "Investigate manually")


def triage_summary(
    summary_path: Path | None = None,
) -> dict:
    """One-call triage overview for downstream agents.

    Returns a compact dict with severity counts, top-severity slugs,
    and whether a handoff to Codex is recommended.

    Example output::

        {
            "total_unhealthy": 7,
            "high": 2,
            "medium": 4,
            "low": 1,
            "top_high_slugs": ["jwt-generator", "diffmaster"],
            "codex_handoff_recommended": true,
            "triage_entries": [...],
        }
    """
    entries = generate_triage(summary_path)
    if not entries:
        return {
            "total_unhealthy": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "top_high_slugs": [],
            "codex_handoff_recommended": False,
            "triage_entries": [],
        }

    high = [e for e in entries if e.get("severity") == "high"]
    medium = [e for e in entries if e.get("severity") == "medium"]
    low = [e for e in entries if e.get("severity") == "low"]

    return {
        "total_unhealthy": len(entries),
        "high": len(high),
        "medium": len(medium),
        "low": len(low),
        "top_high_slugs": [e["slug"] for e in sort_by_severity(high)],
        "codex_handoff_recommended": len(high) > 0,
        "triage_entries": sort_by_severity(entries),
    }


HEALTH_GRADE_THRESHOLDS = {
    (95, 101): "A",
    (85, 95): "B",
    (70, 85): "C",
    (50, 70): "D",
    (0, 50): "F",
}


def _grade_from_pct(pct: float) -> str:
    for (lo, hi), grade in HEALTH_GRADE_THRESHOLDS.items():
        if lo <= pct < hi:
            return grade
    return "F"


def portfolio_health_score(summary_path: Path | None = None) -> dict:
    """Compute overall portfolio health metrics from STATE_SUMMARY.json.

    Returns a compact dict with live/healthy counts, health percentage,
    checkout coverage, deploy gap, canonical drift count, and a letter
    grade (A-F) for quick status assessment.
    """
    if summary_path is None:
        summary_path = ROOT / "STATE_SUMMARY.json"
    try:
        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {
            "live_count": 0,
            "healthy_count": 0,
            "health_pct": 0.0,
            "grade": "F",
            "checkout_covered": False,
            "deploy_gap": 0,
            "canonical_drift": 0,
            "unhealthy_count": 0,
        }

    live = summary.get("live_count", 0)
    healthy = summary.get("healthy_count", 0)
    health_pct = round(healthy / live * 100, 1) if live > 0 else 0.0
    grade = _grade_from_pct(health_pct)

    checkout_gap = summary.get("checkout_gap_count", 0)
    deploy_gap = summary.get("deploy_missing_or_bad_url", 0)
    canonical_drift = canonical_drift_count(summary)

    return {
        "live_count": live,
        "healthy_count": healthy,
        "unhealthy_count": summary.get("unhealthy_count", 0),
        "health_pct": health_pct,
        "grade": grade,
        "checkout_covered": checkout_gap == 0,
        "deploy_gap": deploy_gap,
        "canonical_drift": canonical_drift,
    }


GLM_BRIEF_SCOPE_THRESHOLD = 60

CODEX_ONLY_CODES = {401, 451}

GLM_BRIEF_TEMPLATES = {
    "server_error": (
        "## Brief: {slug} — Server Error (HTTP {code})\n"
        "| Alan | Not |\n"
        "|---|---|\n"
        "| Problem | {slug} canonical URL returns HTTP {code} — build/runtime failure |\n"
        "| Önerilen dosyalar | `products/{slug}/` — Vercel deployment logs |\n"
        "| Kabul kriteri | Canonical URL 200 dönmeli |\n"
        "| Risk | Düşük — redeploy ile çözülebilir |\n"
    ),
    "sso_protection": (
        "## Brief: {slug} — Vercel SSO Protection (HTTP {code})\n"
        "| Alan | Not |\n"
        "|---|---|\n"
        "| Problem | {slug} Vercel Authentication/SSO aktif — public erişim engelli |\n"
        "| Önerilen dosyalar | Vercel dashboard → project settings → disable Vercel Auth |\n"
        "| Kabul kriteri | HTTP {code} yerine 200 dönmeli |\n"
        "| Risk | Düşük — settings değişikliği |\n"
    ),
    "geo_block": (
        "## Brief: {slug} — Geo Block (HTTP {code})\n"
        "| Alan | Not |\n"
        "|---|---|\n"
        "| Problem | {slug} Vercel firewall geo-block aktif |\n"
        "| Önerilen dosyalar | Vercel dashboard → Firewall → geo rules |\n"
        "| Kabul kriteri | Tüm bölgelerden erişilebilir olmalı |\n"
        "| Risk | Düşük — firewall kuralı değişikliği |\n"
    ),
    "canonical_drift": (
        "## Brief: {slug} — Canonical URL Drift ({status})\n"
        "| Alan | Not |\n"
        "|---|---|\n"
        "| Problem | {slug} canonical URL bozuk ({status}), fallback alias ile ayakta |\n"
        "| Önerilen dosyalar | STATE.json → canonical URL update veya Vercel'de redeploy |\n"
        "| Kabul kriteri | Canonical URL 200 dönmeli |\n"
        "| Risk | Orta — Vercel proje ismi/sahiplik değişimi gerekebilir |\n"
    ),
}


def generate_glm_brief(
    summary_path: Path | None = None,
) -> dict:
    """Auto-generate GLM fix brief content from current triage data.

    Returns a dict with:
      - ``glm_scope``: list of brief entries GLM can handle (< threshold)
      - ``codex_scope``: list of brief entries that need Codex
      - ``markdown``: formatted markdown suitable for glm_fix_brief.md
    """
    entries = generate_triage(summary_path)
    ts = _utc_now_iso()

    glm_scope: list[str] = []
    codex_scope: list[str] = []

    for entry in sort_by_severity(entries):
        slug = entry["slug"]
        code = entry.get("http_code", 0)
        label = entry.get("label", "")
        status = entry.get("suggested_action", "")

        if code in CODEX_ONLY_CODES:
            codex_scope.append(slug)
            continue

        is_drift = label.startswith("canonical_drift/")
        if is_drift:
            template = GLM_BRIEF_TEMPLATES["canonical_drift"]
            brief_text = template.format(slug=slug, status=label)
        else:
            base_label = label.split("/")[-1] if "/" in label else label
            template = GLM_BRIEF_TEMPLATES.get(base_label)
            if template:
                brief_text = template.format(slug=slug, code=code)
            else:
                brief_text = (
                    f"## Brief: {slug} — {label} (HTTP {code})\n"
                    "| Alan | Not |\n"
                    "|---|---|\n"
                    f"| Problem | {slug} returns HTTP {code}: {label} |\n"
                    "| Önerilen dosyalar | products/{slug}/ |\n"
                    "| Kabul kriteri | HTTP 200 dönmeli |\n"
                    "| Risk | Orta — araştırma gerekli |\n"
                ).format(slug=slug, code=code, label=label)

        glm_scope.append(brief_text)

    if not entries:
        markdown = (
            f"## GLM Fix Brief\n"
            f"**Tarih:** {ts}\n\n"
            f"Tüm live ürünler sağlıklı — aktif brief yok.\n"
        )
    else:
        sections = [
            f"## GLM Fix Brief\n**Tarih:** {ts}\n",
        ]
        if glm_scope:
            sections.append("### GLM Scope (küçük, güvenli)")
            for brief in glm_scope:
                sections.append(brief)
                sections.append("")
        if codex_scope:
            sections.append("### Codex Scope (Vercel erişimi gerekli)")
            for slug in codex_scope:
                sections.append(f"- **{slug}** → Codex'e bırakıldı (Vercel dashboard erişimi gerekli)")
            sections.append("")
        markdown = "\n".join(sections)

    return {
        "glm_scope": glm_scope,
        "codex_scope": codex_scope,
        "markdown": markdown,
    }


def main(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(
        description="Triage unhealthy live products from STATE_SUMMARY.json"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output triage result as JSON",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Also output triage_summary() overview",
    )
    parser.add_argument(
        "--health-score",
        action="store_true",
        dest="health_score",
        help="Output portfolio_health_score() as JSON",
    )
    parser.add_argument(
        "--drift-fix",
        action="store_true",
        dest="drift_fix",
        help="Output canonical_drift_fix_suggestions() as JSON",
    )
    args = parser.parse_args(argv)

    if args.health_score:
        score = portfolio_health_score()
        print(json.dumps(score, indent=2))
        return {"health_score": score}

    if args.drift_fix:
        suggestions = canonical_drift_fix_suggestions()
        print(json.dumps(suggestions, indent=2))
        return {"drift_fix": len(suggestions)}

    entries = generate_triage()
    if not entries:
        if args.json_output:
            print(json.dumps({"unhealthy": 0, "entries": []}))
        else:
            print("All live products healthy.")
        return {"unhealthy": 0}

    if args.json_output:
        output = {"unhealthy": len(entries), "entries": sort_by_severity(entries)}
        if args.summary:
            output["summary"] = triage_summary()
        print(json.dumps(output, indent=2))
    else:
        report = write_triage_report(entries)
        print(report)

    return {"unhealthy": len(entries)}


if __name__ == "__main__":
    result = main()
    sys.exit(1 if result["unhealthy"] > 0 else 0)
