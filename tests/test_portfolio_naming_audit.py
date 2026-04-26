"""Tests for portfolio_naming_audit.py"""

from __future__ import annotations

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from scripts.portfolio_naming_audit import (
    _strip_suffix,
    _extract_base_type,
    audit_suffixes,
    audit_type_words,
    audit_separators,
    audit_suffix_distribution,
    generate_fix_suggestions,
    run_audit,
    format_audit_report,
    main,
)


def _make_product(name: str, slug: str = "") -> dict:
    return {"name": name, "slug": slug or name.lower().replace(" ", "-")}


class TestStripSuffix:
    def test_pro_suffix(self):
        assert _strip_suffix("UUID Generator Pro") == ("UUID Generator", "Pro")

    def test_plus_suffix(self):
        assert _strip_suffix("PDF Forge Plus") == ("PDF Forge", "Plus")

    def test_no_suffix(self):
        assert _strip_suffix("QR Forge") == ("QR Forge", "")

    def test_premium_suffix(self):
        assert _strip_suffix("Hash Generator Premium") == ("Hash Generator", "Premium")

    def test_lite_suffix(self):
        assert _strip_suffix("GeoIP Lite") == ("GeoIP", "Lite")

    def test_empty_name(self):
        assert _strip_suffix("") == ("", "")


class TestExtractBaseType:
    def test_generator(self):
        base, cat = _extract_base_type("UUID Generator Pro")
        assert cat == "generator"
        assert "uuid" in base

    def test_validator(self):
        base, cat = _extract_base_type("TOML Validator")
        assert cat == "validator"

    def test_converter(self):
        base, cat = _extract_base_type("YAML to JSON Converter")
        assert cat == "converter"

    def test_no_match(self):
        base, cat = _extract_base_type("QR Forge")
        assert cat == ""

    def test_formatter(self):
        base, cat = _extract_base_type("SQL Query Formatter")
        assert cat == "formatter"

    def test_encoder(self):
        base, cat = _extract_base_type("URL Encoder/Decoder Pro")
        assert cat == "encoder"


class TestAuditSuffixes:
    def test_detects_inconsistency(self):
        products = [
            _make_product("UUID Generator Pro", "uuid-gen-pro"),
            _make_product("UUID Generator", "uuid-gen"),
        ]
        result = audit_suffixes(products)
        assert len(result) == 1
        assert result[0]["type"] == "suffix_inconsistency"
        assert len(result[0]["products"]) == 2

    def test_no_inconsistency_same_suffix(self):
        products = [
            _make_product("Hash Generator Pro", "hash-gen-pro"),
            _make_product("PDF Generator Pro", "pdf-gen-pro"),
        ]
        result = audit_suffixes(products)
        assert len(result) == 0

    def test_single_product_no_issue(self):
        products = [_make_product("UUID Generator Pro")]
        result = audit_suffixes(products)
        assert len(result) == 0

    def test_three_way_inconsistency(self):
        products = [
            _make_product("Tool Pro", "tool-pro"),
            _make_product("Tool Lite", "tool-lite"),
            _make_product("Tool", "tool"),
        ]
        result = audit_suffixes(products)
        assert len(result) == 1
        assert len(result[0]["suffixes"]) == 3


class TestAuditTypeWords:
    def test_detects_overlap(self):
        products = [
            _make_product("QR Code Generator", "qr-gen"),
            _make_product("QR Code Builder", "qr-builder"),
        ]
        result = audit_type_words(products)
        assert len(result) >= 1

    def test_no_overlap_same_type(self):
        products = [
            _make_product("UUID Generator", "uuid-gen"),
            _make_product("Hash Generator", "hash-gen"),
        ]
        result = audit_type_words(products)
        assert len(result) == 0


class TestAuditSeparators:
    def test_detects_slash(self):
        products = [_make_product("URL Encoder/Decoder Pro", "url-enc")]
        result = audit_separators(products)
        assert len(result) == 1
        assert "/" in result[0]["separators"]

    def test_detects_ampersand(self):
        products = [_make_product("XML Formatter & Validator", "xml-fv")]
        result = audit_separators(products)
        assert len(result) == 1

    def test_clean_name(self):
        products = [_make_product("UUID Generator Pro", "uuid-gen")]
        result = audit_separators(products)
        assert len(result) == 0

    def test_detects_plus(self):
        products = [_make_product("JSON + XML Tool", "jsonxml")]
        result = audit_separators(products)
        assert len(result) == 1


class TestAuditSuffixDistribution:
    def test_counts_pro(self):
        products = [
            _make_product("UUID Generator Pro"),
            _make_product("Hash Generator Pro"),
            _make_product("QR Forge"),
        ]
        result = audit_suffix_distribution(products)
        assert result["suffix_distribution"]["Pro"] == 2
        assert result["no_suffix_count"] == 1
        assert result["total"] == 3

    def test_empty(self):
        result = audit_suffix_distribution([])
        assert result["total"] == 0
        assert result["no_suffix_count"] == 0


class TestGenerateFixSuggestions:
    def test_suggests_pro_as_canonical(self):
        suffix_issues = [
            {
                "base_name": "uuid generator",
                "products": [
                    {"name": "UUID Generator Pro", "slug": "uuid-gen-pro", "suffix": "Pro"},
                    {"name": "UUID Generator", "slug": "uuid-gen", "suffix": ""},
                ],
                "suffixes": ["", "Pro"],
            }
        ]
        suggestions = generate_fix_suggestions(suffix_issues, [])
        assert len(suggestions) == 1
        assert suggestions[0]["keep_slug"] == "uuid-gen-pro"

    def test_no_issues(self):
        suggestions = generate_fix_suggestions([], [])
        assert suggestions == []


class TestRunAudit:
    def test_with_mock_products(self, tmp_path):
        state = {
            "products": {
                "active": [
                    {"name": "UUID Generator Pro", "slug": "uuid-gen-pro"},
                    {"name": "UUID Generator", "slug": "uuid-gen"},
                    {"name": "QR Forge", "slug": "qr-forge"},
                ]
            }
        }
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(state))

        result = run_audit(state_file)
        assert result["total_products"] == 3
        assert result["suffix_inconsistencies"] >= 1
        assert "suffix_distribution" in result

    def test_empty_state(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_file.write_text("{}")
        result = run_audit(state_file)
        assert "error" in result

    def test_missing_state(self, tmp_path):
        result = run_audit(tmp_path / "nonexistent.json")
        assert "error" in result


class TestFormatAuditReport:
    def test_basic_format(self):
        audit = {
            "total_products": 10,
            "suffix_inconsistencies": 2,
            "type_word_overlaps": 1,
            "separator_issues": 0,
            "suffix_distribution": {"suffix_distribution": {"Pro": 8}, "no_suffix_count": 2},
            "suffix_issues": [],
            "type_issues": [],
            "separator_issues_list": [],
        }
        report = format_audit_report(audit)
        assert "Portfolio Naming Audit" in report
        assert "10" in report
        assert "Pro: 8" in report


class TestMain:
    def test_main_text_output(self, tmp_path):
        state = {
            "products": {
                "active": [
                    {"name": "Hash Pro", "slug": "hash-pro"},
                    {"name": "Hash", "slug": "hash"},
                ]
            }
        }
        sf = tmp_path / "STATE.json"
        sf.write_text(json.dumps(state))
        with patch("sys.argv", ["portfolio_naming_audit"]):
            result = main(state_path=sf)
        assert result["total_products"] == 2

    def test_main_json_output(self, tmp_path, capsys):
        state = {"products": {"active": [{"name": "Test Pro", "slug": "test-pro"}]}}
        sf = tmp_path / "STATE.json"
        sf.write_text(json.dumps(state))
        with patch("sys.argv", ["portfolio_naming_audit", "--json"]):
            main(state_path=sf)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["total_products"] == 1

    def test_main_fix_suggestions(self, tmp_path, capsys):
        state = {
            "products": {
                "active": [
                    {"name": "UUID Generator Pro", "slug": "uuid-pro"},
                    {"name": "UUID Generator", "slug": "uuid"},
                ]
            }
        }
        sf = tmp_path / "STATE.json"
        sf.write_text(json.dumps(state))
        with patch("sys.argv", ["portfolio_naming_audit", "--fix-suggestions"]):
            main(state_path=sf)
        captured = capsys.readouterr()
        assert "uuid" in captured.out.lower() or "consider" in captured.out.lower()
