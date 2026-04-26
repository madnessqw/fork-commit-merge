import json
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from scripts.commit_activity_tracker import (
    _identify_agent,
    compute_agent_stats,
    compute_daily_breakdown,
    compute_summary,
    format_markdown_report,
    format_telegram_summary,
    _parse_git_log,
    _parse_git_log_with_stats,
)


class TestIdentifyAgent:
    def test_glm_prefix(self):
        assert _identify_agent("glm: 20260426-2030 — test file added") == "glm"

    def test_codex_prefix(self):
        assert _identify_agent("codex: fix checkout sync") == "codex"

    def test_kimi_prefix(self):
        assert _identify_agent("kimi: cycle 1205 — state sync") == "kimi"

    def test_claude_prefix(self):
        assert _identify_agent("claude: implement feature") == "claude"

    def test_unknown_no_prefix(self):
        assert _identify_agent("random commit message") == "unknown"

    def test_case_insensitive(self):
        assert _identify_agent("GLM: test") == "glm"

    def test_space_after_prefix(self):
        assert _identify_agent("glm : test") == "glm"

    def test_prefix_in_middle(self):
        assert _identify_agent("some glm: message") == "unknown"


class TestComputeAgentStats:
    def test_basic_stats(self):
        commits = [
            {"agent": "glm", "date": "2026-04-26T10:00:00", "message": "glm: test1",
             "files_changed": 3, "lines_added": 100, "lines_removed": 10, "file_list": ["a.py", "b.py", "c.py"]},
            {"agent": "glm", "date": "2026-04-26T11:00:00", "message": "glm: test2",
             "files_changed": 1, "lines_added": 50, "lines_removed": 5, "file_list": ["d.py"]},
            {"agent": "kimi", "date": "2026-04-26T12:00:00", "message": "kimi: sync",
             "files_changed": 2, "lines_added": 200, "lines_removed": 20, "file_list": ["e.json", "f.md"]},
        ]
        stats = compute_agent_stats(commits)
        assert stats["glm"]["commits"] == 2
        assert stats["glm"]["files_changed"] == 4
        assert stats["glm"]["lines_added"] == 150
        assert stats["glm"]["lines_removed"] == 15
        assert stats["kimi"]["commits"] == 1
        assert stats["kimi"]["lines_added"] == 200

    def test_empty_commits(self):
        stats = compute_agent_stats([])
        assert stats == {}

    def test_file_type_tracking(self):
        commits = [
            {"agent": "glm", "date": "2026-04-26T10:00:00", "message": "glm: test",
             "files_changed": 3, "lines_added": 10, "lines_removed": 0,
             "file_list": ["script.py", "test.py", "data.json"]},
        ]
        stats = compute_agent_stats(commits)
        assert stats["glm"]["top_file_types"][".py"] == 2
        assert stats["glm"]["top_file_types"][".json"] == 1

    def test_peak_hour(self):
        commits = [
            {"agent": "glm", "date": "2026-04-26T09:00:00", "message": "glm: a",
             "files_changed": 0, "lines_added": 0, "lines_removed": 0, "file_list": []},
            {"agent": "glm", "date": "2026-04-26T09:30:00", "message": "glm: b",
             "files_changed": 0, "lines_added": 0, "lines_removed": 0, "file_list": []},
            {"agent": "glm", "date": "2026-04-26T14:00:00", "message": "glm: c",
             "files_changed": 0, "lines_added": 0, "lines_removed": 0, "file_list": []},
        ]
        stats = compute_agent_stats(commits)
        assert stats["glm"]["peak_hour"] == 9

    def test_latest_messages(self):
        commits = [
            {"agent": "glm", "date": "2026-04-26T10:00:00", "message": "first commit msg",
             "files_changed": 0, "lines_added": 0, "lines_removed": 0, "file_list": []},
            {"agent": "glm", "date": "2026-04-26T11:00:00", "message": "second commit msg",
             "files_changed": 0, "lines_added": 0, "lines_removed": 0, "file_list": []},
            {"agent": "glm", "date": "2026-04-26T12:00:00", "message": "third commit msg",
             "files_changed": 0, "lines_added": 0, "lines_removed": 0, "file_list": []},
            {"agent": "glm", "date": "2026-04-26T13:00:00", "message": "fourth commit msg",
             "files_changed": 0, "lines_added": 0, "lines_removed": 0, "file_list": []},
        ]
        stats = compute_agent_stats(commits)
        assert len(stats["glm"]["latest_messages"]) == 3
        assert "fourth" in stats["glm"]["latest_messages"][-1]


class TestComputeSummary:
    def test_basic_summary(self):
        commits = [
            {"agent": "glm", "date": "2026-04-26T10:00:00", "files_changed": 2, "lines_added": 100, "lines_removed": 10},
            {"agent": "kimi", "date": "2026-04-26T11:00:00", "files_changed": 1, "lines_added": 50, "lines_removed": 5},
        ]
        summary = compute_summary(commits)
        assert summary["total_commits"] == 2
        assert summary["total_files_changed"] == 3
        assert summary["total_lines_added"] == 150
        assert summary["total_lines_removed"] == 15
        assert summary["most_active_agent"] == "glm"

    def test_empty_commits(self):
        summary = compute_summary([])
        assert summary["total_commits"] == 0

    def test_agent_breakdown(self):
        commits = [
            {"agent": "glm"}, {"agent": "glm"}, {"agent": "kimi"},
        ]
        summary = compute_summary(commits)
        assert summary["agent_breakdown"]["glm"] == 2
        assert summary["agent_breakdown"]["kimi"] == 1


class TestComputeDailyBreakdown:
    def test_daily(self):
        commits = [
            {"date": "2026-04-26T10:00:00", "agent": "glm", "files_changed": 2, "lines_added": 100},
            {"date": "2026-04-26T14:00:00", "agent": "kimi", "files_changed": 1, "lines_added": 50},
            {"date": "2026-04-25T09:00:00", "agent": "glm", "files_changed": 3, "lines_added": 200},
        ]
        daily = compute_daily_breakdown(commits)
        assert "2026-04-25" in daily
        assert "2026-04-26" in daily
        assert daily["2026-04-26"]["total_commits"] == 2
        assert daily["2026-04-25"]["total_commits"] == 1
        assert daily["2026-04-26"]["agents"]["glm"] == 1
        assert daily["2026-04-26"]["agents"]["kimi"] == 1

    def test_empty(self):
        daily = compute_daily_breakdown([])
        assert daily == {}

    def test_invalid_date_skipped(self):
        commits = [
            {"date": "invalid", "agent": "glm", "files_changed": 1, "lines_added": 10},
        ]
        daily = compute_daily_breakdown(commits)
        assert daily == {}


class TestFormatMarkdownReport:
    def test_basic_report(self):
        agent_stats = {
            "glm": {
                "commits": 5, "files_changed": 10, "lines_added": 200,
                "lines_removed": 50, "peak_hour": 9,
                "top_file_types": {".py": 8, ".md": 2},
                "latest_messages": ["msg1"],
            },
        }
        summary = {
            "date_range": "2026-04-25 → 2026-04-26",
            "total_commits": 5,
            "total_files_changed": 10,
            "total_lines_added": 200,
            "total_lines_removed": 50,
            "most_active_agent": "glm",
        }
        md = format_markdown_report(agent_stats, summary)
        assert "# Commit Activity Report" in md
        assert "glm" in md
        assert "09:00" in md

    def test_empty_stats(self):
        md = format_markdown_report({}, {"date_range": "?", "total_commits": 0,
                                          "total_files_changed": 0,
                                          "total_lines_added": 0,
                                          "total_lines_removed": 0,
                                          "most_active_agent": None})
        assert "# Commit Activity Report" in md


class TestFormatTelegramSummary:
    def test_basic(self):
        agent_stats = {
            "glm": {"commits": 3, "files_changed": 5, "lines_added": 100, "lines_removed": 20},
        }
        summary = {"total_commits": 3, "total_lines_added": 100, "total_lines_removed": 20}
        result = format_telegram_summary(summary, agent_stats)
        assert "Commit Activity" in result
        assert "glm" in result


class TestParseGitLog:
    @patch("scripts.commit_activity_tracker.subprocess.run")
    def test_parse_failure_returns_empty(self, mock_run):
        mock_run.side_effect = FileNotFoundError("git not found")
        result = _parse_git_log(10)
        assert result == []

    @patch("scripts.commit_activity_tracker.subprocess.run")
    def test_parse_with_valid_output(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "abc1234\x002026-04-26 10:00:00 +0300\x00glm: test commit\n"
        mock_run.return_value = mock_result
        result = _parse_git_log(1)
        assert len(result) == 1
        assert result[0]["agent"] == "glm"
        assert result[0]["hash"] == "abc1234"

    @patch("scripts.commit_activity_tracker.subprocess.run")
    def test_parse_with_malformed_line(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "bad line without null bytes\n"
        mock_run.return_value = mock_result
        result = _parse_git_log(1)
        assert result == []


class TestParseGitLogWithStats:
    @patch("scripts.commit_activity_tracker.subprocess.run")
    def test_parse_with_numstat(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "abc1234\x002026-04-26 10:00:00 +0300\x00glm: test\n"
            "10\t5\tscripts/foo.py\n"
            "3\t0\ttests/test_foo.py\n"
            "def5678\x002026-04-26 11:00:00 +0300\x00kimi: sync\n"
            "20\t10\tSTATE.json\n"
        )
        mock_run.return_value = mock_result
        result = _parse_git_log_with_stats(2)
        assert len(result) == 2
        assert result[0]["agent"] == "glm"
        assert result[0]["files_changed"] == 2
        assert result[0]["lines_added"] == 13
        assert result[0]["lines_removed"] == 5
        assert result[1]["agent"] == "kimi"
        assert result[1]["files_changed"] == 1

    @patch("scripts.commit_activity_tracker.subprocess.run")
    def test_binary_files_handled(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "abc1234\x002026-04-26 10:00:00 +0300\x00glm: test\n"
            "-\t-\tbinary_file.png\n"
            "5\t2\tnormal.py\n"
        )
        mock_run.return_value = mock_result
        result = _parse_git_log_with_stats(1)
        assert len(result) == 1
        assert result[0]["files_changed"] == 2
        assert result[0]["lines_added"] == 5
        assert result[0]["lines_removed"] == 2

    @patch("scripts.commit_activity_tracker.subprocess.run")
    def test_failure_returns_empty(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired("git", 60)
        result = _parse_git_log_with_stats(10)
        assert result == []
