"""Tests for scripts.cycle_delta"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cycle_delta import (
    compute_delta,
    delta_summary,
    format_delta_markdown,
    last_n_deltas,
    _load_snapshots,
)


def _write_trend(path: Path, snapshots: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(s) for s in snapshots]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_compute_delta_no_change():
    older = {"cycle": 100, "ts": "t1", "health_pct": 95.0, "live": 80, "healthy": 76}
    newer = {"cycle": 101, "ts": "t2", "health_pct": 95.0, "live": 80, "healthy": 76}
    delta = compute_delta(older, newer)
    assert delta["direction"] == "stable"
    assert delta["health_pct_delta"] == 0.0
    assert delta["changes"] == {}


def test_compute_delta_improving():
    older = {"cycle": 100, "ts": "t1", "health_pct": 90.0, "healthy": 72, "unhealthy": 8}
    newer = {"cycle": 101, "ts": "t2", "health_pct": 95.0, "healthy": 76, "unhealthy": 4}
    delta = compute_delta(older, newer)
    assert delta["direction"] == "improving"
    assert delta["health_pct_delta"] == 5.0
    assert delta["changes"]["healthy"]["delta"] == 4
    assert delta["changes"]["unhealthy"]["delta"] == -4


def test_compute_delta_degrading():
    older = {"cycle": 200, "ts": "t1", "health_pct": 97.0, "unhealthy": 2}
    newer = {"cycle": 201, "ts": "t2", "health_pct": 90.0, "unhealthy": 9}
    delta = compute_delta(older, newer)
    assert delta["direction"] == "degrading"
    assert delta["health_pct_delta"] == -7.0
    assert delta["changes"]["unhealthy"]["delta"] == 7


def test_compute_delta_cycle_ids():
    older = {"cycle": 50, "ts": "2026-01-01"}
    newer = {"cycle": 51, "ts": "2026-01-02"}
    delta = compute_delta(older, newer)
    assert delta["older_cycle"] == 50
    assert delta["newer_cycle"] == 51


def test_load_snapshots_empty(tmp_path):
    result = _load_snapshots(tmp_path / "nonexistent.jsonl")
    assert result == []


def test_load_snapshots_with_data(tmp_path):
    trend = tmp_path / "trend.jsonl"
    _write_trend(trend, [
        {"cycle": 1, "live": 10},
        {"cycle": 2, "live": 12},
    ])
    result = _load_snapshots(trend)
    assert len(result) == 2
    assert result[0]["cycle"] == 1


def test_load_snapshots_skips_bad_json(tmp_path):
    trend = tmp_path / "trend.jsonl"
    trend.write_text('{"cycle":1}\nbadjson\n{"cycle":2}\n', encoding="utf-8")
    result = _load_snapshots(trend)
    assert len(result) == 2


def test_last_n_deltas_insufficient_data(tmp_path):
    trend = tmp_path / "trend.jsonl"
    _write_trend(trend, [{"cycle": 1, "health_pct": 90.0}])
    deltas = last_n_deltas(trend_path=trend)
    assert deltas == []


def test_last_n_deltas_single_pair(tmp_path):
    trend = tmp_path / "trend.jsonl"
    _write_trend(trend, [
        {"cycle": 100, "ts": "t1", "health_pct": 90.0, "healthy": 70, "unhealthy": 10},
        {"cycle": 101, "ts": "t2", "health_pct": 95.0, "healthy": 74, "unhealthy": 6},
    ])
    deltas = last_n_deltas(trend_path=trend)
    assert len(deltas) == 1
    assert deltas[0]["older_cycle"] == 100
    assert deltas[0]["newer_cycle"] == 101


def test_last_n_deltas_multiple_pairs(tmp_path):
    trend = tmp_path / "trend.jsonl"
    _write_trend(trend, [
        {"cycle": 100, "ts": "t1", "health_pct": 85.0},
        {"cycle": 101, "ts": "t2", "health_pct": 90.0},
        {"cycle": 102, "ts": "t3", "health_pct": 92.0},
        {"cycle": 103, "ts": "t4", "health_pct": 88.0},
    ])
    deltas = last_n_deltas(n=4, trend_path=trend)
    assert len(deltas) == 3
    assert deltas[0]["older_cycle"] == 100
    assert deltas[-1]["newer_cycle"] == 103


def test_delta_summary_from_real_data(tmp_path):
    trend = tmp_path / "trend.jsonl"
    _write_trend(trend, [
        {"cycle": 1100, "ts": "t1", "health_pct": 94.0, "live": 85, "healthy": 80},
        {"cycle": 1105, "ts": "t2", "health_pct": 95.0, "live": 88, "healthy": 84},
        {"cycle": 1109, "ts": "t3", "health_pct": 96.7, "live": 90, "healthy": 87},
    ])
    result = delta_summary(n=3, trend_path=trend)
    assert result["from_cycle"] == 1100
    assert result["to_cycle"] == 1109
    assert result["direction"] == "improving"
    assert result["health_pct_delta"] == 2.7
    assert "live" in result["changes"]


def test_delta_summary_insufficient_data(tmp_path):
    result = delta_summary(trend_path=tmp_path / "nonexistent.jsonl")
    assert "error" in result


def test_format_delta_markdown_with_changes():
    delta = compute_delta(
        {"cycle": 100, "ts": "t1", "health_pct": 90.0, "healthy": 70, "unhealthy": 10},
        {"cycle": 101, "ts": "t2", "health_pct": 95.0, "healthy": 74, "unhealthy": 6},
    )
    md = format_delta_markdown(delta)
    assert "100" in md
    assert "101" in md
    assert "improving" in md
    assert "healthy" in md
    assert "+4" in md
    assert "-4" in md


def test_format_delta_markdown_no_changes():
    delta = compute_delta(
        {"cycle": 1, "ts": "t1", "health_pct": 95.0},
        {"cycle": 2, "ts": "t2", "health_pct": 95.0},
    )
    md = format_delta_markdown(delta)
    assert "No metric changes" in md


def test_delta_summary_n_larger_than_data(tmp_path):
    trend = tmp_path / "trend.jsonl"
    _write_trend(trend, [
        {"cycle": 100, "ts": "t1", "health_pct": 90.0},
        {"cycle": 101, "ts": "t2", "health_pct": 95.0},
    ])
    result = delta_summary(n=10, trend_path=trend)
    assert result["from_cycle"] == 100
    assert result["to_cycle"] == 101


def test_compute_delta_all_metric_keys():
    older = {
        "cycle": 1, "ts": "t1", "health_pct": 80.0,
        "live": 50, "healthy": 40, "unhealthy": 10,
        "checkout_gap": 5, "deploy_gap": 8, "canonical_drift": 3,
    }
    newer = {
        "cycle": 2, "ts": "t2", "health_pct": 90.0,
        "live": 55, "healthy": 50, "unhealthy": 5,
        "checkout_gap": 0, "deploy_gap": 3, "canonical_drift": 1,
    }
    delta = compute_delta(older, newer)
    assert len(delta["changes"]) == 6
    assert delta["changes"]["checkout_gap"]["delta"] == -5
    assert delta["changes"]["deploy_gap"]["delta"] == -5
    assert delta["changes"]["canonical_drift"]["delta"] == -2


def test_compute_delta_boundary_stable():
    older = {"cycle": 1, "ts": "t1", "health_pct": 95.0}
    newer = {"cycle": 2, "ts": "t2", "health_pct": 95.3}
    delta = compute_delta(older, newer)
    assert delta["direction"] == "stable"
    assert delta["health_pct_delta"] == 0.3


def test_compute_delta_boundary_improving_exact():
    older = {"cycle": 1, "ts": "t1", "health_pct": 90.0}
    newer = {"cycle": 2, "ts": "t2", "health_pct": 90.6}
    delta = compute_delta(older, newer)
    assert delta["direction"] == "improving"
