import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from scripts.product_waste_cleaner import (
    WASTE_DIRS,
    _dir_size,
    _fmt_kb,
    clean_waste,
    format_report,
    scan_waste,
)


@pytest.fixture
def tmp_products(tmp_path):
    state = {"products": {"active": [{"slug": "active-prod"}, {"slug": "another-prod"}]}}
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))

    products_dir = tmp_path / "products"

    (products_dir / "active-prod" / "node_modules" / "pkg").mkdir(parents=True)
    (products_dir / "active-prod" / "node_modules" / "pkg" / "index.js").write_text(
        "x" * 5000
    )
    (products_dir / "active-prod" / ".vercel").mkdir(parents=True)
    (products_dir / "active-prod" / ".vercel" / "config.json").write_text("{}")

    (products_dir / "another-prod" / "dist").mkdir(parents=True)
    (products_dir / "another-prod" / "dist" / "bundle.js").write_text("y" * 3000)

    (products_dir / "orphan-prod" / "node_modules" / "lib").mkdir(parents=True)
    (products_dir / "orphan-prod" / "node_modules" / "lib" / "a.js").write_text("z" * 2000)

    (products_dir / "clean-prod").mkdir(parents=True)
    (products_dir / "clean-prod" / "package.json").write_text("{}")

    return products_dir, state_file


class TestScanWaste:
    def test_finds_all_waste(self, tmp_products):
        products_dir, state_file = tmp_products
        results = scan_waste(products_dir, state_file)
        assert len(results) == 4

    def test_sorted_by_size_desc(self, tmp_products):
        products_dir, state_file = tmp_products
        results = scan_waste(products_dir, state_file)
        for i in range(len(results) - 1):
            assert results[i]["size_bytes"] >= results[i + 1]["size_bytes"]

    def test_filter_by_type(self, tmp_products):
        products_dir, state_file = tmp_products
        results = scan_waste(products_dir, state_file, waste_types=["node_modules"])
        assert all(r["waste_type"] == "node_modules" for r in results)
        assert len(results) == 2

    def test_filter_by_slug(self, tmp_products):
        products_dir, state_file = tmp_products
        results = scan_waste(products_dir, state_file, slug_filter="active-prod")
        assert all(r["slug"] == "active-prod" for r in results)

    def test_min_size_filter(self, tmp_products):
        products_dir, state_file = tmp_products
        results = scan_waste(products_dir, state_file, min_size_kb=10)
        for r in results:
            assert r["size_kb"] >= 10

    def test_active_flag(self, tmp_products):
        products_dir, state_file = tmp_products
        results = scan_waste(products_dir, state_file)
        active = [r for r in results if r["is_active"]]
        orphan = [r for r in results if not r["is_active"]]
        assert len(active) >= 2
        assert len(orphan) >= 1

    def test_empty_products_dir(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_file.write_text("{}")
        empty_dir = tmp_path / "products"
        empty_dir.mkdir()
        results = scan_waste(empty_dir, state_file)
        assert results == []

    def test_no_products_dir(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_file.write_text("{}")
        results = scan_waste(tmp_path / "nonexistent", state_file)
        assert results == []


class TestCleanWaste:
    def test_dry_run_does_not_delete(self, tmp_products):
        products_dir, state_file = tmp_products
        entries = scan_waste(products_dir, state_file)
        result = clean_waste(entries, dry_run=True)
        assert result["cleaned_count"] == 4
        assert result["dry_run"] is True
        for e in entries:
            assert Path(e["path"]).is_dir()

    def test_apply_deletes_dirs(self, tmp_products):
        products_dir, state_file = tmp_products
        entries = scan_waste(products_dir, state_file)
        result = clean_waste(entries, dry_run=False)
        assert result["cleaned_count"] == 4
        for e in entries:
            assert not Path(e["path"]).exists()

    def test_total_reclaimed(self, tmp_products):
        products_dir, state_file = tmp_products
        entries = scan_waste(products_dir, state_file)
        result = clean_waste(entries, dry_run=True)
        expected = sum(e["size_bytes"] for e in entries)
        assert result["total_reclaimed_bytes"] == expected

    def test_missing_path_error(self, tmp_path):
        entries = [{"slug": "x", "waste_type": "node_modules", "size_bytes": 100, "path": "/nonexistent/path"}]
        result = clean_waste(entries, dry_run=False)
        assert result["cleaned_count"] == 0
        assert len(result["errors"]) == 1


class TestFormatReport:
    def test_empty_entries(self):
        report = format_report([])
        assert "No waste directories found" in report

    def test_includes_waste_by_type(self, tmp_products):
        products_dir, state_file = tmp_products
        entries = scan_waste(products_dir, state_file)
        report = format_report(entries)
        assert "Waste by Type" in report
        assert "node_modules" in report

    def test_includes_cleanup_result(self):
        entries = [{"slug": "test", "waste_type": "node_modules", "size_kb": 100, "is_active": True, "size_bytes": 102400}]
        clean_result = {"cleaned_count": 1, "total_reclaimed_mb": 0.1, "errors": [], "dry_run": True, "total_reclaimed_bytes": 102400, "total_reclaimed_kb": 100.0}
        report = format_report(entries, clean_result)
        assert "DRY RUN" in report
        assert "1 entries" in report


class TestFmtKb:
    def test_small(self):
        assert _fmt_kb(500) == "500.0 KB"

    def test_large(self):
        assert _fmt_kb(2048) == "2.0 MB"
