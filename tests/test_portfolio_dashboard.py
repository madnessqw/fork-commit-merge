import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.portfolio_dashboard import (
    category_breakdown,
    checkout_coverage,
    generate_dashboard,
    load_json,
    load_products,
    status_breakdown,
    tag_analysis,
    url_health,
)


@pytest.fixture
def sample_products():
    return [
        {"_dir": "prod-a", "name": "Prod A", "slug": "prod-a", "status": "live",
         "category": "dev-tools", "tags": ["generator", "utility"],
         "vercel_url": "https://prod-a.vercel.app",
         "checkout_url": "https://buy.polar.sh/abc"},
        {"_dir": "prod-b", "name": "Prod B", "slug": "prod-b", "status": "live",
         "category": "dev-tools", "tags": ["validator"],
         "vercel_url": "https://prod-b.vercel.app",
         "checkout_url": ""},
        {"_dir": "prod-c", "name": "Prod C", "slug": "prod-c", "status": "pending",
         "category": "security", "tags": ["scanner", "security"],
         "vercel_url": "",
         "checkout_url": ""},
    ]


def test_status_breakdown(sample_products):
    result = status_breakdown(sample_products)
    assert result["live"] == 2
    assert result["pending"] == 1


def test_category_breakdown(sample_products):
    result = category_breakdown(sample_products)
    assert result["dev-tools"] == 2
    assert result["security"] == 1


def test_checkout_coverage(sample_products):
    result = checkout_coverage(sample_products)
    assert result["total"] == 3
    assert result["with_checkout"] == 1
    assert result["without"] == 2
    assert result["percentage"] == pytest.approx(33.3, abs=0.1)


def test_checkout_coverage_empty():
    assert checkout_coverage([])["percentage"] == 0


def test_tag_analysis(sample_products):
    result = tag_analysis(sample_products)
    tags = {t for t, _ in result}
    assert "generator" in tags
    assert "security" in tags


def test_tag_analysis_empty():
    assert tag_analysis([]) == []


def test_url_health(sample_products):
    result = url_health(sample_products)
    assert result["missing_vercel_url"] == 1
    assert result["missing_checkout_url"] == 2
    assert "prod-c" in result["missing_vercel_list"]
    assert "prod-b" in result["missing_checkout_list"]


def test_load_json_missing():
    assert load_json("/nonexistent/path.json") == {}


def test_load_json_invalid(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{invalid")
    assert load_json(str(bad)) == {}


def test_load_json_valid(tmp_path):
    good = tmp_path / "good.json"
    good.write_text('{"key": "val"}')
    assert load_json(str(good)) == {"key": "val"}


def test_load_products_no_dir(tmp_path):
    with patch("scripts.portfolio_dashboard.PRODUCTS_DIR", tmp_path / "missing"):
        assert load_products() == []


def test_load_products_with_data(tmp_path):
    prod_dir = tmp_path / "products" / "test-prod"
    prod_dir.mkdir(parents=True)
    (prod_dir / "product.json").write_text(json.dumps({
        "name": "Test", "slug": "test-prod", "status": "live"
    }))
    with patch("scripts.portfolio_dashboard.PRODUCTS_DIR", tmp_path / "products"):
        result = load_products()
        assert len(result) == 1
        assert result[0]["name"] == "Test"
        assert result[0]["_dir"] == "test-prod"


def test_load_products_skips_bad_json(tmp_path):
    prod_dir = tmp_path / "products" / "bad-prod"
    prod_dir.mkdir(parents=True)
    (prod_dir / "product.json").write_text("{bad")
    with patch("scripts.portfolio_dashboard.PRODUCTS_DIR", tmp_path / "products"):
        assert load_products() == []


def test_load_products_skips_files(tmp_path):
    products = tmp_path / "products"
    products.mkdir()
    (products / "readme.md").write_text("not a dir")
    with patch("scripts.portfolio_dashboard.PRODUCTS_DIR", products):
        assert load_products() == []


def test_generate_dashboard_basic():
    with patch("scripts.portfolio_dashboard.load_products", return_value=[
        {"_dir": "x", "name": "X", "slug": "x", "status": "live",
         "category": "tools", "tags": [], "vercel_url": "https://x.vercel.app",
         "checkout_url": "https://buy.polar.sh/x"}
    ]):
        d = generate_dashboard()
        assert d["total_products"] == 1
        assert "generated_at" in d
        assert d["checkout"]["with_checkout"] == 1


def test_generate_dashboard_with_summary():
    with patch("scripts.portfolio_dashboard.load_products", return_value=[]), \
         patch("scripts.portfolio_dashboard.load_json", return_value={"cycle": 42, "healthy_count": 100, "live_count": 110, "deploy_missing_or_bad_url": 5}):
        d = generate_dashboard()
        assert d["state_summary_cycle"] == 42
        assert d["state_summary_healthy"] == "100/110"


def test_generate_dashboard_include_details():
    with patch("scripts.portfolio_dashboard.load_products", return_value=[]):
        d = generate_dashboard(include_details=True)
        assert "stale_products" in d


def test_generate_dashboard_no_details():
    with patch("scripts.portfolio_dashboard.load_products", return_value=[]):
        d = generate_dashboard(include_details=False)
        assert "stale_products" not in d


def test_checkout_coverage_all_covered():
    prods = [
        {"checkout_url": "https://buy.polar.sh/a"},
        {"checkout_url": "https://buy.polar.sh/b"},
    ]
    result = checkout_coverage(prods)
    assert result["percentage"] == 100.0
    assert result["without"] == 0


def test_url_health_all_healthy():
    prods = [
        {"_dir": "a", "vercel_url": "https://a.vercel.app", "checkout_url": "https://buy.polar.sh/a"},
    ]
    result = url_health(prods)
    assert result["missing_vercel_url"] == 0
    assert result["missing_checkout_url"] == 0


def test_tag_analysis_counts_correctly():
    prods = [
        {"tags": ["Generator", "generator", "Utility"]},
        {"tags": ["generator"]},
    ]
    result = tag_analysis(prods)
    gen_count = next(c for t, c in result if t == "generator")
    assert gen_count == 3
