import json
import os
import tempfile
from unittest.mock import patch

import pytest

from scripts.update_state import (
    add_learning,
    load_state,
    save_state,
    set_agent_status,
    update_cycle,
    update_message,
)


@pytest.fixture
def sample_state():
    return {
        "cycle": 100,
        "timestamp": "2026-01-01T00:00:00+00:00",
        "message": "test",
        "team": {
            "agents": [
                {"name": "planner", "status": "idle"},
                {"name": "executor", "status": "idle"},
                {"name": "researcher", "status": "working"},
            ]
        },
    }


@pytest.fixture
def state_file(sample_state, tmp_path):
    path = tmp_path / "STATE.json"
    path.write_text(json.dumps(sample_state))
    return str(path)


class TestLoadState:
    def test_load_valid(self, state_file):
        state = load_state(state_file)
        assert state["cycle"] == 100

    def test_load_missing_exits(self):
        with pytest.raises(SystemExit):
            load_state("/nonexistent/STATE.json")


class TestSaveState:
    def test_save_roundtrip(self, sample_state, tmp_path):
        path = str(tmp_path / "STATE.json")
        save_state(sample_state, path)
        loaded = json.loads(open(path).read())
        assert loaded["cycle"] == 100


class TestUpdateCycle:
    def test_update_cycle_number(self, sample_state):
        result = update_cycle(sample_state, cycle=200)
        assert result["cycle"] == 200

    def test_update_cycle_preserves_if_none(self, sample_state):
        result = update_cycle(sample_state, cycle=None)
        assert result["cycle"] == 100

    def test_update_cycle_sets_timestamp(self, sample_state):
        result = update_cycle(sample_state)
        assert "timestamp" in result
        assert result["timestamp"] != "2026-01-01T00:00:00+00:00"


class TestUpdateMessage:
    def test_update_message(self, sample_state):
        result = update_message(sample_state, message="new msg")
        assert result["message"] == "new msg"

    def test_update_next_priority(self, sample_state):
        result = update_message(sample_state, next_priority="do stuff")
        assert result["next_priority"] == "do stuff"

    def test_no_change_if_none(self, sample_state):
        result = update_message(sample_state)
        assert result.get("message") == "test"
        assert "next_priority" not in result


class TestSetAgentStatus:
    def test_set_single_agent(self, sample_state):
        state, count = set_agent_status(sample_state, ["planner"], "working")
        assert count == 1
        assert state["team"]["agents"][0]["status"] == "working"

    def test_set_multiple_agents(self, sample_state):
        state, count = set_agent_status(sample_state, ["planner", "executor"], "done")
        assert count == 2

    def test_set_nonexistent_agent(self, sample_state):
        state, count = set_agent_status(sample_state, ["ghost"], "active")
        assert count == 0

    def test_empty_agents_list(self):
        state, count = set_agent_status({"team": {"agents": []}}, ["x"], "y")
        assert count == 0

    def test_missing_team_key(self):
        state, count = set_agent_status({}, ["x"], "y")
        assert count == 0


class TestAddLearning:
    def test_add_first_learning(self, sample_state):
        result = add_learning(sample_state, "learned something")
        assert result["learnings"] == ["learned something"]

    def test_append_learning(self, sample_state):
        sample_state["learnings"] = ["old"]
        result = add_learning(sample_state, "new")
        assert result["learnings"] == ["old", "new"]


class TestCLI:
    def test_dry_run(self, state_file, capsys):
        with patch("sys.argv", ["update_state.py", "--state-file", state_file, "--dry-run"]):
            from scripts.update_state import main
            main()
        output = capsys.readouterr().out
        data = json.loads(output)
        assert "cycle" in data

    def test_cycle_update(self, state_file):
        with patch("sys.argv", ["update_state.py", "--state-file", state_file, "--cycle", "999"]):
            from scripts.update_state import main
            main()
        state = json.loads(open(state_file).read())
        assert state["cycle"] == 999

    def test_agent_status_update(self, state_file):
        with patch("sys.argv", ["update_state.py", "--state-file", state_file,
                                "--agent-status", "planner,executor", "done"]):
            from scripts.update_state import main
            main()
        state = json.loads(open(state_file).read())
        names = {a["name"]: a["status"] for a in state["team"]["agents"]}
        assert names["planner"] == "done"
        assert names["executor"] == "done"
        assert names["researcher"] == "working"

    def test_learning_add(self, state_file):
        with patch("sys.argv", ["update_state.py", "--state-file", state_file,
                                "--learning", "test learning"]):
            from scripts.update_state import main
            main()
        state = json.loads(open(state_file).read())
        assert "test learning" in state["learnings"]
