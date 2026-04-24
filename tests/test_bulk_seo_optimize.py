"""Tests for scripts/bulk_seo_optimize.py — SEO meta tag injection pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.bulk_seo_optimize import (
    SCHEMA_TEMPLATE,
    OPENGRAPH_TEMPLATE,
    TWITTER_CARD_TEMPLATE,
    PRODUCT_SEO_DATA,
    get_vercel_url,
    add_seo_to_html,
)


class TestGetVercelUrl:
    def test_finds_slug_in_state(self):
        state = {"products": {"active": [{"slug": "codesnap", "vercel_url": "https://codesnap.vercel.app"}]}}
        assert get_vercel_url("codesnap", state) == "https://codesnap.vercel.app"

    def test_slug_missing_returns_default(self):
        state = {"products": {"active": [{"slug": "other", "vercel_url": "https://other.vercel.app"}]}}
        assert get_vercel_url("codesnap", state) == "https://codesnap.vercel.app"

    def test_empty_products(self):
        assert get_vercel_url("codesnap", {}) == "https://codesnap.vercel.app"

    def test_slug_present_no_vercel_url_field(self):
        state = {"products": {"active": [{"slug": "codesnap"}]}}
        assert get_vercel_url("codesnap", state) == "https://codesnap.vercel.app"


class TestAddSeoToHtml:
    BASIC_HTML = "<html><head><title>Test</title></head><body></body></html>"

    def test_injects_all_meta_tags(self):
        seo_data = {"description": "A test tool", "keywords": "test", "price": "9", "rating_count": "50"}
        result, modified = add_seo_to_html(self.BASIC_HTML, "test-slug", "Test Tool", seo_data, "https://test.vercel.app")
        assert modified is True
        assert "schema.org" in result
        assert "og:title" in result
        assert "twitter:card" in result
        assert 'rel="canonical"' in result
        assert "UniverseCreator" in result

    def test_returns_unchanged_if_already_has_schema(self):
        html = '<html><head><script type="application/ld+json">{"@context":"https://schema.org"}</script></head><body></body></html>'
        result, modified = add_seo_to_html(html, "s", "N", {}, "https://x.vercel.app")
        assert modified is False
        assert result == html

    def test_returns_unchanged_if_no_head_tag(self):
        html = "<html><body>No head</body></html>"
        result, modified = add_seo_to_html(html, "s", "N", {}, "https://x.vercel.app")
        assert modified is False

    def test_inserts_after_description_meta(self):
        html = '<html><head><meta name="description" content="desc"><title>T</title></head><body></body></html>'
        seo_data = {"description": "d", "keywords": "k", "price": "9", "rating_count": "10"}
        result, modified = add_seo_to_html(html, "s", "N", seo_data, "https://x.vercel.app")
        assert modified is True
        assert "og:title" in result

    def test_inserts_after_viewport_meta(self):
        html = '<html><head><meta name="viewport" content="width=device-width"></head><body></body></html>'
        seo_data = {"description": "d", "keywords": "k", "price": "9", "rating_count": "10"}
        result, modified = add_seo_to_html(html, "s", "N", seo_data, "https://x.vercel.app")
        assert modified is True

    def test_uses_seo_data_defaults_when_missing_fields(self):
        seo_data = {}
        result, modified = add_seo_to_html(self.BASIC_HTML, "slug", "Tool Name", seo_data, "https://slug.vercel.app")
        assert modified is True
        assert "Tool Name" in result
        assert "Professional developer tool" in result


class TestProductSeoData:
    def test_known_slugs_have_required_fields(self):
        required = {"description", "keywords", "price", "rating_count"}
        for slug, data in PRODUCT_SEO_DATA.items():
            missing = required - set(data.keys())
            assert not missing, f"{slug} missing fields: {missing}"

    def test_at_least_10_products_have_data(self):
        assert len(PRODUCT_SEO_DATA) >= 10

    def test_prices_are_numeric_strings(self):
        for slug, data in PRODUCT_SEO_DATA.items():
            assert data["price"].isdigit(), f"{slug} price is not numeric: {data['price']}"


class TestTemplates:
    def test_schema_template_formats_correctly(self):
        result = SCHEMA_TEMPLATE.format(name="TestApp", description="A test", price="19", rating_count="100")
        assert '"SoftwareApplication"' in result
        assert "TestApp" in result

    def test_opengraph_template_formats_correctly(self):
        result = OPENGRAPH_TEMPLATE.format(title="T", description="D", url="https://x.vercel.app")
        assert "og:title" in result
        assert "og:image" in result

    def test_twitter_card_template_formats_correctly(self):
        result = TWITTER_CARD_TEMPLATE.format(title="T", description="D", url="https://x.vercel.app")
        assert "twitter:card" in result
        assert "summary_large_image" in result
