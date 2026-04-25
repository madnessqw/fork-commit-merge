import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.portfolio_overlap_analyzer import (
    OVERLAP_GROUPS,
    analyze_overlaps,
    format_markdown,
    select_primary,
    slug_quality_score,
    url_quality_score,
)

MOCK_PRODUCTS = [
    {"n": "CronMaster", "s": "cronmaster", "st": "live", "v": "https://cronmaster.vercel.app", "c": "https://buy.polar.sh/1"},
    {"n": "Cron Express", "s": "cron-express", "st": "live", "v": "https://cron-express.vercel.app", "c": "https://buy.polar.sh/2"},
    {"n": "Cron Expression Builder", "s": "cron-expression-builder", "st": "live", "v": "https://cron-expression-builder.vercel.app", "c": "https://buy.polar.sh/3"},
    {"n": "Cron Expression Parser", "s": "cron-expression-parser", "st": "live", "v": "https://cron-expression-parser.vercel.app", "c": "https://buy.polar.sh/4"},
    {"n": "Cron Expression Tester", "s": "cron-expression-tester", "st": "live", "v": "https://cron-expression-tester.vercel.app", "c": "https://buy.polar.sh/5"},
    {"n": "CronCraft", "s": "croncraft", "st": "live", "v": "https://quickcron.vercel.app", "c": "https://buy.polar.sh/6"},
    {"n": "Cron Master", "s": "cron-master", "st": "live", "v": "https://cron-master.vercel.app", "c": "https://buy.polar.sh/7"},
    {"n": "JWT Generator", "s": "jwt-generator", "st": "live", "v": "https://jwt-generator-rho.vercel.app", "c": "https://buy.polar.sh/8"},
    {"n": "JWT Generator Pro", "s": "jwt-generator-pro", "st": "live", "v": "https://jwt-generator-pro.vercel.app", "c": "https://buy.polar.sh/9"},
    {"n": "JWT Debugger Pro", "s": "jwt-debugger-pro", "st": "live", "v": "https://jwt-debugger-pro.vercel.app", "c": "https://buy.polar.sh/10"},
    {"n": "HTML Entity", "s": "html-entity", "st": "live", "v": "https://html-entity.vercel.app", "c": "https://buy.polar.sh/11"},
    {"n": "HTML Entity Encoder", "s": "html-entity-encoder", "st": "live", "v": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app", "c": "https://buy.polar.sh/12"},
    {"n": "HTML Entities Pro", "s": "html-entities", "st": "live", "v": "https://html-entities.vercel.app", "c": "https://buy.polar.sh/13"},
    {"n": "UUID Generator Pro", "s": "uuid-generator-pro", "st": "live", "v": "https://uuid-generator-pro.vercel.app", "c": "https://buy.polar.sh/14"},
    {"n": "Base64 Pro", "s": "base64-pro", "st": "live", "v": "https://base64-pro.vercel.app", "c": "https://buy.polar.sh/15"},
    {"n": "Base64 Encoder Pro", "s": "base64-encoder-pro", "st": "live", "v": "https://base64-encoder-pro.vercel.app", "c": "https://buy.polar.sh/16"},
]


class TestSlugQualityScore:
    def test_clean_slug(self):
        assert slug_quality_score("uuid-generator") >= 90

    def test_long_slug(self):
        assert slug_quality_score("cron-expression-builder-pro") < slug_quality_score("cronmaster")

    def test_numeric_suffix_penalty(self):
        assert slug_quality_score("tool-123") < slug_quality_score("tool-pro")

    def test_simple_slug(self):
        assert slug_quality_score("cronmaster") >= 90

    def test_bounds(self):
        for slug in ["a", "x" * 50, "my-tool-v2-pro"]:
            score = slug_quality_score(slug)
            assert 0 <= score <= 100


class TestUrlQualityScore:
    def test_clean_url(self):
        assert url_quality_score("https://cronmaster.vercel.app") >= 90

    def test_deployment_url(self):
        assert url_quality_score("https://chmod-calculator-azjwwgvl6-madnessqws-projects.vercel.app") < 60

    def test_suffixed_url(self):
        score = url_quality_score("https://pdf-forge-five.vercel.app")
        assert score < url_quality_score("https://pdf-forge.vercel.app")

    def test_branch_url(self):
        score = url_quality_score("https://chmod-calculator-azjwwgvl6-madnessqws-projects.vercel.app")
        assert score < 60

    def test_bounds(self):
        for url in ["https://a.vercel.app", "https://x-y-z-abc123-madnessqws.vercel.app"]:
            score = url_quality_score(url)
            assert 0 <= score <= 100


class TestSelectPrimary:
    def test_prefers_clean_url(self):
        products = [
            {"n": "A", "s": "tool-a", "v": "https://tool-a-abc123-madnessqws.vercel.app", "c": ""},
            {"n": "B", "s": "tool-b", "v": "https://tool-b.vercel.app", "c": ""},
        ]
        result = select_primary(products)
        assert result["s"] == "tool-b"

    def test_prefers_pro_slug(self):
        products = [
            {"n": "JWT Generator", "s": "jwt-generator", "v": "https://jwt-generator.vercel.app", "c": ""},
            {"n": "JWT Generator Pro", "s": "jwt-generator-pro", "v": "https://jwt-generator-pro.vercel.app", "c": ""},
        ]
        result = select_primary(products)
        assert result["s"] == "jwt-generator-pro"


class TestAnalyzeOverlaps:
    def test_cron_overlap(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        cron_group = next((r for r in results if r["group"] == "Cron Tools"), None)
        assert cron_group is not None
        assert cron_group["count"] == 7
        assert cron_group["severity"] == "critical"

    def test_jwt_overlap(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        jwt_group = next((r for r in results if r["group"] == "JWT Tools"), None)
        assert jwt_group is not None
        assert jwt_group["count"] >= 2

    def test_html_entity_overlap(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        html_group = next((r for r in results if r["group"] == "HTML Entity Tools"), None)
        assert html_group is not None
        assert html_group["count"] >= 3

    def test_base64_overlap(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        b64_group = next((r for r in results if r["group"] == "Base64 Tools"), None)
        assert b64_group is not None
        assert b64_group["count"] >= 2

    def test_no_overlap_single(self):
        single = [MOCK_PRODUCTS[13]]
        results = analyze_overlaps(single)
        assert len(results) == 0

    def test_sorted_by_overlap_score(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        scores = [r["overlap_score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_has_primary_and_secondary(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        for r in results:
            assert "primary" in r
            assert "secondary" in r
            assert isinstance(r["secondary"], list)
            assert len(r["secondary"]) == r["count"] - 1

    def test_recommendation_populated(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        for r in results:
            assert r["recommendation"]


class TestFormatMarkdown:
    def test_output_structure(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        md = format_markdown(results)
        assert "# Portfolio Overlap Analysis" in md
        assert "Overlap Groups:" in md

    def test_critical_section(self):
        results = analyze_overlaps(MOCK_PRODUCTS)
        md = format_markdown(results)
        assert "Critical Overlap" in md
        assert "Cron Tools" in md

    def test_empty_results(self):
        md = format_markdown([])
        assert "# Portfolio Overlap Analysis" in md


class TestOverlapGroups:
    def test_groups_defined(self):
        assert len(OVERLAP_GROUPS) > 10

    def test_group_structure(self):
        for g in OVERLAP_GROUPS:
            assert "name" in g
            assert "keywords" in g
            assert isinstance(g["keywords"], list)
