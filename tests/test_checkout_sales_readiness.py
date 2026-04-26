#!/usr/bin/env python3
"""Tests for checkout_sales_readiness.py — sales readiness scoring, audit,
summary, and fix-dry-run functionality."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_sales_readiness import (
    check_checkout_url,
    check_description,
    check_meta_description,
    check_meta_title,
    check_name,
    check_og_image,
    check_price,
    fix_dry_run,
    load_product_json,
    score_product,
    audit,
    summary,
    NAME_MIN_LENGTH,
    DESC_MIN_LENGTH,
    TITLE_MIN_LENGTH,
    META_DESC_MIN_LENGTH,
    READINESS_WEIGHTS,
)

PERFECT_PRODUCT = {
    "name": "Super Cool Developer Tool Pro",
    "description": "A very useful tool that helps developers write better code every day.",
    "short_description": "A very useful tool that helps developers write better code every day.",
    "price": "$19",
    "checkout_url": "https://buy.polar.sh/polar_cl_abc123",
    "og_image": "https://example.com/image.png",
    "meta_title": "Super Cool Developer Tool Pro - Best Tool",
    "meta_description": "The best developer tool for writing better code. Try it now for free and upgrade later.",
}

MINIMAL_PRODUCT = {
    "name": "X",
}


class TestCheckCheckoutUrl:
    def test_valid_polar_url(self):
        ok, detail = check_checkout_url({"checkout_url": "https://buy.polar.sh/polar_cl_abc"})
        assert ok is True
        assert detail == "ok"

    def test_missing_url(self):
        ok, detail = check_checkout_url({})
        assert ok is False
        assert detail == "missing"

    def test_empty_url(self):
        ok, detail = check_checkout_url({"checkout_url": ""})
        assert ok is False
        assert detail == "missing"

    def test_http_scheme(self):
        ok, detail = check_checkout_url({"checkout_url": "http://buy.polar.sh/abc"})
        assert ok is False
        assert detail == "invalid_scheme"

    def test_non_polar_url(self):
        ok, detail = check_checkout_url({"checkout_url": "https://example.com/buy"})
        assert ok is False
        assert detail == "non_polar"

    def test_polar_checkout_url_field(self):
        ok, detail = check_checkout_url({"polar_checkout_url": "https://buy.polar.sh/polar_cl_x"})
        assert ok is True

    def test_checkout_url_with_checkout_keyword(self):
        ok, detail = check_checkout_url({"checkout_url": "https://mystore.com/checkout/product1"})
        assert ok is True


class TestCheckName:
    def test_valid_name(self):
        ok, detail = check_name({"name": "Great Product Name"})
        assert ok is True

    def test_too_short(self):
        ok, detail = check_name({"name": "X"})
        assert ok is False
        assert detail == "too_short"

    def test_empty_name(self):
        ok, detail = check_name({"name": ""})
        assert ok is False

    def test_missing_name(self):
        ok, detail = check_name({})
        assert ok is False


class TestCheckDescription:
    def test_valid_description(self):
        ok, detail = check_description({"description": "A" * DESC_MIN_LENGTH})
        assert ok is True

    def test_short_description_field(self):
        ok, detail = check_description({"short_description": "A" * DESC_MIN_LENGTH})
        assert ok is True

    def test_too_short(self):
        ok, detail = check_description({"description": "short"})
        assert ok is False
        assert detail == "too_short"

    def test_empty(self):
        ok, detail = check_description({})
        assert ok is False


class TestCheckPrice:
    def test_valid_string_dollar(self):
        ok, detail = check_price({"price": "$19"})
        assert ok is True

    def test_valid_numeric(self):
        ok, detail = check_price({"price": 15})
        assert ok is True

    def test_zero_price(self):
        ok, detail = check_price({"price": 0})
        assert ok is False
        assert detail == "zero"

    def test_missing_price(self):
        ok, detail = check_price({})
        assert ok is False
        assert detail == "missing"

    def test_invalid_price(self):
        ok, detail = check_price({"price": "free"})
        assert ok is False
        assert detail == "invalid"

    def test_euro_price(self):
        ok, detail = check_price({"price": "€15"})
        assert ok is True


class TestCheckOgImage:
    def test_valid_url(self):
        ok, detail = check_og_image({"og_image": "https://example.com/img.png"})
        assert ok is True

    def test_image_field(self):
        ok, detail = check_og_image({"image": "https://example.com/img.png"})
        assert ok is True

    def test_missing(self):
        ok, detail = check_og_image({})
        assert ok is False
        assert detail == "missing"

    def test_relative_path(self):
        ok, detail = check_og_image({"og_image": "/img.png"})
        assert ok is False


class TestCheckMetaTitle:
    def test_valid(self):
        ok, detail = check_meta_title({"meta_title": "A" * TITLE_MIN_LENGTH})
        assert ok is True

    def test_title_fallback(self):
        ok, detail = check_meta_title({"title": "A" * TITLE_MIN_LENGTH})
        assert ok is True

    def test_too_short(self):
        ok, detail = check_meta_title({"meta_title": "short"})
        assert ok is False

    def test_empty(self):
        ok, detail = check_meta_title({})
        assert ok is False


class TestCheckMetaDescription:
    def test_valid(self):
        ok, detail = check_meta_description({"meta_description": "A" * META_DESC_MIN_LENGTH})
        assert ok is True

    def test_too_short(self):
        ok, detail = check_meta_description({"meta_description": "short"})
        assert ok is False

    def test_empty(self):
        ok, detail = check_meta_description({})
        assert ok is False


class TestScoreProduct:
    def test_perfect_score(self):
        score, issues = score_product(PERFECT_PRODUCT)
        assert score == 100
        assert len(issues) == 0

    def test_minimal_score(self):
        score, issues = score_product(MINIMAL_PRODUCT)
        assert score < 30
        assert len(issues) > 3

    def test_no_checkout_url(self):
        p = {**PERFECT_PRODUCT}
        del p["checkout_url"]
        score, issues = score_product(p)
        assert score < 100
        assert any("has_checkout_url" in i for i in issues)

    def test_weights_sum_100(self):
        assert sum(READINESS_WEIGHTS.values()) == 100

    def test_partial_product(self):
        p = {
            "name": "Good Product Name",
            "description": "A" * DESC_MIN_LENGTH,
            "price": "$10",
            "checkout_url": "https://buy.polar.sh/polar_cl_test",
        }
        score, issues = score_product(p)
        assert 40 <= score < 80
        assert any("has_og_image" in i for i in issues)


class TestLoadProductJson:
    def test_loads_valid(self, tmp_path):
        pdir = tmp_path / "products" / "test-prod"
        pdir.mkdir(parents=True)
        (pdir / "product.json").write_text(json.dumps({"name": "Test"}))
        with patch("scripts.checkout_sales_readiness.PRODUCTS_DIR", tmp_path / "products"):
            data = load_product_json("test-prod")
        assert data["name"] == "Test"

    def test_missing_dir(self, tmp_path):
        with patch("scripts.checkout_sales_readiness.PRODUCTS_DIR", tmp_path / "nonexistent"):
            data = load_product_json("missing")
        assert data is None

    def test_invalid_json(self, tmp_path):
        pdir = tmp_path / "products" / "bad-json"
        pdir.mkdir(parents=True)
        (pdir / "product.json").write_text("{invalid json}")
        with patch("scripts.checkout_sales_readiness.PRODUCTS_DIR", tmp_path / "products"):
            data = load_product_json("bad-json")
        assert data is None


class TestAudit:
    def test_audit_output(self, capsys, tmp_path):
        pdir = tmp_path / "products" / "ready-prod"
        pdir.mkdir(parents=True)
        (pdir / "product.json").write_text(json.dumps(PERFECT_PRODUCT))
        with patch("scripts.checkout_sales_readiness.PRODUCTS_DIR", tmp_path / "products"):
            results = audit()
        out = capsys.readouterr().out
        assert "Checkout Sales Readiness Audit" in out
        assert "Ready (80+)" in out
        assert len(results) == 1
        assert results[0]["score"] == 100

    def test_audit_no_products(self, capsys, tmp_path):
        empty = tmp_path / "empty_products"
        empty.mkdir()
        with patch("scripts.checkout_sales_readiness.PRODUCTS_DIR", empty):
            results = audit()
        assert results == []


class TestSummary:
    def test_summary_output(self, capsys, tmp_path):
        pdir = tmp_path / "products" / "prod1"
        pdir.mkdir(parents=True)
        (pdir / "product.json").write_text(json.dumps(PERFECT_PRODUCT))
        with patch("scripts.checkout_sales_readiness.PRODUCTS_DIR", tmp_path / "products"):
            summary()
        out = capsys.readouterr().out
        assert "Sales Readiness Summary" in out
        assert "Average readiness" in out


class TestFixDryRun:
    def test_fix_suggestions(self, capsys, tmp_path):
        pdir = tmp_path / "products" / "minimal-prod"
        pdir.mkdir(parents=True)
        (pdir / "product.json").write_text(json.dumps(MINIMAL_PRODUCT))
        with patch("scripts.checkout_sales_readiness.PRODUCTS_DIR", tmp_path / "products"):
            fixes = fix_dry_run()
        out = capsys.readouterr().out
        assert "Fix Dry Run" in out
        assert len(fixes) == 1
        assert any("price" in s for s in fixes[0]["suggestions"])

    def test_no_fixes_needed(self, capsys, tmp_path):
        pdir = tmp_path / "products" / "ready-prod"
        pdir.mkdir(parents=True)
        (pdir / "product.json").write_text(json.dumps(PERFECT_PRODUCT))
        with patch("scripts.checkout_sales_readiness.PRODUCTS_DIR", tmp_path / "products"):
            fixes = fix_dry_run()
        assert len(fixes) == 0
