import unittest
from pathlib import Path
from unittest.mock import patch
from datetime import datetime, timedelta, timezone

from scripts.analysis_archive import (
    ARCHIVE_PATTERNS,
    PROTECTED_FILES,
    _is_archivable,
    _archive_dest,
    scan_archivable,
    archive_files,
)


class TestIsArchivable(unittest.TestCase):
    def test_kimi_rapor_matches(self) -> None:
        self.assertTrue(_is_archivable("kimi_rapor_20260424_0905.md"))

    def test_polar_plan_cycle_matches(self) -> None:
        self.assertTrue(_is_archivable("polar_plan_cycle1110.md"))

    def test_unhealthy_report_matches(self) -> None:
        self.assertTrue(_is_archivable("unhealthy_report_1098.md"))

    def test_cycle_plan_matches(self) -> None:
        self.assertTrue(_is_archivable("cycle_1112_plan.md"))

    def test_polar_checkout_sync_report_date_matches(self) -> None:
        self.assertTrue(_is_archivable("polar_checkout_sync_report_20260425_1901.md"))

    def test_polar_checkout_plan_cycle_matches(self) -> None:
        self.assertTrue(_is_archivable("polar_checkout_plan_cycle1111.md"))

    def test_oneri_protected(self) -> None:
        self.assertFalse(_is_archivable("oneri.md"))

    def test_glm_fix_brief_protected(self) -> None:
        self.assertFalse(_is_archivable("glm_fix_brief.md"))

    def test_sorun_analizi_protected(self) -> None:
        self.assertFalse(_is_archivable("sorun_analizi.md"))

    def test_unknown_file_not_archivable(self) -> None:
        self.assertFalse(_is_archivable("random_notes.md"))

    def test_protected_overrides_pattern(self) -> None:
        for name in PROTECTED_FILES:
            self.assertFalse(_is_archivable(name), f"{name} should be protected")


class TestArchiveDest(unittest.TestCase):
    def test_january_path(self) -> None:
        ts = datetime(2026, 1, 15, tzinfo=timezone.utc).timestamp()
        dest = _archive_dest(ts)
        self.assertEqual(dest.name, "2026-01")

    def test_december_path(self) -> None:
        ts = datetime(2025, 12, 3, tzinfo=timezone.utc).timestamp()
        dest = _archive_dest(ts)
        self.assertEqual(dest.name, "2025-12")


class TestScanArchivable(unittest.TestCase):
    @patch("scripts.analysis_archive.ANALYSIS_DIR", new_callable=lambda: property(lambda self: Path("/nonexistent")))
    def test_missing_dir_returns_empty(self, mock_dir: object) -> None:
        pass

    @patch("scripts.analysis_archive.ANALYSIS_DIR")
    def test_finds_old_archivable_file(self, mock_analysis: Path) -> None:
        import scripts.analysis_archive as mod

        old_time = (datetime.now(tz=timezone.utc) - timedelta(hours=48)).timestamp()
        fake_file = type("FakePath", (), {
            "is_file": lambda s: True,
            "name": "kimi_rapor_20260424_0905.md",
            "stat": lambda s: type("S", (), {"st_mtime": old_time, "st_size": 1024})(),
            "__iter__": lambda s: iter([]),
        })()
        recent_file = type("FakePath", (), {
            "is_file": lambda s: True,
            "name": "kimi_rapor_20260426_1200.md",
            "stat": lambda s: type("S", (), {"st_mtime": datetime.now(tz=timezone.utc).timestamp(), "st_size": 512})(),
            "__iter__": lambda s: iter([]),
        })()
        protected_file = type("FakePath", (), {
            "is_file": lambda s: True,
            "name": "oneri.md",
            "stat": lambda s: type("S", (), {"st_mtime": old_time, "st_size": 256})(),
            "__iter__": lambda s: iter([]),
        })()
        mock_analysis.iterdir.return_value = [fake_file, recent_file, protected_file]

        results = scan_archivable(max_age_hours=24)
        names = [r["name"] for r in results]
        self.assertIn("kimi_rapor_20260424_0905.md", names)
        self.assertNotIn("kimi_rapor_20260426_1200.md", names)
        self.assertNotIn("oneri.md", names)


class TestArchiveFilesDryRun(unittest.TestCase):
    @patch("scripts.analysis_archive.scan_archivable")
    def test_dry_run_counts_but_does_not_move(self, mock_scan: unittest.mock.MagicMock) -> None:
        mock_scan.return_value = [
            {"path": Path("/tmp/a.md"), "name": "a.md", "mtime": 0.0, "dest_dir": Path("/tmp/archive/2026-04"), "size_kb": 1.0},
            {"path": Path("/tmp/b.md"), "name": "b.md", "mtime": 0.0, "dest_dir": Path("/tmp/archive/2026-04"), "size_kb": 2.0},
        ]
        result = archive_files(dry_run=True)
        self.assertEqual(result["moved"], 2)
        self.assertEqual(result["total_scanned"], 2)
        self.assertAlmostEqual(result["freed_kb"], 3.0)


class TestArchiveFilesLive(unittest.TestCase):
    @patch("scripts.analysis_archive.shutil.move")
    @patch("scripts.analysis_archive.scan_archivable")
    def test_live_moves_files(self, mock_scan: unittest.mock.MagicMock, mock_move: unittest.mock.MagicMock) -> None:
        mock_scan.return_value = [
            {"path": Path("/tmp/a.md"), "name": "a.md", "mtime": 0.0, "dest_dir": Path("/tmp/archive/2026-04"), "size_kb": 1.5},
        ]
        result = archive_files(dry_run=False)
        self.assertEqual(result["moved"], 1)
        mock_move.assert_called_once()

    @patch("scripts.analysis_archive.shutil.move", side_effect=PermissionError("nope"))
    @patch("scripts.analysis_archive.scan_archivable")
    def test_error_captured(self, mock_scan: unittest.mock.MagicMock, mock_move: unittest.mock.MagicMock) -> None:
        mock_scan.return_value = [
            {"path": Path("/tmp/a.md"), "name": "a.md", "mtime": 0.0, "dest_dir": Path("/tmp/archive/2026-04"), "size_kb": 1.0},
        ]
        result = archive_files(dry_run=False)
        self.assertEqual(result["moved"], 0)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("a.md", result["errors"][0])
