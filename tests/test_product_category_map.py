from __future__ import annotations

import json
import textwrap
from pathlib import Path

from scripts.product_category_map import (
    build_category_map,
    categorize_product,
    consolidation_report,
    find_overlap_categories,
    find_shared_checkout,
    report_markdown,
)


def _product(**overrides):
    base = {"n": "Test Product", "s": "test-product", "st": "live", "v": "https://test-product.vercel.app", "c": "https://buy.polar.sh/test"}
    base.update(overrides)
    return base


def _summary(products, tmp_path: Path):
    data = {"cycle": 1, "live_count": len(products), "healthy_count": len(products), "products": products}
    p = tmp_path / "STATE_SUMMARY.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


class TestCategorizeProduct:
    def test_cron_category(self):
        cats = categorize_product(_product(n="Cron Expression Builder", s="cron-expr"))
        assert "cron" in cats

    def test_jwt_category(self):
        cats = categorize_product(_product(n="JWT Debugger Pro", s="jwt-debugger"))
        assert "jwt" in cats

    def test_multiple_categories(self):
        cats = categorize_product(_product(n="JSON to CSV Converter", s="json-csv"))
        assert "json" in cats
        assert "csv" in cats

    def test_unknown_goes_to_other(self):
        cats = categorize_product(_product(n="Foobar", s="foobar"))
        assert cats == ["other"]

    def test_toml_variants(self):
        for slug in ["toml-toolkit", "toml-validator", "toml-parser"]:
            cats = categorize_product(_product(s=slug))
            assert "toml" in cats

    def test_docker_category(self):
        cats = categorize_product(_product(s="docker-compose-generator"))
        assert "docker" in cats

    def test_html_category(self):
        cats = categorize_product(_product(s="html-beautifier"))
        assert "html" in cats

    def test_security_category(self):
        cats = categorize_product(_product(s="password-strength-checker"))
        assert "security" in cats


class TestBuildCategoryMap:
    def test_groups_by_category(self):
        products = [
            _product(s="cron-a", n="Cron Alpha"),
            _product(s="cron-b", n="Cron Beta"),
            _product(s="jwt-x", n="JWT X"),
        ]
        cat_map = build_category_map(products)
        assert "cron" in cat_map
        assert len(cat_map["cron"]) == 2
        assert "jwt" in cat_map

    def test_empty_products(self):
        cat_map = build_category_map([])
        assert cat_map == {}


class TestFindOverlapCategories:
    def test_threshold_default(self):
        cat_map = {
            "cron": [{"slug": f"cron-{i}"} for i in range(4)],
            "jwt": [{"slug": "jwt-1"}],
        }
        overlaps = find_overlap_categories(cat_map, threshold=3)
        assert len(overlaps) == 1
        assert overlaps[0]["category"] == "cron"
        assert overlaps[0]["count"] == 4

    def test_no_overlaps(self):
        cat_map = {"jwt": [{"slug": "jwt-1"}], "svg": [{"slug": "svg-1"}]}
        overlaps = find_overlap_categories(cat_map, threshold=3)
        assert overlaps == []


class TestFindSharedCheckout:
    def test_detects_shared(self):
        products = [
            _product(s="a", c="https://buy.polar.sh/shared"),
            _product(s="b", c="https://buy.polar.sh/shared"),
            _product(s="c", c="https://buy.polar.sh/unique"),
        ]
        shared = find_shared_checkout(products)
        assert len(shared) == 1
        assert shared[0]["count"] == 2
        assert "a" in shared[0]["slugs"]
        assert "b" in shared[0]["slugs"]

    def test_no_shared(self):
        products = [
            _product(s="a", c="https://buy.polar.sh/a"),
            _product(s="b", c="https://buy.polar.sh/b"),
        ]
        shared = find_shared_checkout(products)
        assert shared == []

    def test_skips_empty_checkout(self):
        products = [
            _product(s="a", c=""),
            _product(s="b", c=""),
        ]
        shared = find_shared_checkout(products)
        assert shared == []


class TestConsolidationReport:
    def test_report_structure(self):
        products = [
            _product(s="cron-1", n="Cron One", c="https://buy.polar.sh/c1"),
            _product(s="cron-2", n="Cron Two", c="https://buy.polar.sh/c2"),
            _product(s="cron-3", n="Cron Three", c="https://buy.polar.sh/c3"),
            _product(s="jwt-1", n="JWT One", c="https://buy.polar.sh/j1"),
            _product(s="jwt-2", n="JWT Two", c="https://buy.polar.sh/j1"),
        ]
        report = consolidation_report(products=products)
        assert report["total_unique_products"] == 5
        assert report["total_categories"] > 0
        assert report["shared_checkout_groups"] == 1
        assert report["shared_checkout_products"] == 2
        assert "cron" in report["categories"]
        assert report["categories"]["cron"] >= 3


class TestReportMarkdown:
    def test_generates_markdown(self):
        report = {
            "total_unique_products": 10,
            "total_categories": 5,
            "overlaps": [],
            "shared_checkout_groups": 0,
            "shared_checkout_products": 0,
            "categories": {"jwt": 3, "cron": 4, "html": 2, "css": 1},
            "shared_checkout_details": [],
        }
        md = report_markdown(report)
        assert "# Product Category Map" in md
        assert "jwt" in md
        assert "cron" in md
        assert "OVERLAP" in md

    def test_with_shared_checkout(self):
        report = {
            "total_unique_products": 3,
            "total_categories": 2,
            "overlaps": [],
            "shared_checkout_groups": 1,
            "shared_checkout_products": 2,
            "categories": {"jwt": 2, "cron": 1},
            "shared_checkout_details": [{"checkout_url": "https://buy.polar.sh/x", "count": 2, "slugs": ["a", "b"]}],
        }
        md = report_markdown(report)
        assert "Shared Checkout URLs" in md
        assert "a" in md
