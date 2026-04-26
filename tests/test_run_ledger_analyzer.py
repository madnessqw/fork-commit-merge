import json
import textwrap

from scripts.run_ledger_analyzer import (
    agent_name,
    compute_by_agent,
    compute_summary,
    compute_trend,
    load_entries,
    summary_to_markdown,
    by_agent_to_markdown,
    trend_to_markdown,
)


def test_agent_name():
    assert agent_name("codex-20260422-0140") == "codex"
    assert agent_name("glm-20260422-0500") == "glm"
    assert agent_name("kimi-20260426-1700") == "kimi"
    assert agent_name("claude-123") == "claude"
    assert agent_name("ledger-init-abc") == "system"
    assert agent_name("") == "unknown"
    assert agent_name("custom-123") == "custom"


def test_compute_summary_empty():
    result = compute_summary([])
    assert result["total"] == 0


def test_compute_summary_basic(tmp_path):
    entries = [
        {"run_id": "codex-1", "status": "done", "duration_min": 10, "cost_est": 0.05, "mode": "EXECUTION", "cycle": 100},
        {"run_id": "codex-2", "status": "done", "duration_min": 20, "cost_est": 0.10, "mode": "OPTIMIZE", "cycle": 101},
        {"run_id": "glm-1", "status": "fail", "duration_min": 5, "cost_est": 0.01, "mode": "BUILD", "cycle": 102},
    ]
    result = compute_summary(entries)
    assert result["total"] == 3
    assert result["done"] == 2
    assert result["fail"] == 1
    assert result["success_rate"] == 66.7
    assert result["avg_duration_min"] == 11.7
    assert result["total_cost_est"] == 0.16
    assert result["cycle_range"] == [100, 102]


def test_compute_by_agent(tmp_path):
    entries = [
        {"run_id": "codex-1", "status": "done", "mode": "EXECUTION", "cycle": 100},
        {"run_id": "codex-2", "status": "fail", "mode": "EXECUTION", "cycle": 101},
        {"run_id": "glm-1", "status": "done", "mode": "BUILD", "cycle": 102},
    ]
    result = compute_by_agent(entries)
    assert "codex" in result
    assert "glm" in result
    assert result["codex"]["total"] == 2
    assert result["codex"]["done"] == 1
    assert result["glm"]["total"] == 1


def test_compute_trend(tmp_path):
    entries = [
        {"run_id": f"codex-{i}", "status": "done", "mode": "EXECUTION", "cycle": 100 + i, "task": f"task-{i}", "duration_min": 10, "cost_est": 0.05}
        for i in range(15)
    ]
    trend = compute_trend(entries, window=5)
    assert len(trend) == 5
    assert trend[0]["run_id"] == "codex-10"

    trend_all = compute_trend(entries, window=20)
    assert len(trend_all) == 15


def test_compute_trend_empty():
    assert compute_trend([]) == []


def test_summary_to_markdown():
    summary = {
        "total": 5,
        "done": 4,
        "fail": 1,
        "other": 0,
        "success_rate": 80.0,
        "avg_duration_min": 15.3,
        "total_cost_est": 0.25,
        "modes": {"EXECUTION": 3, "OPTIMIZE": 2},
        "agents": {"codex": 4, "glm": 1},
        "cycle_range": [100, 105],
    }
    md = summary_to_markdown(summary)
    assert "**Total runs:** 5" in md
    assert "**Success:** 4" in md
    assert "80.0%" in md


def test_summary_to_markdown_empty():
    assert "No ledger entries" in summary_to_markdown({"total": 0})


def test_by_agent_to_markdown():
    data = {
        "codex": {"total": 3, "success_rate": 100.0, "avg_duration_min": 20, "total_cost_est": 0.1},
        "glm": {"total": 1, "success_rate": 0, "avg_duration_min": 5, "total_cost_est": 0.0},
    }
    md = by_agent_to_markdown(data)
    assert "codex" in md
    assert "glm" in md


def test_trend_to_markdown():
    trend = [
        {"run_id": "codex-1", "cycle": 100, "mode": "EXEC", "status": "done", "duration_min": 10, "cost_est": 0.05},
    ]
    md = trend_to_markdown(trend)
    assert "codex" in md
    assert "100" in md


def test_load_entries_with_real_ledger():
    entries = load_entries()
    assert isinstance(entries, list)
    if entries:
        assert "run_id" in entries[0]


def test_load_entries_missing_file(tmp_path):
    from pathlib import Path
    import scripts.run_ledger_analyzer as m
    orig = m.LEDGER_PATH
    m.LEDGER_PATH = tmp_path / "nonexistent.jsonl"
    try:
        assert load_entries(m.LEDGER_PATH) == []
    finally:
        m.LEDGER_PATH = orig
