"""Tests for scripts.checkout_duplicate_detector"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_duplicate_detector import (
    cleanup_suggestions,
    detect_duplicates,
    duplicate_summary,
    _slug_of,
    _checkout_of,
    _status_of,
    _is_better_candidate,
)


def _make_summary(products):
    return {"products": products}


def _make_product(slug, checkout="https://buy.polar.sh/abc123", status="live", url=""):
    if not url:
        url = f"https://{slug}.vercel.app"
    return {"s": slug, "c": checkout, "st": status, "v": url}


@pytest.fixture
def tmp_summary(tmp_path):
    def _write(products):
        p = tmp_path / "summary.json"
        p.write_text(json.dumps(_make_summary(products)), encoding="utf-8")
        return p
    return _write


class TestSlugOf:
    def test_prefers_s_key(self):
        assert _slug_of({"s": "my-slug", "slug": "other", "n": "Name"}) == "my-slug"

    def test_falls_back_to_slug(self):
        assert _slug_of({"slug": "other", "n": "Name"}) == "other"

    def test_falls_back_to_n(self):
        assert _slug_of({"n": "Name"}) == "Name"

    def test_unknown_when_empty(self):
        assert _slug_of({}) == "unknown"


class TestCheckoutOf:
    def test_prefers_c_key(self):
        assert _checkout_of({"c": "https://buy.polar.sh/abc", "checkout_url": "other"}) == "https://buy.polar.sh/abc"

    def test_returns_empty_for_missing(self):
        assert _checkout_of({}) == ""


class TestStatusOf:
    def test_prefers_st_key(self):
        assert _status_of({"st": "live", "status": "building"}) == "live"


class TestDetectDuplicates:
    def test_no_duplicates(self, tmp_summary):
        p = tmp_summary([
            _make_product("slug-a", checkout="https://buy.polar.sh/a"),
            _make_product("slug-b", checkout="https://buy.polar.sh/b"),
        ])
        result = detect_duplicates(p)
        assert result == []

    def test_single_duplicate_pair(self, tmp_summary):
        checkout = "https://buy.polar.sh/shared"
        p = tmp_summary([
            _make_product("slug-a", checkout=checkout),
            _make_product("slug-b", checkout=checkout),
        ])
        result = detect_duplicates(p)
        assert len(result) == 1
        assert result[0]["count"] == 2
        slugs = {e["slug"] for e in result[0]["products"]}
        assert slugs == {"slug-a", "slug-b"}

    def test_multiple_groups(self, tmp_summary):
        co1 = "https://buy.polar.sh/group1"
        co2 = "https://buy.polar.sh/group2"
        p = tmp_summary([
            _make_product("a1", checkout=co1),
            _make_product("a2", checkout=co1),
            _make_product("b1", checkout=co2),
            _make_product("b2", checkout=co2),
            _make_product("b3", checkout=co2),
            _make_product("c1", checkout="https://buy.polar.sh/unique"),
        ])
        result = detect_duplicates(p)
        assert len(result) == 2
        counts = sorted(g["count"] for g in result)
        assert counts == [2, 3]

    def test_skips_non_http_checkout(self, tmp_summary):
        p = tmp_summary([
            {"s": "no-co", "c": "", "st": "live"},
            {"s": "bad-co", "c": "not-a-url", "st": "live"},
        ])
        result = detect_duplicates(p)
        assert result == []

    def test_handles_missing_file(self, tmp_path):
        result = detect_duplicates(tmp_path / "nonexistent.json")
        assert result == []

    def test_handles_invalid_json(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("not json", encoding="utf-8")
        result = detect_duplicates(bad)
        assert result == []

    def test_handles_non_list_products(self, tmp_summary):
        p = tmp_summary([])
        raw = json.loads(p.read_text())
        raw["products"] = "not a list"
        p.write_text(json.dumps(raw), encoding="utf-8")
        result = detect_duplicates(p)
        assert result == []


class TestDuplicateSummary:
    def test_summary_fields(self, tmp_summary):
        co = "https://buy.polar.sh/shared"
        p = tmp_summary([
            _make_product("a", checkout=co),
            _make_product("b", checkout=co),
            _make_product("c", checkout="https://buy.polar.sh/unique"),
        ])
        result = duplicate_summary(p)
        assert result["duplicate_groups"] == 1
        assert result["total_affected_products"] == 2
        assert result["redundant_products"] == 1
        assert "a" in result["slugs"]
        assert "b" in result["slugs"]

    def test_no_duplicates_summary(self, tmp_summary):
        p = tmp_summary([
            _make_product("a", checkout="https://buy.polar.sh/a"),
            _make_product("b", checkout="https://buy.polar.sh/b"),
        ])
        result = duplicate_summary(p)
        assert result["duplicate_groups"] == 0
        assert result["total_affected_products"] == 0
        assert result["redundant_products"] == 0


class TestIsBetterCandidate:
    def test_canonical_url_beats_non_canonical(self):
        c = {"slug": "my-tool", "url": "https://my-tool.vercel.app", "status": "building"}
        cur = {"slug": "my-tool-alt", "url": "https://my-tool-alt-git.vercel.app", "status": "live"}
        assert _is_better_candidate(c, cur) is True

    def test_live_beats_non_live(self):
        c = {"slug": "a", "url": "https://a-suffix.vercel.app", "status": "live"}
        cur = {"slug": "b", "url": "https://b-suffix.vercel.app", "status": "building"}
        assert _is_better_candidate(c, cur) is True

    def test_alphabetical_tiebreak(self):
        c = {"slug": "alpha", "url": "https://alpha-suffix.vercel.app", "status": "live"}
        cur = {"slug": "beta", "url": "https://beta-suffix.vercel.app", "status": "live"}
        assert _is_better_candidate(c, cur) is True


class TestCleanupSuggestions:
    def test_suggests_canonical_slug(self, tmp_summary):
        co = "https://buy.polar.sh/shared"
        p = tmp_summary([
            _make_product("uuid-generator-pro", checkout=co, url="https://uuid-generator-pro.vercel.app"),
            _make_product("uuid-generator", checkout=co, url="https://uuid-generator-git.vercel.app"),
        ])
        result = cleanup_suggestions(p)
        assert len(result) == 1
        assert result[0]["keep_slug"] == "uuid-generator-pro"
        assert "uuid-generator" in result[0]["remove_slugs"]

    def test_live_preferred_when_no_canonical(self, tmp_summary):
        co = "https://buy.polar.sh/shared"
        p = tmp_summary([
            _make_product("tool-a", checkout=co, status="building", url="https://tool-a-git.vercel.app"),
            _make_product("tool-b", checkout=co, status="live", url="https://tool-b-git.vercel.app"),
        ])
        result = cleanup_suggestions(p)
        assert result[0]["keep_slug"] == "tool-b"

    def test_no_suggestions_when_no_duplicates(self, tmp_summary):
        p = tmp_summary([
            _make_product("a", checkout="https://buy.polar.sh/a"),
        ])
        result = cleanup_suggestions(p)
        assert result == []
