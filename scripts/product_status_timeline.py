#!/usr/bin/env python3
"""Product Status Timeline Analyzer — cycle bazli urun durum degisim trendi."""

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = ROOT / "products"
STATE_PATH = ROOT / "STATE.json"
STATE_SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
LOGS_DIR = ROOT / "logs"
LEDGER_PATH = LOGS_DIR / "run_ledger.jsonl"


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_products():
    products = []
    if not PRODUCTS_DIR.exists():
        return products
    for d in PRODUCTS_DIR.iterdir():
        if not d.is_dir():
            continue
        pj = d / "product.json"
        if pj.exists():
            try:
                data = json.loads(pj.read_text())
                data["_dir"] = d.name
                products.append(data)
            except json.JSONDecodeError:
                pass
    return products


def load_ledger():
    entries = []
    if not LEDGER_PATH.exists():
        return entries
    with open(LEDGER_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries


def status_snapshot(products):
    return {
        "total": len(products),
        "live": sum(1 for p in products if p.get("status") == "live"),
        "building": sum(1 for p in products if p.get("status") == "building"),
        "pending": sum(1 for p in products if p.get("status") == "pending"),
        "inactive": sum(1 for p in products if p.get("status") == "inactive"),
    }


def category_status_matrix(products):
    matrix = defaultdict(Counter)
    for p in products:
        cat = p.get("category", "uncategorized")
        status = p.get("status", "unknown")
        matrix[cat][status] += 1
    return dict(matrix)


def checkout_readiness(products):
    live = [p for p in products if p.get("status") == "live"]
    with_co = sum(1 for p in live if (p.get("checkout_url") or "").startswith("http"))
    with_url = sum(1 for p in live if (p.get("vercel_url") or "").startswith("http"))
    return {
        "live_total": len(live),
        "with_checkout": with_co,
        "with_vercel_url": with_url,
        "checkout_pct": round(with_co / len(live) * 100, 1) if live else 0,
        "url_pct": round(with_url / len(live) * 100, 1) if live else 0,
    }


def ledger_mode_summary(ledger):
    if not ledger:
        return {"total_runs": 0, "modes": {}, "fail_count": 0}
    modes = Counter(e.get("mode", "unknown") for e in ledger)
    fails = sum(1 for e in ledger if e.get("status") == "fail")
    return {"total_runs": len(ledger), "modes": dict(modes), "fail_count": fails}


def recent_cycle_health(ledger, last_n=10):
    recent = ledger[-last_n:] if len(ledger) >= last_n else ledger
    if not recent:
        return []
    results = []
    for e in recent:
        results.append({
            "cycle": e.get("cycle", "?"),
            "mode": e.get("mode", "?"),
            "status": e.get("status", "?"),
            "agent": e.get("agent", "?"),
        })
    return results


def generate_timeline(include_details=False):
    products = load_products()
    state = load_json(STATE_PATH)
    summary = load_json(STATE_SUMMARY_PATH)
    ledger = load_ledger()

    timeline = {
        "generated_at": datetime.now().isoformat(),
        "current_cycle": state.get("cycle", summary.get("cycle", "?")),
        "current_mode": state.get("mode", summary.get("mode", "?")),
        "status_snapshot": status_snapshot(products),
        "checkout_readiness": checkout_readiness(products),
        "category_matrix": category_status_matrix(products),
        "ledger_summary": ledger_mode_summary(ledger),
    }

    if include_details:
        timeline["recent_cycles"] = recent_cycle_health(ledger)

    return timeline


def format_timeline(timeline):
    snap = timeline["status_snapshot"]
    co = timeline["checkout_readiness"]
    ls = timeline["ledger_summary"]

    lines = [
        f"# Status Timeline — {timeline['generated_at'][:16]}",
        f"",
        f"## Current State",
        f"- Cycle: {timeline['current_cycle']} | Mode: {timeline['current_mode']}",
        f"- Products: {snap['total']} total, {snap['live']} live, {snap['building']} building",
        f"",
        f"## Checkout Readiness",
        f"- Live: {co['live_total']} | Checkout: {co['with_checkout']} ({co['checkout_pct']}%) | URL: {co['with_vercel_url']} ({co['url_pct']}%)",
        f"",
        f"## Category Status Matrix",
    ]

    matrix = timeline["category_matrix"]
    for cat in sorted(matrix.keys()):
        statuses = matrix[cat]
        parts = [f"{k}={v}" for k, v in sorted(statuses.items())]
        lines.append(f"- {cat}: {', '.join(parts)}")

    lines.append("")
    lines.append("## Ledger Summary")
    lines.append(f"- Total runs: {ls['total_runs']} | Fails: {ls['fail_count']}")
    if ls["modes"]:
        for mode, count in sorted(ls["modes"].items(), key=lambda x: -x[1]):
            lines.append(f"- {mode}: {count} runs")

    if timeline.get("recent_cycles"):
        lines.append("")
        lines.append("## Recent Cycles")
        for rc in timeline["recent_cycles"]:
            lines.append(f"- Cycle {rc['cycle']}: {rc['agent']} / {rc['mode']} → {rc['status']}")

    return "\n".join(lines)


def main():
    include_details = "--details" in sys.argv
    output_format = "json"
    if "--markdown" in sys.argv or "--md" in sys.argv:
        output_format = "markdown"

    timeline = generate_timeline(include_details=include_details)

    if output_format == "markdown":
        print(format_timeline(timeline))
    else:
        print(json.dumps(timeline, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
