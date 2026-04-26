"""Tests for checkout_link_validator.

Validates URL format checking, Polar ID extraction, portfolio validation,
and health score computation.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from scripts.checkout_link_validator import (
    POLAR_URL_PATTERN,
    extract_polar_id,
    health_score,
    validate_portfolio,
    validate_url_format,
)

VALID_URL = "https://buy.polar.sh/polar_cl_LITjFT1XdMD9kD9nw1Gbxr4YV5la5dYdbKY5x1TPXq2"
VALID_ID = "polar_cl_LITjFT1XdMD9kD9nw1Gbxr4YV5la5dYdbKY5x1TPXq2"


def _make_summary(tmp_path: Path, products: list[dict]) -> Path:
    p = tmp_path / "STATE_SUMMARY.json"
    p.write_text(json.dumps({"products": products}), encoding="utf-8")
    return p


class TestExtractPolarId:
    def test_valid_url(self):
        assert extract_polar_id(VALID_URL) == VALID_ID

    def test_no_id(self):
        assert extract_polar_id("https://example.com/foo") is None

    def test_embedded_id(self):
        url = "https://other.polar.sh/checkout/polar_cl_AbCd1234EfGh"
        assert extract_polar_id(url) == "polar_cl_AbCd1234EfGh"

    def test_empty_string(self):
        assert extract_polar_id("") is None


class TestValidateUrlFormat:
    def test_valid_polar_url(self):
        result = validate_url_format(VALID_URL)
        assert result["valid"] is True
        assert result["issues"] == []
        assert result["polar_id"] == VALID_ID

    def test_empty_url(self):
        result = validate_url_format("")
        assert result["valid"] is False
        assert "missing" in result["issues"]

    def test_http_not_https(self):
        url = "http://buy.polar.sh/polar_cl_AbCd1234EfGh5678"
        result = validate_url_format(url)
        assert result["valid"] is False
        assert "not_https" in result["issues"]

    def test_wrong_domain(self):
        url = "https://example.com/polar_cl_AbCd1234EfGh5678"
        result = validate_url_format(url)
        assert result["valid"] is False
        assert "not_polar_domain" in result["issues"]

    def test_no_polar_id(self):
        url = "https://buy.polar.sh/some_other_path"
        result = validate_url_format(url)
        assert result["valid"] is False
        assert "no_polar_id" in result["issues"]


class TestValidatePortfolio:
    def test_all_valid(self, tmp_path):
        products = [
            {"n": "Product A", "s": "product-a", "st": "live",
             "c": "https://buy.polar.sh/polar_cl_AAAA1111BBBB2222CCCC"},
            {"n": "Product B", "s": "product-b", "st": "live",
             "c": "https://buy.polar.sh/polar_cl_DDDD3333EEEE4444FFFF"},
        ]
        p = _make_summary(tmp_path, products)
        report = validate_portfolio(p)
        assert report["total"] == 2
        assert report["valid"] == 2
        assert report["invalid"] == 0
        assert report["missing"] == 0
        assert report["duplicate_id_count"] == 0

    def test_missing_checkout(self, tmp_path):
        products = [
            {"n": "No Checkout", "s": "no-checkout", "st": "live", "c": ""},
        ]
        p = _make_summary(tmp_path, products)
        report = validate_portfolio(p)
        assert report["missing"] == 1
        assert report["valid"] == 0

    def test_invalid_url(self, tmp_path):
        products = [
            {"n": "Bad URL", "s": "bad-url", "st": "live",
             "c": "https://example.com/not-polar"},
        ]
        p = _make_summary(tmp_path, products)
        report = validate_portfolio(p)
        assert report["invalid"] == 1

    def test_duplicate_ids(self, tmp_path):
        url = "https://buy.polar.sh/polar_cl_SAMEID111111111111111111"
        products = [
            {"n": "A", "s": "a", "st": "live", "c": url},
            {"n": "B", "s": "b", "st": "live", "c": url},
        ]
        p = _make_summary(tmp_path, products)
        report = validate_portfolio(p)
        assert report["duplicate_id_count"] == 1
        assert "polar_cl_SAMEID111111111111111111" in report["duplicate_ids"]

    def test_live_missing_checkout(self, tmp_path):
        products = [
            {"n": "Live No CO", "s": "live-no-co", "st": "live", "c": ""},
            {"n": "Draft No CO", "s": "draft-no-co", "st": "draft", "c": ""},
        ]
        p = _make_summary(tmp_path, products)
        report = validate_portfolio(p)
        assert report["live_missing_checkout"] == 1

    def test_missing_file(self, tmp_path):
        p = tmp_path / "nonexistent.json"
        report = validate_portfolio(p)
        assert report["total"] == 0
        assert len(report["issues"]) > 0

    def test_invalid_json(self, tmp_path):
        p = tmp_path / "STATE_SUMMARY.json"
        p.write_text("not json{{{", encoding="utf-8")
        report = validate_portfolio(p)
        assert report["total"] == 0

    def test_products_not_list(self, tmp_path):
        p = tmp_path / "STATE_SUMMARY.json"
        p.write_text(json.dumps({"products": "oops"}), encoding="utf-8")
        report = validate_portfolio(p)
        assert report["total"] == 0


class TestHealthScore:
    def test_perfect_score(self, tmp_path):
        products = [
            {"n": "A", "s": "a", "st": "live",
             "c": "https://buy.polar.sh/polar_cl_AAAA1111BBBB2222CCCC"},
            {"n": "B", "s": "b", "st": "live",
             "c": "https://buy.polar.sh/polar_cl_DDDD3333EEEE4444FFFF"},
        ]
        p = _make_summary(tmp_path, products)
        result = health_score(p)
        assert result["score"] >= 90
        assert result["grade"] in ("A+", "A")

    def test_missing_penalty(self, tmp_path):
        products = [
            {"n": "A", "s": "a", "st": "live", "c": ""},
        ]
        p = _make_summary(tmp_path, products)
        result = health_score(p)
        assert result["score"] < 50

    def test_empty_portfolio(self, tmp_path):
        p = _make_summary(tmp_path, [])
        result = health_score(p)
        assert result["score"] == 0
        assert result["grade"] == "F"

    def test_no_products_file(self, tmp_path):
        p = tmp_path / "nonexistent.json"
        result = health_score(p)
        assert result["score"] == 0
