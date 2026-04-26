import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from vercel_response_monitor import (
    load_live_products,
    probe_url,
    run_checks,
    summarize,
    format_report,
)


class TestLoadLiveProducts:
    def test_returns_live_products_with_url(self, tmp_path, monkeypatch):
        state_file = tmp_path / "STATE_SUMMARY.json"
        state_file.write_text(json.dumps({
            "products": [
                {"n": "A", "s": "a", "st": "live", "v": "https://a.vercel.app"},
                {"n": "B", "s": "b", "st": "building", "v": "https://b.vercel.app"},
                {"n": "C", "s": "c", "st": "live", "v": None},
            ]
        }))
        monkeypatch.setattr("vercel_response_monitor.STATE_FILE", state_file)
        result = load_live_products()
        assert len(result) == 1
        assert result[0]["s"] == "a"

    def test_returns_empty_on_missing_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("vercel_response_monitor.STATE_FILE", tmp_path / "nope.json")
        assert load_live_products() == []

    def test_returns_empty_on_invalid_json(self, tmp_path, monkeypatch):
        f = tmp_path / "STATE_SUMMARY.json"
        f.write_text("not json")
        monkeypatch.setattr("vercel_response_monitor.STATE_FILE", f)
        assert load_live_products() == []


class TestProbeUrl:
    def test_success_200(self):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        with patch("vercel_response_monitor.urllib.request.urlopen", return_value=mock_resp):
            result = probe_url("https://example.com")
        assert result["status"] == 200
        assert result["error"] is None
        assert result["elapsed_ms"] >= 0

    def test_http_error(self):
        import urllib.error
        err = urllib.error.HTTPError("url", 403, "Forbidden", {}, None)
        with patch("vercel_response_monitor.urllib.request.urlopen", side_effect=err):
            result = probe_url("https://example.com")
        assert result["status"] == 403
        assert "403" in result["error"]

    def test_url_error(self):
        import urllib.error
        err = urllib.error.URLError("Connection refused")
        with patch("vercel_response_monitor.urllib.request.urlopen", side_effect=err):
            result = probe_url("https://example.com")
        assert result["status"] is None
        assert result["error"] is not None

    def test_timeout_error(self):
        with patch("vercel_response_monitor.urllib.request.urlopen", side_effect=TimeoutError("timed out")):
            result = probe_url("https://example.com", timeout=1)
        assert result["error"] is not None
        assert result["status"] is None


class TestRunChecks:
    def test_probes_all_products(self):
        products = [
            {"s": "prod-a", "n": "Product A", "v": "https://a.vercel.app"},
            {"s": "prod-b", "n": "Product B", "v": "https://b.vercel.app"},
        ]
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        with patch("vercel_response_monitor.urllib.request.urlopen", return_value=mock_resp):
            results = run_checks(products, timeout=5, workers=2)
        assert len(results) == 2
        slugs = {r["slug"] for r in results}
        assert slugs == {"prod-a", "prod-b"}


class TestSummarize:
    def test_all_ok(self):
        results = [
            {"slug": "a", "status": 200, "error": None, "elapsed_ms": 100},
            {"slug": "b", "status": 200, "error": None, "elapsed_ms": 200},
        ]
        s = summarize(results)
        assert s["total"] == 2
        assert s["ok_200"] == 2
        assert s["error_count"] == 0
        assert s["slow_count"] == 0
        assert s["avg_ms"] == 150

    def test_mixed_status(self):
        results = [
            {"slug": "a", "status": 200, "error": None, "elapsed_ms": 500},
            {"slug": "b", "status": 403, "error": "HTTPError: 403", "elapsed_ms": 150},
            {"slug": "c", "status": None, "error": "URLError: timeout", "elapsed_ms": 8000},
        ]
        s = summarize(results)
        assert s["total"] == 3
        assert s["ok_200"] == 1
        assert s["error_count"] == 2
        assert s["slow_count"] == 1
        assert s["by_status"] == {200: 1, 403: 1}

    def test_empty(self):
        s = summarize([])
        assert s["total"] == 0
        assert s["ok_200"] == 0
        assert s["avg_ms"] == 0


class TestFormatReport:
    def test_contains_key_sections(self):
        summary = {
            "total": 5,
            "ok_200": 4,
            "error_count": 1,
            "slow_count": 1,
            "avg_ms": 350,
            "by_status": {200: 4, 403: 1},
            "errors": ["slug-x: HTTPError: 403"],
            "slow": [{"slug": "slug-y", "ms": 5000}],
        }
        report = format_report(summary, [])
        assert "Total probed: 5" in report
        assert "HTTP 200: 4/5 (80%)" in report
        assert "HTTP 200: 4" in report
        assert "HTTP 403: 1" in report
        assert "slug-x" in report
        assert "slug-y" in report
        assert "5000ms" in report
