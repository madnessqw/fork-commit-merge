"""Tests for scripts.health_dashboard"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.health_dashboard import (
    _bar,
    _grade,
    _pct,
    _status_icon,
    compute_metrics,
    load_summary,
    render_compact,
    render_full,
    render_json,
)


def _sample_summary(**overrides):
    base = {
        "cycle": 500,
        "mode": "OPTIMIZE",
        "active_count": 100,
        "live_count": 90,
        "healthy_count": 85,
        "canonical_healthy_count": 83,
        "fallback_healthy_count": 2,
        "unhealthy_count": 5,
        "pending_health_count": 0,
        "checkout_gap_count": 0,
        "deploy_missing_or_bad_url": 3,
        "canonical_url_drift": 2,
        "needs_fix_count": 5,
        "spec_ready_count": 1,
        "deploy_readiness_count": 8,
        "gaps": {
            "unhealthy_live": [
                {"slug": "jwt-generator", "code": 500},
                {"slug": "diffmaster", "code": 401},
            ],
            "canonical_url_drift": [
                {
                    "slug": "pdf-forge",
                    "url": "https://pdf-forge-alt.vercel.app",
                    "ideal_url": "https://pdf-forge.vercel.app",
                },
                {
                    "slug": "webhook-tester",
                    "url": "https://webhook-tester-alt.vercel.app",
                    "ideal_url": "https://webhook-tester.vercel.app",
                },
            ],
        },
    }
    base.update(overrides)
    return base


def test_grade():
    assert _grade(97) == "A"
    assert _grade(95) == "A"
    assert _grade(94.9) == "B"
    assert _grade(85) == "B"
    assert _grade(70) == "C"
    assert _grade(50) == "D"
    assert _grade(30) == "F"
    assert _grade(0) == "F"


def test_pct():
    assert _pct(96.7) == "96.7%"
    assert _pct(0.0) == "0.0%"


def test_bar_length():
    result = _bar(50, width=10)
    assert "█" in result
    assert "░" in result


def test_bar_full():
    result = _bar(100, width=10)
    assert result.count("█") == 10


def test_bar_zero():
    result = _bar(0, width=10)
    assert result.count("░") == 10


def test_status_icon_ok():
    assert "✓" in _status_icon(True)
    assert "✗" not in _status_icon(True)


def test_status_icon_fail():
    assert "✗" in _status_icon(False)
    assert "✓" not in _status_icon(False)


def test_compute_metrics_basic():
    summary = _sample_summary()
    m = compute_metrics(summary)
    assert m["active"] == 100
    assert m["live"] == 90
    assert m["healthy"] == 85
    assert m["canonical_healthy"] == 83
    assert m["fallback_healthy"] == 2
    assert m["unhealthy"] == 5
    assert m["health_pct"] == round(85 / 90 * 100, 1)
    assert m["grade"] == "B"
    assert m["checkout_ok"] is True
    assert m["deploy_gap"] == 3
    assert m["canonical_drift"] == 2
    assert m["cycle"] == 500


def test_compute_metrics_derives_canonical_healthy_from_fallback_visibility():
    summary = _sample_summary(
        healthy_count=88,
        canonical_healthy_count=None,
        fallback_healthy_count=4,
    )
    m = compute_metrics(summary)
    assert m["healthy"] == 88
    assert m["canonical_healthy"] == 84
    assert m["fallback_healthy"] == 4


def test_compute_metrics_zero_live():
    m = compute_metrics({"live_count": 0, "healthy_count": 0})
    assert m["health_pct"] == 0.0
    assert m["grade"] == "F"


def test_compute_metrics_checkout_gap():
    summary = _sample_summary(checkout_gap_count=3)
    m = compute_metrics(summary)
    assert m["checkout_ok"] is False
    assert m["checkout_gap"] == 3


def test_compute_metrics_surfaces_ready_for_payment_health_issues():
    summary = _sample_summary(
        gaps={
            "unhealthy_live": [
                {"slug": "jwt-generator", "code": 500},
                {"slug": "diffmaster", "code": 401},
            ],
            "canonical_url_drift": [
                {
                    "slug": "pdf-forge",
                    "url": "https://pdf-forge-alt.vercel.app",
                    "ideal_url": "https://pdf-forge.vercel.app",
                },
                {
                    "slug": "webhook-tester",
                    "url": "https://webhook-tester-alt.vercel.app",
                    "ideal_url": "https://webhook-tester.vercel.app",
                },
            ],
            "ready_for_payment_health": [
                {
                    "slug": "code-formatter-universal",
                    "code": 404,
                    "health_status": "not_found",
                }
            ],
        },
    )
    m = compute_metrics(summary)
    assert m["ready_for_payment_unhealthy"] == 1
    assert "code-formatter-universal" in [
        item.get("slug", "?") for item in m["ready_for_payment_entries"]
    ]
    assert "RFPU:1" in render_compact(m)
    assert "READY FOR PAYMENT" in render_full(m)


def test_render_compact_contains_grade():
    m = compute_metrics(_sample_summary())
    result = render_compact(m)
    assert "B" in result
    assert "85/90" in result
    assert "CH:83" in result
    assert "FH:2" in result


def test_render_full_contains_sections():
    m = compute_metrics(_sample_summary())
    result = render_full(m)
    assert "DASHBOARD" in result
    assert "PRODUCTS" in result
    assert "COVERAGE" in result
    assert "PIPELINE" in result
    assert "UNHEALTHY" in result
    assert "CANONICAL DRIFT" in result
    assert "Canonical healthy" in result
    assert "Fallback healthy" in result
    assert "jwt-generator" in result
    assert "pdf-forge" in result


def test_render_full_truncates_long_lists():
    unhealthy = [{"slug": f"app-{i}", "code": 500} for i in range(12)]
    summary = _sample_summary()
    summary["gaps"]["unhealthy_live"] = unhealthy
    m = compute_metrics(summary)
    result = render_full(m)
    assert "+4 more" in result


def test_render_json_valid():
    m = compute_metrics(_sample_summary())
    output = render_json(m)
    data = json.loads(output)
    assert data["live"] == 90
    assert data["grade"] == "B"
    assert data["canonical_healthy"] == 83
    assert data["fallback_healthy"] == 2
    assert data["unhealthy_slugs"] == ["jwt-generator", "diffmaster"]
    assert "pdf-forge" in data["drift_slugs"]
    assert "unhealthy_live" not in data


def test_render_json_no_internal_keys():
    m = compute_metrics(_sample_summary())
    output = render_json(m)
    data = json.loads(output)
    assert "unhealthy_live" not in data
    assert "drift_entries" not in data
    assert "unhealthy_live_count" in data
    assert "drift_entries_count" in data


def test_load_summary_valid(tmp_path):
    f = tmp_path / "STATE_SUMMARY.json"
    f.write_text(json.dumps({"live_count": 5, "healthy_count": 4}))
    data = load_summary(f)
    assert data["live_count"] == 5


def test_load_summary_missing(tmp_path):
    data = load_summary(tmp_path / "nonexistent.json")
    assert data == {}


def test_load_summary_invalid_json(tmp_path):
    f = tmp_path / "STATE_SUMMARY.json"
    f.write_text("not json")
    data = load_summary(f)
    assert data == {}


def test_main_compact(capsys):
    from scripts.health_dashboard import main
    main(["--compact"])
    out = capsys.readouterr().out
    assert "Portfolio" in out


def test_main_json(capsys):
    from scripts.health_dashboard import main
    rc = main(["--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert "grade" in data


def test_main_default(capsys):
    from scripts.health_dashboard import main
    rc = main([])
    assert rc == 0
    out = capsys.readouterr().out
    assert "DASHBOARD" in out


def test_render_full_no_unhealthy():
    m = compute_metrics({"live_count": 10, "healthy_count": 10})
    result = render_full(m)
    assert "UNHEALTHY" not in result


def test_render_full_no_drift():
    m = compute_metrics({"live_count": 10, "healthy_count": 10})
    result = render_full(m)
    assert "CANONICAL DRIFT" not in result
