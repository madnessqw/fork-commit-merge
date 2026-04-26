import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.agent_cycle_reporter import (
    _identify_agent,
    compute_commit_stats,
    compute_efficiency,
    compute_ledger_stats,
    format_markdown,
    format_telegram,
    load_ledger,
)


class TestIdentifyAgent:
    def test_glm(self):
        assert _identify_agent("glm: fix something") == "glm"

    def test_codex(self):
        assert _identify_agent("codex: deploy product") == "codex"

    def test_kimi(self):
        assert _identify_agent("kimi: analysis report") == "kimi"

    def test_claude(self):
        assert _identify_agent("claude: cycle 1200") == "claude"

    def test_unknown(self):
        assert _identify_agent("chore: cleanup") == "unknown"

    def test_case_insensitive(self):
        assert _identify_agent("GLM: test") == "glm"
        assert _identify_agent("Codex: fix") == "codex"


class TestLoadLedger:
    def test_loads_entries(self, tmp_path):
        ledger = tmp_path / "run_ledger.jsonl"
        entries_data = [
            {"run_id": "glm-001", "mode": "BUILD", "status": "done", "duration_min": 5},
            {"run_id": "codex-002", "mode": "EXECUTION", "status": "fail", "duration_min": 10},
        ]
        ledger.write_text("\n".join(json.dumps(e) for e in entries_data))

        with patch("scripts.agent_cycle_reporter.LEDGER_FILE", ledger):
            result = load_ledger()
        assert len(result) == 2
        assert result[0]["run_id"] == "glm-001"

    def test_empty_file(self, tmp_path):
        ledger = tmp_path / "run_ledger.jsonl"
        ledger.write_text("")
        with patch("scripts.agent_cycle_reporter.LEDGER_FILE", ledger):
            result = load_ledger()
        assert result == []

    def test_missing_file(self, tmp_path):
        with patch("scripts.agent_cycle_reporter.LEDGER_FILE", tmp_path / "nonexistent.jsonl"):
            result = load_ledger()
        assert result == []

    def test_limit(self, tmp_path):
        ledger = tmp_path / "run_ledger.jsonl"
        entries = [{"run_id": f"glm-{i:03d}", "mode": "BUILD", "status": "done"} for i in range(10)]
        ledger.write_text("\n".join(json.dumps(e) for e in entries))
        with patch("scripts.agent_cycle_reporter.LEDGER_FILE", ledger):
            result = load_ledger(limit=3)
        assert len(result) == 3


class TestComputeLedgerStats:
    def test_basic_stats(self):
        entries = [
            {"run_id": "glm-001", "status": "done", "duration_min": 5, "cost_est": 0.01, "mode": "BUILD", "task": "fix script"},
            {"run_id": "glm-002", "status": "fail", "duration_min": 3, "cost_est": 0.02, "mode": "BUILD", "task": "fix other"},
            {"run_id": "codex-003", "status": "done", "duration_min": 20, "cost_est": 0.1, "mode": "EXECUTION", "task": "deploy"},
        ]
        stats = compute_ledger_stats(entries)
        assert stats["glm"]["runs"] == 2
        assert stats["glm"]["success_rate"] == 50.0
        assert stats["glm"]["fail_count"] == 1
        assert stats["codex"]["runs"] == 1
        assert stats["codex"]["success_rate"] == 100.0

    def test_empty(self):
        stats = compute_ledger_stats([])
        assert stats == {}

    def test_avg_duration(self):
        entries = [
            {"run_id": "glm-001", "status": "done", "duration_min": 10},
            {"run_id": "glm-002", "status": "done", "duration_min": 20},
        ]
        stats = compute_ledger_stats(entries)
        assert stats["glm"]["avg_duration_min"] == 15.0


class TestComputeCommitStats:
    def test_basic(self):
        commits = [
            {"agent": "glm", "hour": 14, "message": "glm: fix"},
            {"agent": "glm", "hour": 14, "message": "glm: test"},
            {"agent": "codex", "hour": 10, "message": "codex: deploy"},
        ]
        stats = compute_commit_stats(commits)
        assert stats["glm"]["commits"] == 2
        assert stats["glm"]["peak_hour"] == 14
        assert stats["codex"]["commits"] == 1

    def test_empty(self):
        stats = compute_commit_stats([])
        assert stats == {}


class TestComputeEfficiency:
    def test_basic(self):
        ls = {"glm": {"runs": 10, "success_rate": 90.0, "avg_duration_min": 5.2}}
        cs = {"glm": {"commits": 8}}
        eff = compute_efficiency(ls, cs)
        assert eff["glm"]["efficiency"] == 0.8
        assert eff["glm"]["commits"] == 8
        assert eff["glm"]["runs"] == 10

    def test_zero_runs(self):
        ls = {}
        cs = {"unknown": {"commits": 5}}
        eff = compute_efficiency(ls, cs)
        assert eff["unknown"]["efficiency"] == 0
        assert eff["unknown"]["runs"] == 0

    def test_mixed_agents(self):
        ls = {
            "glm": {"runs": 5, "success_rate": 80.0, "avg_duration_min": 3.0},
            "codex": {"runs": 3, "success_rate": 100.0, "avg_duration_min": 25.0},
        }
        cs = {
            "glm": {"commits": 4},
            "codex": {"commits": 3},
            "kimi": {"commits": 10},
        }
        eff = compute_efficiency(ls, cs)
        assert len(eff) == 3
        assert eff["kimi"]["efficiency"] == 0


class TestFormatMarkdown:
    def test_produces_report(self):
        ls = {"glm": {"runs": 5, "success_rate": 80.0, "fail_count": 1, "avg_duration_min": 4.0, "total_cost": 0.05, "top_modes": {"BUILD": 5}, "latest_tasks": ["fix script"]}}
        cs = {"glm": {"commits": 4, "peak_hour": 14, "latest_messages": ["glm: fix"]}}
        eff = {"glm": {"runs": 5, "commits": 4, "efficiency": 0.8, "success_rate": 80.0, "avg_duration_min": 4.0}}
        md = format_markdown(ls, cs, eff)
        assert "# Agent Cycle Report" in md
        assert "glm" in md
        assert "0.8" in md


class TestFormatTelegram:
    def test_produces_summary(self):
        eff = {"glm": {"runs": 5, "commits": 4, "efficiency": 0.8, "success_rate": 80.0}}
        tg = format_telegram(eff)
        assert "Agent Cycle Report" in tg
        assert "glm" in tg
        assert "80.0%" in tg
