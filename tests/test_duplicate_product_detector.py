"""Tests for scripts.duplicate_product_detector."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.duplicate_product_detector import (
    find_name_duplicates,
    find_slug_similarities,
    generate_report,
)

SAMPLE_PRODUCTS = [
    {"n": "UUID Generator Pro", "s": "uuid-generator-pro", "st": "live", "v": "https://uuid-generator-pro.vercel.app", "c": "https://buy.polar.sh/checkout_1"},
    {"n": "UUID Generator Pro", "s": "uuid-generator", "st": "live", "v": "https://uuid-generator.vercel.app", "c": "https://buy.polar.sh/checkout_1"},
    {"n": "Base64 Pro", "s": "base64-pro", "st": "live", "v": "https://base64-pro.vercel.app", "c": "https://buy.polar.sh/checkout_2"},
    {"n": "Hash Tool", "s": "hash-tool", "st": "live", "v": "https://hash-tool.vercel.app", "c": "https://buy.polar.sh/checkout_3"},
    {"n": "TOML Parser Pro", "s": "toml-parser-pro", "st": "live", "v": "https://toml-parser-pro.vercel.app", "c": "https://buy.polar.sh/checkout_4"},
    {"n": "TOML Parser Pro", "s": "toml-parser", "st": "live", "v": "https://toml-parser.vercel.app", "c": "https://buy.polar.sh/checkout_4"},
]


class TestFindNameDuplicates:
    def test_no_duplicates(self):
        products = [
            {"n": "Tool A", "s": "tool-a"},
            {"n": "Tool B", "s": "tool-b"},
        ]
        result = find_name_duplicates(products)
        assert result == []

    def test_detects_duplicates(self):
        result = find_name_duplicates(SAMPLE_PRODUCTS)
        names = [r["name"] for r in result]
        assert "UUID Generator Pro" in names
        assert "TOML Parser Pro" in names

    def test_duplicate_count(self):
        result = find_name_duplicates(SAMPLE_PRODUCTS)
        uuid_group = next(r for r in result if "UUID" in r["name"])
        assert uuid_group["count"] == 2

    def test_same_checkout_flag(self):
        result = find_name_duplicates(SAMPLE_PRODUCTS)
        uuid_group = next(r for r in result if "UUID" in r["name"])
        assert uuid_group["same_checkout"] is True

    def test_slugs_extracted(self):
        result = find_name_duplicates(SAMPLE_PRODUCTS)
        uuid_group = next(r for r in result if "UUID" in r["name"])
        assert set(uuid_group["slugs"]) == {"uuid-generator-pro", "uuid-generator"}

    def test_case_insensitive(self):
        products = [
            {"n": "My Tool", "s": "my-tool"},
            {"n": "my tool", "s": "my-tool-2"},
        ]
        result = find_name_duplicates(products)
        assert len(result) == 1

    def test_empty_products(self):
        assert find_name_duplicates([]) == []


class TestFindSlugSimilarities:
    def test_slug_pro_variants(self):
        products = [
            {"s": "yaml-validator", "n": "YAML Validator"},
            {"s": "yaml-validator-pro", "n": "YAML Validator Pro"},
        ]
        result = find_slug_similarities(products)
        all_variants = []
        for g in result:
            all_variants.extend(g["variants"])
        assert "yaml-validator" in all_variants
        assert "yaml-validator-pro" in all_variants

    def test_no_similar_slugs(self):
        products = [
            {"s": "tool-a", "n": "Tool A"},
            {"s": "tool-b", "n": "Tool B"},
        ]
        result = find_slug_similarities(products)
        assert len(result) == 0


class TestGenerateReport:
    def test_report_contains_summary(self):
        dupes = find_name_duplicates(SAMPLE_PRODUCTS)
        slugs = find_slug_similarities(SAMPLE_PRODUCTS)
        report = generate_report(dupes, slugs, SAMPLE_PRODUCTS)
        assert "**Total products:** 6" in report
        assert "UUID Generator Pro" in report

    def test_report_effective_unique(self):
        dupes = find_name_duplicates(SAMPLE_PRODUCTS)
        slugs = find_slug_similarities(SAMPLE_PRODUCTS)
        report = generate_report(dupes, slugs, SAMPLE_PRODUCTS)
        assert "Effective unique products:" in report

    def test_empty_report(self):
        report = generate_report([], [], [])
        assert "**Total products:** 0" in report


class TestMainCLI:
    def test_json_output(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        summary = tmp_path / "STATE_SUMMARY.json"
        summary.write_text(json.dumps({"products": SAMPLE_PRODUCTS}))
        import scripts.duplicate_product_detector as mod
        monkeypatch.setattr(mod, "SUMMARY_PATH", summary)
        monkeypatch.setattr("sys.argv", ["duplicate_product_detector", "--json"])
        from io import StringIO
        captured = StringIO()
        monkeypatch.setattr("sys.stdout", captured)
        mod.main()
        output = json.loads(captured.getvalue())
        assert output["total_products"] == 6
        assert output["duplicate_name_groups"] == 2
