from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.retry_probe import (
    _slug_from_summary,
    format_table,
    probe_url,
    retry_probe,
)


@pytest.fixture
def sample_summary(tmp_path: Path) -> Path:
    data = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "jwt-generator", "code": 500, "url": "https://jwt-generator.vercel.app"},
                {"slug": "diffmaster", "code": 401, "url": "https://diffmaster.vercel.app"},
            ],
            "canonical_url_drift": [
                {"slug": "pdf-forge", "canonical_code": 404, "ideal_url": "https://pdf-forge.vercel.app"},
            ],
        }
    }
    p = tmp_path / "STATE_SUMMARY.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


class TestSlugFromSummary:
    def test_extracts_unhealthy(self, sample_summary: Path):
        with open(sample_summary) as f:
            summary = json.load(f)
        items = _slug_from_summary(summary)
        slugs = {i["slug"] for i in items}
        assert "jwt-generator" in slugs
        assert "diffmaster" in slugs
        assert "pdf-forge" in slugs

    def test_empty_gaps(self, tmp_path: Path):
        p = tmp_path / "STATE_SUMMARY.json"
        p.write_text(json.dumps({"gaps": {}}))
        with open(p) as f:
            summary = json.load(f)
        assert _slug_from_summary(summary) == []


class TestProbeUrl:
    @patch("scripts.retry_probe.subprocess.run")
    def test_success(self, mock_run: MagicMock):
        mock_run.return_value = MagicMock(stdout="200 https://example.com")
        result = probe_url("https://example.com")
        assert result["code"] == 200
        assert result["effective_url"] == "https://example.com"

    @patch("scripts.retry_probe.subprocess.run")
    def test_error_code(self, mock_run: MagicMock):
        mock_run.return_value = MagicMock(stdout="500 https://example.com")
        result = probe_url("https://example.com")
        assert result["code"] == 500

    @patch("scripts.retry_probe.subprocess.run")
    def test_timeout(self, mock_run: MagicMock):
        mock_run.return_value = MagicMock(stdout="0 ")
        result = probe_url("https://example.com")
        assert result["code"] == 0

    @patch("scripts.retry_probe.subprocess.run", side_effect=Exception("boom"))
    def test_exception(self, mock_run: MagicMock):
        result = probe_url("https://example.com")
        assert result["code"] == 0


class TestRetryProbe:
    @patch("scripts.retry_probe.probe_url")
    def test_retry_recovers(self, mock_probe, sample_summary: Path):
        mock_probe.side_effect = [
            {"code": 200, "effective_url": "https://jwt-generator.vercel.app", "raw": ""},
            {"code": 401, "effective_url": "https://diffmaster.vercel.app", "raw": ""},
            {"code": 200, "effective_url": "https://pdf-forge.vercel.app", "raw": ""},
        ]
        results = retry_probe(summary_path=sample_summary)
        assert len(results) == 3
        recovered = [r for r in results if r["recovered"]]
        assert len(recovered) == 2
        jwt = next(r for r in results if r["slug"] == "jwt-generator")
        assert jwt["recovered"] is True
        diff = next(r for r in results if r["slug"] == "diffmaster")
        assert diff["recovered"] is False

    @patch("scripts.retry_probe.probe_url")
    def test_retry_uses_compact_canonical_drift_snapshot(self, mock_probe, tmp_path: Path):
        summary = {
            "gaps": {
                "unhealthy_live": [],
                "canonical_url_drift": [],
            },
            "canonical_url_drift": 1,
            "canonical_url_drift_products": ["pdf-forge"],
            "products": [
                {
                    "s": "pdf-forge",
                    "v": "https://pdf-forge-five.vercel.app",
                }
            ],
        }
        p = tmp_path / "STATE_SUMMARY.json"
        p.write_text(json.dumps(summary), encoding="utf-8")
        mock_probe.return_value = {
            "code": 200,
            "effective_url": "https://pdf-forge.vercel.app",
            "raw": "",
        }

        results = retry_probe(summary_path=p)
        assert len(results) == 1
        assert results[0]["slug"] == "pdf-forge"
        assert results[0]["category"] == "canonical_drift"
        assert results[0]["url"] == "https://pdf-forge.vercel.app"

    @patch("scripts.retry_probe.probe_url")
    def test_slug_filter(self, mock_probe, sample_summary: Path):
        mock_probe.return_value = {"code": 200, "effective_url": "x", "raw": ""}
        results = retry_probe(summary_path=sample_summary, slug_filter="jwt")
        assert len(results) == 1
        assert results[0]["slug"] == "jwt-generator"

    @patch("scripts.retry_probe.probe_url")
    def test_no_targets_returns_empty(self, mock_probe, tmp_path: Path):
        p = tmp_path / "STATE_SUMMARY.json"
        p.write_text(json.dumps({"gaps": {"unhealthy_live": [], "canonical_url_drift": []}}))
        results = retry_probe(summary_path=p)
        assert results == []
        mock_probe.assert_not_called()


class TestFormatTable:
    def test_empty(self):
        assert "No unhealthy" in format_table([])

    def test_with_results(self):
        results = [
            {
                "slug": "test-prod",
                "category": "unhealthy",
                "prior_code": 500,
                "retried_code": 200,
                "recovered": True,
                "url": "https://test-prod.vercel.app",
            }
        ]
        table = format_table(results)
        assert "test-prod" in table
        assert "YES" in table
        assert "**Recovered:** 1/1" in table

    def test_recovery_percentage(self):
        results = [
            {
                "slug": "prod-a",
                "category": "unhealthy",
                "prior_code": 500,
                "retried_code": 200,
                "recovered": True,
                "url": "https://prod-a.vercel.app",
            },
            {
                "slug": "prod-b",
                "category": "unhealthy",
                "prior_code": 500,
                "retried_code": 500,
                "recovered": False,
                "url": "https://prod-b.vercel.app",
            },
        ]
        table = format_table(results)
        assert "50%" in table
        assert "**Recovered:** 1/2" in table


