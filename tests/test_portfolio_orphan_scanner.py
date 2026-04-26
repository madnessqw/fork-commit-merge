import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.portfolio_orphan_scanner import (
    _active_slugs,
    _categorize,
    _check_richness,
    _dir_size,
    _folder_slugs,
    format_report,
    scan_orphans,
)


@pytest.fixture
def tmp_env(tmp_path):
    state = {
        "products": {
            "active": [
                {"slug": "live-product-a"},
                {"slug": "live-product-b"},
            ]
        }
    }
    state_path = tmp_path / "STATE.json"
    state_path.write_text(json.dumps(state))

    products_dir = tmp_path / "products"
    products_dir.mkdir()

    for slug in ["live-product-a", "live-product-b"]:
        (products_dir / slug).mkdir()

    for slug in ["orphan-code", "orphan-spec", "orphan-dead", "orphan-deployable"]:
        d = products_dir / slug
        d.mkdir()

    (products_dir / "orphan-code" / "package.json").write_text("{}")
    (products_dir / "orphan-spec" / "spec.json").write_text("{}")
    (products_dir / "orphan-spec" / "product.json").write_text("{}")
    (products_dir / "orphan-deployable" / "package.json").write_text("{}")
    (products_dir / "orphan-deployable" / "vercel.json").write_text("{}")
    (products_dir / "orphan-dead" / "random.txt").write_text("x")

    return state_path, products_dir


class TestActiveSlugs:
    def test_extracts_slugs(self, tmp_env):
        state_path, _ = tmp_env
        result = _active_slugs(state_path)
        assert result == {"live-product-a", "live-product-b"}

    def test_handles_missing_file(self, tmp_path):
        result = _active_slugs(tmp_path / "nonexistent.json")
        assert result == set()

    def test_ignores_empty_slugs(self, tmp_path):
        state = {"products": {"active": [{"slug": ""}, {"slug": "valid"}]}}
        p = tmp_path / "STATE.json"
        p.write_text(json.dumps(state))
        result = _active_slugs(p)
        assert "valid" in result
        assert "" not in result


class TestFolderSlugs:
    def test_extracts_dirs(self, tmp_env):
        _, products_dir = tmp_env
        result = _folder_slugs(products_dir)
        assert "live-product-a" in result
        assert "orphan-code" in result

    def test_skips_hidden_dirs(self, tmp_path):
        products_dir = tmp_path / "products"
        products_dir.mkdir()
        (products_dir / ".hidden").mkdir()
        (products_dir / "visible").mkdir()
        result = _folder_slugs(products_dir)
        assert ".hidden" not in result
        assert "visible" in result

    def test_handles_missing_dir(self, tmp_path):
        result = _folder_slugs(tmp_path / "nonexistent")
        assert result == set()


class TestCheckRichness:
    def test_full_richness(self, tmp_path):
        d = tmp_path / "product"
        d.mkdir()
        for f in ["product.json", "vercel.json", "package.json", "spec.json", "README.md"]:
            (d / f).write_text("{}")
        result = _check_richness(d)
        assert all(result.values())

    def test_empty_dir(self, tmp_path):
        d = tmp_path / "empty"
        d.mkdir()
        result = _check_richness(d)
        assert not any(result.values())


class TestCategorize:
    def test_deployable(self):
        r = {"has_package_json": True, "has_vercel_json": True}
        assert _categorize(r) == "deployable"

    def test_has_code(self):
        r = {"has_package_json": True, "has_vercel_json": False}
        assert _categorize(r) == "has_code"

    def test_has_spec(self):
        r = {"has_package_json": False, "has_spec_json": True, "has_product_json": False, "has_vercel_json": False}
        assert _categorize(r) == "has_spec"

    def test_minimal(self):
        r = {"has_package_json": False, "has_spec_json": False, "has_product_json": False, "has_vercel_json": False, "has_readme": True}
        assert _categorize(r) == "minimal"

    def test_dead(self):
        r = {k: False for k in ["has_package_json", "has_vercel_json", "has_spec_json", "has_product_json", "has_readme"]}
        assert _categorize(r) == "dead"


class TestDirSize:
    def test_calculates_size(self, tmp_path):
        d = tmp_path / "dir"
        d.mkdir()
        (d / "file.txt").write_text("hello world")
        size = _dir_size(d)
        assert size > 0

    def test_empty_dir(self, tmp_path):
        d = tmp_path / "empty"
        d.mkdir()
        assert _dir_size(d) == 0


class TestScanOrphans:
    def test_finds_orphans(self, tmp_env):
        state_path, products_dir = tmp_env
        result = scan_orphans(state_path, products_dir)
        assert result["total_orphans"] == 4

    def test_categories(self, tmp_env):
        state_path, products_dir = tmp_env
        result = scan_orphans(state_path, products_dir)
        cats = result["categories"]
        assert cats["deployable"] == 1
        assert cats["has_code"] == 1
        assert cats["has_spec"] == 1
        assert cats["dead"] == 1

    def test_size_calculation(self, tmp_env):
        state_path, products_dir = tmp_env
        result = scan_orphans(state_path, products_dir, calc_size=True)
        assert result["total_size_bytes"] is not None
        assert result["total_size_bytes"] > 0
        assert result["total_size_mb"] is not None

    def test_no_size_by_default(self, tmp_env):
        state_path, products_dir = tmp_env
        result = scan_orphans(state_path, products_dir)
        assert result["total_size_bytes"] is None


class TestFormatReport:
    def test_contains_categories(self):
        result = {
            "total_orphans": 5,
            "categories": {"deployable": 2, "has_code": 1, "has_spec": 1, "minimal": 0, "dead": 1},
            "category_lists": {"deployable": ["a", "b"], "has_code": ["c"], "has_spec": ["d"], "minimal": [], "dead": ["e"]},
            "orphans": [],
            "total_size_bytes": None,
            "total_size_mb": None,
        }
        report = format_report(result)
        assert "**Total orphans:** 5" in report
        assert "deployable" in report
        assert "dead" in report

    def test_shows_size(self):
        result = {
            "total_orphans": 1,
            "categories": {"deployable": 0, "has_code": 0, "has_spec": 0, "minimal": 0, "dead": 1},
            "category_lists": {"deployable": [], "has_code": [], "has_spec": [], "minimal": [], "dead": ["x"]},
            "orphans": [],
            "total_size_bytes": 1024,
            "total_size_mb": 0.0,
        }
        report = format_report(result)
        assert "Total size" in report
