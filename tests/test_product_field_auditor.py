import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.product_field_auditor import (
    REQUIRED_FIELDS,
    RECOMMENDED_FIELDS,
    audit_products,
    fix_products,
    generate_report,
    get_all_slugs,
    load_product,
    save_product,
)


@pytest.fixture
def temp_products(tmp_path):
    products_dir = tmp_path / "products"
    products_dir.mkdir()

    full_product = {
        "name": "Full Product",
        "slug": "full-product",
        "tagline": "A complete product",
        "description": "Full description",
        "price": "9",
        "features": ["feat1", "feat2"],
        "tech_stack": "Vercel",
        "status": "live",
        "vercel_url": "https://full-product.vercel.app",
        "checkout_url": "https://buy.polar.sh/test",
        "github_url": "https://github.com/test/full-product",
        "created_cycle": 100,
        "deployed_cycle": 110,
        "seo_optimized": True,
        "spec_version": "1.0",
        "payment_provider": "polar",
    }

    minimal_product = {
        "name": "Minimal",
        "slug": "minimal-product",
        "status": "live",
    }

    empty_fields_product = {
        "name": "Empty Fields",
        "slug": "empty-fields",
        "tagline": "",
        "description": "",
        "features": [],
        "status": "active",
    }

    for slug, data in [
        ("full-product", full_product),
        ("minimal-product", minimal_product),
        ("empty-fields", empty_fields_product),
    ]:
        pdir = products_dir / slug
        pdir.mkdir()
        (pdir / "product.json").write_text(json.dumps(data, indent=2))

    return products_dir


class TestLoadProduct:
    def test_load_existing(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            result = load_product("full-product")
        assert result is not None
        assert result["name"] == "Full Product"

    def test_load_missing(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            result = load_product("nonexistent")
        assert result is None

    def test_load_invalid_json(self, temp_products):
        bad_dir = temp_products / "bad-json"
        bad_dir.mkdir()
        (bad_dir / "product.json").write_text("{invalid}")
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            result = load_product("bad-json")
        assert result is None


class TestGetAllSlugs:
    def test_returns_slugs(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            slugs = get_all_slugs()
        assert "full-product" in slugs
        assert "minimal-product" in slugs
        assert "empty-fields" in slugs

    def test_excludes_dirs_without_product_json(self, temp_products):
        nodir = temp_products / "no-product"
        nodir.mkdir()
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            slugs = get_all_slugs()
        assert "no-product" not in slugs


class TestAuditProducts:
    def test_full_product_high_score(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            results = audit_products(["full-product"])
        score_info = results["product_scores"]["full-product"]
        assert score_info["score"] >= 90
        assert len(score_info["missing"]) == 0

    def test_minimal_product_low_score(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            results = audit_products(["minimal-product"])
        score_info = results["product_scores"]["minimal-product"]
        assert score_info["score"] < 50
        assert "tagline" in score_info["missing"]
        assert "description" in score_info["missing"]

    def test_empty_fields_detected(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            results = audit_products(["empty-fields"])
        score_info = results["product_scores"]["empty-fields"]
        assert "tagline" in score_info["empty"]
        assert "features" in score_info["empty"]

    def test_field_gaps_populated(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            results = audit_products()
        assert "tagline" in results["field_gaps"]
        assert "minimal-product" in results["field_gaps"]["tagline"]

    def test_total_count(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            results = audit_products()
        assert results["total"] == 3


class TestFixProducts:
    def test_fix_slug_from_dir(self, temp_products):
        data = {"name": "Test"}
        slug_dir = temp_products / "test-slug"
        slug_dir.mkdir(exist_ok=True)
        (slug_dir / "product.json").write_text(json.dumps(data))

        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            result = fix_products(["test-slug"], dry_run=True)
        assert result["fixed"] == 1
        assert "test-slug" in result["products"]

    def test_fix_status_live_when_vercel_url(self, temp_products):
        data = {"name": "Test", "vercel_url": "https://test.vercel.app"}
        slug_dir = temp_products / "auto-status"
        slug_dir.mkdir(exist_ok=True)
        (slug_dir / "product.json").write_text(json.dumps(data))

        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            fix_products(["auto-status"], dry_run=False)
            product = json.loads((slug_dir / "product.json").read_text())
        assert product["status"] == "live"

    def test_fix_polar_provider(self, temp_products):
        data = {"name": "Test", "checkout_url": "https://buy.polar.sh/test"}
        slug_dir = temp_products / "auto-polar"
        slug_dir.mkdir(exist_ok=True)
        (slug_dir / "product.json").write_text(json.dumps(data))

        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            fix_products(["auto-polar"], dry_run=False)
            product = json.loads((slug_dir / "product.json").read_text())
        assert product["payment_provider"] == "polar"

    def test_dry_run_no_write(self, temp_products):
        original = {"name": "Test"}
        slug_dir = temp_products / "dry-test"
        slug_dir.mkdir(exist_ok=True)
        (slug_dir / "product.json").write_text(json.dumps(original))

        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            fix_products(["dry-test"], dry_run=True)
            product = json.loads((slug_dir / "product.json").read_text())
        assert "slug" not in product

    def test_fix_name_from_slug(self, temp_products):
        data = {"status": "live"}
        slug_dir = temp_products / "my-cool-tool"
        slug_dir.mkdir(exist_ok=True)
        (slug_dir / "product.json").write_text(json.dumps(data))

        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            fix_products(["my-cool-tool"], dry_run=False)
            product = json.loads((slug_dir / "product.json").read_text())
        assert product["name"] == "My Cool Tool"


class TestGenerateReport:
    def test_report_includes_summary(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            results = audit_products()
        report = generate_report(results)
        assert "Product Field Coverage Report" in report
        assert "Summary" in report
        assert "Average coverage" in report

    def test_report_shows_field_gaps(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            results = audit_products()
        report = generate_report(results)
        assert "tagline" in report

    def test_report_shows_lowest_products(self, temp_products):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", temp_products):
            results = audit_products()
        report = generate_report(results)
        assert "Lowest Coverage" in report

    def test_empty_products(self):
        report = generate_report({"total": 0, "field_gaps": {}, "product_scores": {}, "empty_fields": {}})
        assert "No products found" in report
