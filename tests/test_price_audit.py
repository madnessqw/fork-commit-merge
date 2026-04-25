"""Tests for scripts/price_audit.py"""

from __future__ import annotations

import json
import pytest
from pathlib import Path
from unittest.mock import patch

from scripts.price_audit import (
    audit_product_prices,
    detect_price_format,
    fix_product_prices,
    format_price_dollars,
    parse_price,
    price_coverage_report,
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

    def test_missing_state_file(self, tmp_path):
        state_file = tmp_path / "nonexistent.json"
        result = audit_product_prices(state_path=state_file)
        assert result["total"] == 0
        assert result["inconsistencies"] == []

    def test_products_as_list(self, tmp_path):
        products = [
            {"slug": "list-prod", "price": "$9"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps({"products": products}))
        result = audit_product_prices(state_path=state_file)
        assert result["total"] == 1

    def test_spec_ready_products_included(self, tmp_path):
        state = {
            "products": {
                "active": [{"slug": "active-prod", "price": "$9"}],
                "spec_ready": [{"slug": "spec-prod", "price": "19"}],
            }
        }
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(state))
        result = audit_product_prices(state_path=state_file)
        assert result["total"] == 2

    def test_non_dict_items_skipped(self, tmp_path):
        products = [
            "not_a_dict",
            42,
            {"slug": "valid", "price": "$9"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = audit_product_prices(state_path=state_file)
        assert result["total"] == 3
        assert len(result["inconsistencies"]) == 0

    def test_unparseable_price_tracked(self, tmp_path):
        products = [
            {"slug": "bad-price", "price": "call_us"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = audit_product_prices(state_path=state_file)
        assert any(i["issue"] == "unparseable" for i in result["inconsistencies"])


class TestParsePriceEdgeCases:
    def test_negative_int(self):
        assert parse_price(-5) == -500

    def test_whitespace_string(self):
        assert parse_price("  $19  ") == 1900

    def test_string_with_comma(self):
        assert parse_price("$1,299") == 129900

    def test_large_float(self):
        assert parse_price(299.99) == 29999

    def test_very_small_float(self):
        assert parse_price(0.01) == 1

    def test_bool_false(self):
        assert parse_price(False) == 0

    def test_string_only_dollar_sign(self):
        assert parse_price("$") is None


class TestPriceCoverageReport:
    def _make_state(self, products):
        return {"products": {"active": products}}

    def test_empty_state(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state([])))
        result = price_coverage_report(state_path=state_file)
        assert result["total"] == 0
        assert result["coverage_pct"] == 0.0

    def test_full_coverage(self, tmp_path):
        products = [
            {"slug": "a", "price": "$9"},
            {"slug": "b", "price": "$19"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = price_coverage_report(state_path=state_file)
        assert result["total"] == 2
        assert result["coverage_pct"] == 100.0
        assert result["canonical_pct"] == 100.0
        assert result["missing_count"] == 0

    def test_partial_coverage(self, tmp_path):
        products = [
            {"slug": "a", "price": "$9"},
            {"slug": "b"},
            {"slug": "c", "price": "$19"},
            {"slug": "d"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = price_coverage_report(state_path=state_file)
        assert result["total"] == 4
        assert result["coverage_pct"] == 50.0
        assert result["missing_count"] == 2

    def test_mixed_formats(self, tmp_path):
        products = [
            {"slug": "a", "price": "$9"},
            {"slug": "b", "price": "19"},
            {"slug": "c", "price": 12},
            {"slug": "d"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = price_coverage_report(state_path=state_file)
        assert result["total"] == 4
        assert result["coverage_pct"] == 75.0
        assert result["inconsistency_count"] == 2
        assert result["canonical_pct"] == 25.0

    def test_format_distribution_present(self, tmp_path):
        products = [
            {"slug": "a", "price": "$9"},
            {"slug": "b", "price": "19"},
            {"slug": "c", "price": 12},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = price_coverage_report(state_path=state_file)
        assert "str_dollar_integer" in result["format_distribution"]
        assert "str_integer" in result["format_distribution"]
        assert "int_bare" in result["format_distribution"]


class TestFixProductPrices:
    def _make_state(self, products):
        return {"products": {"active": products}}

    def test_dry_run_no_write(self, tmp_path):
        products = [
            {"slug": "a", "price": "9"},
            {"slug": "b", "price": "$19"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = fix_product_prices(state_path=state_file, dry_run=True)
        assert result["fixed_count"] == 1
        assert result["dry_run"] is True
        state = json.loads(state_file.read_text())
        assert state["products"]["active"][0]["price"] == "9"

    def test_fix_writes_normalized(self, tmp_path):
        products = [
            {"slug": "a", "price": "9"},
            {"slug": "b", "price": 12},
            {"slug": "c", "price": "$19"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = fix_product_prices(state_path=state_file)
        assert result["fixed_count"] == 2
        assert result["dry_run"] is False
        assert result["already_canonical"] == 1
        state = json.loads(state_file.read_text())
        assert state["products"]["active"][0]["price"] == "$9"
        assert state["products"]["active"][1]["price"] == "$12"
        assert state["products"]["active"][2]["price"] == "$19"

    def test_fix_preserves_other_fields(self, tmp_path):
        products = [
            {"slug": "a", "price": "9", "status": "live", "url": "https://a.vercel.app"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        fix_product_prices(state_path=state_file)
        state = json.loads(state_file.read_text())
        p = state["products"]["active"][0]
        assert p["price"] == "$9"
        assert p["status"] == "live"
        assert p["url"] == "https://a.vercel.app"

    def test_fix_skips_missing_price(self, tmp_path):
        products = [
            {"slug": "a"},
            {"slug": "b", "price": "9"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = fix_product_prices(state_path=state_file)
        assert result["skipped"] == 1
        assert result["fixed_count"] == 1

    def test_fix_skips_unparseable(self, tmp_path):
        products = [
            {"slug": "a", "price": "call_us"},
            {"slug": "b", "price": "9"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = fix_product_prices(state_path=state_file)
        assert result["skipped"] == 1

    def test_fix_no_changes_no_write(self, tmp_path):
        products = [
            {"slug": "a", "price": "$9"},
        ]
        state_file = tmp_path / "STATE.json"
        original = json.dumps(self._make_state(products))
        state_file.write_text(original)
        result = fix_product_prices(state_path=state_file)
        assert result["fixed_count"] == 0
        assert result["already_canonical"] == 1
        assert state_file.read_text() == original

    def test_fix_invalid_state(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_file.write_text("bad json")
        result = fix_product_prices(state_path=state_file)
        assert result["fixed_count"] == 0
        assert "error" in result

    def test_fix_products_as_list(self, tmp_path):
        products = [
            {"slug": "list-prod", "price": "19"},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps({"products": products}))
        result = fix_product_prices(state_path=state_file)
        assert result["fixed_count"] == 1

    def test_fix_spec_ready_included(self, tmp_path):
        state = {
            "products": {
                "active": [{"slug": "a", "price": "$9"}],
                "spec_ready": [{"slug": "b", "price": "19"}],
            }
        }
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(state))
        result = fix_product_prices(state_path=state_file)
        assert result["fixed_count"] == 1
        assert result["already_canonical"] == 1

    def test_fixed_products_detail(self, tmp_path):
        products = [
            {"slug": "a", "price": "9"},
            {"slug": "b", "price": 14},
        ]
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(self._make_state(products)))
        result = fix_product_prices(state_path=state_file, dry_run=True)
        assert len(result["fixed_products"]) == 2
        fp = result["fixed_products"]
        slugs = {x["slug"] for x in fp}
        assert slugs == {"a", "b"}
        for entry in fp:
            assert entry["new_price"].startswith("$")
