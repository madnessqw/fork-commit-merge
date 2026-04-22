import json
import tempfile
from pathlib import Path
import unittest

from scripts.qa_dispatch import dispatch_qa_pending


TEAM_STATUS_TEMPLATE = """```json
{
  "cycle_count": 1073,
  "last_updated": "2026-04-22T04:22:00Z",
  "teammates": {
    "qa-tester": {
      "status": "idle",
      "prompt_count": 0,
      "last_prompt": null
    }
  },
  "signals": {
    "qa_pending": false,
    "deploy_ready": false
  }
}
```
"""


class QaDispatchTests(unittest.TestCase):
    def _build_workspace(self, slug: str = "health-canonical-drift") -> tuple[Path, Path]:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        root = Path(tempdir.name) / "UniverseCreator"
        team_home = Path(tempdir.name) / ".claude" / "teams" / "universe-prime"

        (root / ".signals").mkdir(parents=True)
        (root / "analysis").mkdir(parents=True)
        (team_home / "inboxes").mkdir(parents=True)

        (root / "STATE_SUMMARY.json").write_text(json.dumps({"cycle": 1076}), encoding="utf-8")
        (root / "analysis" / "team_status.md").write_text(TEAM_STATUS_TEMPLATE, encoding="utf-8")
        (root / ".signals" / "qa_pending").write_text(
            json.dumps({"slug": slug, "ts": "2026-04-22T02:44:42Z"}) + "\n",
            encoding="utf-8",
        )
        (team_home / "inboxes" / "qa-tester.json").write_text(json.dumps({"messages": []}), encoding="utf-8")
        (team_home / "inboxes" / "team-lead.json").write_text(json.dumps({"messages": []}), encoding="utf-8")

        return root, team_home

    def test_dispatch_appends_inbox_message_and_updates_status(self) -> None:
        root, team_home = self._build_workspace()

        result = dispatch_qa_pending(root, team_home)

        self.assertEqual(result, "QA_DISPATCHED slug=health-canonical-drift")

        qa_inbox = json.loads((team_home / "inboxes" / "qa-tester.json").read_text(encoding="utf-8"))
        lead_inbox = json.loads((team_home / "inboxes" / "team-lead.json").read_text(encoding="utf-8"))
        team_status = (root / "analysis" / "team_status.md").read_text(encoding="utf-8")

        self.assertEqual(len(qa_inbox["messages"]), 1)
        self.assertEqual(qa_inbox["messages"][0]["slug"], "health-canonical-drift")
        self.assertEqual(qa_inbox["messages"][0]["type"], "qa_request")
        self.assertEqual(len(lead_inbox["messages"]), 1)
        self.assertEqual(lead_inbox["messages"][0]["type"], "qa_dispatched")
        self.assertIn('"qa_pending": true', team_status)
        self.assertIn('"status": "active"', team_status)
        self.assertTrue((root / ".signals" / "qa_dispatch.json").exists())

    def test_dispatch_is_idempotent_for_same_pending(self) -> None:
        root, team_home = self._build_workspace()

        first = dispatch_qa_pending(root, team_home)
        second = dispatch_qa_pending(root, team_home)

        qa_inbox = json.loads((team_home / "inboxes" / "qa-tester.json").read_text(encoding="utf-8"))

        self.assertEqual(first, "QA_DISPATCHED slug=health-canonical-drift")
        self.assertEqual(second, "QA_ALREADY_DISPATCHED slug=health-canonical-drift")
        self.assertEqual(len(qa_inbox["messages"]), 1)

    def test_completed_result_clears_pending_without_dispatching_again(self) -> None:
        root, team_home = self._build_workspace()
        result_path = root / "analysis" / "qa_result.md"
        result_path.write_text(
            "## Durum: PASS\n**Slug:** health-canonical-drift\n**Cycle:** 1076\n",
            encoding="utf-8",
        )
        pending_path = root / ".signals" / "qa_pending"
        result_mtime = pending_path.stat().st_mtime + 10
        result_path.touch()
        result_path.write_text(
            "## Durum: PASS\n**Slug:** health-canonical-drift\n**Cycle:** 1076\n",
            encoding="utf-8",
        )
        import os

        os.utime(result_path, (result_mtime, result_mtime))

        result = dispatch_qa_pending(root, team_home)

        qa_inbox = json.loads((team_home / "inboxes" / "qa-tester.json").read_text(encoding="utf-8"))
        team_status = (root / "analysis" / "team_status.md").read_text(encoding="utf-8")

        self.assertEqual(result, "QA_COMPLETED slug=health-canonical-drift")
        self.assertFalse(pending_path.exists())
        self.assertFalse((root / ".signals" / "qa_dispatch.json").exists())
        self.assertEqual(len(qa_inbox["messages"]), 0)
        self.assertIn('"qa_pending": false', team_status)
        self.assertIn('"status": "idle"', team_status)


if __name__ == "__main__":
    unittest.main()
