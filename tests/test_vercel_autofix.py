from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.vercel_autofix import (
    DIAGNOSIS_RULES,
    _check_api_health,
    _inspect_product_dir,
    autofix_deprecated_routes,
    diagnose_product,
    format_report,
    run_autofix,
)


@pytest.fixture
def sample_summary(tmp_path: Path) -> Path:
    data = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "jwt-generator", "code": 500, "url": "https://jwt-generator.vercel.app"},
                {"slug": "diffmaster", "code": 401, "url": "https://diffmaster.vercel.app"},
                {"slug": "timestamp-converter", "code": 451, "url": "https://timestamp-converter.vercel.app"},
            ],
            "canonical_url_drift": [
                {"slug": "pdf-forge", "canonical_code": 404, "ideal_url": "https://pdf-forge.vercel.app"},
            ],
        }
    }
    p = tmp_path / "STATE_SUMMARY.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


@pytest.fixture
def mock_product_dir(tmp_path: Path) -> Path:
    products_dir = tmp_path / "products" / "test-product"
    products_dir.mkdir(parents=True)
    (products_dir / "index.html").write_text("<html></html>", encoding="utf-8")
    (products_dir / "vercel.json").write_text(
        json.dumps({
            "version": 2,
            "routes": [
                {"src": "/api/health", "dest": "/api/health.js"},
                {"src": "/(.*)", "dest": "/index.html"},
            ],
        }),
        encoding="utf-8",
    )
    (products_dir / "package.json").write_text(
        json.dumps({"name": "test-product", "version": "1.0.0"}),
        encoding="utf-8",
    )
    api_dir = products_dir / "api"
    api_dir.mkdir()
    (api_dir / "health.js").write_text("module.exports = (req, res) => res.status(200).end();", encoding="utf-8")
    return products_dir


class TestInspectProductDir:
    def test_existing_product(self, mock_product_dir: Path, monkeypatch):
        monkeypatch.setattr("scripts.vercel_autofix.ROOT", mock_product_dir.parent.parent)
        result = _inspect_product_dir("test-product")
        assert result["exists"] is True
        assert result["has_vercel_json"] is True
        assert result["has_index_html"] is True
        assert result["has_api_dir"] is True
        assert "health.js" in result["api_files"]
        assert result["uses_deprecated_routes"] is True
        assert "uses_deprecated_routes" in result["config_issues"]

    def test_nonexistent_product(self, tmp_path: Path, monkeypatch):
        monkeypatch.setattr("scripts.vercel_autofix.ROOT", tmp_path)
        result = _inspect_product_dir("nonexistent-product")
        assert result["exists"] is False


class TestDiagnosisRules:
    def test_all_codes_have_rules(self):
        for code in [401, 402, 404, 429, 451, 500, 0]:
            assert code in DIAGNOSIS_RULES
            rule = DIAGNOSIS_RULES[code]
            assert "root_cause" in rule
            assert "fix_type" in rule
            assert "fix_steps" in rule

    def test_401_not_auto_fixable(self):
        assert DIAGNOSIS_RULES[401]["auto_fixable"] is False

    def test_500_auto_fixable(self):
        assert DIAGNOSIS_RULES[500]["auto_fixable"] is True

    def test_451_not_auto_fixable(self):
        assert DIAGNOSIS_RULES[451]["auto_fixable"] is False


class TestDiagnoseProduct:
    @patch("scripts.vercel_autofix._inspect_product_dir")
    @patch("scripts.vercel_autofix._check_api_health")
    def test_server_error_diagnosis(self, mock_health, mock_inspect):
        mock_inspect.return_value = {
            "exists": True,
            "slug": "jwt-generator",
            "has_api_dir": True,
            "api_files": ["health.js", "process.js"],
            "config_issues": [],
            "uses_deprecated_routes": False,
        }
        mock_health.return_value = {"has_health_endpoint": True, "health_check": None}

        result = diagnose_product("jwt-generator", 500, "https://jwt-generator.vercel.app")
        assert result["http_code"] == 500
        assert result["root_cause"] == "Server error — build or runtime failure"
        assert result["fix_type"] == "code_fix"
        assert result["auto_fixable"] is True

    @patch("scripts.vercel_autofix._inspect_product_dir")
    @patch("scripts.vercel_autofix._check_api_health")
    def test_sso_protection_diagnosis(self, mock_health, mock_inspect):
        mock_inspect.return_value = {
            "exists": True,
            "slug": "diffmaster",
            "has_api_dir": False,
            "config_issues": [],
            "uses_deprecated_routes": False,
        }
        mock_health.return_value = {"has_health_endpoint": False}

        result = diagnose_product("diffmaster", 401, "https://diffmaster.vercel.app")
        assert result["fix_type"] == "vercel_settings"
        assert result["auto_fixable"] is False


class TestAutofixDeprecatedRoutes:
    def test_migrates_routes(self, mock_product_dir: Path, monkeypatch):
        monkeypatch.setattr("scripts.vercel_autofix.ROOT", mock_product_dir.parent.parent)
        result = autofix_deprecated_routes("test-product")
        assert result is not None
        assert result["routes_count"] == 2
        assert result["rewrites_count"] == 2

        updated = json.loads(
            (mock_product_dir.parent.parent / "products" / "test-product" / "vercel.json").read_text()
        )
        assert "routes" not in updated
        assert len(updated["rewrites"]) == 2
        assert updated["rewrites"][0]["source"] == "/api/health"
        assert updated["rewrites"][0]["destination"] == "/api/health.js"

    def test_no_routes_returns_none(self, tmp_path: Path, monkeypatch):
        products_dir = tmp_path / "products" / "no-routes"
        products_dir.mkdir(parents=True)
        (products_dir / "vercel.json").write_text(
            json.dumps({"version": 2, "rewrites": [{"source": "/(.*)", "destination": "/index.html"}]}),
            encoding="utf-8",
        )
        monkeypatch.setattr("scripts.vercel_autofix.ROOT", tmp_path)
        result = autofix_deprecated_routes("no-routes")
        assert result is None

    def test_no_vercel_json_returns_none(self, tmp_path: Path, monkeypatch):
        products_dir = tmp_path / "products" / "bare"
        products_dir.mkdir(parents=True)
        monkeypatch.setattr("scripts.vercel_autofix.ROOT", tmp_path)
        result = autofix_deprecated_routes("bare")
        assert result is None


class TestCheckApiHealth:
    @patch("scripts.vercel_autofix.probe_url")
    def test_healthy_api(self, mock_probe):
        mock_probe.return_value = {"code": 200, "effective_url": "https://test.vercel.app/api/health"}
        inspection = {"has_api_dir": True, "api_files": ["health.js"]}
        result = _check_api_health("test-product", inspection)
        assert result["has_health_endpoint"] is True
        assert result["health_check"]["healthy"] is True

    @patch("scripts.vercel_autofix.probe_url")
    def test_unhealthy_api(self, mock_probe):
        mock_probe.return_value = {"code": 500, "effective_url": "https://test.vercel.app/api/health"}
        inspection = {"has_api_dir": True, "api_files": ["health.js"]}
        result = _check_api_health("test-product", inspection)
        assert result["health_check"]["healthy"] is False

    def test_no_api_dir(self):
        result = _check_api_health("test", {"has_api_dir": False, "api_files": []})
        assert result["has_health_endpoint"] is False


class TestRunAutofix:
    @patch("scripts.vercel_autofix.probe_url")
    @patch("scripts.vercel_autofix._inspect_product_dir")
    @patch("scripts.vercel_autofix._check_api_health")
    def test_with_filter(self, mock_health, mock_inspect, mock_probe, sample_summary: Path):
        mock_inspect.return_value = {"exists": True, "has_api_dir": False, "config_issues": [], "api_files": [], "uses_deprecated_routes": False}
        mock_health.return_value = {"has_health_endpoint": False}
        mock_probe.return_value = {"code": 500, "effective_url": "https://jwt-generator.vercel.app"}

        results = run_autofix(summary_path=sample_summary, slug_filter="jwt")
        assert len(results) == 1
        assert results[0]["slug"] == "jwt-generator"

    @patch("scripts.vercel_autofix.probe_url")
    @patch("scripts.vercel_autofix._inspect_product_dir")
    @patch("scripts.vercel_autofix._check_api_health")
    def test_no_targets(self, mock_health, mock_inspect, mock_probe, tmp_path: Path):
        p = tmp_path / "STATE_SUMMARY.json"
        p.write_text(json.dumps({"gaps": {}}))
        results = run_autofix(summary_path=p)
        assert results == []


class TestFormatReport:
    def test_empty_results(self):
        report = format_report([])
        assert "no autofix" in report.lower() or "healthy" in report.lower()

    def test_with_results(self):
        results = [{
            "slug": "jwt-generator",
            "http_code": 500,
            "current_code": 500,
            "prior_code": 500,
            "url": "https://jwt-generator.vercel.app",
            "root_cause": "Server error",
            "fix_type": "code_fix",
            "auto_fixable": True,
            "fix_steps": ["Check logs", "Fix code"],
            "recovered": False,
            "inspection": {"exists": True, "config_issues": [], "has_api_dir": True, "api_files": ["health.js"]},
            "api_health": {"has_health_endpoint": True, "health_check": {"url": "https://jwt-generator.vercel.app/api/health", "code": 500, "healthy": False}},
        }]
        report = format_report(results)
        assert "jwt-generator" in report
        assert "HTTP 500" in report
        assert "health.js" in report
