import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.fix_dead_checkout_buttons import (
    discover_dead_button_slugs,
    fix_dead_buttons,
    get_checkout_url,
)


@pytest.fixture
def tmp_product(tmp_path, monkeypatch):
    monkeypatch.setattr("scripts.fix_dead_checkout_buttons.ROOT", tmp_path)

    def _make(slug: str, checkout_url: str | None = None, html: str = "") -> Path:
        prod_dir = tmp_path / "products" / slug
        prod_dir.mkdir(parents=True, exist_ok=True)
        if checkout_url is not None:
            (prod_dir / "product.json").write_text(
                json.dumps({"checkout_url": checkout_url})
            )
        if html:
            (prod_dir / "index.html").write_text(html)
        return prod_dir

    return _make


class TestGetCheckoutUrl:
    def test_returns_url_when_present(self, tmp_product):
        tmp_product("test-slug", checkout_url="https://buy.polar.sh/abc123")
        assert get_checkout_url("test-slug") == "https://buy.polar.sh/abc123"

    def test_returns_none_when_missing(self, tmp_product):
        tmp_product("no-co", checkout_url=None)
        assert get_checkout_url("no-co") is None

    def test_returns_none_when_no_product_json(self, tmp_product):
        tmp_product("ghost", checkout_url=None, html="<html></html>")
        assert get_checkout_url("ghost") is None

    def test_returns_none_for_invalid_json(self, tmp_product):
        prod_dir = Path("/tmp") / "test_invalid_json_fix"
        prod_dir.mkdir(parents=True, exist_ok=True)
        (prod_dir / "product.json").write_text("NOT JSON")
        with patch("scripts.fix_dead_checkout_buttons.ROOT", Path("/tmp") / "test_invalid_json_fix"):
            (prod_dir / "products" / "x").mkdir(parents=True, exist_ok=True)
            (prod_dir / "products" / "x" / "product.json").write_text("NOT JSON")
            assert get_checkout_url("x") is None


class TestFixDeadButtons:
    def test_returns_false_when_no_index_html(self, tmp_product):
        tmp_product("no-html", checkout_url="https://buy.polar.sh/abc")
        assert fix_dead_buttons("no-html") is False

    def test_returns_false_when_no_checkout_url(self, tmp_product):
        tmp_product("no-url", html="<html><body><button>Buy Now $19</button></body></html>")
        assert fix_dead_buttons("no-url") is False

    def test_returns_false_when_already_wired(self, tmp_product):
        html = '<html><body><script>const CHECKOUT_URL = "https://buy.polar.sh/abc";</script></body></html>'
        tmp_product("already-fixed", checkout_url="https://buy.polar.sh/abc", html=html)
        assert fix_dead_buttons("already-fixed") is False

    def test_fixes_button_with_get_access(self, tmp_product):
        html = '<html><body><button class="buy-btn">Get Access - $19</button></body></html>'
        tmp_product("fix-me", checkout_url="https://buy.polar.sh/abc", html=html)
        result = fix_dead_buttons("fix-me")
        assert result is True
        fixed = (Path("/tmp") / "products" / "fix-me" / "index.html").read_text() if False else ""
        from pathlib import Path as P
        from scripts.fix_dead_checkout_buttons import ROOT as R
        fixed = (R / "products" / "fix-me" / "index.html").read_text()
        assert "CHECKOUT_URL" in fixed

    def test_fixes_dead_href_hash(self, tmp_product):
        html = '<html><body><a href="#">Get Access Now</a></body></html>'
        tmp_product("dead-link", checkout_url="https://buy.polar.sh/xyz", html=html)
        result = fix_dead_buttons("dead-link")
        assert result is True

    def test_fixes_pricing_anchor(self, tmp_product):
        html = '<html><body><a href="#pricing">Buy Now</a></body></html>'
        tmp_product("pricing-link", checkout_url="https://buy.polar.sh/pr", html=html)
        result = fix_dead_buttons("pricing-link")
        assert result is True

    def test_adds_checkout_script_to_body(self, tmp_product):
        html = '<html><body><p>No buttons</p></body></html>'
        tmp_product("no-buttons", checkout_url="https://buy.polar.sh/nb", html=html)
        result = fix_dead_buttons("no-buttons")
        assert result is True
        from scripts.fix_dead_checkout_buttons import ROOT
        fixed = (ROOT / "products" / "no-buttons" / "index.html").read_text()
        assert "window.open(CHECKOUT_URL" in fixed
        assert "</script>" in fixed


class TestDiscoverDeadButtonSlugs:
    def test_discovers_unwired_product(self, tmp_product):
        html = '<html><body><button class="buy-btn">Buy Now</button></body></html>'
        tmp_product("unwired-prod", checkout_url="https://buy.polar.sh/abc", html=html)
        slugs = discover_dead_button_slugs()
        assert "unwired-prod" in slugs

    def test_skips_already_wired(self, tmp_product):
        html = '<html><body><script>const CHECKOUT_URL = "https://buy.polar.sh/abc";</script></body></html>'
        tmp_product("wired-prod", checkout_url="https://buy.polar.sh/abc", html=html)
        slugs = discover_dead_button_slugs()
        assert "wired-prod" not in slugs

    def test_skips_no_checkout_url(self, tmp_product):
        html = '<html><body><button>Buy</button></body></html>'
        tmp_product("no-co-prod", checkout_url=None, html=html)
        slugs = discover_dead_button_slugs()
        assert "no-co-prod" not in slugs

    def test_returns_list(self):
        slugs = discover_dead_button_slugs()
        assert isinstance(slugs, list)
