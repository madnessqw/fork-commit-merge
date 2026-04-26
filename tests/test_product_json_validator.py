import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.product_json_validator import (
    REQUIRED_LIVE,
    URL_FIELDS,
    VALID_STATUSES,
    _load_product,
    _validate_price,
    _validate_slug,
    _validate_url,
    validate_all,
    validate_product,
)


def _make_product(**overrides):
    base = {
        "name": "Test Product",
        "slug": "test-product",
        "status": "live",
        "price": "9",
        "vercel_url": "https://test-product.vercel.app",
        "checkout_url": "https://buy.polar.sh/polar_cl_ABC123xyz",
        "github_url": "https://github.com/test/test-product",
        "payment_provider": "polar",
        "polar_product_id": "id-123",
    }
    base.update(overrides)
    return base


class TestValidateUrl:
    def test_checkout_url_valid(self):
        assert _validate_url("https://buy.polar.sh/polar_cl_ABC123xyz", "checkout_url") == []

    def test_checkout_url_invalid(self):
        issues = _validate_url("https://example.com/pay", "checkout_url")
        assert len(issues) == 1
        assert "format mismatch" in issues[0]

    def test_vercel_url_valid(self):
        assert _validate_url("https://my-app.vercel.app", "vercel_url") == []

    def test_vercel_url_invalid(self):
        issues = _validate_url("https://example.com", "vercel_url")
        assert len(issues) == 1

    def test_github_url_valid(self):
        assert _validate_url("https://github.com/org/repo", "github_url") == []

    def test_github_url_invalid(self):
        issues = _validate_url("https://gitlab.com/org/repo", "github_url")
        assert len(issues) == 1

    def test_none_value(self):
        assert _validate_url(None, "vercel_url") == []

    def test_empty_string(self):
        assert _validate_url("", "vercel_url") == []


class TestValidatePrice:
    def test_valid_integer(self):
        assert _validate_price("9") == []

    def test_valid_decimal(self):
        assert _validate_price("19.99") == []

    def test_valid_int_type(self):
        assert _validate_price(9) == []

    def test_zero_price(self):
        issues = _validate_price("0")
        assert any("positive" in i for i in issues)

    def test_negative_price(self):
        issues = _validate_price("-5")
        assert len(issues) > 0

    def test_text_price(self):
        issues = _validate_price("free")
        assert len(issues) > 0

    def test_high_price(self):
        issues = _validate_price("9999")
        assert any("suspiciously high" in i for i in issues)

    def test_none_price(self):
        issues = _validate_price(None)
        assert any("missing" in i for i in issues)


class TestValidateSlug:
    def test_valid_slug(self):
        assert _validate_slug("my-product", "my-product") == []

    def test_slug_dir_mismatch(self):
        issues = _validate_slug("my-product", "different-dir")
        assert any("mismatch" in i for i in issues)

    def test_none_slug(self):
        issues = _validate_slug(None, "dir")
        assert any("missing" in i for i in issues)

    def test_single_char_slug(self):
        assert _validate_slug("a", "a") == []

    def test_numeric_slug(self):
        assert _validate_slug("v2-tool", "v2-tool") == []


class TestValidateProduct:
    def test_valid_live_product(self):
        data = _make_product()
        result = validate_product(data, "test-product")
        assert result["valid"] is True
        assert result["status"] == "live"

    def test_valid_building_product(self):
        data = {"name": "Test", "slug": "test", "status": "building"}
        result = validate_product(data, "test")
        assert result["valid"] is True
        assert result["status"] == "building"

    def test_live_missing_required(self):
        data = {"name": "Test", "slug": "test", "status": "live"}
        result = validate_product(data, "test")
        assert result["valid"] is False
        assert any("price" in e for e in result["errors"])
        assert any("vercel_url" in e for e in result["errors"])
        assert any("checkout_url" in e for e in result["errors"])

    def test_invalid_status(self):
        data = {"name": "Test", "slug": "test", "status": "borked"}
        result = validate_product(data, "test")
        assert result["valid"] is False
        assert any("invalid status" in e for e in result["errors"])

    def test_optional_fields_warnings(self):
        data = _make_product(description="A tool", features=["f1"])
        del data["description"]
        del data["features"]
        result = validate_product(data, "test-product")
        assert result["valid"] is True
        assert any("description" in w for w in result["warnings"])

    def test_invalid_payment_provider(self):
        data = _make_product(payment_provider="unknown_provider")
        result = validate_product(data, "test-product")
        assert result["valid"] is False
        assert any("payment_provider" in e for e in result["errors"])

    def test_slug_mismatch_error(self):
        data = _make_product(slug="wrong-slug")
        result = validate_product(data, "test-product")
        assert result["valid"] is False
        assert any("mismatch" in e for e in result["errors"])


class TestLoadProduct:
    def test_valid_json(self, tmp_path):
        p = tmp_path / "product.json"
        p.write_text('{"name": "Test"}')
        result = _load_product(p)
        assert result == {"name": "Test"}

    def test_invalid_json(self, tmp_path):
        p = tmp_path / "product.json"
        p.write_text("{invalid json")
        result = _load_product(p)
        assert result is None

    def test_missing_file(self, tmp_path):
        p = tmp_path / "nonexistent.json"
        result = _load_product(p)
        assert result is None


class TestValidateAll:
    def test_empty_products_dir(self, tmp_path):
        with patch("scripts.product_json_validator.PRODUCTS_DIR", tmp_path):
            report = validate_all()
            assert report["total"] == 0

    def test_single_valid_product(self, tmp_path):
        prod_dir = tmp_path / "test-product"
        prod_dir.mkdir()
        (prod_dir / "product.json").write_text(json.dumps(_make_product()))
        with patch("scripts.product_json_validator.PRODUCTS_DIR", tmp_path):
            report = validate_all()
            assert report["total"] == 1
            assert report["valid"] == 1
            assert report["invalid"] == 0

    def test_single_invalid_product(self, tmp_path):
        prod_dir = tmp_path / "bad-product"
        prod_dir.mkdir()
        (prod_dir / "product.json").write_text(json.dumps({"status": "live"}))
        with patch("scripts.product_json_validator.PRODUCTS_DIR", tmp_path):
            report = validate_all()
            assert report["total"] == 1
            assert report["invalid"] == 1

    def test_status_filter(self, tmp_path):
        for slug, status in [("live-prod", "live"), ("build-prod", "building")]:
            d = tmp_path / slug
            d.mkdir()
            data = _make_product(slug=slug, status=status)
            if status != "live":
                data.pop("vercel_url", None)
                data.pop("checkout_url", None)
                data.pop("price", None)
            (d / "product.json").write_text(json.dumps(data))
        with patch("scripts.product_json_validator.PRODUCTS_DIR", tmp_path):
            report = validate_all(status_filter="live")
            assert report["total"] == 1

    def test_unreadable_json(self, tmp_path):
        prod_dir = tmp_path / "broken"
        prod_dir.mkdir()
        (prod_dir / "product.json").write_text("{bad json")
        with patch("scripts.product_json_validator.PRODUCTS_DIR", tmp_path):
            report = validate_all()
            assert report["total"] == 1
            assert report["invalid"] == 1
            assert any("unreadable" in e for e in report["results"][0]["errors"])

    def test_summary_cross_reference(self, tmp_path):
        prod_dir = tmp_path / "test-product"
        prod_dir.mkdir()
        (prod_dir / "product.json").write_text(json.dumps(_make_product()))
        summary = {"products": [{"s": "test-product", "st": "building", "v": "https://other.vercel.app", "c": "https://other.checkout"}]}
        summary_path = tmp_path / "STATE_SUMMARY.json"
        summary_path.write_text(json.dumps(summary))
        with (
            patch("scripts.product_json_validator.PRODUCTS_DIR", tmp_path),
            patch("scripts.product_json_validator.STATE_SUMMARY_PATH", summary_path),
        ):
            report = validate_all()
            warned = report["warned_products"]
            assert len(warned) > 0
            msgs = [w for p in warned for w in p["warnings"]]
            assert any("status mismatch" in m for m in msgs)

    def test_mixed_products(self, tmp_path):
        for i, status in enumerate(["live", "building", "live"]):
            d = tmp_path / f"prod-{i}"
            d.mkdir()
            data = _make_product(slug=f"prod-{i}", status=status)
            if status != "live":
                data.pop("vercel_url", None)
                data.pop("checkout_url", None)
                data.pop("price", None)
            (d / "product.json").write_text(json.dumps(data))
        with patch("scripts.product_json_validator.PRODUCTS_DIR", tmp_path):
            report = validate_all()
            assert report["total"] == 3
            assert report["status_counts"]["live"] == 2
            assert report["status_counts"]["building"] == 1
