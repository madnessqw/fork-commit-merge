import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.product_search_indexer import (
    STOP_WORDS,
    _tokenize,
    build_index,
    compute_stats,
    find_duplicates,
    format_results,
    load_products,
    search,
)


class TestTokenize:
    def test_basic(self):
        tokens = _tokenize("UUID Generator Pro")
        assert "uuid" in tokens
        assert "generator" not in tokens
        assert "pro" not in tokens

    def test_hyphenated(self):
        tokens = _tokenize("json-to-csv converter")
        assert "json" in tokens
        assert "csv" in tokens
        assert "converter" in tokens

    def test_stop_words_removed(self):
        tokens = _tokenize("the best tool for web")
        assert "the" not in tokens
        assert "best" in tokens

    def test_single_chars_removed(self):
        tokens = _tokenize("a b c tool")
        assert "a" not in tokens
        assert "b" not in tokens
        assert "tool" not in tokens

    def test_empty(self):
        assert _tokenize("") == []

    def test_special_chars(self):
        tokens = _tokenize("api/v2 @socket.io!")
        assert "api" in tokens
        assert "socket" in tokens

    def test_case_insensitive(self):
        assert _tokenize("UUID") == _tokenize("uuid")


class TestLoadProducts:
    def test_loads_from_state(self, tmp_path):
        state_file = tmp_path / "STATE.json"
        state_data = {
            "products": {
                "active": [
                    {"slug": "test-prod", "name": "Test Product", "status": "live"},
                ]
            }
        }
        state_file.write_text(json.dumps(state_data))

        with patch("scripts.product_search_indexer.STATE_FILE", state_file):
            result = load_products()
        assert len(result) == 1
        assert result[0]["slug"] == "test-prod"

    def test_missing_file(self, tmp_path):
        with patch("scripts.product_search_indexer.STATE_FILE", tmp_path / "none.json"):
            result = load_products()
        assert result == []

    def test_invalid_json(self, tmp_path):
        bad = tmp_path / "STATE.json"
        bad.write_text("not json{{{")
        with patch("scripts.product_search_indexer.STATE_FILE", bad):
            result = load_products()
        assert result == []


class TestBuildIndex:
    def _sample_products(self):
        return [
            {"slug": "uuid-gen", "name": "UUID Generator", "category": "dev", "tags": ["generator"]},
            {"slug": "json-parser", "name": "JSON Parser", "category": "dev", "tags": ["parser", "json"]},
            {"slug": "color-picker", "name": "Color Picker", "category": "design", "tags": ["color"]},
        ]

    def test_builds_inverted_index(self):
        products = self._sample_products()
        idx = build_index(products)
        assert "uuid" in idx["inverted"]
        assert "json" in idx["inverted"]
        assert "color" in idx["inverted"]

    def test_token_map(self):
        products = self._sample_products()
        idx = build_index(products)
        assert "uuid-gen" in idx["token_map"]
        assert "uuid" in idx["token_map"]["uuid-gen"]

    def test_categories(self):
        products = self._sample_products()
        idx = build_index(products)
        assert "uuid-gen" in idx["categories"]["dev"]
        assert "color-picker" in idx["categories"]["design"]

    def test_product_count(self):
        products = self._sample_products()
        idx = build_index(products)
        assert idx["product_count"] == 3

    def test_empty_products(self):
        idx = build_index([])
        assert idx["product_count"] == 0
        assert idx["inverted"] == {}


class TestSearch:
    def _setup(self):
        products = [
            {"slug": "uuid-gen", "name": "UUID Generator", "category": "dev", "tags": ["id"], "status": "live"},
            {"slug": "json-validator", "name": "JSON Validator", "category": "dev", "tags": ["json"], "status": "live"},
            {"slug": "csv-to-json", "name": "CSV to JSON Converter", "category": "dev", "tags": ["csv", "json"], "status": "live"},
            {"slug": "color-picker", "name": "Color Picker", "category": "design", "tags": ["color"], "status": "building"},
        ]
        index = build_index(products)
        return products, index

    def test_exact_match(self):
        products, index = self._setup()
        results = search(index, products, "uuid")
        assert len(results) >= 1
        assert results[0]["slug"] == "uuid-gen"

    def test_partial_match(self):
        products, index = self._setup()
        results = search(index, products, "json")
        assert len(results) >= 2
        slugs = [r["slug"] for r in results]
        assert "json-validator" in slugs
        assert "csv-to-json" in slugs

    def test_category_filter(self):
        products, index = self._setup()
        results = search(index, products, "json", category="design")
        assert len(results) == 0

    def test_no_results(self):
        products, index = self._setup()
        results = search(index, products, "quantum blockchain")
        assert results == []

    def test_empty_query(self):
        products, index = self._setup()
        results = search(index, products, "")
        assert results == []

    def test_limit(self):
        products, index = self._setup()
        results = search(index, products, "json", limit=1)
        assert len(results) <= 1

    def test_result_structure(self):
        products, index = self._setup()
        results = search(index, products, "uuid")
        r = results[0]
        assert "slug" in r
        assert "name" in r
        assert "category" in r
        assert "status" in r
        assert "score" in r
        assert "tags" in r


class TestFindDuplicates:
    def test_similar_names(self):
        products = [
            {"slug": "json-formatter", "name": "JSON Formatter"},
            {"slug": "json-formatter-pro", "name": "JSON Formatter Pro"},
            {"slug": "color-picker", "name": "Color Picker"},
        ]
        pairs = find_duplicates(products, threshold=0.5)
        slugs = [(p["product_a"], p["product_b"]) for p in pairs]
        assert any("json-formatter" in s for s in slugs)

    def test_no_duplicates(self):
        products = [
            {"slug": "uuid-gen", "name": "UUID Generator"},
            {"slug": "color-picker", "name": "Color Picker"},
            {"slug": "csv-exporter", "name": "CSV Exporter"},
        ]
        pairs = find_duplicates(products, threshold=0.9)
        assert len(pairs) == 0

    def test_threshold(self):
        products = [
            {"slug": "json-tool", "name": "JSON Tool"},
            {"slug": "json-tool-v2", "name": "JSON Tool V2"},
        ]
        high = find_duplicates(products, threshold=0.95)
        low = find_duplicates(products, threshold=0.3)
        assert len(low) >= len(high)

    def test_limit(self):
        products = [{"slug": f"prod-{i}", "name": f"Product {i}"} for i in range(60)]
        products.append({"slug": "prod-0-copy", "name": "Product 0 Copy"})
        pairs = find_duplicates(products, threshold=0.3, limit=5)
        assert len(pairs) <= 5

    def test_similarity_field(self):
        products = [
            {"slug": "a", "name": "Test A"},
            {"slug": "a-copy", "name": "Test A Copy"},
        ]
        pairs = find_duplicates(products, threshold=0.3)
        if pairs:
            assert "similarity" in pairs[0]
            assert 0 <= pairs[0]["similarity"] <= 1


class TestComputeStats:
    def test_basic_stats(self):
        products = [
            {"category": "dev", "status": "live", "tags": ["json", "parser"], "price": "$29"},
            {"category": "dev", "status": "building", "tags": ["json"], "price": "$19"},
            {"category": "design", "status": "live", "tags": ["color"], "price": "free"},
        ]
        index = build_index(products)
        stats = compute_stats(products, index)

        assert stats["total_products"] == 3
        assert stats["categories"]["dev"] == 2
        assert stats["categories"]["design"] == 1
        assert stats["statuses"]["live"] == 2
        assert stats["statuses"]["building"] == 1
        assert "json" in stats["top_tags"]

    def test_empty(self):
        index = build_index([])
        stats = compute_stats([], index)
        assert stats["total_products"] == 0
        assert stats["categories"] == {}

    def test_uncategorized(self):
        products = [{"status": "live", "tags": [], "price": "none"}]
        index = build_index(products)
        stats = compute_stats(products, index)
        assert stats["categories"]["uncategorized"] == 1


class TestFormatResults:
    def test_search_format(self):
        results = [
            {"slug": "test", "name": "Test", "category": "dev", "score": 2.5, "tags": []},
        ]
        output = format_results(results, "Search: test")
        assert "Test" in output
        assert "test" in output

    def test_duplicate_format(self):
        results = [
            {"product_a": "a", "product_b": "b", "name_a": "Alpha", "name_b": "Beta", "similarity": 0.8},
        ]
        output = format_results(results, "Duplicates")
        assert "Alpha" in output
        assert "Beta" in output
        assert "0.8" in output

    def test_empty(self):
        output = format_results([], "Empty")
        assert "Empty" in output
