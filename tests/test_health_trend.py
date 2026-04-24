import json
import tempfile
from pathlib import Path
import unittest

from scripts.health_trend import (
    record_snapshot,
    load_trend,
    compute_trend,
    trend_summary_text,
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


if __name__ == "__main__":
    unittest.main()
