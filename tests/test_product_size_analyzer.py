import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.product_size_analyzer import (
    WASTE_DIRS,
    _active_slugs,
    _dir_size,
    _fmt_kb,
    _subdir_sizes,
    _tier_for_kb,
    format_report,
    scan_products,
)


@pytest.fixture
def tmp_products(tmp_path):
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps({
        "products": {
            "active": [
                {"slug": "alpha"},
                {"slug": "beta"},
            ]
        }
    }))

    products_dir = tmp_path / "products"
    (products_dir / "alpha" / "src").mkdir(parents=True)
    (products_dir / "alpha" / "src" / "app.js").write_text("x" * 500)
    (products_dir / "alpha" / "package.json").write_text("{}")

    (products_dir / "beta").mkdir(parents=True)
    (products_dir / "beta" / "index.html").write_text("<h1>hi</h1>")

    (products_dir / "orphan-one").mkdir(parents=True)
    (products_dir / "orphan-one" / "README.md").write_text("# old")

    (products_dir / "orphan-bloated" / "node_modules" / "pkg").mkdir(parents=True)
    (products_dir / "orphan-bloated" / "node_modules" / "pkg" / "index.js").write_text(
        "y" * 10000
    )
    (products_dir / "orphan-bloated" / ".next" / "cache").mkdir(parents=True)
    (products_dir / "orphan-bloated" / ".next" / "cache" / "data.bin").write_text(
        "z" * 20000
    )

    return tmp_path, products_dir, state_file


class TestActiveSlugs:
    def test_reads_active_slugs(self, tmp_products):
        _, _, state_file = tmp_products
        slugs = _active_slugs(state_file)
        assert slugs == {"alpha", "beta"}

    def test_empty_state(self, tmp_path):
        sf = tmp_path / "STATE.json"
        sf.write_text("{}")
        assert _active_slugs(sf) == set()

    def test_missing_file(self, tmp_path):
        assert _active_slugs(tmp_path / "nope.json") == set()


class TestDirSize:
    def test_measures_recursive(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        (d / "a.txt").write_text("a" * 100)
        (d / "nested").mkdir()
        (d / "nested" / "b.txt").write_text("b" * 200)
        assert _dir_size(d) == 300

    def test_empty_dir(self, tmp_path):
        d = tmp_path / "empty"
        d.mkdir()
        assert _dir_size(d) == 0


class TestSubdirSizes:
    def test_returns_subdir_sizes(self, tmp_path):
        (tmp_path / "a").mkdir()
        (tmp_path / "a" / "f.txt").write_text("x" * 50)
        (tmp_path / "b").mkdir()
        (tmp_path / "b" / "f.txt").write_text("y" * 100)
        (tmp_path / "file.txt").write_text("z")
        sizes = _subdir_sizes(tmp_path)
        assert sizes["a"] == 50
        assert sizes["b"] == 100
        assert "file.txt" not in sizes


class TestTierForKb:
    def test_tiny(self):
        assert _tier_for_kb(0) == "tiny"
        assert _tier_for_kb(5) == "tiny"

    def test_small(self):
        assert _tier_for_kb(50) == "small"

    def test_medium(self):
        assert _tier_for_kb(500) == "medium"

    def test_large(self):
        assert _tier_for_kb(2000) == "large"

    def test_huge(self):
        assert _tier_for_kb(50000) == "huge"


class TestFmtKb:
    def test_kb(self):
        assert "KB" in _fmt_kb(500)

    def test_mb(self):
        assert "MB" in _fmt_kb(2048)


class TestScanProducts:
    def test_basic_scan(self, tmp_products):
        tmp_root, products_dir, state_file = tmp_products
        result = scan_products(products_dir, state_file, top=10)
        assert result["total_products"] == 4
        assert result["active_count"] == 2
        assert result["orphan_count"] == 2
        assert result["total_size_kb"] > 0
        assert result["active_size_kb"] > 0
        assert result["orphan_size_kb"] > 0

    def test_waste_detection(self, tmp_products):
        tmp_root, products_dir, state_file = tmp_products
        result = scan_products(products_dir, state_file)
        assert result["total_waste_kb"] > 0
        assert "node_modules" in result["waste_breakdown_kb"]
        assert ".next" in result["waste_breakdown_kb"]

    def test_tier_distribution(self, tmp_products):
        _, products_dir, state_file = tmp_products
        result = scan_products(products_dir, state_file)
        tiers = result["tier_distribution"]
        total = sum(tiers.values())
        assert total == 4

    def test_sorted_by_size(self, tmp_products):
        _, products_dir, state_file = tmp_products
        result = scan_products(products_dir, state_file)
        sizes = [e["size_bytes"] for e in result["top_largest"]]
        assert sizes == sorted(sizes, reverse=True)

    def test_missing_products_dir(self, tmp_path):
        result = scan_products(tmp_path / "nope", tmp_path / "STATE.json")
        assert "error" in result

    def test_top_waste_sorted(self, tmp_products):
        _, products_dir, state_file = tmp_products
        result = scan_products(products_dir, state_file)
        top_waste = result.get("top_waste", [])
        if len(top_waste) > 1:
            wastes = [e.get("waste_kb", 0) for e in top_waste]
            assert wastes == sorted(wastes, reverse=True)


class TestFormatReport:
    def test_full_report(self, tmp_products):
        _, products_dir, state_file = tmp_products
        result = scan_products(products_dir, state_file)
        report = format_report(result)
        assert "# Product Size Analysis" in report
        assert "Top 15" in report
        assert "alpha" in report

    def test_waste_section(self, tmp_products):
        _, products_dir, state_file = tmp_products
        result = scan_products(products_dir, state_file)
        report = format_report(result)
        assert "Waste Breakdown" in report
        assert "node_modules" in report

    def test_error_report(self):
        report = format_report({"error": "oops"})
        assert "Error" in report

    def test_recommendations_orphan(self, tmp_products):
        _, products_dir, state_file = tmp_products
        result = scan_products(products_dir, state_file)
        report = format_report(result)
        assert "Recommendations" in report
