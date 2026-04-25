#!/usr/bin/env python3
"""Track portfolio health score over time and detect trends.

Records a snapshot each cycle into logs/health_trend.jsonl and can
produce a short trend summary (improving / stable / degrading).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TREND_FILE = ROOT / "logs" / "health_trend.jsonl"

from scripts.summary_visibility import canonical_drift_count, canonical_drift_entries
from scripts.unhealthy_triage import portfolio_health_score, _grade_from_pct

SNAPSHOT_KEYS = (
    "live_count",
    "healthy_count",
    "unhealthy_count",
    "checkout_gap_count",
    "deploy_missing_or_bad_url",
    "canonical_url_drift",
    "fallback_healthy_count",
)


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def record_snapshot(summary_path: Path | None = None) -> dict:
    if summary_path is None:
        summary_path = ROOT / "STATE_SUMMARY.json"

    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    live = summary.get("live_count", 0)
    healthy = summary.get("healthy_count", 0)
    health_pct = round(healthy / live * 100, 1) if live > 0 else 0.0

    canonical_drift = canonical_drift_count(summary)

    drift_items = canonical_drift_entries(summary)
    drift_slugs = [d.get("slug", "") for d in drift_items if d.get("slug")]

    fallback_healthy = summary.get("fallback_healthy_count", len(summary.get("gaps", {}).get("fallback_healthy", [])))

    grade = _grade_from_pct(health_pct)

    snapshot = {
        "ts": _utc_now_iso(),
        "cycle": summary.get("cycle", 0),
        "live": live,
        "healthy": healthy,
        "health_pct": health_pct,
        "grade": grade,
        "unhealthy": summary.get("unhealthy_count", 0),
        "checkout_gap": summary.get("checkout_gap_count", 0),
        "deploy_gap": summary.get("deploy_missing_or_bad_url", 0),
        "canonical_drift": canonical_drift,
        "fallback_healthy": fallback_healthy,
        "drift_slugs": drift_slugs,
    }

    TREND_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TREND_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(snapshot, ensure_ascii=False) + "\n")

    return snapshot


def load_trend(limit: int = 50) -> list[dict]:
    if not TREND_FILE.exists():
        return []
    lines: list[str] = []
    with open(TREND_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)
    recent = lines[-limit:]
    entries: list[dict] = []
    for line in recent:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def compute_trend(entries: list[dict] | None = None) -> dict:
    if entries is None:
        entries = load_trend(limit=20)

    if len(entries) < 2:
        return {
            "direction": "unknown",
            "health_delta": 0.0,
            "snapshots": len(entries),
        }

    first = entries[0]
    last = entries[-1]
    delta = round(last.get("health_pct", 0) - first.get("health_pct", 0), 1)

    if delta > 1.0:
        direction = "improving"
    elif delta < -1.0:
        direction = "degrading"
    else:
        direction = "stable"

    return {
        "direction": direction,
        "health_delta": delta,
        "from_pct": first.get("health_pct", 0),
        "to_pct": last.get("health_pct", 0),
        "from_cycle": first.get("cycle", 0),
        "to_cycle": last.get("cycle", 0),
        "snapshots": len(entries),
        "latest_deploy_gap": last.get("deploy_gap", 0),
        "latest_canonical_drift": last.get("canonical_drift", 0),
        "latest_fallback_healthy": last.get("fallback_healthy", 0),
    }


STUCK_METRIC_KEYS = (
    "deploy_gap",
    "canonical_drift",
    "fallback_healthy",
    "unhealthy",
    "checkout_gap",
)

DELTA_METRIC_KEYS = (
    ("live", "live"),
    ("healthy", "healthy"),
    ("unhealthy", "unhealthy"),
    ("health_pct", "health_pct"),
    ("checkout_gap", "checkout_gap"),
    ("deploy_gap", "deploy_gap"),
    ("canonical_drift", "canonical_drift"),
    ("fallback_healthy", "fallback_healthy"),
)


def cycle_delta_report(entries: list[dict] | None = None) -> dict:
    if entries is None:
        entries = load_trend(limit=50)

    if len(entries) < 2:
        return {"available": False, "reason": "insufficient_snapshots", "snapshots": len(entries)}

    prev = entries[-2]
    curr = entries[-1]

    deltas: list[dict] = []
    for key, label in DELTA_METRIC_KEYS:
        p = prev.get(key, 0)
        c = curr.get(key, 0)
        d = round(c - p, 1) if isinstance(p, float) or isinstance(c, float) else c - p
        if d != 0:
            deltas.append({"metric": label, "prev": p, "curr": c, "delta": d})

    grade_change = None
    pg = prev.get("grade", "")
    cg = curr.get("grade", "")
    if pg and cg and pg != cg:
        grade_change = {"from": pg, "to": cg}

    new_drift = set(curr.get("drift_slugs", [])) - set(prev.get("drift_slugs", []))
    resolved_drift = set(prev.get("drift_slugs", [])) - set(curr.get("drift_slugs", []))

    return {
        "available": True,
        "from_cycle": prev.get("cycle", 0),
        "to_cycle": curr.get("cycle", 0),
        "deltas": deltas,
        "changed": len(deltas) > 0,
        "grade_change": grade_change,
        "new_drift_slugs": sorted(new_drift),
        "resolved_drift_slugs": sorted(resolved_drift),
        "snapshots": len(entries),
    }


def stuck_metrics(entries: list[dict] | None = None, *, window: int = 5) -> dict:
    if entries is None:
        entries = load_trend(limit=max(window, 20))

    if len(entries) < 2:
        return {"stuck_count": 0, "stuck_metrics": [], "window": window, "snapshots": len(entries)}

    recent = entries[-window:]
    first_values = recent[0]
    last_values = recent[-1]

    stuck: list[dict] = []
    for key in STUCK_METRIC_KEYS:
        first_val = first_values.get(key, 0)
        last_val = last_values.get(key, 0)
        if first_val == 0 and last_val == 0:
            continue
        all_same = all(e.get(key, 0) == first_val for e in recent)
        if all_same and first_val > 0:
            stuck.append({
                "metric": key,
                "value": first_val,
                "stale_snapshots": len(recent),
            })

    return {
        "stuck_count": len(stuck),
        "stuck_metrics": stuck,
        "window": window,
        "snapshots": len(recent),
    }


def health_plateau(entries: list[dict] | None = None, *, tolerance: float = 0.5) -> dict:
    if entries is None:
        entries = load_trend(limit=50)

    if not entries:
        return {"plateau": False, "streak": 0, "snapshots": 0}

    latest_pct = entries[-1].get("health_pct", 0)
    streak = 0
    for entry in reversed(entries):
        if abs(entry.get("health_pct", 0) - latest_pct) <= tolerance:
            streak += 1
        else:
            break

    total = len(entries)
    pct_of_total = round(streak / total * 100, 1) if total > 0 else 0

    return {
        "plateau": streak >= 5,
        "streak": streak,
        "health_pct": latest_pct,
        "pct_of_total": pct_of_total,
        "snapshots": total,
        "warning": f"Health stuck at {latest_pct}% for {streak} cycles" if streak >= 5 else None,
    }


def rolling_health_stats(entries: list[dict] | None = None, *, window: int = 10) -> dict:
    if entries is None:
        entries = load_trend(limit=max(window, 50))

    if len(entries) < 2:
        return {"available": False, "reason": "insufficient_data", "snapshots": len(entries)}

    recent = entries[-window:]
    pcts = [e.get("health_pct", 0) for e in recent]

    min_val = min(pcts)
    max_val = max(pcts)
    avg_val = round(sum(pcts) / len(pcts), 2)
    variance = sum((p - avg_val) ** 2 for p in pcts) / len(pcts)
    std_val = round(variance ** 0.5, 2)
    volatility = "high" if std_val > 2.0 else "medium" if std_val > 0.5 else "low"

    return {
        "available": True,
        "window": len(recent),
        "min": min_val,
        "max": max_val,
        "range": round(max_val - min_val, 2),
        "avg": avg_val,
        "std": std_val,
        "volatility": volatility,
        "latest": pcts[-1],
        "from_cycle": recent[0].get("cycle", 0),
        "to_cycle": recent[-1].get("cycle", 0),
    }


def drift_slug_history(limit: int = 100) -> dict:
    entries = load_trend(limit=limit)
    slug_first_seen: dict[str, str] = {}
    slug_last_seen: dict[str, str] = {}
    for entry in entries:
        drift_slugs = entry.get("drift_slugs", [])
        ts = entry.get("ts", "")
        for slug in drift_slugs:
            if slug not in slug_first_seen:
                slug_first_seen[slug] = ts
            slug_last_seen[slug] = ts

    result: dict[str, dict] = {}
    for slug in sorted(slug_first_seen):
        result[slug] = {
            "first_seen": slug_first_seen[slug],
            "last_seen": slug_last_seen[slug],
        }
    return {"drift_slug_count": len(result), "slugs": result}


def trend_summary_text() -> str:
    snapshot = record_snapshot()
    if not snapshot:
        return "Trend verisi yok — STATE_SUMMARY.json okunamadı"

    trend = compute_trend()
    arrow = {"improving": "↑", "degrading": "↓", "stable": "→"}.get(
        trend["direction"], "?"
    )
    grade = snapshot.get("grade", _grade_from_pct(snapshot["health_pct"]))
    fallback = snapshot.get("fallback_healthy", 0)
    fb_tag = f" | Fallback: {fallback}" if fallback else ""

    stuck = stuck_metrics()
    stuck_tag = ""
    if stuck.get("stuck_count", 0) > 0:
        items = ", ".join(
            f"{m['metric']}={m['value']}" for m in stuck.get("stuck_metrics", [])
        )
        stuck_tag = f" | STUCK: {items}"

    return (
        f"[{grade}] Sağlık: {snapshot['health_pct']}% {arrow} "
        f"(trend: {trend['direction']}, Δ{trend['health_delta']:+.1f}%) | "
        f"Unhealthy: {snapshot['unhealthy']} | "
        f"Drift: {snapshot['canonical_drift']}{fb_tag} | "
        f"Deploy gap: {snapshot['deploy_gap']}{stuck_tag}"
    )


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "stuck":
        print(json.dumps(stuck_metrics(), indent=2, ensure_ascii=False))
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "drift-history":
        print(json.dumps(drift_slug_history(), indent=2, ensure_ascii=False))
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        print(trend_summary_text())
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "trend":
        trend = compute_trend()
        print(json.dumps(trend, indent=2, ensure_ascii=False))
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "delta":
        print(json.dumps(cycle_delta_report(), indent=2, ensure_ascii=False))
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "plateau":
        print(json.dumps(health_plateau(), indent=2, ensure_ascii=False))
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "rolling":
        print(json.dumps(rolling_health_stats(), indent=2, ensure_ascii=False))
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "grade":
        score = portfolio_health_score()
        print(json.dumps(score, indent=2, ensure_ascii=False))
        return 0

    snapshot = record_snapshot()
    if not snapshot:
        print("HATA: snapshot kaydedilemedi")
        return 1

    print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
