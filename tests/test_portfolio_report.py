from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.portfolio_report import (
    _checkout_coverage,
    format_markdown,
    generate_report,
)


def _make_summary(**overrides):
    base = {
        "cycle": 42,
        "mode": "OPTIMIZE",
        "active_count": 10,
        "live_count": 8,
        "healthy_count": 7,
        "unhealthy_count": 1,
        "checkout_gap_count": 2,
        "deploy_missing_or_bad_url": 3,
        "gaps": {
            "missing_checkout": ["slug-a", "slug-b"],
            "canonical_url_drift": [{"slug": "drift-1"}],
        },
    }
    base.update(overrides)
    return base


@pytest.fixture
def tmp_summary(tmp_path):
    p = tmp_path / "STATE_SUMMARY.json"
    p.write_text(json.dumps(_make_summary()), encoding="utf-8")
    return p


class TestCheckoutCoverage:
    def test_basic(self):
        summary = _make_summary()
        result = _checkout_coverage(summary)
        assert result["live_count"] == 8
        assert result["gap_count"] == 2
        assert result["covered_count"] == 6
        assert result["coverage_pct"] == 75.0
        assert result["missing_slugs"] == ["slug-a", "slug-b"]

    def test_zero_live(self):
        summary = _make_summary(live_count=0, checkout_gap_count=0)
        result = _checkout_coverage(summary)
        assert result["coverage_pct"] == 0.0
        assert result["covered_count"] == 0

    def test_full_coverage(self):
        summary = _make_summary(checkout_gap_count=0)
        result = _checkout_coverage(summary)
        assert result["coverage_pct"] == 100.0


class TestGenerateReport:
    def test_reads_summary(self, tmp_summary):
        with patch("scripts.portfolio_report.audit_product_prices", return_value=[]), \
             patch("scripts.portfolio_report.detect_duplicates", return_value={"duplicate_checkout_urls": {}}):
            report = generate_report(tmp_summary)
        assert report["cycle"] == 42
        assert report["mode"] == "OPTIMIZE"
        assert report["live_products"] == 8
        assert report["deploy_gap"] == 3
        assert report["canonical_drift"] == 1

    def test_missing_file(self, tmp_path):
        report = generate_report(tmp_path / "nonexistent.json")
        assert "error" in report

    def test_health_section(self, tmp_summary):
        with patch("scripts.portfolio_report.audit_product_prices", return_value=[]), \
             patch("scripts.portfolio_report.detect_duplicates", return_value={"duplicate_checkout_urls": {}}):
            report = generate_report(tmp_summary)
        assert "health" in report
        assert "grade" in report["health"]
        assert "health_pct" in report["health"]

    def test_triage_section(self, tmp_summary):
        with patch("scripts.portfolio_report.audit_product_prices", return_value=[]), \
             patch("scripts.portfolio_report.detect_duplicates", return_value={"duplicate_checkout_urls": {}}):
            report = generate_report(tmp_summary)
        assert "triage" in report
        assert "total_unhealthy" in report["triage"]
        assert "codex_handoff" in report["triage"]

    def test_checkout_section(self, tmp_summary):
        with patch("scripts.portfolio_report.audit_product_prices", return_value=[]), \
             patch("scripts.portfolio_report.detect_duplicates", return_value={"duplicate_checkout_urls": {}}):
            report = generate_report(tmp_summary)
        assert report["checkout"]["gap_count"] == 2
        assert report["checkout"]["coverage_pct"] == 75.0

    def test_exception_handling(self, tmp_summary):
        with patch("scripts.portfolio_report.audit_product_prices", side_effect=RuntimeError("boom")), \
             patch("scripts.portfolio_report.detect_duplicates", return_value={"duplicate_checkout_urls": {}}):
            report = generate_report(tmp_summary)
        assert report["price_issues_count"] == 0

    def test_canonical_drift_uses_top_level_count_when_gap_detail_missing(self, tmp_path):
        summary = _make_summary(
            canonical_url_drift=2,
            gaps={"missing_checkout": ["slug-a", "slug-b"]},
        )
        summary_file = tmp_path / "STATE_SUMMARY.json"
        summary_file.write_text(json.dumps(summary), encoding="utf-8")

        with patch("scripts.portfolio_report.audit_product_prices", return_value=[]), \
             patch("scripts.portfolio_report.detect_duplicates", return_value={"duplicate_checkout_urls": {}}):
            report = generate_report(summary_file)

        assert report["canonical_drift"] == 2


class TestFormatMarkdown:
    def test_basic_render(self):
        report = generate_report.__wrapped__ if hasattr(generate_report, "__wrapped__") else None
        sample = {
            "ts": "2026-04-24 12:00",
            "cycle": 42,
            "mode": "OPTIMIZE",
            "live_products": 88,
            "deploy_gap": 5,
            "canonical_drift": 2,
            "health": {"grade": "A", "health_pct": 96.7, "healthy_count": 85, "unhealthy_count": 3},
            "triage": {"total_unhealthy": 3, "high": 1, "medium": 1, "low": 1, "top_high_slugs": ["jwt-gen"], "codex_handoff": True},
            "checkout": {"covered_count": 86, "live_count": 88, "coverage_pct": 97.7, "missing_slugs": ["a", "b"]},
            "checkout_duplicates": 0,
            "price_issues_count": 0,
        }
        md = format_markdown(sample)
        assert "# Portfolio Report" in md
        assert "Grade: **A**" in md
        assert "jwt-gen" in md
        assert "Missing: a, b" in md
        assert "Codex handoff: YES" in md

    def test_no_missing_checkout(self):
        sample = {
            "ts": "2026-04-24 12:00",
            "cycle": 1,
            "mode": "IDLE",
            "live_products": 10,
            "deploy_gap": 0,
            "canonical_drift": 0,
            "health": {"grade": "A", "health_pct": 100.0, "healthy_count": 10, "unhealthy_count": 0},
            "triage": {"total_unhealthy": 0, "high": 0, "medium": 0, "low": 0, "top_high_slugs": [], "codex_handoff": False},
            "checkout": {"covered_count": 10, "live_count": 10, "coverage_pct": 100.0, "missing_slugs": []},
            "checkout_duplicates": 0,
            "price_issues_count": 0,
        }
        md = format_markdown(sample)
        assert "Missing:" not in md
        assert "Codex handoff: no" in md
