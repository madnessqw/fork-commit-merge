#!/usr/bin/env python3
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from seo_mass_optimize import find_index_html, add_seo_to_product, update_state_json, JSON_LD_TEMPLATE, PRODUCTS


def test_find_index_html_public():
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "test-slug"
        pub_dir = Path(tmpdir) / "products" / slug / "public"
        pub_dir.mkdir(parents=True)
        (pub_dir / "index.html").write_text("<html></html>")
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = find_index_html(slug)
        finally:
            os.chdir(orig_cwd)
        assert result is not None
        assert "public/index.html" in result


def test_find_index_html_root():
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
        assert "public" not in result


def test_find_index_html_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            result = find_index_html("nonexistent")
        finally:
            os.chdir(orig_cwd)
        assert result is None


def test_add_seo_to_product_no_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            product = {"slug": "nonexistent", "name": "Test", "description": "d", "price": "9.00", "category": "Dev", "url": "http://x.com"}
            result = add_seo_to_product(product)
        finally:
            os.chdir(orig_cwd)
        assert result["status"] == "error"
        assert "not found" in result["message"]


def test_add_seo_to_product_success():
    html = '<html><head></head><body></body></html>'
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "toml-toolkit"
        prod_dir = Path(tmpdir) / "products" / slug
        prod_dir.mkdir(parents=True)
        (prod_dir / "index.html").write_text(html)
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            product = {"slug": slug, "name": "TOML Toolkit", "description": "Test desc", "price": "9.00", "category": "Dev", "url": "http://x.com"}
            result = add_seo_to_product(product)
        finally:
            os.chdir(orig_cwd)
        assert result["status"] == "success"
        content = (prod_dir / "index.html").read_text()
        assert "application/ld+json" in content


def test_add_seo_skips_existing():
    html = '<html><head><script type="application/ld+json">{"@type":"Thing"}</script></head><body></body></html>'
    with tempfile.TemporaryDirectory() as tmpdir:
        slug = "toml-toolkit"
        prod_dir = Path(tmpdir) / "products" / slug
        prod_dir.mkdir(parents=True)
        (prod_dir / "index.html").write_text(html)
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            product = {"slug": slug, "name": "TOML Toolkit", "description": "Test", "price": "9.00", "category": "Dev", "url": "http://x.com"}
            result = add_seo_to_product(product)
        finally:
            os.chdir(orig_cwd)
        assert result["status"] == "skipped"


def test_products_list_valid():
    for p in PRODUCTS:
        assert "slug" in p
        assert "name" in p
        assert "description" in p
        assert "price" in p
        assert "category" in p
        assert "url" in p
        assert len(p["slug"]) > 0


def test_json_ld_template_format():
    result = JSON_LD_TEMPLATE.format(
        name="Test App", description="Test desc",
        category="Dev", price="9.00"
    )
    assert "Test App" in result
    assert "9.00" in result
    assert "schema.org" in result


def test_update_state_json():
    state = {"products": {"active": [{"slug": "toml-toolkit"}, {"slug": "other"}]}}
    with tempfile.TemporaryDirectory() as tmpdir:
        state_file = Path(tmpdir) / "STATE.json"
        state_file.write_text(json.dumps(state))
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            count = update_state_json(["toml-toolkit"])
        finally:
            os.chdir(orig_cwd)
        assert count == 1
        updated = json.loads(state_file.read_text())
        for p in updated["products"]["active"]:
            if p["slug"] == "toml-toolkit":
                assert p["seo_optimized"] is True
            else:
                assert "seo_optimized" not in p
