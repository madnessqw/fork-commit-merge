#!/usr/bin/env python3
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from seo_fix_batch import fix_product, SEO_DATA, update_state_json


def test_fix_product_no_index_file():
    with patch.object(Path, 'exists', return_value=False):
        result = fix_product("nonexistent-slug")
    assert result is False


def test_fix_product_no_seo_data():
    html = "<html><head><title>Test</title></head><body></body></html>"
    with tempfile.TemporaryDirectory() as tmpdir:
        products_dir = Path(tmpdir) / "products" / "unknown-slug"
        products_dir.mkdir(parents=True)
        index_file = products_dir / "index.html"
        index_file.write_text(html, encoding='utf-8')
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = fix_product("unknown-slug")
        finally:
            os.chdir(orig_cwd)
    assert result is False


def test_fix_product_success():
    html = '<html><head><title>Chart Studio</title></head><body></body></html>'
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "chart-studio"
        products_dir = Path(tmpdir) / "products" / slug
        products_dir.mkdir(parents=True)
        index_file = products_dir / "index.html"
        index_file.write_text(html, encoding='utf-8')
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = fix_product(slug)
        finally:
            os.chdir(orig_cwd)
        if result:
            updated = index_file.read_text(encoding='utf-8')
            assert 'meta name="description"' in updated
            assert 'og:title' in updated or 'og:type' in updated
            assert 'application/ld+json' in updated


def test_fix_product_no_head_section():
    html = "<html><body>No head</body></html>"
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "chart-studio"
        products_dir = Path(tmpdir) / "products" / slug
        products_dir.mkdir(parents=True)
        index_file = products_dir / "index.html"
        index_file.write_text(html, encoding='utf-8')
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = fix_product(slug)
        finally:
            os.chdir(orig_cwd)
    assert result is False


def test_seo_data_has_required_fields():
    for slug, data in SEO_DATA.items():
        assert "description" in data, f"{slug}: missing description"
        assert "keywords" in data, f"{slug}: missing keywords"
        assert len(data["description"]) > 10, f"{slug}: description too short"


def test_seo_data_description_not_empty():
    for slug, data in SEO_DATA.items():
        assert data["description"].strip(), f"{slug}: empty description"


def test_update_state_json():
    state = {
        "products": {
            "active": [
                {"slug": "ai-cost-dashboard"},
                {"slug": "chart-studio"},
                {"slug": "other-product"},
            ]
        }
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = Path(tmpdir) / "STATE.json"
        state_file.write_text(json.dumps(state), encoding='utf-8')
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            count = update_state_json(["ai-cost-dashboard", "chart-studio"])
        finally:
            os.chdir(orig_cwd)
        updated_state = json.loads(state_file.read_text(encoding='utf-8'))
        for p in updated_state["products"]["active"]:
            if p["slug"] in ("ai-cost-dashboard", "chart-studio"):
                assert p["seo_optimized"] is True
                assert "seo_optimized_at" in p
            else:
                assert "seo_optimized" not in p


def test_fix_product_preserves_existing_styles():
    html = '<html><head><title>Chart Studio</title>\n<link rel="stylesheet" href="style.css">\n<style>body{margin:0}</style>\n</head><body></body></html>'
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "chart-studio"
        products_dir = Path(tmpdir) / "products" / slug
        products_dir.mkdir(parents=True)
        index_file = products_dir / "index.html"
        index_file.write_text(html, encoding='utf-8')
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = fix_product(slug)
        finally:
            os.chdir(orig_cwd)
        if result:
            updated = index_file.read_text(encoding='utf-8')
            assert 'style.css' in updated
            assert 'body{margin:0}' in updated


def test_seo_data_slugs_are_strings():
    for slug in SEO_DATA:
        assert isinstance(slug, str)
        assert "-" in slug or slug.isalpha()
