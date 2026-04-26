from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
for p in (str(ROOT), str(SCRIPTS)):
    if p not in sys.path:
        sys.path.insert(0, p)

sys.modules.pop("product_readiness_scorer", None)
sys.modules.pop("product_lifecycle_analyzer", None)
sys.modules.pop("portfolio_overlap_analyzer", None)
sys.modules.pop("portfolio_summary_reporter", None)

from portfolio_summary_reporter import (
    _collect_state_meta,
    _load_json,
    format_report,
    generate_report,
)


def _make_state(
    cycle=1200,
    mode="OPTIMIZE",
    active=5,
    live=5,
    healthy=5,
    missing_checkout=0,
    deploy_missing=0,
    drift=0,
    balance=0.0,
):
    return {
        "cycle": cycle,
        "mode": mode,
        "active_count": active,
        "live_count": live,
        "healthy_count": healthy,
        "missing_checkout": missing_checkout,
        "deploy_missing_or_bad_url": deploy_missing,
        "canonical_url_drift": drift,
        "balance": balance,
        "last_updated": "2026-04-26T00:00:00Z",
        "products": {
            "active": [
                {
                    "slug": f"prod-{i}",
                    "name": f"Product {i}",
                    "status": "live",
                    "st": "live",
                    "health_status": "healthy",
                    "last_health_code": 200,
                    "vercel_url": f"https://prod-{i}.vercel.app",
                    "ideal_vercel_url": f"https://prod-{i}.vercel.app",
                    "v": f"https://prod-{i}.vercel.app",
                    "checkout_url": f"https://buy.polar.sh/polar_cl_{i}",
                    "c": f"https://buy.polar.sh/polar_cl_{i}",
                    "price": "$19",
                    "seo_optimized": True,
                    "og_optimized": True,
                    "schema_optimized": True,
                    "checkout_status": "active",
                }
                for i in range(active)
            ]
        },
    }


def _make_summary(products):
    return {
        "cycle": 1200,
        "products": products,
    }


@pytest.fixture
def tmp_state(tmp_path):
    return tmp_path / "STATE.json"


@pytest.fixture
def tmp_summary(tmp_path):
    return tmp_path / "STATE_SUMMARY.json"


class TestCollectStateMeta:
    def test_extracts_fields(self):
        state = _make_state(cycle=42, mode="BUILD", active=10)
        meta = _collect_state_meta(state)
        assert meta["cycle"] == 42
        assert meta["mode"] == "BUILD"
        assert meta["active_count"] == 10
        assert meta["balance"] == 0.0

    def test_missing_fields_default(self):
        meta = _collect_state_meta({})
        assert meta["cycle"] == 0
        assert meta["mode"] == "UNKNOWN"
        assert meta["active_count"] == 0


class TestLoadJson:
    def test_valid_json(self, tmp_state):
        tmp_state.write_text('{"key": "value"}')
        result = _load_json(tmp_state)
        assert result == {"key": "value"}

    def test_missing_file(self):
        result = _load_json(Path("/nonexistent/file.json"))
        assert result == {}

    def test_invalid_json(self, tmp_state):
        tmp_state.write_text("not json")
        result = _load_json(tmp_state)
        assert result == {}


class TestGenerateReport:
    def test_full_report_structure(self, tmp_state, tmp_summary):
        state = _make_state(active=3)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        assert "state" in report
        assert "readiness" in report
        assert "lifecycle" in report
        assert "overlap" in report
        assert "insights" in report
        assert "generated_at" in report
        assert report["state"]["cycle"] == 1200
        assert report["state"]["active_count"] == 3

    def test_healthy_portfolio_insight(self, tmp_state, tmp_summary):
        state = _make_state(active=2, missing_checkout=0, deploy_missing=0, drift=0)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        assert any("fully healthy" in i.lower() for i in report["insights"])

    def test_missing_checkout_insight(self, tmp_state, tmp_summary):
        state = _make_state(active=2, missing_checkout=3)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        assert any("missing checkout" in i for i in report["insights"])

    def test_drift_insight(self, tmp_state, tmp_summary):
        state = _make_state(active=2, drift=7)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        assert any("canonical drift" in i for i in report["insights"])

    def test_deploy_gap_insight(self, tmp_state, tmp_summary):
        state = _make_state(active=2, deploy_missing=5)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        assert any("deploy gap" in i for i in report["insights"])

    def test_readiness_data(self, tmp_state, tmp_summary):
        state = _make_state(active=3)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        assert report["readiness"]["total"] == 3
        assert isinstance(report["readiness"]["avg_score"], float)

    def test_lifecycle_data(self, tmp_state, tmp_summary):
        state = _make_state(active=3)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        assert isinstance(report["lifecycle"]["health_score"], float)


class TestFormatReport:
    def test_contains_key_sections(self, tmp_state, tmp_summary):
        state = _make_state(active=2)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        formatted = format_report(report)

        assert "# Portfolio Summary Report" in formatted
        assert "## State Overview" in formatted
        assert "## Readiness Score" in formatted
        assert "## Lifecycle" in formatted
        assert "## Portfolio Overlap" in formatted
        assert "## Insights" in formatted

    def test_includes_cycle(self, tmp_state, tmp_summary):
        state = _make_state(cycle=999)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        formatted = format_report(report)
        assert "999" in formatted

    def test_includes_balance(self, tmp_state, tmp_summary):
        state = _make_state(balance=12.50)
        tmp_state.write_text(json.dumps(state))
        summary = _make_summary(state["products"]["active"])
        tmp_summary.write_text(json.dumps(summary))

        report = generate_report(tmp_state, tmp_summary)
        formatted = format_report(report)
        assert "$12.50" in formatted
