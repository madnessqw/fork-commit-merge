import json
import tempfile
from pathlib import Path
import unittest

from scripts.codex_auth_manager import (
    classify_output,
    choose_state,
    record_state,
    parse_limit_until,
    all_accounts_blocked,
    next_available_account,
)


class CodexAuthManagerTests(unittest.TestCase):
    def _workspace(self) -> tuple[Path, Path]:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        root = Path(tempdir.name) / "UniverseCreator"
        state_file = root / ".signals" / "codex_auth_state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        return root, state_file

    def test_choose_defaults_to_account_one(self) -> None:
        _, state_file = self._workspace()

        chosen = choose_state(state_file)

        self.assertEqual(chosen["preferred_account"], 1)
        self.assertEqual(chosen["fallback_account"], 2)

    def test_record_success_keeps_preferred_account(self) -> None:
        _, state_file = self._workspace()
        state_file.write_text(json.dumps({"preferred_account": 1}), encoding="utf-8")

        state = record_state(
            state_file,
            preferred_account=1,
            active_account=1,
            attempted_accounts=[1],
            outcome="success",
            cycle=12,
            exit_code=0,
        )

        self.assertEqual(state["preferred_account"], 1)
        self.assertEqual(state["last_active_account"], 1)
        self.assertEqual(state["last_result"], "success")
        self.assertEqual(state["last_success_account"], 1)

    def test_record_auth_switch_success_flips_preferred_account(self) -> None:
        _, state_file = self._workspace()
        state_file.write_text(json.dumps({"preferred_account": 1}), encoding="utf-8")

        state = record_state(
            state_file,
            preferred_account=1,
            active_account=2,
            attempted_accounts=[1, 2],
            outcome="auth_switch_success",
            cycle=13,
            exit_code=0,
            last_error="usage limit",
        )

        self.assertEqual(state["preferred_account"], 2)
        self.assertEqual(state["last_active_account"], 2)
        self.assertEqual(state["last_result"], "auth_switch_success")
        self.assertEqual(state["last_switch_from_account"], 1)
        self.assertEqual(state["last_switch_to_account"], 2)
        self.assertEqual(state["switch_count"], 1)

    def test_record_non_auth_failure_keeps_preferred_account(self) -> None:
        _, state_file = self._workspace()
        state_file.write_text(json.dumps({"preferred_account": 2}), encoding="utf-8")

        state = record_state(
            state_file,
            preferred_account=2,
            active_account=2,
            attempted_accounts=[2],
            outcome="failure",
            cycle=14,
            exit_code=13,
            last_error="exit_code=13",
        )

        self.assertEqual(state["preferred_account"], 2)
        self.assertEqual(state["last_active_account"], 2)
        self.assertEqual(state["last_result"], "failure")
        self.assertEqual(state["last_failure_account"], 2)

    def test_classify_output_detects_auth_switch(self) -> None:
        self.assertEqual(classify_output("usage limit hit", 1), "auth_switch")
        self.assertEqual(classify_output("high demand / try later", 1), "auth_switch")
        self.assertEqual(classify_output("something else failed", 2), "failure")
        self.assertEqual(classify_output("all good", 0), "success")

    def test_parse_limit_until_extracts_date(self) -> None:
        output = "You've hit your usage limit. try again at Apr 28th, 2026 9:35 PM."
        result = parse_limit_until(output)
        self.assertIsNotNone(result)
        self.assertIn("2026", result)

    def test_parse_limit_until_returns_none_when_absent(self) -> None:
        self.assertIsNone(parse_limit_until("something else happened"))

    def test_all_accounts_blocked(self) -> None:
        state = {
            "account_1_blocked_until": "2099-01-01T00:00:00Z",
            "account_2_blocked_until": "2099-01-01T00:00:00Z",
        }
        self.assertTrue(all_accounts_blocked(state))

    def test_not_all_blocked_when_one_free(self) -> None:
        state = {
            "account_1_blocked_until": "2099-01-01T00:00:00Z",
        }
        self.assertFalse(all_accounts_blocked(state))

    def test_not_all_blocked_when_expired(self) -> None:
        state = {
            "account_1_blocked_until": "2020-01-01T00:00:00Z",
            "account_2_blocked_until": "2020-01-01T00:00:00Z",
        }
        self.assertFalse(all_accounts_blocked(state))

    def test_next_available_account_returns_free_account(self) -> None:
        state = {
            "account_1_blocked_until": "2099-01-01T00:00:00Z",
        }
        self.assertEqual(next_available_account(state), 2)

    def test_next_available_account_returns_none_when_all_blocked(self) -> None:
        state = {
            "account_1_blocked_until": "2099-01-01T00:00:00Z",
            "account_2_blocked_until": "2099-01-01T00:00:00Z",
        }
        self.assertIsNone(next_available_account(state))

    def test_record_state_captures_blocked_until_on_auth_switch(self) -> None:
        _, state_file = self._workspace()
        state_file.write_text(json.dumps({"preferred_account": 1}), encoding="utf-8")
        state = record_state(
            state_file,
            preferred_account=1,
            active_account=2,
            attempted_accounts=[1, 2],
            outcome="auth_switch_success",
            cycle=20,
            exit_code=0,
            last_error="usage limit",
            raw_output="usage limit hit. try again at Apr 28th, 2026 9:35 PM.",
        )
        self.assertIn("account_1_blocked_until", state)
        self.assertIsNotNone(state["account_1_blocked_until"])


if __name__ == "__main__":
    unittest.main()
