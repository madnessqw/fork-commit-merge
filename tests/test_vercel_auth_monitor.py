"""Tests for vercel_auth_monitor.py."""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.vercel_auth_monitor import (
    VercelAuthStatus,
    CodexAuthStatus,
    DeploymentPipelineStatus,
    AuthMonitorReport,
    check_codex_auth,
    check_deployment_pipeline,
    build_report,
    format_report,
    report_to_dict,
    main,
    _truncate,
    AUTH_STATE_PATH,
    SUMMARY_PATH,
    AUTH_LOG_PATH,
)


class TestTruncate:
    def test_short_string(self):
        assert _truncate("hello", 10) == "hello"

    def test_exact_length(self):
        assert _truncate("12345", 5) == "12345"

    def test_long_string(self):
        result = _truncate("a" * 200, 50)
        assert len(result) == 50
        assert result.endswith("...")


class TestVercelAuthStatus:
    def test_defaults(self):
        s = VercelAuthStatus()
        assert s.vercel_cli_available is False
        assert s.vercel_token_env is False
        assert s.vercel_token_preview == ""
        assert s.vercel_whoami == ""
        assert s.vercel_whoami_ok is False


class TestCodexAuthStatus:
    def test_defaults(self):
        s = CodexAuthStatus()
        assert s.preferred_account == 0
        assert s.last_result == ""
        assert s.blocked is False
        assert s.blocked_until == ""
        assert s.switch_count == 0


class TestDeploymentPipelineStatus:
    def test_defaults(self):
        s = DeploymentPipelineStatus()
        assert s.total_products == 0
        assert s.live_products == 0
        assert s.healthy_products == 0
        assert s.deploy_gap == 0
        assert s.vercel_auth_issue is False


class TestCheckCodexAuth:
    def test_missing_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("scripts.vercel_auth_monitor.AUTH_STATE_PATH", tmp_path / "nonexistent.json")
        result = check_codex_auth()
        assert result.preferred_account == 0
        assert result.blocked is False

    def test_valid_auth_state(self, tmp_path, monkeypatch):
        auth_file = tmp_path / "codex_auth_state.json"
        auth_file.write_text(json.dumps({
            "preferred_account": 2,
            "last_result": "success",
            "reason": "ok",
            "account_1_status": "active",
            "account_2_status": "active",
            "switch_count": 5,
            "last_error": "",
        }))
        monkeypatch.setattr("scripts.vercel_auth_monitor.AUTH_STATE_PATH", auth_file)
        result = check_codex_auth()
        assert result.preferred_account == 2
        assert result.last_result == "success"
        assert result.blocked is False
        assert result.switch_count == 5

    def test_blocked_auth_state(self, tmp_path, monkeypatch):
        auth_file = tmp_path / "codex_auth_state.json"
        auth_file.write_text(json.dumps({
            "preferred_account": 1,
            "last_result": "auth_switch_failure",
            "reason": "usage limit",
            "account_1_status": "blocked",
            "account_2_status": "blocked",
            "switch_count": 100,
            "last_error": "You've hit your usage limit. Upgrade to Pro. try again at Apr 28th, 2026",
        }))
        monkeypatch.setattr("scripts.vercel_auth_monitor.AUTH_STATE_PATH", auth_file)
        result = check_codex_auth()
        assert result.blocked is True
        assert result.preferred_account == 1

    def test_invalid_json(self, tmp_path, monkeypatch):
        auth_file = tmp_path / "codex_auth_state.json"
        auth_file.write_text("not json {{{")
        monkeypatch.setattr("scripts.vercel_auth_monitor.AUTH_STATE_PATH", auth_file)
        result = check_codex_auth()
        assert result.preferred_account == 0


class TestCheckDeploymentPipeline:
    def test_missing_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("scripts.vercel_auth_monitor.SUMMARY_PATH", tmp_path / "nonexistent.json")
        result = check_deployment_pipeline()
        assert result.total_products == 0

    def test_valid_summary(self, tmp_path, monkeypatch):
        summary_file = tmp_path / "STATE_SUMMARY.json"
        summary_file.write_text(json.dumps({
            "active_count": 179,
            "live_count": 177,
            "healthy_count": 177,
            "deploy_missing_or_bad_url": 0,
            "vercel_auth_issue": True,
            "next_action": "fix auth",
        }))
        monkeypatch.setattr("scripts.vercel_auth_monitor.SUMMARY_PATH", summary_file)
        result = check_deployment_pipeline()
        assert result.total_products == 179
        assert result.live_products == 177
        assert result.healthy_products == 177
        assert result.vercel_auth_issue is True
        assert result.next_action == "fix auth"


class TestBuildReport:
    def test_report_structure(self):
        report = build_report()
        assert report.timestamp
        assert isinstance(report.vercel, VercelAuthStatus)
        assert isinstance(report.codex, CodexAuthStatus)
        assert isinstance(report.pipeline, DeploymentPipelineStatus)
        assert isinstance(report.blockers, list)
        assert isinstance(report.recommendations, list)


class TestFormatReport:
    def test_contains_sections(self):
        report = build_report()
        text = format_report(report)
        assert "Vercel CLI" in text
        assert "Codex Auth" in text
        assert "Deployment Pipeline" in text

    def test_blockers_shown(self):
        report = AuthMonitorReport(
            blockers=["Test blocker"],
            recommendations=["Fix it"],
        )
        text = format_report(report)
        assert "Active Blockers" in text
        assert "Test blocker" in text
        assert "Recommendations" in text


class TestReportToDict:
    def test_serializable(self):
        report = build_report()
        d = report_to_dict(report)
        assert "timestamp" in d
        assert "vercel" in d
        assert "codex" in d
        assert "pipeline" in d
        assert "blockers" in d
        text = json.dumps(d)
        assert text


class TestMain:
    def test_text_output(self):
        with patch("scripts.vercel_auth_monitor.build_report") as mock_build:
            mock_build.return_value = AuthMonitorReport()
            rc = main([])
            assert rc == 0

    def test_json_output(self, capsys):
        with patch("scripts.vercel_auth_monitor.build_report") as mock_build:
            mock_build.return_value = AuthMonitorReport()
            rc = main(["--json"])
            captured = capsys.readouterr()
            data = json.loads(captured.out)
            assert "timestamp" in data
            assert rc == 0

    def test_exit_code_with_blockers(self):
        with patch("scripts.vercel_auth_monitor.build_report") as mock_build:
            mock_build.return_value = AuthMonitorReport(blockers=["Something wrong"])
            rc = main([])
            assert rc == 1

    def test_log_flag(self, tmp_path, monkeypatch):
        log_file = tmp_path / "auth_monitor.jsonl"
        monkeypatch.setattr("scripts.vercel_auth_monitor.AUTH_LOG_PATH", log_file)
        monkeypatch.setattr("scripts.vercel_auth_monitor.AUTH_LOG_DIR", tmp_path)
        with patch("scripts.vercel_auth_monitor.build_report") as mock_build:
            mock_build.return_value = AuthMonitorReport()
            main(["--log"])
        assert log_file.exists()
        lines = log_file.read_text().strip().split("\n")
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert "timestamp" in data
