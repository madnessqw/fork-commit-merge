import json
import os
import tempfile
from pathlib import Path

import pytest

from scripts.product_overlap_analyzer import (
    STOP_WORDS,
    _extract_keywords,
    _jaccard_similarity,
    _tokenize,
    category_clustering,
    compute_overlap_matrix,
    consolidation_suggestions,
    load_products,
    overlap_summary,
)


def _make_product(slug, name="Test", tagline="", description="",
                  features=None, **kw):
    p = {"slug": slug, "name": name, "tagline": tagline,
         "description": description, "features": features or []}
    p.update(kw)
    return p


def _write_products(tmp, products):
    for p in products:
        slug = p.get("slug", p.get("_dir", "unknown"))
        d = tmp / slug
        d.mkdir(parents=True, exist_ok=True)
        data = {k: v for k, v in p.items() if k != "_dir"}
        (d / "product.json").write_text(json.dumps(data), encoding="utf-8")


class TestTokenize:
    def test_basic(self):
        tokens = _tokenize("UUID Generator Pro")
        assert "uuid" in tokens
        assert "pro" not in tokens

    def test_stop_words_removed(self):
        tokens = _tokenize("this is a test for the tool")
        assert "this" not in tokens
        assert "test" in tokens

    def test_short_words_filtered(self):
        tokens = _tokenize("I am ok")
        assert "ok" not in tokens
        assert len(tokens) == 0

    def test_numbers_kept(self):
        tokens = _tokenize("base64 encode")
        assert "base64" in tokens
        assert "encode" in tokens


class TestExtractKeywords:
    def test_from_name(self):
        p = _make_product("test", name="JSON Formatter Pro")
        kw = _extract_keywords(p)
        assert "json" in kw
        assert "formatter" not in kw

    def test_from_features(self):
        p = _make_product("test", features=["Encode base64 data", "Decode URLs"])
        kw = _extract_keywords(p)
        assert "base64" in kw
        assert "decode" in kw
        assert "urls" in kw

    def test_empty_product(self):
        p = _make_product("x", name="")
        kw = _extract_keywords(p)
        assert kw == []

    def test_combined_fields(self):
        p = _make_product("test", name="Cron Expression Builder",
                          tagline="Build cron expressions easily",
                          description="A cron expression tool for developers",
                          features=["Parse cron syntax"])
        kw = _extract_keywords(p)
        assert "cron" in kw
        assert "expression" in kw


class TestJaccardSimilarity:
    def test_identical(self):
        sim = _jaccard_similarity({"a", "b", "c"}, {"a", "b", "c"})
        assert sim == 1.0

    def test_disjoint(self):
        sim = _jaccard_similarity({"a", "b"}, {"c", "d"})
        assert sim == 0.0

    def test_partial(self):
        sim = _jaccard_similarity({"a", "b", "c"}, {"b", "c", "d"})
        assert 0.0 < sim < 1.0

    def test_empty_sets(self):
        assert _jaccard_similarity(set(), {"a"}) == 0.0
        assert _jaccard_similarity(set(), set()) == 0.0


class TestComputeOverlapMatrix:
    def test_no_overlap(self):
        products = [
            _make_product("json-tool", name="JSON Formatter",
                          features=["Format JSON data"]),
            _make_product("cron-tool", name="Cron Expression Builder",
                          features=["Build cron schedules"]),
        ]
        result = compute_overlap_matrix(products, threshold=0.1)
        assert len(result) == 0

    def test_high_overlap(self):
        products = [
            _make_product("uuid-gen-1", name="UUID Generator",
                          features=["Generate UUID v4", "UUID v1 generation"]),
            _make_product("uuid-gen-2", name="UUID Creator",
                          features=["Generate UUID v4", "UUID v1 generation"]),
        ]
        result = compute_overlap_matrix(products, threshold=0.3)
        assert len(result) == 1
        assert result[0]["similarity"] >= 0.3
        assert "uuid" in result[0]["shared_keywords"]

    def test_threshold_filtering(self):
        products = [
            _make_product("a", name="JSON Parser",
                          features=["Parse JSON files"]),
            _make_product("b", name="YAML Parser",
                          features=["Parse YAML files"]),
        ]
        result_low = compute_overlap_matrix(products, threshold=0.1)
        result_high = compute_overlap_matrix(products, threshold=0.9)
        assert len(result_low) >= len(result_high)


class TestOverlapSummary:
    def test_summary_structure(self):
        products = [
            _make_product("a", name="JSON Tool", features=["parse json"]),
            _make_product("b", name="JSON Parser", features=["parse json data"]),
            _make_product("c", name="Cron Builder", features=["build cron"]),
        ]
        summary = overlap_summary(products, threshold=0.1)
        assert "total_products" in summary
        assert "overlap_pairs" in summary
        assert "affected_products" in summary
        assert "similarity_buckets" in summary
        assert "top_shared_keywords" in summary
        assert summary["total_products"] == 3

    def test_similarity_buckets(self):
        products = [
            _make_product("a", name="JSON Parser Pro",
                          features=["parse json data validate"]),
            _make_product("b", name="JSON Formatter",
                          features=["format json data beautify"]),
        ]
        summary = overlap_summary(products, threshold=0.1)
        assert "similarity_buckets" in summary
        total = sum(summary["similarity_buckets"].values())
        assert total == summary["overlap_pairs"]


class TestConsolidationSuggestions:
    def test_high_similarity_suggestion(self):
        overlaps = [{
            "slug_a": "uuid-gen", "name_a": "UUID Generator",
            "slug_b": "uuid-creator", "name_b": "UUID Creator",
            "similarity": 0.75, "shared_keywords": ["uuid", "generate"],
            "shared_count": 2,
        }]
        suggestions = consolidation_suggestions(overlaps)
        assert len(suggestions) == 1
        assert suggestions[0]["keep"] == "uuid-creator"
        assert suggestions[0]["merge_into"] == "uuid-gen"

    def test_low_similarity_excluded(self):
        overlaps = [{
            "slug_a": "a", "name_a": "A",
            "slug_b": "b", "name_b": "B",
            "similarity": 0.35, "shared_keywords": ["json"],
            "shared_count": 1,
        }]
        suggestions = consolidation_suggestions(overlaps)
        assert len(suggestions) == 0

    def test_keep_longer_slug(self):
        overlaps = [{
            "slug_a": "json-fmt", "name_a": "JSON Format",
            "slug_b": "json-formatter-pro", "name_b": "JSON Formatter",
            "similarity": 0.8, "shared_keywords": ["json"],
            "shared_count": 1,
        }]
        suggestions = consolidation_suggestions(overlaps)
        assert suggestions[0]["keep"] == "json-formatter-pro"


class TestCategoryClustering:
    def test_basic_clustering(self):
        products = [
            _make_product("json-tool", name="JSON Formatter"),
            _make_product("cron-tool", name="Cron Builder"),
            _make_product("json-parser", name="JSON Parser"),
        ]
        clusters = category_clustering(products)
        assert isinstance(clusters, dict)
        assert len(clusters) > 0

    def test_empty_products(self):
        clusters = category_clustering([])
        assert clusters == {}


class TestLoadProducts:
    def test_load_from_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            _write_products(tmp_path, [
                _make_product("test-prod", name="Test Product"),
            ])
            products = load_products(tmp_path)
            assert len(products) == 1
            assert products[0]["slug"] == "test-prod"

    def test_skip_missing_product_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "empty-dir").mkdir()
            products = load_products(tmp_path)
            assert len(products) == 0

    def test_skip_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            d = tmp_path / "bad"
            d.mkdir()
            (d / "product.json").write_text("not json", encoding="utf-8")
            products = load_products(tmp_path)
            assert len(products) == 0

    def test_nonexistent_dir(self):
        products = load_products(Path("/nonexistent"))
        assert products == []
