import json
import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from scripts.category_normalizer import (
    build_reverse_map,
    normalize_category,
    load_state_products,
    audit,
    normalize_products,
    CANONICAL_CATEGORIES,
    STATE_FILE,
    PRODUCTS_DIR,
)


class TestBuildReverseMap:
    def test_all_canonical_have_entries(self):
        rm = build_reverse_map()
        for canonical in CANONICAL_CATEGORIES:
            assert canonical.lower() in rm

    def test_aliases_mapped_correctly(self):
        rm = build_reverse_map()
        assert rm["developer tools"] == "developer-tools"
        assert rm["developer_tools"] == "developer-tools"
        assert rm["security_tools"] == "security"
        assert rm["devops_tools"] == "devops"
        assert rm["design_tools"] == "design-tools"
        assert rm["utilities"] == "utilities"
        assert rm["api services"] == "api-services"
        assert rm["ai_tools"] == "ai-tools"

    def test_case_insensitive(self):
        rm = build_reverse_map()
        assert rm["developer tools"] == "developer-tools"
        assert rm["developer_tools"] == "developer-tools"
        assert rm["DEVELOPER TOOLS".lower()] == "developer-tools"


class TestNormalizeCategory:
    def test_empty_string(self):
        assert normalize_category("", {}) == "uncategorized"

    def test_none(self):
        assert normalize_category(None, {}) == "uncategorized"

    def test_uncategorized_passthrough(self):
        assert normalize_category("uncategorized", {}) == "uncategorized"

    def test_known_alias(self):
        rm = build_reverse_map()
        assert normalize_category("Developer Tools", rm) == "developer-tools"
        assert normalize_category("developer_tools", rm) == "developer-tools"
        assert normalize_category("security_tools", rm) == "security"

    def test_unknown_category_preserved(self):
        rm = build_reverse_map()
        assert normalize_category("custom-category", rm) == "custom-category"

    def test_whitespace_stripped(self):
        rm = build_reverse_map()
        assert normalize_category("  Developer Tools  ", rm) == "developer-tools"


class TestAudit:
    def test_audit_with_mock_products(self):
        products = [
            {"slug": "a", "category": "Developer Tools"},
            {"slug": "b", "category": "developer_tools"},
            {"slug": "c", "category": "security_tools"},
            {"slug": "d"},
            {"slug": "e", "category": "uncategorized"},
        ]
        result = audit(products)
        assert result["total"] == 5
        assert result["mismatch_count"] == 3
        assert result["uncategorized_count"] == 2
        assert result["canonical_count"] == 3
        assert result["normalized_categories"]["developer-tools"] == 2
        assert result["normalized_categories"]["security"] == 1

    def test_audit_empty_products(self):
        result = audit([])
        assert result["total"] == 0
        assert result["mismatch_count"] == 0
        assert result["uncategorized_count"] == 0

    def test_audit_no_mismatches(self):
        products = [
            {"slug": "a", "category": "developer-tools"},
            {"slug": "b", "category": "security"},
        ]
        result = audit(products)
        assert result["mismatch_count"] == 0


class TestNormalizeProducts:
    def test_normalize_dry_run_no_files_written(self, tmp_path):
        prod_dir = tmp_path / "products" / "test-prod"
        prod_dir.mkdir(parents=True)
        pj = prod_dir / "product.json"
        pj.write_text(json.dumps({"slug": "test-prod", "category": "Developer Tools"}))

        with patch("scripts.category_normalizer.PRODUCTS_DIR", tmp_path / "products"):
            result = normalize_products(dry_run=True)

        assert result["dry_run"] is True
        assert result["updated"] == 1
        assert pj.read_text() == json.dumps({"slug": "test-prod", "category": "Developer Tools"})

    def test_normalize_live_writes_files(self, tmp_path):
        prod_dir = tmp_path / "products" / "test-prod"
        prod_dir.mkdir(parents=True)
        pj = prod_dir / "product.json"
        pj.write_text(json.dumps({"slug": "test-prod", "category": "Developer Tools"}))

        with patch("scripts.category_normalizer.PRODUCTS_DIR", tmp_path / "products"):
            result = normalize_products(dry_run=False)

        assert result["updated"] == 1
        data = json.loads(pj.read_text())
        assert data["category"] == "developer-tools"

    def test_normalize_skips_already_canonical(self, tmp_path):
        prod_dir = tmp_path / "products" / "test-prod"
        prod_dir.mkdir(parents=True)
        pj = prod_dir / "product.json"
        pj.write_text(json.dumps({"slug": "test-prod", "category": "developer-tools"}))

        with patch("scripts.category_normalizer.PRODUCTS_DIR", tmp_path / "products"):
            result = normalize_products(dry_run=False)

        assert result["updated"] == 0
        assert result["unchanged"] == 1

    def test_normalize_skips_uncategorized(self, tmp_path):
        prod_dir = tmp_path / "products" / "test-prod"
        prod_dir.mkdir(parents=True)
        pj = prod_dir / "product.json"
        pj.write_text(json.dumps({"slug": "test-prod"}))

        with patch("scripts.category_normalizer.PRODUCTS_DIR", tmp_path / "products"):
            result = normalize_products(dry_run=False)

        assert result["updated"] == 0

    def test_normalize_handles_corrupt_json(self, tmp_path):
        prod_dir = tmp_path / "products" / "bad-prod"
        prod_dir.mkdir(parents=True)
        pj = prod_dir / "product.json"
        pj.write_text("{invalid json}")

        with patch("scripts.category_normalizer.PRODUCTS_DIR", tmp_path / "products"):
            result = normalize_products(dry_run=False)

        assert len(result["errors"]) == 1
        assert result["errors"][0]["slug"] == "bad-prod"

    def test_normalize_no_products_dir(self, tmp_path):
        with patch("scripts.category_normalizer.PRODUCTS_DIR", tmp_path / "nonexistent"):
            result = normalize_products(dry_run=False)

        assert result["updated"] == 0
        assert "error" in result


class TestCanonicalCategories:
    def test_all_aliases_map_to_canonical(self):
        rm = build_reverse_map()
        for canonical, aliases in CANONICAL_CATEGORIES.items():
            for alias in aliases:
                assert rm[alias.lower()] == canonical, f"{alias} -> {rm.get(alias.lower())} != {canonical}"

    def test_canonical_in_reverse_map(self):
        rm = build_reverse_map()
        for canonical in CANONICAL_CATEGORIES:
            assert canonical in rm, f"{canonical} missing from reverse map"
