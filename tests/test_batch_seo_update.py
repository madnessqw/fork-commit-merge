"""Tests for scripts/batch_seo_update.py — SEO meta tag updater."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.batch_seo_update import (
    SEO_DESCRIPTIONS,
    KEYWORDS,
    update_product_seo,
    update_state_json,
    main,
)


@pytest.fixture
def product_dir(tmp_path, monkeypatch):
    slug = "test-product-slug"
    pdir = tmp_path / "products" / slug
    pdir.mkdir(parents=True)
    index = pdir / "index.html"
    index.write_text(
        textwrap.dedent("""\
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Test Product Slug</title>
        </head>
        <body>Hello</body>
        </html>
        """),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    return tmp_path, slug, index


class TestUpdateProductSeo:
    def test_updates_meta_tags(self, product_dir):
        tmp, slug, index = product_dir
        result = update_product_seo(slug)
        assert result is True
        content = index.read_text(encoding="utf-8")
        assert '<meta name="description"' in content
        assert '<meta name="keywords"' in content
        assert 'seo_optimized' in content
        assert "og:title" in content
        assert "twitter:card" in content
        assert "application/ld+json" in content

    def test_skips_already_optimized(self, product_dir):
        tmp, slug, index = product_dir
        update_product_seo(slug)
        content = index.read_text(encoding="utf-8")
        result = update_product_seo(slug)
        assert result is True

    def test_returns_false_missing_index(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = update_product_seo("nonexistent-slug")
        assert result is False

    def test_uses_default_description_for_unknown_slug(self, product_dir):
        tmp, slug, index = product_dir
        result = update_product_seo(slug)
        assert result is True
        content = index.read_text(encoding="utf-8")
        assert '<meta name="description"' in content

    def test_known_slug_uses_seo_descriptions(self, tmp_path, monkeypatch):
        slug = "jwt-generator"
        pdir = tmp_path / "products" / slug
        pdir.mkdir(parents=True)
        (pdir / "index.html").write_text(
            "<html><head><title>JWT</title></head><body></body></html>",
            encoding="utf-8",
        )
        monkeypatch.chdir(tmp_path)
        result = update_product_seo(slug)
        assert result is True
        content = (pdir / "index.html").read_text(encoding="utf-8")
        assert SEO_DESCRIPTIONS[slug] in content

    def test_json_ld_contains_schema_org(self, product_dir):
        tmp, slug, index = product_dir
        update_product_seo(slug)
        content = index.read_text(encoding="utf-8")
        assert "https://schema.org" in content
        assert "WebApplication" in content


class TestUpdateStateJson:
    def test_marks_products_seo_optimized(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        state = {
            "products": {
                "active": [
                    {"slug": "jwt-generator", "status": "live"},
                    {"slug": "pdf-forge", "status": "live"},
                ]
            }
        }
        (tmp_path / "STATE.json").write_text(json.dumps(state), encoding="utf-8")
        count = update_state_json(["jwt-generator", "pdf-forge"])
        assert count == 2
        updated = json.loads((tmp_path / "STATE.json").read_text(encoding="utf-8"))
        slugs_in_state = [
            p["slug"] for p in updated["products"]["active"] if p.get("seo_optimized")
        ]
        assert "jwt-generator" in slugs_in_state
        assert "pdf-forge" in slugs_in_state

    def test_handles_missing_state_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        count = update_state_json(["some-slug"])
        assert count == 0


class TestMain:
    def test_main_with_custom_slugs(self, tmp_path, monkeypatch):
        slug = "dataflip"
        pdir = tmp_path / "products" / slug
        pdir.mkdir(parents=True)
        (pdir / "index.html").write_text(
            "<html><head><title>DataFlip</title></head><body></body></html>",
            encoding="utf-8",
        )
        monkeypatch.chdir(tmp_path)
        with patch("sys.argv", ["batch_seo_update.py", slug]):
            result = main()
        assert result == 1
