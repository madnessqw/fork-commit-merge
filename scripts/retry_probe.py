#!/usr/bin/env python3
"""Retry health probe for unhealthy / canonical-drift products.

Reads STATE_SUMMARY.json, extracts products with known issues (unhealthy_live
or canonical_drift), re-probes them via curl, and produces a concise report
with before/after HTTP codes so operators can see if issues are transient.

Usage:
    python3 scripts/retry_probe.py              # probe all unhealthy + drift
    python3 scripts/retry_probe.py --slug jwt   # probe specific slug substring
    python3 scripts/retry_probe.py --json       # machine-readable output
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.unhealthy_triage import generate_triage, sort_by_severity


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def probe_url(url: str, timeout: int = 10) -> dict:
    try:
        result = subprocess.run(
            [
                "curl", "-4", "-L", "-sS",
                "-o", "/dev/null",
                "-w", "%{http_code} %{url_effective}",
                "--max-time", str(timeout),
                url,
            ],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        stdout = (result.stdout or "").strip()
        parts = stdout.split(" ", 1)
        code_str = parts[0] if parts else "0"
        effective = parts[1].rstrip("/") if len(parts) > 1 else url
        code = int(code_str) if code_str.isdigit() else 0
        return {"code": code, "effective_url": effective, "raw": stdout}
    except Exception as exc:
        return {"code": 0, "effective_url": url, "raw": str(exc)}


def _slug_from_summary(summary: dict) -> list[dict]:
    gaps = summary.get("gaps", {})
    items: list[dict] = []
    for u in gaps.get("unhealthy_live", []):
        items.append({
            "slug": u.get("slug", "unknown"),
            "prior_code": u.get("code", 0),
            "category": "unhealthy",
            "url": u.get("url", ""),
        })
    for d in gaps.get("canonical_url_drift", []):
        items.append({
            "slug": d.get("slug", "unknown"),
            "prior_code": d.get("canonical_code", 0),
            "category": "canonical_drift",
            "url": d.get("ideal_url", f"https://{d.get('slug', '')}.vercel.app"),
        })
    return items


def retry_probe(
    summary_path: Path | None = None,
    slug_filter: str = "",
    workers: int = 4,
) -> list[dict]:
    if summary_path is None:
        summary_path = ROOT / "STATE_SUMMARY.json"
    with open(summary_path, encoding="utf-8") as f:
        summary = json.load(f)

    targets = _slug_from_summary(summary)
    if slug_filter:
        targets = [t for t in targets if slug_filter in t.get("slug", "")]

    if not targets:
        return []

    results: list[dict] = []

    def _probe_one(target: dict) -> dict:
        slug = target["slug"]
        url = target.get("url") or f"https://{slug}.vercel.app"
        probe = probe_url(url)
        return {
            "slug": slug,
            "category": target["category"],
            "prior_code": target["prior_code"],
            "retried_code": probe["code"],
            "url": url,
            "effective_url": probe["effective_url"],
            "recovered": probe["code"] == 200 and target["prior_code"] != 200,
            "probed_at": _utc_now_iso(),
        }

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_probe_one, t): t for t in targets}
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda r: (0 if r["recovered"] else 1, str(r["slug"])))
    return results


def format_table(results: list[dict]) -> str:
    if not results:
        return "No unhealthy or drift products to probe."
    lines = [
        "# Retry Probe Report",
        f"**Generated:** {_utc_now_iso()}",
        f"**Probed:** {len(results)}",
        "",
        "| Slug | Category | Before | After | Recovered | URL |",
        "|------|----------|--------|-------|-----------|-----|",
    ]
    for r in results:
        rec = "YES" if r["recovered"] else "no"
        lines.append(
            f"| {r['slug']} | {r['category']} | {r['prior_code']} | "
            f"{r['retried_code']} | {rec} | `{r['url']}` |"
        )
    recovered_count = sum(1 for r in results if r["recovered"])
    lines.append("")
    lines.append(f"**Recovered:** {recovered_count}/{len(results)}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Retry probe unhealthy products")
    parser.add_argument("--slug", default="", help="Filter by slug substring")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--output", default="", help="Write report to file")
    args = parser.parse_args()

    results = retry_probe(slug_filter=args.slug)

    if args.as_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        report = format_table(results)
        print(report)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
