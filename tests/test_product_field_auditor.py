"""Tests for product_field_auditor.py"""

from __future__ import annotations

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from scripts.product_field_auditor import (
    audit_slug,
    find_all_slugs,
    load_product,
    run_audit,
    format_markdown,
    REQUIRED_FIELDS,
    URL_FIELDS,
    VALID_STATUSES,
)

PRODUCTS_DIR = Path(__file__).resolve().parents[1] / "products"


def _make_product(slug: str = "test-product", **overrides) -> dict:
    base = {
        "name": "Test Product",
        "slug": slug,
        "tagline": "A test product",
        "description": "Test description",
        "price": "$29",
        "features": ["feature1", "feature2"],
        "tech_stack": "Vercel",
        "status": "live",
        "vercel_url": "https://test-product.vercel.app",
        "github_url": "https://github.com/test/test-product",
        "checkout_url": "https://buy.polar.sh/test",
    }
    base.update(overrides)
    return base


class TestLoadProduct:
    def test_load_existing(self, tmp_path):
        p = tmp_path / "my-prod" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps({"name": "My Prod", "slug": "my-prod"}))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = load_product("my-prod")
        assert result is not None
        assert result["slug"] == "my-prod"

    def test_load_missing(self, tmp_path):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = load_product("nonexistent")
        assert result is None

    def test_load_invalid_json(self, tmp_path):
        p = tmp_path / "bad-prod" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text("{invalid json")
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = load_product("bad-prod")
        assert result is None


class TestFindAllSlugs:
    def test_empty_dir(self, tmp_path):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            slugs = find_all_slugs()
        assert slugs == []

    def test_finds_products(self, tmp_path):
        for slug in ["alpha", "beta", "gamma"]:
            p = tmp_path / slug / "product.json"
            p.parent.mkdir(parents=True)
            p.write_text("{}")
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            slugs = find_all_slugs()
        assert slugs == ["alpha", "beta", "gamma"]

    def test_ignores_dirs_without_product_json(self, tmp_path):
        (tmp_path / "nope").mkdir()
        p = tmp_path / "yes" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text("{}")
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            slugs = find_all_slugs()
        assert slugs == ["yes"]


class TestAuditSlug:
    def test_perfect_product(self, tmp_path):
        data = _make_product()
        p = tmp_path / "test-product" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("test-product")
        assert result["score"] == 100
        assert result["issues"] == []

    def test_missing_product_json(self, tmp_path):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("nonexistent")
        assert result["score"] == 0
        assert any(i["problem"] == "missing_or_unreadable" for i in result["issues"])

    def test_missing_required_field(self, tmp_path):
        data = _make_product()
        del data["tagline"]
        p = tmp_path / "test-product" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("test-product")
        assert result["score"] < 100
        assert any(i["field"] == "tagline" and i["problem"] == "missing" for i in result["issues"])

    def test_empty_string_field(self, tmp_path):
        data = _make_product(description="")
        p = tmp_path / "test-product" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("test-product")
        assert any(i["field"] == "description" and i["problem"] == "empty" for i in result["issues"])

    def test_empty_features_list(self, tmp_path):
        data = _make_product(features=[])
        p = tmp_path / "test-product" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("test-product")
        assert any(i["field"] == "features" and i["problem"] == "empty_list" for i in result["issues"])

    def test_invalid_url(self, tmp_path):
        data = _make_product(vercel_url="not-a-url")
        p = tmp_path / "test-product" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("test-product")
        assert any(i["field"] == "vercel_url" and i["problem"] == "invalid_url" for i in result["issues"])

    def test_slug_mismatch(self, tmp_path):
        data = _make_product(slug="wrong-slug")
        p = tmp_path / "test-product" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("test-product")
        assert any(i["field"] == "slug" and i["problem"] == "mismatch" for i in result["issues"])

    def test_invalid_status(self, tmp_path):
        data = _make_product(status="bogus")
        p = tmp_path / "test-product" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("test-product")
        assert any(i["field"] == "status" and i["problem"] == "invalid_status" for i in result["issues"])

    def test_price_no_digits(self, tmp_path):
        data = _make_product(price="FREE")
        p = tmp_path / "test-product" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("test-product")
        assert any(i["field"] == "price" and i["problem"] == "no_numeric_value" for i in result["issues"])

    def test_valid_statuses(self, tmp_path):
        for status in VALID_STATUSES:
            data = _make_product(status=status)
            p = tmp_path / f"prod-{status}" / "product.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps(data))
            with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
                result = audit_slug(f"prod-{status}")
            assert not any(i["field"] == "status" for i in result["issues"]), f"status={status} flagged"

    def test_score_never_negative(self, tmp_path):
        data = {"slug": "empty"}
        p = tmp_path / "empty" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            result = audit_slug("empty")
        assert result["score"] >= 0


class TestRunAudit:
    def test_full_portfolio(self, tmp_path):
        for slug in ["aaa", "bbb"]:
            data = _make_product(slug=slug)
            p = tmp_path / slug / "product.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            report = run_audit()
        assert report["total_products"] == 2
        assert report["perfect_count"] == 2
        assert report["average_score"] == 100.0

    def test_single_slug(self, tmp_path):
        data = _make_product(slug="target")
        p = tmp_path / "target" / "product.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(data))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            report = run_audit("target")
        assert report["total_products"] == 1
        assert report["perfect_count"] == 1

    def test_empty_portfolio(self, tmp_path):
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            report = run_audit()
        assert report["total_products"] == 0
        assert report["average_score"] == 0

    def test_mixed_quality(self, tmp_path):
        good = _make_product(slug="good")
        bad_data = {"name": "Bad"}
        for slug, d in [("good", good), ("bad", bad_data)]:
            p = tmp_path / slug / "product.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps(d))
        with patch("scripts.product_field_auditor.PRODUCTS_DIR", tmp_path):
            report = run_audit()
        assert report["perfect_count"] == 1
        assert len(report["products_with_issues"]) == 1
        assert report["average_score"] < 100


class TestFormatMarkdown:
    def test_basic_format(self):
        report = {
            "timestamp": "2026-04-26T16:00:00Z",
            "total_products": 5,
            "perfect_count": 3,
            "average_score": 85.0,
            "issue_summary": {"missing": 2},
            "field_issues": {"tagline": 2},
            "products_with_issues": [
                {"slug": "bad-prod", "score": 60, "issues": [{"field": "tagline", "problem": "missing"}]}
            ],
        }
        md = format_markdown(report)
        assert "# Product Field Audit" in md
        assert "5" in md
        assert "bad-prod" in md

    def test_no_issues(self):
        report = {
            "timestamp": "2026-04-26T16:00:00Z",
            "total_products": 3,
            "perfect_count": 3,
            "average_score": 100.0,
            "issue_summary": {},
            "field_issues": {},
            "products_with_issues": [],
        }
        md = format_markdown(report)
        assert "3" in md
        assert "100.0" in md


class TestRealPortfolio:
    def test_audit_all_products(self):
        if not PRODUCTS_DIR.exists():
            pytest.skip("No products directory")
        report = run_audit()
        assert report["total_products"] > 0
        assert report["average_score"] >= 0

    def test_audit_specific_slug(self):
        first_slug = "uuid-generator-pro"
        p = PRODUCTS_DIR / first_slug / "product.json"
        if not p.exists():
            pytest.skip("uuid-generator-pro not found")
        report = run_audit(first_slug)
        assert report["total_products"] == 1
        assert report["products_with_issues"] == [] or report["average_score"] > 50
