"""Tests for scripts/price_audit.py"""

from __future__ import annotations

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from scripts.price_audit import (
    audit_product_prices,
    detect_price_format,
    format_price_dollars,
    parse_price,
)


class TestParsePrice:
    def test_integer_dollars(self):
        assert parse_price(9) == 900

    def test_integer_large(self):
        assert parse_price(2900) == 2900

    def test_float(self):
        assert parse_price(19.99) == 1999

    def test_string_integer(self):
        assert parse_price("19") == 1900

    def test_string_dollar_integer(self):
        assert parse_price("$19") == 1900

    def test_string_dollar_decimal(self):
        assert parse_price("$9.99") == 999

    def test_string_decimal(self):
        assert parse_price("29.00") == 2900

    def test_none(self):
        assert parse_price(None) is None

    def test_empty_string(self):
        assert parse_price("") is None

    def test_garbage(self):
        assert parse_price("free") is None

    def test_zero(self):
        assert parse_price(0) == 0

    def test_string_zero(self):
        assert parse_price("0") == 0


class TestFormatPriceDollars:
    def test_whole_dollar(self):
        assert format_price_dollars(900) == "$9"

    def test_decimal(self):
        assert format_price_dollars(999) == "$9.99"

    def test_zero(self):
        assert format_price_dollars(0) == "$0"

    def test_large(self):
        assert format_price_dollars(2900) == "$29"

    def test_forty_nine_cents(self):
        assert format_price_dollars(149) == "$1.49"


class TestDetectPriceFormat:
    def test_missing(self):
        assert detect_price_format(None) == "missing"

    def test_int_bare(self):
        assert detect_price_format(12) == "int_bare"

    def test_float_bare(self):
        assert detect_price_format(9.99) == "float_bare"

    def test_str_dollar_integer(self):
        assert detect_price_format("$19") == "str_dollar_integer"

    def test_str_dollar_decimal(self):
        assert detect_price_format("$9.99") == "str_dollar_decimal"

    def test_str_integer(self):
        assert detect_price_format("9") == "str_integer"

    def test_str_decimal(self):
        assert detect_price_format("19.00") == "str_decimal"

    def test_empty_string(self):
        assert detect_price_format("") == "empty_string"

    def test_unknown(self):
        assert detect_price_format("free") == "unknown"


class TestAuditProductPrices:
    def _make_state(self, products):
        return {"products": {"active": products}}

    def test_empty_state(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state([])))
        result = audit_product_prices(state_path=state_file)
        assert result["total"] == 0
        assert result["inconsistencies"] == []
        assert result["missing_price"] == []

    def test_canonical_prices_no_inconsistencies(self, tmp_path):
        products = [
            {"slug": "prod-a", "price": "$19"},
            {"slug": "prod-b", "price": "$9"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = audit_product_prices(state_path=state_file)
        assert result["total"] == 2
        assert result["inconsistencies"] == []

    def test_non_canonical_detected(self, tmp_path):
        products = [
            {"slug": "prod-a", "price": "9"},
            {"slug": "prod-b", "price": 12},
            {"slug": "prod-c", "price": "$19"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = audit_product_prices(state_path=state_file)
        slugs = [i["slug"] for i in result["inconsistencies"]]
        assert "prod-a" in slugs
        assert "prod-b" in slugs
        assert "prod-c" not in slugs

    def test_missing_price_tracked(self, tmp_path):
        products = [
            {"slug": "no-price"},
            {"slug": "has-price", "price": "$9"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = audit_product_prices(state_path=state_file)
        assert "no-price" in result["missing_price"]
        assert "has-price" not in result["missing_price"]

    def test_suggested_fixes(self, tmp_path):
        products = [
            {"slug": "str-nine", "price": "9"},
            {"slug": "int-twelve", "price": 12},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = audit_product_prices(state_path=state_file)
        assert result["suggested_fixes"]["str-nine"] == "$9"
        assert result["suggested_fixes"]["int-twelve"] == "$12"

    def test_format_counts(self, tmp_path):
        products = [
            {"slug": "a", "price": "$19"},
            {"slug": "b", "price": "9"},
            {"slug": "c", "price": 12},
            {"slug": "d"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = audit_product_prices(state_path=state_file)
        assert result["format_counts"]["str_dollar_integer"] == 1
        assert result["format_counts"]["str_integer"] == 1
        assert result["format_counts"]["int_bare"] == 1
        assert result["format_counts"]["missing"] == 1

    def test_invalid_json_file(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_file.write_text("not json")
        result = audit_product_prices(state_path=state_file)
        assert result["total"] == 0

    def test_slug_from_s_field(self, tmp_path):
        products = [
            {"s": "alt-slug", "price": "9"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = audit_product_prices(state_path=state_file)
        assert any(i["slug"] == "alt-slug" for i in result["inconsistencies"])
