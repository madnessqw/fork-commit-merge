#!/usr/bin/env python3
"""Vercel deployment response monitor for UniverseCreator portfolio.

Probes all live product URLs and records HTTP status codes + response times.
Useful for detecting deployment outages, slow responses, and Vercel auth blocks.

Usage:
    python3 scripts/vercel_response_monitor.py check
    python3 scripts/vercel_response_monitor.py check --timeout 10 --top 10
    python3 scripts/vercel_response_monitor.py check --json
"""

from __future__ import annotations

import json
import time
import urllib.request
import urllib.error
import argparse
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "STATE_SUMMARY.json"
RESULTS_FILE = ROOT / "analysis" / "vercel_response_report.json"

DEFAULT_TIMEOUT = 8
DEFAULT_WORKERS = 10


def load_live_products() -> list[dict[str, Any]]:
    if not STATE_FILE.exists():
        return []
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return [p for p in data.get("products", []) if p.get("st") == "live" and p.get("v")]


def probe_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    start = time.monotonic()
    result: dict[str, Any] = {"url": url, "status": None, "error": None, "elapsed_ms": 0}
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "UniverseCreator-Monitor/1.0")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result["status"] = resp.status
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["error"] = f"HTTPError: {e.code}"
    except urllib.error.URLError as e:
        result["error"] = f"URLError: {e.reason}"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
    result["elapsed_ms"] = round((time.monotonic() - start) * 1000)
    return result


def run_checks(
    products: list[dict[str, Any]],
    timeout: int = DEFAULT_TIMEOUT,
    workers: int = DEFAULT_WORKERS,
) -> list[dict[str, Any]]:
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_map = {}
        for p in products:
            url = p.get("v", "")
            slug = p.get("s", "")
            name = p.get("n", "")
            future = pool.submit(probe_url, url, timeout)
            future_map[future] = {"slug": slug, "name": name, "url": url}

        for future in as_completed(future_map):
            meta = future_map[future]
            probe = future.result()
            results.append({**meta, **probe})

    results.sort(key=lambda x: x.get("slug", ""))
    return results


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    by_status: dict[int, int] = defaultdict(int)
    errors: list[str] = []
    slow: list[dict] = []
    elapsed_sum = 0

    for r in results:
        status = r.get("status")
        if status:
            by_status[status] += 1
        if r.get("error"):
            errors.append(f"{r['slug']}: {r['error']}")
        ms = r.get("elapsed_ms", 0)
        elapsed_sum += ms
        if ms > 3000:
            slow.append({"slug": r["slug"], "ms": ms})

    avg_ms = round(elapsed_sum / total) if total else 0
    ok_count = by_status.get(200, 0)

    return {
        "total": total,
        "ok_200": ok_count,
        "error_count": len(errors),
        "slow_count": len(slow),
        "avg_ms": avg_ms,
        "by_status": dict(by_status),
        "errors": errors[:20],
        "slow": sorted(slow, key=lambda x: -x["ms"])[:10],
    }


def format_report(summary: dict[str, Any], results: list[dict]) -> str:
    lines = [
        "# Vercel Response Monitor Report",
        "",
        f"Total probed: {summary['total']}",
        f"HTTP 200: {summary['ok_200']}/{summary['total']} "
        f"({round(summary['ok_200'] / max(summary['total'], 1) * 100)}%)",
        f"Avg response: {summary['avg_ms']}ms",
        f"Slow (>3s): {summary['slow_count']}",
        f"Errors: {summary['error_count']}",
        "",
        "## Status Distribution",
    ]
    for code, count in sorted(summary["by_status"].items()):
        lines.append(f"- HTTP {code}: {count}")

    if summary["slow"]:
        lines += ["", "## Slow Products (>3s)"]
        for s in summary["slow"]:
            lines.append(f"- `{s['slug']}`: {s['ms']}ms")

    if summary["errors"]:
        lines += ["", "## Errors"]
        for e in summary["errors"]:
            lines.append(f"- {e}")

    return "\n".join(lines)


def main() -> dict[str, Any]:
    parser = argparse.ArgumentParser(description="Vercel deployment response monitor")
    parser.add_argument("command", nargs="?", default="check", choices=["check"])
    parser.add_argument("--timeout", "-t", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--workers", "-w", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--top", type=int, default=10, help="Top N slowest to show")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    products = load_live_products()
    if not products:
        print("No live products found in STATE_SUMMARY.json")
        return {"total": 0}

    print(f"Probing {len(products)} live product URLs (timeout={args.timeout}s)...")
    results = run_checks(products, timeout=args.timeout, workers=args.workers)
    summary = summarize(results)

    report = format_report(summary, results)

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(
        json.dumps({"summary": summary, "results": results}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if args.json:
        print(json.dumps({"summary": summary}, indent=2, ensure_ascii=False))
    else:
        print(report)

    print(f"\nFull results saved to {RESULTS_FILE}")
    return summary


if __name__ == "__main__":
    main()
