from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.slug_consistency_checker import (
    check_consistency,
    format_report,
    _slugs_from_state,
    _slugs_from_summary,
    _slugs_from_folders,
)

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"
PRODUCTS_DIR = ROOT / "products"


class TestSlugsFromState:
    def test_returns_set(self):
        result = _slugs_from_state()
        assert isinstance(result, set)

    def test_non_empty(self):
        result = _slugs_from_state()
        assert len(result) > 0

    def test_known_slug_present(self):
        result = _slugs_from_state()
        assert "uuid-generator-pro" in result

    def test_no_empty_strings(self):
        result = _slugs_from_state()
        assert "" not in result


class TestSlugsFromSummary:
    def test_returns_set(self):
        result = _slugs_from_summary()
        assert isinstance(result, set)

    def test_non_empty(self):
        result = _slugs_from_summary()
        assert len(result) > 0

    def test_known_slug_present(self):
        result = _slugs_from_summary()
        assert "uuid-generator-pro" in result

    def test_no_empty_strings(self):
        result = _slugs_from_summary()
        assert "" not in result


class TestSlugsFromFolders:
    def test_returns_set(self):
        result = _slugs_from_folders()
        assert isinstance(result, set)

    def test_non_empty(self):
        result = _slugs_from_folders()
        assert len(result) > 0

    def test_no_hidden_dirs(self):
        result = _slugs_from_folders()
        for s in result:
            assert not s.startswith(".")

    def test_no_empty_strings(self):
        result = _slugs_from_folders()
        assert "" not in result


class TestCheckConsistency:
    def test_returns_dict_with_keys(self):
        result = check_consistency()
        expected_keys = {
            "state_count", "summary_count", "folder_count",
            "everywhere_count", "state_missing_folder",
            "folder_orphan", "summary_only",
            "total_issues", "issues", "health_pct",
        }
        assert expected_keys <= set(result.keys())

    def test_state_count_positive(self):
        result = check_consistency()
        assert result["state_count"] > 0

    def test_summary_count_positive(self):
        result = check_consistency()
        assert result["summary_count"] > 0

    def test_folder_count_positive(self):
        result = check_consistency()
        assert result["folder_count"] > 0

    def test_health_pct_range(self):
        result = check_consistency()
        assert 0.0 <= result["health_pct"] <= 100.0

    def test_issues_is_list(self):
        result = check_consistency()
        assert isinstance(result["issues"], list)

    def test_state_missing_folder_is_sorted(self):
        result = check_consistency()
        smf = result["state_missing_folder"]
        assert smf == sorted(smf)

    def test_folder_orphan_is_sorted(self):
        result = check_consistency()
        fo = result["folder_orphan"]
        assert fo == sorted(fo)


class TestFormatReport:
    def test_contains_header(self):
        result = check_consistency()
        report = format_report(result)
        assert "Slug Consistency Report" in report

    def test_contains_counts(self):
        result = check_consistency()
        report = format_report(result)
        assert "STATE.json:" in report
        assert "STATE_SUMMARY.json:" in report
        assert "products/ folders:" in report

    def test_contains_health_pct(self):
        result = check_consistency()
        report = format_report(result)
        assert "Consistency:" in report
