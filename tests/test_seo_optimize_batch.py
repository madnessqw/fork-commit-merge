from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from scripts.seo_optimize_batch import PRODUCTS_META, update_meta_tags


@pytest.fixture
def product_dir(tmp_path, monkeypatch):
    slug = "webterminal-pro"
    pdir = tmp_path / "products" / slug
    pdir.mkdir(parents=True)
    index = pdir / "index.html"
    index.write_text(
        textwrap.dedent("""\
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Old Title</title>
        </head>
        <body></body>
        </html>
        """),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    return {"slug": slug, "dir": pdir, "index": index}


def _read_index(product_dir):
    return product_dir["index"].read_text(encoding="utf-8")


def test_update_meta_tags_updates_title(product_dir):
    meta = PRODUCTS_META[product_dir["slug"]]
    result = update_meta_tags(product_dir["slug"], meta)
    assert result is True
    content = _read_index(product_dir)
    assert "<title>WebTerminal Pro - Browser-Based SSH Terminal</title>" in content


def test_update_meta_tags_adds_description(product_dir):
    meta = PRODUCTS_META[product_dir["slug"]]
    update_meta_tags(product_dir["slug"], meta)
    content = _read_index(product_dir)
    assert 'meta name="description" content="' in content
    assert "Professional web-based SSH terminal" in content


def test_update_meta_tags_adds_keywords(product_dir):
    meta = PRODUCTS_META[product_dir["slug"]]
    update_meta_tags(product_dir["slug"], meta)
    content = _read_index(product_dir)
    assert 'meta name="keywords" content="' in content


def test_update_meta_tags_adds_robots(product_dir):
    meta = PRODUCTS_META[product_dir["slug"]]
    update_meta_tags(product_dir["slug"], meta)
    content = _read_index(product_dir)
    assert 'meta name="robots" content="index, follow"' in content


def test_update_meta_tags_adds_author(product_dir):
    meta = PRODUCTS_META[product_dir["slug"]]
    update_meta_tags(product_dir["slug"], meta)
    content = _read_index(product_dir)
    assert 'meta name="author" content="Universe7Creator"' in content


def test_update_meta_tags_adds_schema_ld_json(product_dir):
    meta = PRODUCTS_META[product_dir["slug"]]
    update_meta_tags(product_dir["slug"], meta)
    content = _read_index(product_dir)
    assert '<script type="application/ld+json">' in content
    assert '"@type": "SoftwareApplication"' in content


def test_update_meta_tags_returns_false_missing_slug(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = update_meta_tags("nonexistent-slug", {"title": "X"})
    assert result is False


def test_update_meta_tags_uses_public_subdir(tmp_path, monkeypatch):
    slug = "webterminal-pro"
    pdir = tmp_path / "products" / slug / "public"
    pdir.mkdir(parents=True)
    index = pdir / "index.html"
    index.write_text(
        textwrap.dedent("""\
        <!DOCTYPE html>
        <html><head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Old</title>
        </head><body></body></html>
        """),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    meta = {"title": "New Title", "description": "New desc", "keywords": "k1,k2", "category": "DeveloperApplication"}
    result = update_meta_tags(slug, meta)
    assert result is True
    assert "<title>New Title</title>" in index.read_text(encoding="utf-8")
