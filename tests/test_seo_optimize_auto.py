#!/usr/bin/env python3
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from seo_optimize_auto import (
    generate_keywords, generate_description, find_index_html, update_product_seo
)


def test_generate_keywords_basic():
    result = generate_keywords("UUID Generator Pro")
    assert "uuid" in result.lower()
    assert "developer tools" in result.lower()


def test_generate_keywords_no_category_match():
    result = generate_keywords("RandomTool")
    assert "developer tools" in result.lower()
    assert "productivity" in result.lower()


def test_generate_keywords_html():
    result = generate_keywords("HTML Encoder")
    assert "html" in result.lower()
    assert "web development" in result.lower()


def test_generate_keywords_css():
    result = generate_keywords("CSS Gradient Studio")
    assert "css" in result.lower()
    assert "web design" in result.lower()


def test_generate_keywords_json():
    result = generate_keywords("JSON Formatter")
    assert "json" in result.lower()


def test_generate_description_returns_string():
    result = generate_description("UUID Generator Pro", "uuid-generator-pro")
    assert isinstance(result, str)
    assert len(result) > 20


def test_generate_description_consistent():
    r1 = generate_description("Test Tool", "test-tool")
    r2 = generate_description("Test Tool", "test-tool")
    assert r1 == r2


def test_generate_description_different_slugs():
    r1 = generate_description("Tool A", "tool-a")
    r2 = generate_description("Tool B", "tool-b")
    assert isinstance(r1, str) and isinstance(r2, str)


def test_find_index_html_exists():
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "test-slug"
        prod_dir = Path(tmpdir) / "products" / slug
        prod_dir.mkdir(parents=True)
        (prod_dir / "index.html").write_text("<html></html>")
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = find_index_html(slug)
        finally:
            os.chdir(orig_cwd)
        assert result is not None


def test_find_index_html_not_exists():
    with tempfile.TemporaryDirectory() as tmpdir:
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = find_index_html("no-such-slug")
        finally:
            os.chdir(orig_cwd)
        assert result is None


def test_update_product_seo_no_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            ok, msg = update_product_seo({"slug": "nonexistent", "name": "X", "vercel_url": "https://x.com"})
        finally:
            os.chdir(orig_cwd)
        assert ok is False
        assert "bulunamadı" in msg


def test_update_product_seo_success():
    html = '<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><title>Old</title></head><body></body></html>'
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "test-slug"
        prod_dir = Path(tmpdir) / "products" / slug
        prod_dir.mkdir(parents=True)
        (prod_dir / "index.html").write_text(html)
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            ok, msg = update_product_seo({"slug": slug, "name": "Test Slug", "vercel_url": "https://test-slug.vercel.app"})
        finally:
            os.chdir(orig_cwd)
        assert ok is True
        content = (prod_dir / "index.html").read_text()
        assert "Test Slug" in content
        assert 'application/ld+json' in content


def test_update_product_seo_adds_canonical():
    html = '<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><title>T</title></head><body></body></html>'
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "my-tool"
        prod_dir = Path(tmpdir) / "products" / slug
        prod_dir.mkdir(parents=True)
        (prod_dir / "index.html").write_text(html)
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            ok, msg = update_product_seo({"slug": slug, "name": "My Tool", "vercel_url": "https://my-tool.vercel.app"})
        finally:
            os.chdir(orig_cwd)
        assert ok is True
        content = (prod_dir / "index.html").read_text()
        assert "my-tool.vercel.app" in content


def test_update_product_seo_adds_robots():
    html = '<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><title>T</title></head><body></body></html>'
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "robots-test"
        prod_dir = Path(tmpdir) / "products" / slug
        prod_dir.mkdir(parents=True)
        (prod_dir / "index.html").write_text(html)
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            ok, msg = update_product_seo({"slug": slug, "name": "Robots Test", "vercel_url": "https://r.com"})
        finally:
            os.chdir(orig_cwd)
        assert ok is True
        content = (prod_dir / "index.html").read_text()
        assert 'meta name="description"' in content
