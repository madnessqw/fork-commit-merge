import json
from pathlib import Path

from scripts.product_readiness_scorer import (
    DIMENSIONS,
    _has_canonical_url,
    _has_valid_checkout,
    _has_valid_price,
    _is_checkout_active,
    _is_healthy,
    _is_og_optimized,
    _is_schema_optimized,
    _is_seo_optimized,
    score_portfolio,
    score_product,
)


def _perfect_product(**overrides):
    base = {
        "slug": "test-product",
        "s": "test-product",
        "name": "Test Product",
        "n": "Test Product",
        "status": "live",
        "st": "live",
        "health_status": "healthy",
        "last_health_code": 200,
        "vercel_url": "https://test-product.vercel.app",
        "v": "https://test-product.vercel.app",
        "ideal_vercel_url": "https://test-product.vercel.app",
        "price": "9",
        "checkout_url": "https://buy.polar.sh/polar_cl_abc123",
        "c": "https://buy.polar.sh/polar_cl_abc123",
        "checkout_status": "active",
        "seo_optimized": True,
        "og_optimized": True,
        "schema_optimized": True,
    }
    base.update(overrides)
    return base


def test_perfect_product_scores_100():
    p = _perfect_product()
    result = score_product(p)
    assert result["score"] == 100.0
    assert result["points"] == 100
    assert len(result["failed"]) == 0


def test_unhealthy_product():
    p = _perfect_product(health_status="unhealthy", last_health_code=500)
    result = score_product(p)
    assert "healthy" in result["failed"]
    assert result["score"] < 100


def test_no_price():
    p = _perfect_product(price=None)
    result = score_product(p)
    assert "valid_price" in result["failed"]


def test_zero_price():
    p = _perfect_product(price="0")
    result = score_product(p)
    assert "valid_price" in result["failed"]


def test_no_checkout():
    p = _perfect_product(checkout_url="", c="")
    result = score_product(p)
    assert "valid_checkout" in result["failed"]


def test_canonical_mismatch():
    p = _perfect_product(vercel_url="https://alias.vercel.app")
    result = score_product(p)
    assert "canonical_url" in result["failed"]


def test_seo_not_optimized():
    p = _perfect_product(seo_optimized=False)
    result = score_product(p)
    assert "seo_optimized" in result["failed"]


def test_og_not_optimized():
    p = _perfect_product(og_optimized=False)
    result = score_product(p)
    assert "og_optimized" in result["failed"]


def test_schema_not_optimized():
    p = _perfect_product(schema_optimized=False)
    result = score_product(p)
    assert "schema_optimized" in result["failed"]


def test_checkout_not_active():
    p = _perfect_product(checkout_status="inactive")
    result = score_product(p)
    assert "checkout_active" in result["failed"]


def test_price_with_dollar_sign():
    assert _has_valid_price({"price": "$15"}) is True


def test_price_non_numeric():
    assert _has_valid_price({"price": "free"}) is False


def test_price_none():
    assert _has_valid_price({"price": None}) is False


def test_checkout_non_polar():
    assert _has_valid_checkout({"checkout_url": "https://stripe.com/pay/123"}) is False


def test_checkout_empty():
    assert _has_valid_checkout({}) is False


def test_healthy_checks():
    assert _is_healthy({"health_status": "healthy", "last_health_code": 200}) is True
    assert _is_healthy({"health_status": "healthy", "last_health_code": 500}) is False
    assert _is_healthy({"health_status": "unhealthy", "last_health_code": 200}) is False


def test_canonical_url_checks():
    assert _has_canonical_url({
        "vercel_url": "https://x.vercel.app",
        "ideal_vercel_url": "https://x.vercel.app",
    }) is True
    assert _has_canonical_url({
        "vercel_url": "https://alias.vercel.app",
        "ideal_vercel_url": "https://x.vercel.app",
    }) is False


def test_score_portfolio_empty(tmp_path):
    state_file = tmp_path / "STATE.json"
    state_file.write_text("{}")
    result = score_portfolio(state_path=state_file)
    assert result["total"] == 0
    assert result["avg_score"] == 0


def test_score_portfolio_with_products(tmp_path):
    state = {
        "products": {
            "active": [
                _perfect_product(slug="a", s="a", n="A"),
                _perfect_product(slug="b", s="b", n="B", price=None),
            ]
        }
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))
    result = score_portfolio(state_path=state_file)
    assert result["total"] == 2
    assert result["ready_count"] == 1
    assert result["needs_attention_count"] == 1
    assert "valid_price" in result["failing_dimensions"]


def test_dimensions_weight_sum():
    total_weight = sum(w for _, w, _ in DIMENSIONS)
    assert total_weight == 100


def test_slug_fallback():
    p = {"n": "Some Name", "s": "some-name"}
    result = score_product(p)
    assert result["slug"] == "some-name"


def test_bottom_5_sorted(tmp_path):
    products = []
    dims = [
        ("perfect", {}),
        ("no_seo", {"seo_optimized": False}),
        ("no_og", {"og_optimized": False}),
        ("no_schema", {"schema_optimized": False}),
        ("no_price", {"price": None}),
        ("no_checkout", {"checkout_url": "", "c": "", "checkout_status": "inactive"}),
    ]
    for i, (slug, overrides) in enumerate(dims):
        products.append(_perfect_product(slug=slug, s=slug, n=slug, **overrides))

    state = {"products": {"active": products}}
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))
    result = score_portfolio(state_path=state_file)
    assert len(result["bottom_5"]) == 5
    scores_by_slug = {s["slug"]: s["score"] for s in result["scores"]}
    assert scores_by_slug["no_checkout"] < scores_by_slug["no_price"]
