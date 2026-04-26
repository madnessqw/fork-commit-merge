"""Tests for checkout_url_health — URL reachability checker."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_url_health import (
    CheckoutResult,
    HealthReport,
    _load_products,
    format_report,
    run_health_check,
)


@pytest.fixture
def sample_summary(tmp_path: Path) -> Path:
    data = {
        "products": [
            {"n": "Test A", "s": "test-a", "st": "live", "c": "https://buy.polar.sh/abc123"},
            {"n": "Test B", "s": "test-b", "st": "live", "c": "https://buy.polar.sh/def456"},
            {"n": "No URL", "s": "no-url", "st": "live", "c": ""},
        ]
    }
    p = tmp_path / "STATE_SUMMARY.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


class TestCheckoutResult:
    def test_defaults(self):
        r = CheckoutResult(slug="x", name="X", checkout_url="http://x")
        assert r.status_code is None
        assert r.reachable is False
        assert r.error is None

    def test_reachable_set(self):
        r = CheckoutResult(slug="x", name="X", checkout_url="http://x", status_code=200, reachable=True)
        assert r.reachable


class TestHealthReport:
    def test_score_100_when_all_reachable(self):
        report = HealthReport(total=5, reachable=5)
        assert report.score == 100
        assert report.grade == "A+"

    def test_score_0_when_none_reachable(self):
        report = HealthReport(total=5, reachable=0)
        assert report.score == 0
        assert report.grade == "F"

    def test_score_empty(self):
        report = HealthReport(total=0)
        assert report.score == 100

    def test_grade_boundaries(self):
        assert HealthReport(total=100, reachable=98).grade == "A+"
        assert HealthReport(total=100, reachable=95).grade == "A"
        assert HealthReport(total=100, reachable=90).grade == "B"
        assert HealthReport(total=100, reachable=80).grade == "C"
        assert HealthReport(total=100, reachable=70).grade == "D"


class TestLoadProducts:
    def test_loads_all(self, sample_summary: Path):
        products = _load_products(sample_summary)
        assert len(products) == 3

    def test_slug_filter(self, sample_summary: Path):
        products = _load_products(sample_summary, slug_filter="test-a")
        assert len(products) == 1
        assert products[0]["s"] == "test-a"

    def test_missing_file(self, tmp_path: Path):
        with pytest.raises(SystemExit):
            _load_products(tmp_path / "nonexistent.json")


class TestRunHealthCheck:
    @patch("scripts.checkout_url_health._check_url")
    def test_mixed_results(self, mock_check, sample_summary: Path):
        mock_check.side_effect = [
            CheckoutResult(slug="test-a", name="Test A", checkout_url="https://buy.polar.sh/abc123",
                          status_code=200, reachable=True, latency_ms=50),
            CheckoutResult(slug="test-b", name="Test B", checkout_url="https://buy.polar.sh/def456",
                          status_code=404, reachable=False, error="Not Found"),
        ]
        report = run_health_check(sample_summary)
        assert report.total == 3
        assert report.reachable == 1
        assert report.unreachable == 1
        assert report.missing_url == 1

    @patch("scripts.checkout_url_health._check_url")
    def test_quick_mode_limits(self, mock_check, sample_summary: Path):
        mock_check.return_value = CheckoutResult(
            slug="x", name="X", checkout_url="http://x", status_code=200, reachable=True
        )
        report = run_health_check(sample_summary, quick=True)
        assert report.total == 3


class TestFormatReport:
    def test_json_output(self):
        report = HealthReport(total=2, reachable=1, unreachable=1)
        report.results = [
            CheckoutResult(slug="a", name="A", checkout_url="http://a",
                          status_code=200, reachable=True),
        ]
        output = format_report(report, json_output=True)
        parsed = json.loads(output)
        assert parsed["score"] == 50
        assert parsed["grade"] == "F"
        assert len(parsed["results"]) == 1

    def test_markdown_output(self):
        report = HealthReport(total=2, reachable=2)
        output = format_report(report)
        assert "Score: 100/100 (A+)" in output
        assert "Reachable: 2/2" in output

    def test_markdown_shows_unreachable(self):
        report = HealthReport(total=2, reachable=0, unreachable=2)
        report.results = [
            CheckoutResult(slug="bad", name="Bad", checkout_url="http://bad",
                          status_code=500, reachable=False, error="timeout"),
        ]
        output = format_report(report)
        assert "## Unreachable" in output
        assert "bad" in output

    def test_markdown_shows_missing(self):
        report = HealthReport(total=1, reachable=0, missing_url=1)
        report.results = [
            CheckoutResult(slug="no-url", name="No URL", checkout_url=""),
        ]
        output = format_report(report)
        assert "## Missing URL" in output
        assert "no-url" in output
