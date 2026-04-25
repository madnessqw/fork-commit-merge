import json
import sys
import tempfile
from pathlib import Path
import unittest

from scripts.health_trend import (
    record_snapshot,
    load_trend,
    compute_trend,
    trend_summary_text,
    stuck_metrics,
    drift_slug_history,
    cycle_delta_report,
)


class HealthTrendTests(unittest.TestCase):
    def _workspace(self) -> tuple[Path, Path]:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        root = Path(tempdir.name) / "UniverseCreator"
        summary = root / "STATE_SUMMARY.json"
        summary.parent.mkdir(parents=True, exist_ok=True)
        return root, summary

    def _write_summary(self, path: Path, **overrides: object) -> None:
        data = {
            "cycle": 100,
            "live_count": 90,
            "healthy_count": 87,
            "unhealthy_count": 3,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 6,
            "gaps": {"canonical_url_drift": []},
        }
        data.update(overrides)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_record_snapshot_creates_file(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(summary)
            snap = record_snapshot(summary)
            self.assertEqual(snap["live"], 90)
            self.assertEqual(snap["healthy"], 87)
            self.assertAlmostEqual(snap["health_pct"], 96.7, places=0)
            self.assertTrue(trend_file.exists())
        finally:
            ht.TREND_FILE = orig

    def test_compute_trend_improving(self) -> None:
        entries = [
            {"health_pct": 90.0, "cycle": 1},
            {"health_pct": 95.0, "cycle": 2},
        ]
        trend = compute_trend(entries)
        self.assertEqual(trend["direction"], "improving")
        self.assertAlmostEqual(trend["health_delta"], 5.0)

    def test_compute_trend_degrading(self) -> None:
        entries = [
            {"health_pct": 95.0, "cycle": 1},
            {"health_pct": 88.0, "cycle": 2},
        ]
        trend = compute_trend(entries)
        self.assertEqual(trend["direction"], "degrading")

    def test_compute_trend_stable(self) -> None:
        entries = [
            {"health_pct": 95.0, "cycle": 1},
            {"health_pct": 95.5, "cycle": 2},
        ]
        trend = compute_trend(entries)
        self.assertEqual(trend["direction"], "stable")

    def test_compute_trend_unknown_with_one_entry(self) -> None:
        trend = compute_trend([{"health_pct": 90.0}])
        self.assertEqual(trend["direction"], "unknown")

    def test_load_trend_empty(self) -> None:
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = Path("/tmp/nonexistent_health_trend_test.jsonl")
        try:
            self.assertEqual(load_trend(), [])
        finally:
            ht.TREND_FILE = orig

    def test_record_snapshot_with_drift(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(
                summary,
                gaps={"canonical_url_drift": [{"slug": "a"}, {"slug": "b"}]},
            )
            snap = record_snapshot(summary)
            self.assertEqual(snap["canonical_drift"], 2)
        finally:
            ht.TREND_FILE = orig

    def test_record_snapshot_includes_grade(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(summary)
            snap = record_snapshot(summary)
            self.assertEqual(snap["grade"], "A")
        finally:
            ht.TREND_FILE = orig

    def test_record_snapshot_grade_b(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(summary, live_count=100, healthy_count=90)
            snap = record_snapshot(summary)
            self.assertEqual(snap["grade"], "B")
        finally:
            ht.TREND_FILE = orig

    def test_trend_summary_text_includes_grade(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(summary)
            text = trend_summary_text()
            import re
            self.assertTrue(re.search(r"\[[A-F]\]", text), f"No grade found in: {text}")
        finally:
            ht.TREND_FILE = orig_trend

    def test_record_snapshot_uses_top_level_canonical_drift_when_detail_missing(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(summary, canonical_url_drift=3, gaps={})
            snap = record_snapshot(summary)
            self.assertEqual(snap["canonical_drift"], 3)
        finally:
            ht.TREND_FILE = orig

    def test_record_snapshot_includes_fallback_healthy(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(summary, fallback_healthy_count=4)
            snap = record_snapshot(summary)
            self.assertEqual(snap["fallback_healthy"], 4)
        finally:
            ht.TREND_FILE = orig

    def test_record_snapshot_fallback_healthy_from_gaps_array(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(
                summary,
                gaps={"fallback_healthy": [{"slug": "a"}, {"slug": "b"}]},
            )
            snap = record_snapshot(summary)
            self.assertEqual(snap["fallback_healthy"], 2)
        finally:
            ht.TREND_FILE = orig

    def test_trend_summary_text_includes_fallback_when_nonzero(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(summary, fallback_healthy_count=3)
            text = trend_summary_text()
            self.assertIn("Fallback: 3", text)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root

    def test_trend_summary_text_no_fallback_when_zero(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(summary, fallback_healthy_count=0)
            text = trend_summary_text()
            self.assertNotIn("Fallback", text)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root

    def test_stuck_metrics_detects_stuck_deploy_gap(self) -> None:
        entries = [
            {"deploy_gap": 5, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 0},
            {"deploy_gap": 5, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 0},
            {"deploy_gap": 5, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 0},
        ]
        result = stuck_metrics(entries, window=3)
        self.assertEqual(result["stuck_count"], 1)
        self.assertEqual(result["stuck_metrics"][0]["metric"], "deploy_gap")
        self.assertEqual(result["stuck_metrics"][0]["value"], 5)

    def test_stuck_metrics_no_stuck_when_improving(self) -> None:
        entries = [
            {"deploy_gap": 5, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 0},
            {"deploy_gap": 3, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 0},
            {"deploy_gap": 1, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 0},
        ]
        result = stuck_metrics(entries, window=3)
        self.assertEqual(result["stuck_count"], 0)

    def test_stuck_metrics_multiple_stuck(self) -> None:
        entries = [
            {"deploy_gap": 5, "canonical_drift": 7, "fallback_healthy": 7, "unhealthy": 0, "checkout_gap": 0},
            {"deploy_gap": 5, "canonical_drift": 7, "fallback_healthy": 7, "unhealthy": 0, "checkout_gap": 0},
            {"deploy_gap": 5, "canonical_drift": 7, "fallback_healthy": 7, "unhealthy": 0, "checkout_gap": 0},
        ]
        result = stuck_metrics(entries, window=3)
        self.assertEqual(result["stuck_count"], 3)

    def test_stuck_metrics_unknown_with_one_entry(self) -> None:
        result = stuck_metrics([{"deploy_gap": 5}])
        self.assertEqual(result["stuck_count"], 0)
        self.assertEqual(result["snapshots"], 1)

    def test_stuck_metrics_ignores_zero_values(self) -> None:
        entries = [
            {"deploy_gap": 0, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 0},
            {"deploy_gap": 0, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 0},
        ]
        result = stuck_metrics(entries, window=2)
        self.assertEqual(result["stuck_count"], 0)

    def test_main_default_outputs_snapshot(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(summary)
            from scripts.health_trend import main
            import io
            captured = io.StringIO()
            import contextlib
            with contextlib.redirect_stdout(captured):
                ret = main()
            self.assertEqual(ret, 0)
            output = json.loads(captured.getvalue())
            self.assertEqual(output["live"], 90)
            self.assertEqual(output["healthy"], 87)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root

    def test_main_stuck_subcommand(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(summary)
            from scripts.health_trend import main
            import io, contextlib
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                orig_argv = sys.argv
                sys.argv = ["health_trend.py", "stuck"]
                try:
                    ret = main()
                finally:
                    sys.argv = orig_argv
            self.assertEqual(ret, 0)
            output = json.loads(captured.getvalue())
            self.assertIn("stuck_count", output)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root

    def test_main_trend_subcommand(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(summary)
            ht.TREND_FILE = trend_file
            from scripts.health_trend import main
            import io, contextlib
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                orig_argv = sys.argv
                sys.argv = ["health_trend.py", "trend"]
                try:
                    ret = main()
                finally:
                    sys.argv = orig_argv
            self.assertEqual(ret, 0)
            output = json.loads(captured.getvalue())
            self.assertIn("direction", output)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root

    def test_compute_trend_includes_deploy_and_drift_details(self) -> None:
        entries = [
            {"health_pct": 90.0, "cycle": 1, "deploy_gap": 5, "canonical_drift": 2, "fallback_healthy": 1},
            {"health_pct": 95.0, "cycle": 2, "deploy_gap": 3, "canonical_drift": 0, "fallback_healthy": 0},
        ]
        trend = compute_trend(entries)
        self.assertEqual(trend["latest_deploy_gap"], 3)
        self.assertEqual(trend["latest_canonical_drift"], 0)
        self.assertEqual(trend["latest_fallback_healthy"], 0)

    def test_stuck_metrics_checkout_gap_stuck(self) -> None:
        entries = [
            {"deploy_gap": 0, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 4},
            {"deploy_gap": 0, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 4},
            {"deploy_gap": 0, "canonical_drift": 0, "fallback_healthy": 0, "unhealthy": 0, "checkout_gap": 4},
        ]
        result = stuck_metrics(entries, window=3)
        self.assertEqual(result["stuck_count"], 1)
        self.assertEqual(result["stuck_metrics"][0]["metric"], "checkout_gap")
        self.assertEqual(result["stuck_metrics"][0]["stale_snapshots"], 3)

    def test_record_snapshot_zero_live(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            self._write_summary(summary, live_count=0, healthy_count=0)
            snap = record_snapshot(summary)
            self.assertEqual(snap["health_pct"], 0.0)
        finally:
            ht.TREND_FILE = orig

    def test_trend_summary_text_includes_stuck_tag(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(
                summary,
                deploy_missing_or_bad_url=6,
                gaps={"canonical_url_drift": [{"slug": "a"}, {"slug": "b"}, {"slug": "c"}]},
            )
            for _ in range(6):
                ht.TREND_FILE = trend_file
                record_snapshot(summary)
            text = trend_summary_text()
            if "STUCK:" in text:
                self.assertIn("deploy_gap=6", text)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root

    def test_trend_summary_text_no_stuck_when_zero(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(summary)
            text = trend_summary_text()
            self.assertNotIn("STUCK:", text)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root

    def test_load_trend_corrupt_line_skipped(self) -> None:
        import scripts.health_trend as ht

        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        trend_file.parent.mkdir(parents=True, exist_ok=True)
        trend_file.write_text('{"health_pct":90}\nCORRUPT\n{"health_pct":95}\n', encoding="utf-8")

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            entries = load_trend(limit=10)
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0]["health_pct"], 90)
            self.assertEqual(entries[1]["health_pct"], 95)
        finally:
            ht.TREND_FILE = orig

    def test_record_snapshot_includes_drift_slugs(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(
                summary,
                gaps={"canonical_url_drift": [{"slug": "alpha"}, {"slug": "beta"}]},
            )
            snap = record_snapshot(summary)
            self.assertEqual(snap["drift_slugs"], ["alpha", "beta"])
        finally:
            ht.TREND_FILE = orig
            ht.ROOT = orig_root

    def test_drift_slug_history_empty(self) -> None:
        import scripts.health_trend as ht

        orig = ht.TREND_FILE
        ht.TREND_FILE = Path("/tmp/nonexistent_drift_history_test.jsonl")
        try:
            result = drift_slug_history()
            self.assertEqual(result["drift_slug_count"], 0)
            self.assertEqual(result["slugs"], {})
        finally:
            ht.TREND_FILE = orig

    def test_drift_slug_history_tracks_slugs(self) -> None:
        import scripts.health_trend as ht

        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        trend_file.parent.mkdir(parents=True, exist_ok=True)

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            trend_file.write_text(
                '{"ts":"2026-01-01T00:00Z","drift_slugs":["a","b"]}\n'
                '{"ts":"2026-01-01T01:00Z","drift_slugs":["a","c"]}\n',
                encoding="utf-8",
            )
            result = drift_slug_history()
            self.assertEqual(result["drift_slug_count"], 3)
            self.assertEqual(result["slugs"]["a"]["first_seen"], "2026-01-01T00:00Z")
            self.assertEqual(result["slugs"]["a"]["last_seen"], "2026-01-01T01:00Z")
            self.assertEqual(result["slugs"]["b"]["first_seen"], "2026-01-01T00:00Z")
            self.assertEqual(result["slugs"]["c"]["first_seen"], "2026-01-01T01:00Z")
        finally:
            ht.TREND_FILE = orig

    def test_drift_slug_history_no_slugs_in_entries(self) -> None:
        import scripts.health_trend as ht

        root, _summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        trend_file.parent.mkdir(parents=True, exist_ok=True)

        orig = ht.TREND_FILE
        ht.TREND_FILE = trend_file
        try:
            trend_file.write_text(
                '{"ts":"2026-01-01T00:00Z","health_pct":100}\n'
                '{"ts":"2026-01-01T01:00Z","health_pct":99}\n',
                encoding="utf-8",
            )
            result = drift_slug_history()
            self.assertEqual(result["drift_slug_count"], 0)
        finally:
            ht.TREND_FILE = orig

    def test_main_drift_history_subcommand(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(summary)
            from scripts.health_trend import main
            import io, contextlib
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                orig_argv = sys.argv
                sys.argv = ["health_trend.py", "drift-history"]
                try:
                    ret = main()
                finally:
                    sys.argv = orig_argv
            self.assertEqual(ret, 0)
            output = json.loads(captured.getvalue())
            self.assertIn("drift_slug_count", output)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root

    def test_cycle_delta_report_insufficient_snapshots(self) -> None:
        result = cycle_delta_report([{"health_pct": 95.0, "cycle": 1}])
        self.assertFalse(result["available"])
        self.assertEqual(result["reason"], "insufficient_snapshots")

    def test_cycle_delta_report_no_changes(self) -> None:
        entries = [
            {"live": 100, "healthy": 95, "unhealthy": 5, "health_pct": 95.0,
             "checkout_gap": 0, "deploy_gap": 0, "canonical_drift": 0,
             "fallback_healthy": 0, "cycle": 1, "grade": "A", "drift_slugs": []},
            {"live": 100, "healthy": 95, "unhealthy": 5, "health_pct": 95.0,
             "checkout_gap": 0, "deploy_gap": 0, "canonical_drift": 0,
             "fallback_healthy": 0, "cycle": 2, "grade": "A", "drift_slugs": []},
        ]
        result = cycle_delta_report(entries)
        self.assertTrue(result["available"])
        self.assertFalse(result["changed"])
        self.assertEqual(result["deltas"], [])
        self.assertIsNone(result["grade_change"])

    def test_cycle_delta_report_detects_changes(self) -> None:
        entries = [
            {"live": 100, "healthy": 90, "unhealthy": 10, "health_pct": 90.0,
             "checkout_gap": 3, "deploy_gap": 5, "canonical_drift": 2,
             "fallback_healthy": 1, "cycle": 1, "grade": "B", "drift_slugs": []},
            {"live": 100, "healthy": 95, "unhealthy": 5, "health_pct": 95.0,
             "checkout_gap": 0, "deploy_gap": 2, "canonical_drift": 0,
             "fallback_healthy": 0, "cycle": 2, "grade": "A", "drift_slugs": []},
        ]
        result = cycle_delta_report(entries)
        self.assertTrue(result["available"])
        self.assertTrue(result["changed"])
        self.assertEqual(result["from_cycle"], 1)
        self.assertEqual(result["to_cycle"], 2)
        self.assertEqual(result["grade_change"], {"from": "B", "to": "A"})

        delta_metrics = {d["metric"]: d["delta"] for d in result["deltas"]}
        self.assertEqual(delta_metrics["healthy"], 5)
        self.assertEqual(delta_metrics["unhealthy"], -5)
        self.assertEqual(delta_metrics["deploy_gap"], -3)
        self.assertEqual(delta_metrics["canonical_drift"], -2)

    def test_cycle_delta_report_drift_slug_changes(self) -> None:
        entries = [
            {"live": 100, "healthy": 95, "unhealthy": 5, "health_pct": 95.0,
             "checkout_gap": 0, "deploy_gap": 0, "canonical_drift": 2,
             "fallback_healthy": 0, "cycle": 1, "drift_slugs": ["a", "b"]},
            {"live": 100, "healthy": 95, "unhealthy": 5, "health_pct": 95.0,
             "checkout_gap": 0, "deploy_gap": 0, "canonical_drift": 2,
             "fallback_healthy": 0, "cycle": 2, "drift_slugs": ["b", "c"]},
        ]
        result = cycle_delta_report(entries)
        self.assertEqual(result["new_drift_slugs"], ["c"])
        self.assertEqual(result["resolved_drift_slugs"], ["a"])

    def test_cycle_delta_report_float_delta(self) -> None:
        entries = [
            {"live": 100, "healthy": 90, "unhealthy": 10, "health_pct": 90.0,
             "checkout_gap": 0, "deploy_gap": 0, "canonical_drift": 0,
             "fallback_healthy": 0, "cycle": 1, "drift_slugs": []},
            {"live": 100, "healthy": 92, "unhealthy": 8, "health_pct": 92.0,
             "checkout_gap": 0, "deploy_gap": 0, "canonical_drift": 0,
             "fallback_healthy": 0, "cycle": 2, "drift_slugs": []},
        ]
        result = cycle_delta_report(entries)
        delta_metrics = {d["metric"]: d["delta"] for d in result["deltas"]}
        self.assertEqual(delta_metrics["health_pct"], 2.0)
        self.assertEqual(delta_metrics["healthy"], 2)

    def test_cycle_delta_report_empty_entries(self) -> None:
        result = cycle_delta_report([])
        self.assertFalse(result["available"])

    def test_cycle_delta_report_same_grade_no_change(self) -> None:
        entries = [
            {"live": 100, "healthy": 97, "unhealthy": 3, "health_pct": 97.0,
             "checkout_gap": 0, "deploy_gap": 0, "canonical_drift": 0,
             "fallback_healthy": 0, "cycle": 1, "grade": "A", "drift_slugs": []},
            {"live": 100, "healthy": 96, "unhealthy": 4, "health_pct": 96.0,
             "checkout_gap": 0, "deploy_gap": 0, "canonical_drift": 0,
             "fallback_healthy": 0, "cycle": 2, "grade": "A", "drift_slugs": []},
        ]
        result = cycle_delta_report(entries)
        self.assertIsNone(result["grade_change"])

    def test_main_delta_subcommand(self) -> None:
        root, summary = self._workspace()
        trend_file = root / "logs" / "health_trend.jsonl"
        import scripts.health_trend as ht

        orig_trend = ht.TREND_FILE
        orig_root = ht.ROOT
        ht.TREND_FILE = trend_file
        ht.ROOT = root
        try:
            self._write_summary(summary)
            from scripts.health_trend import main
            import io, contextlib
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                orig_argv = sys.argv
                sys.argv = ["health_trend.py", "delta"]
                try:
                    ret = main()
                finally:
                    sys.argv = orig_argv
            self.assertEqual(ret, 0)
            output = json.loads(captured.getvalue())
            self.assertIn("available", output)
        finally:
            ht.TREND_FILE = orig_trend
            ht.ROOT = orig_root


if __name__ == "__main__":
    unittest.main()
