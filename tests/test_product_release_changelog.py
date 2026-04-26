"""Tests for scripts.product_release_changelog.

Covers: status_breakdown, checkout_coverage, health_summary,
generate_changelog, format_markdown, CLI flags, edge cases.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


@pytest.fixture()
def sample_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    state_data: dict[str, Any] = {
        "products": {
            "active": [
                {"name": "Tool A", "slug": "tool-a", "status": "live", "url": "https://tool-a.vercel.app", "checkout_url": "https://checkout.a"},
                {"name": "Tool B", "slug": "tool-b", "status": "live", "url": "https://tool-b.vercel.app", "checkout_url": ""},
                {"name": "Tool C", "slug": "tool-c", "status": "building", "url": "", "checkout_url": ""},
                {"name": "Tool D", "slug": "tool-d", "status": "live", "url": "https://tool-d.vercel.app", "checkout_url": "https://checkout.d"},
            ]
        }
    }
    summary_data: dict[str, Any] = {
        "cycle": 42,
        "mode": "BUILD",
        "healthy_count": 3,
        "live_count": 3,
        "unhealthy_count": 0,
        "deploy_missing_or_bad_url": 1,
        "canonical_url_drift": 0,
    }
    state_file = tmp_path / "STATE.json"
    summary_file = tmp_path / "STATE_SUMMARY.json"
    _write_json(state_file, state_data)
    _write_json(summary_file, summary_data)

    import scripts.product_release_changelog as mod

    monkeypatch.setattr(mod, "STATE_PATH", state_file)
    monkeypatch.setattr(mod, "SUMMARY_PATH", summary_file)

    return {"state": state_data, "summary": summary_data}


class TestStatusBreakdown:
    def test_basic_counts(self) -> None:
        from scripts.product_release_changelog import status_breakdown

        products = [
            {"status": "live"},
            {"status": "live"},
            {"status": "building"},
            {"status": "pending"},
        ]
        result = status_breakdown(products)
        assert result == {"live": 2, "building": 1, "pending": 1}

    def test_empty(self) -> None:
        from scripts.product_release_changelog import status_breakdown

        assert status_breakdown([]) == {}

    def test_missing_status_key(self) -> None:
        from scripts.product_release_changelog import status_breakdown

        result = status_breakdown([{}, {"status": "live"}])
        assert result["unknown"] == 1
        assert result["live"] == 1


class TestCheckoutCoverage:
    def test_full_coverage(self) -> None:
        from scripts.product_release_changelog import checkout_coverage

        products = [
            {"checkout_url": "https://a.com"},
            {"checkout_url": "https://b.com"},
        ]
        co = checkout_coverage(products)
        assert co["coverage_pct"] == 100.0
        assert co["without_checkout"] == 0

    def test_zero_products(self) -> None:
        from scripts.product_release_changelog import checkout_coverage

        co = checkout_coverage([])
        assert co["coverage_pct"] == 0.0
        assert co["total"] == 0

    def test_partial_coverage(self) -> None:
        from scripts.product_release_changelog import checkout_coverage

        products = [
            {"checkout_url": "https://a.com"},
            {"checkout_url": ""},
            {"checkout_url": "https://c.com"},
            {"checkout_url": None},
        ]
        co = checkout_coverage(products)
        assert co["with_checkout"] == 2
        assert co["without_checkout"] == 2
        assert co["coverage_pct"] == 50.0

    def test_non_http_url_not_counted(self) -> None:
        from scripts.product_release_changelog import checkout_coverage

        products = [
            {"checkout_url": "ftp://bad.com"},
            {"checkout_url": "https://good.com"},
        ]
        co = checkout_coverage(products)
        assert co["with_checkout"] == 1


class TestHealthSummary:
    def test_from_summary(self) -> None:
        from scripts.product_release_changelog import health_summary

        summary = {
            "healthy_count": 10,
            "live_count": 12,
            "unhealthy_count": 2,
            "deploy_missing_or_bad_url": 3,
            "canonical_url_drift": 1,
        }
        h = health_summary(summary)
        assert h["healthy"] == 10
        assert h["live"] == 12
        assert h["unhealthy"] == 2
        assert h["deploy_missing"] == 3
        assert h["canonical_drift"] == 1

    def test_empty_summary(self) -> None:
        from scripts.product_release_changelog import health_summary

        h = health_summary({})
        assert h["healthy"] == 0
        assert h["live"] == 0


class TestGenerateChangelog:
    def test_full_changelog(self, sample_state: dict[str, Any]) -> None:
        from scripts.product_release_changelog import generate_changelog

        cl = generate_changelog()
        assert cl["cycle"] == 42
        assert cl["mode"] == "BUILD"
        assert "live" in cl["status_breakdown"]
        assert cl["checkout_coverage"]["total"] == 4
        assert cl["checkout_coverage"]["with_checkout"] == 2
        assert cl["health"]["healthy"] == 3

    def test_verbose_includes_sample(self, sample_state: dict[str, Any]) -> None:
        from scripts.product_release_changelog import generate_changelog

        cl = generate_changelog(verbose=True)
        assert "products_sample" in cl
        assert len(cl["products_sample"]) <= 10
        first = cl["products_sample"][0]
        assert "name" in first
        assert "slug" in first

    def test_no_state_files(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        from scripts.product_release_changelog import generate_changelog
        import scripts.product_release_changelog as mod

        monkeypatch.setattr(mod, "STATE_PATH", tmp_path / "nonexistent_STATE.json")
        monkeypatch.setattr(mod, "SUMMARY_PATH", tmp_path / "nonexistent_SUMMARY.json")

        cl = generate_changelog()
        assert cl["status_breakdown"] == {}
        assert cl["checkout_coverage"]["total"] == 0


class TestFormatMarkdown:
    def test_output_contains_sections(self, sample_state: dict[str, Any]) -> None:
        from scripts.product_release_changelog import format_markdown, generate_changelog

        cl = generate_changelog()
        md = format_markdown(cl)
        assert "# Product Release Changelog" in md
        assert "## Status Breakdown" in md
        assert "## Checkout Coverage" in md
        assert "## Health Summary" in md

    def test_verbose_sample_section(self, sample_state: dict[str, Any]) -> None:
        from scripts.product_release_changelog import format_markdown, generate_changelog

        cl = generate_changelog(verbose=True)
        md = format_markdown(cl)
        assert "## Sample Products" in md
        assert "Tool A" in md


class TestCLI:
    def test_json_output(self, sample_state: dict[str, Any], capsys: pytest.CaptureFixture[str]) -> None:
        from scripts.product_release_changelog import main

        import sys

        old_argv = sys.argv
        sys.argv = ["product_release_changelog", "--json"]
        try:
            main()
        finally:
            sys.argv = old_argv

        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["cycle"] == 42
        assert "status_breakdown" in data

    def test_markdown_output(self, sample_state: dict[str, Any], capsys: pytest.CaptureFixture[str]) -> None:
        from scripts.product_release_changelog import main

        import sys

        old_argv = sys.argv
        sys.argv = ["product_release_changelog"]
        try:
            main()
        finally:
            sys.argv = old_argv

        out = capsys.readouterr().out
        assert "Cycle: 42" in out
        assert "BUILD" in out
