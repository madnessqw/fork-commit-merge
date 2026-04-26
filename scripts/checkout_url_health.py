#!/usr/bin/env python3
"""Checkout URL reachability checker.

Validates that every live product's checkout URL resolves to a working
Polar checkout page (HTTP 200 or redirect chain ending in 200).

Usage:
    python3 scripts/checkout_url_health.py [--json] [--quick]
    python3 scripts/checkout_url_health.py --slug croncraft
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
DEFAULT_TIMEOUT = 10
DEFAULT_MAX_WORKERS = 8


@dataclass
class CheckoutResult:
    slug: str
    name: str
    checkout_url: str
    status_code: int | None = None
    reachable: bool = False
    error: str | None = None
    latency_ms: float | None = None


@dataclass
class HealthReport:
    total: int = 0
    reachable: int = 0
    unreachable: int = 0
    missing_url: int = 0
    results: list[CheckoutResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        if self.total == 0:
            return 100
        return round(self.reachable / self.total * 100)

    @property
    def grade(self) -> str:
        s = self.score
        if s >= 98:
            return "A+"
        if s >= 95:
            return "A"
        if s >= 90:
            return "B"
        if s >= 80:
            return "C"
        if s >= 70:
            return "D"
        return "F"


def _load_products(summary_path: Path, slug_filter: str | None = None) -> list[dict[str, Any]]:
    try:
        with open(summary_path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read {summary_path}: {exc}") from exc

    products = data.get("products", [])
    if slug_filter:
        products = [p for p in products if p.get("s") == slug_filter]
    return products


def _check_url(slug: str, name: str, url: str, timeout: int) -> CheckoutResult:
    import requests

    result = CheckoutResult(slug=slug, name=name, checkout_url=url)
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        result.status_code = resp.status_code
        result.reachable = 200 <= resp.status_code < 400
        result.latency_ms = round(resp.elapsed.total_seconds() * 1000)
    except requests.RequestException as exc:
        result.error = str(exc)[:200]
    return result


def run_health_check(
    summary_path: Path = SUMMARY_PATH,
    *,
    slug_filter: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    max_workers: int = DEFAULT_MAX_WORKERS,
    quick: bool = False,
) -> HealthReport:
    products = _load_products(summary_path, slug_filter)
    report = HealthReport(total=len(products))

    urls_to_check: list[tuple[str, str, str]] = []
    for p in products:
        slug = p.get("s", "")
        name = p.get("n", slug)
        checkout_url = (p.get("c") or "").strip()
        if not checkout_url or not checkout_url.startswith("http"):
            report.missing_url += 1
            report.results.append(
                CheckoutResult(slug=slug, name=name, checkout_url=checkout_url or "")
            )
            continue
        urls_to_check.append((slug, name, checkout_url))

    if quick:
        urls_to_check = urls_to_check[:20]

    workers = min(max_workers, len(urls_to_check))
    if workers <= 0:
        return report

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_check_url, slug, name, url, timeout): slug
            for slug, name, url in urls_to_check
        }
        for future in as_completed(futures):
            r = future.result()
            report.results.append(r)
            if r.reachable:
                report.reachable += 1
            else:
                report.unreachable += 1

    report.results.sort(key=lambda r: (0 if r.reachable else 1, r.slug))
    return report


def format_report(report: HealthReport, *, json_output: bool = False) -> str:
    if json_output:
        data = {
            "score": report.score,
            "grade": report.grade,
            "total": report.total,
            "reachable": report.reachable,
            "unreachable": report.unreachable,
            "missing_url": report.missing_url,
            "results": [
                {
                    "slug": r.slug,
                    "name": r.name,
                    "checkout_url": r.checkout_url,
                    "status_code": r.status_code,
                    "reachable": r.reachable,
                    "latency_ms": r.latency_ms,
                    "error": r.error,
                }
                for r in report.results
            ],
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    lines = [
        f"# Checkout URL Health Report",
        f"Score: {report.score}/100 ({report.grade})",
        f"Reachable: {report.reachable}/{report.total} | Unreachable: {report.unreachable} | Missing: {report.missing_url}",
        "",
    ]
    if report.unreachable > 0:
        lines.append("## Unreachable")
        for r in report.results:
            if not r.reachable and r.checkout_url:
                lines.append(f"- {r.slug}: HTTP {r.status_code or 'ERR'} ({r.error or 'n/a'})")
        lines.append("")
    if report.missing_url > 0:
        lines.append("## Missing URL")
        for r in report.results:
            if not r.checkout_url:
                lines.append(f"- {r.slug}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--slug", help="Check single product slug")
    parser.add_argument("--quick", action="store_true", help="Only check first 20 products")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS)
    args = parser.parse_args()

    report = run_health_check(
        slug_filter=args.slug,
        timeout=args.timeout,
        max_workers=args.max_workers,
        quick=args.quick,
    )
    print(format_report(report, json_output=args.json))
    return 1 if report.unreachable > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
