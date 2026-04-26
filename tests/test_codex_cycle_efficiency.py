from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from scripts.codex_cycle_efficiency import (
    daily_breakdown,
    load_entries,
    recent_failures,
    repeated_tasks,
    summary,
)


@pytest.fixture
def sample_entries(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    lines = [
        json.dumps({"run_id": "c-001", "mode": "EXECUTION", "task": "fix drift", "status": "done", "slug": "drift", "duration_min": 20, "cost_est": 0.05, "ts": "2026-04-25T10:00:00Z"}),
        json.dumps({"run_id": "c-002", "mode": "EXECUTION", "task": "fix drift", "status": "done", "slug": "drift", "duration_min": 25, "cost_est": 0.06, "ts": "2026-04-25T11:00:00Z"}),
        json.dumps({"run_id": "c-003", "mode": "EXECUTION", "task": "deploy X", "status": "fail", "slug": "x-prod", "duration_min": 10, "cost_est": 0.03, "ts": "2026-04-26T08:00:00Z"}),
        json.dumps({"run_id": "c-004", "mode": "OPTIMIZE", "task": "optimize Y", "status": "done", "slug": "y-prod", "duration_min": 15, "cost_est": 0.04, "ts": "2026-04-26T09:00:00Z"}),
        json.dumps({"run_id": "c-005", "mode": "EXECUTION", "task": "fix drift", "status": "done", "slug": "drift", "duration_min": 22, "cost_est": 0.05, "ts": "2026-04-26T10:00:00Z"}),
        json.dumps({"run_id": "c-006", "mode": "EXECUTION", "task": "fix drift", "status": "done", "slug": "drift", "duration_min": 30, "cost_est": 0.07, "ts": "2026-04-26T11:00:00Z"}),
    ]
    ledger = tmp_path / "run_ledger.jsonl"
    ledger.write_text("\n".join(lines), encoding="utf-8")
    monkeypatch.setattr("scripts.codex_cycle_efficiency.LEDGER_FILE", ledger)
    return lines


class TestLoadEntries:
    def test_loads_all(self, sample_entries):
        entries = load_entries()
        assert len(entries) == 6

    def test_limit(self, sample_entries):
        entries = load_entries(limit=3)
        assert len(entries) == 3

    def test_empty_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        ledger = tmp_path / "run_ledger.jsonl"
        ledger.write_text("", encoding="utf-8")
        monkeypatch.setattr("scripts.codex_cycle_efficiency.LEDGER_FILE", ledger)
        assert load_entries() == []

    def test_missing_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("scripts.codex_cycle_efficiency.LEDGER_FILE", tmp_path / "nope.jsonl")
        assert load_entries() == []

    def test_skips_bad_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        ledger = tmp_path / "run_ledger.jsonl"
        content = 'bad line\n{"run_id":"ok","status":"done"}\n'
        ledger.write_text(content, encoding="utf-8")
        monkeypatch.setattr("scripts.codex_cycle_efficiency.LEDGER_FILE", ledger)
        entries = load_entries()
        assert len(entries) == 1


class TestSummary:
    def test_basic_counts(self, sample_entries):
        s = summary()
        assert s["total"] == 6
        assert s["done"] == 5
        assert s["fail"] == 1
        assert s["success_rate"] == 83.3

    def test_durations(self, sample_entries):
        s = summary()
        assert s["avg_duration_min"] == 20.3
        assert s["min_duration_min"] == 10
        assert s["max_duration_min"] == 30

    def test_costs(self, sample_entries):
        s = summary()
        assert s["total_cost_est"] == 0.3
        assert s["avg_cost_est"] == 0.05

    def test_modes(self, sample_entries):
        s = summary()
        assert s["modes"]["EXECUTION"] == 5
        assert s["modes"]["OPTIMIZE"] == 1

    def test_top_slugs(self, sample_entries):
        s = summary()
        assert list(s["top_slugs"][0]) == ["drift", 4]

    def test_window(self, sample_entries):
        s = summary(window=2)
        assert s["total"] == 2

    def test_empty(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("scripts.codex_cycle_efficiency.LEDGER_FILE", tmp_path / "nope.jsonl")
        assert summary() == {"total": 0}


class TestRepeatedTasks:
    def test_finds_repeated(self, sample_entries):
        rep = repeated_tasks(min_repeats=3)
        tasks = [r["task"] for r in rep["repeated"]]
        assert "fix drift" in tasks

    def test_unique_tasks(self, sample_entries):
        rep = repeated_tasks()
        assert rep["unique_tasks"] == 3

    def test_empty(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("scripts.codex_cycle_efficiency.LEDGER_FILE", tmp_path / "nope.jsonl")
        rep = repeated_tasks()
        assert rep["repeated"] == []
        assert rep["total_entries"] == 0


class TestRecentFailures:
    def test_failure_count(self, sample_entries):
        f = recent_failures()
        assert f["fail_count"] == 1
        assert f["recent"][0]["run_id"] == "c-003"

    def test_limit_zero(self, sample_entries):
        f = recent_failures(limit=1)
        assert len(f["recent"]) == 1

    def test_no_failures(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        ledger = tmp_path / "run_ledger.jsonl"
        ledger.write_text(json.dumps({"status": "done", "run_id": "x"}) + "\n", encoding="utf-8")
        monkeypatch.setattr("scripts.codex_cycle_efficiency.LEDGER_FILE", ledger)
        f = recent_failures()
        assert f["fail_count"] == 0


class TestDailyBreakdown:
    def test_two_days(self, sample_entries):
        d = daily_breakdown()
        assert d["total_days"] == 2
        assert d["days"]["2026-04-25"]["total"] == 2
        assert d["days"]["2026-04-25"]["done"] == 2
        assert d["days"]["2026-04-26"]["total"] == 4
        assert d["days"]["2026-04-26"]["fail"] == 1

    def test_empty(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("scripts.codex_cycle_efficiency.LEDGER_FILE", tmp_path / "nope.jsonl")
        d = daily_breakdown()
        assert d == {"days": {}, "total_days": 0}
