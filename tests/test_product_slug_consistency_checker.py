"""Tests for product_slug_consistency_checker."""

from __future__ import annotations

import json
import pytest
from scripts.product_slug_consistency_checker import (
    check_slug_format,
    check_name_slug_match,
    analyze,
    _slugify,
    _similarity,
)


class TestCheckSlugFormat:
    def test_valid_slug(self):
        assert check_slug_format("uuid-generator-pro") == []

    def test_valid_simple_slug(self):
        assert check_slug_format("keyforge") == []

    def test_valid_numeric_slug(self):
        assert check_slug_format("base64-pro") == []

    def test_empty_slug(self):
        assert "empty_slug" in check_slug_format("")

    def test_dangling_dash_start(self):
        assert "dangling_dash" in check_slug_format("-starts-dash")

    def test_dangling_dash_end(self):
        assert "dangling_dash" in check_slug_format("ends-dash-")

    def test_double_dash(self):
        assert "double_dash" in check_slug_format("has--double")

    def test_too_short(self):
        assert "too_short" in check_slug_format("ab")

    def test_too_long(self):
        long_slug = "a" * 61
        assert "too_long" in check_slug_format(long_slug)

    def test_uppercase_chars(self):
        assert "uppercase_chars" in check_slug_format("UUID-Generator")

    def test_underscore_separator(self):
        assert "underscore_separator" in check_slug_format("uuid_generator")

    def test_invalid_chars_spaces(self):
        assert "invalid_chars" in check_slug_format("has space")

    def test_multiple_issues(self):
        issues = check_slug_format("A_B")
        assert "uppercase_chars" in issues
        assert "underscore_separator" in issues


class TestSlugify:
    def test_simple_name(self):
        assert _slugify("UUID Generator Pro") == "uuid-generator-pro"

    def test_special_chars(self):
        assert _slugify("HTML Beautifier/Minifier") == "html-beautifier-minifier"

    def test_unicode(self):
        result = _slugify("Ünïcödé Tööl")
        assert all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in result)

    def test_leading_trailing_spaces(self):
        assert _slugify("  spaced  ") == "spaced"


class TestSimilarity:
    def test_identical(self):
        assert _similarity("abc", "abc") == 1.0

    def test_completely_different(self):
        assert _similarity("abc", "xyz") == 0.0

    def test_empty_both(self):
        assert _similarity("", "") == 1.0

    def test_empty_one(self):
        assert _similarity("abc", "") == 0.0

    def test_partial(self):
        score = _similarity("abc", "abd")
        assert 0.0 < score < 1.0


class TestCheckNameSlugMatch:
    def test_perfect_match(self):
        result = check_name_slug_match("UUID Generator Pro", "uuid-generator-pro")
        assert result["match_score"] >= 0.8
        assert not result["mismatch"]

    def test_mismatch(self):
        result = check_name_slug_match("Hash Generator Pro", "something-else")
        assert result["mismatch"]

    def test_expected_slug(self):
        result = check_name_slug_match("KeyForge", "keyforge")
        assert result["expected"] == "keyforge"


class TestAnalyze:
    def test_empty_portfolio(self):
        result = analyze([])
        assert result["total_products"] == 0
        assert result["format_issue_count"] == 0
        assert result["name_mismatch_count"] == 0
        assert result["consistency_score"] == 100.0

    def test_clean_portfolio(self):
        products = [
            {"n": "UUID Generator Pro", "s": "uuid-generator-pro"},
            {"n": "URL Forge", "s": "url-forge"},
            {"n": "KeyForge", "s": "keyforge"},
        ]
        result = analyze(products)
        assert result["total_products"] == 3
        assert result["format_issue_count"] == 0
        assert result["consistency_score"] == 100.0

    def test_format_issues_detected(self):
        products = [
            {"n": "Bad One", "s": "BAD_SLUG"},
            {"n": "Good One", "s": "good-one"},
        ]
        result = analyze(products)
        assert result["format_issue_count"] >= 1

    def test_name_mismatch_detected(self):
        products = [
            {"n": "Completely Different Name", "s": "totally-unrelated"},
        ]
        result = analyze(products)
        assert result["name_mismatch_count"] == 1

    def test_duplicate_slugs_detected(self):
        products = [
            {"n": "Product A", "s": "same-slug"},
            {"n": "Product B", "s": "same-slug"},
        ]
        result = analyze(products)
        assert result["duplicate_slug_count"] == 1
        assert "same-slug" in result["duplicate_slugs"]

    def test_consistency_score_calculation(self):
        products = [
            {"n": "Good Product", "s": "good-product"},
            {"n": "Bad Product", "s": "BAD"},
        ]
        result = analyze(products)
        assert result["consistency_score"] == 50.0

    def test_missing_fields(self):
        products = [
            {"n": "", "s": ""},
        ]
        result = analyze(products)
        assert result["format_issue_count"] >= 1
