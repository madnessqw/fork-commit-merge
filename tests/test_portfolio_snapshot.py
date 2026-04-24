import json
from pathlib import Path

from scripts.portfolio_snapshot import (
    _grade,
    _next_actions,
    _pct,
    snapshot,
    to_markdown,
)

FAKE_SUMMARY = {
    "cycle": 42,
    "mode": "OPTIMIZE",
    "active_count": 100,
    "live_count": 80,
    "healthy_count": 76,
    "canonical_healthy_count": 74,
    "fallback_healthy_count": 2,
    "unhealthy_count": 4,
    "checkout_gap_count": 0,
    "deploy_missing_or_bad_url": 5,
    "spec_ready_count": 10,
    "deploy_readiness_count": 8,
    "gaps": {
        "unhealthy_live": [
            {"slug": "broken-app", "code": 500, "health_status": "error_500"},
            {"slug": "auth-app", "code": 401, "health_status": "unauthorized"},
        ],
        "canonical_url_drift": [
            {
                "slug": "drift-app",
                "url": "https://drift-app-alt.vercel.app",
                "ideal_url": "https://drift-app.vercel.app",
                "canonical_code": 404,
                "canonical_status": "not_found",
            }
        ],
        "fallback_healthy": [
            {"slug": "drift-app"},
        ],
        "deploy_readiness": [
            {
                "slug": "undeployed-1",
                "missing_url_fields": ["vercel_url", "deployment_url"],
                "missing_state_fields": ["deployed_cycle"],
            },
        ],
    },
}


def test_pct():
    assert _pct(76, 80) == 95.0
    assert _pct(0, 0) == 0.0
    assert _pct(1, 3) == 33.3


def test_grade():
    assert _grade(95) == "A"
    assert _grade(94.9) == "B"
    assert _grade(85) == "B"
    assert _grade(84.9) == "C"
    assert _grade(70) == "C"
    assert _grade(50) == "D"
    assert _grade(49.9) == "F"
    assert _grade(0) == "F"


def test_snapshot_basic_fields():
    snap = snapshot(FAKE_SUMMARY)
    assert snap["cycle"] == 42
    assert snap["mode"] == "OPTIMIZE"
    assert snap["live"] == 80
    assert snap["healthy"] == 76
    assert snap["health_pct"] == 95.0
    assert snap["grade"] == "A"
    assert snap["canonical_healthy"] == 74
    assert snap["fallback_healthy"] == 2
    assert snap["unhealthy"] == 4
    assert snap["checkout_gap"] == 0
    assert snap["deploy_gap"] == 5
    assert snap["codex_handoff"] is True


def test_snapshot_unhealthy_detail():
    snap = snapshot(FAKE_SUMMARY)
    assert len(snap["unhealthy_detail"]) == 2
    assert snap["unhealthy_detail"][0]["slug"] == "broken-app"
    assert snap["unhealthy_detail"][0]["code"] == 500


def test_snapshot_drift_detail():
    snap = snapshot(FAKE_SUMMARY)
    assert len(snap["drift_detail"]) == 1
    assert snap["drift_detail"][0]["slug"] == "drift-app"
    assert snap["drift_detail"][0]["canonical_status"] == "not_found"


def test_snapshot_deploy_gap():
    snap = snapshot(FAKE_SUMMARY)
    assert len(snap["deploy_gap_detail"]) == 1
    assert snap["deploy_gap_detail"][0]["slug"] == "undeployed-1"


def test_snapshot_next_actions():
    snap = snapshot(FAKE_SUMMARY)
    assert len(snap["next_actions"]) >= 1
    assert any("unhealthy" in a for a in snap["next_actions"])


def test_snapshot_empty():
    snap = snapshot({})
    assert snap["live"] == 0
    assert snap["health_pct"] == 0.0
    assert snap["grade"] == "F"
    assert snap["codex_handoff"] is False
    assert "healthy" in snap["next_actions"][0].lower()


def test_to_markdown():
    snap = snapshot(FAKE_SUMMARY)
    md = to_markdown(snap)
    assert "# Portfolio Snapshot" in md
    assert "42" in md
    assert "OPTIMIZE" in md
    assert "broken-app" in md
    assert "drift-app" in md
    assert "undeployed-1" in md
    assert "Next Actions" in md


def test_to_markdown_healthy_portfolio():
    healthy = {
        "cycle": 1,
        "mode": "IDLE",
        "active_count": 10,
        "live_count": 10,
        "healthy_count": 10,
        "canonical_healthy_count": 10,
        "fallback_healthy_count": 0,
        "unhealthy_count": 0,
        "checkout_gap_count": 0,
        "deploy_missing_or_bad_url": 0,
        "spec_ready_count": 0,
        "deploy_readiness_count": 0,
        "gaps": {},
    }
    snap = snapshot(healthy)
    md = to_markdown(snap)
    assert "**Grade:** A" in md
    assert "Unhealthy" not in md or "| 0 |" in md


def test_next_actions_all_clear():
    actions = _next_actions(0, 0, 0, [], 0)
    assert len(actions) == 1
    assert "healthy" in actions[0].lower()


def test_next_actions_multiple():
    actions = _next_actions(3, 2, 5, [{"slug": "x"}], 1)
    assert len(actions) == 5


def test_snapshot_fallback_slugs():
    snap = snapshot(FAKE_SUMMARY)
    assert "drift-app" in snap["fallback_slugs"]


def test_snapshot_rebuilds_fallback_visibility_from_compact_summary():
    compact = {
        "cycle": 99,
        "mode": "OPTIMIZE",
        "active_count": 2,
        "live_count": 2,
        "healthy_count": 1,
        "canonical_healthy_count": 0,
        "unhealthy_count": 1,
        "checkout_gap_count": 0,
        "deploy_missing_or_bad_url": 1,
        "spec_ready_count": 0,
        "deploy_readiness_count": 0,
        "canonical_url_drift_products": ["fallback-tool"],
        "fallback_healthy_products": ["fallback-tool"],
        "products": [
            {
                "n": "Broken Tool",
                "s": "broken-tool",
                "st": "live",
                "v": "https://broken-tool.vercel.app",
                "c": None,
            },
            {
                "n": "Fallback Tool",
                "s": "fallback-tool",
                "st": "live",
                "v": "https://fallback-tool-preview.vercel.app",
                "c": None,
            },
        ],
        "gaps": {
            "unhealthy_live": [
                {
                    "slug": "broken-tool",
                    "code": 500,
                    "health_status": "error_500",
                    "url": "https://broken-tool.vercel.app",
                }
            ],
            "pending_health": [],
            "missing_checkout": [],
            "missing_url": [],
            "deploy_readiness": [],
        },
    }

    snap = snapshot(compact)
    assert snap["fallback_healthy"] == 1
    assert snap["codex_handoff"] is True
    assert snap["drift_detail"][0]["slug"] == "fallback-tool"
    assert snap["fallback_slugs"] == ["fallback-tool"]
    assert any("Resolve 1 canonical URL drifts" in action for action in snap["next_actions"])


def test_snapshot_ts_present():
    snap = snapshot(FAKE_SUMMARY)
    assert "ts" in snap
    assert "T" in snap["ts"]
