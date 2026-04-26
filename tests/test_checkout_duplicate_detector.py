import json
import pytest
from pathlib import Path
from unittest.mock import patch
from scripts.checkout_duplicate_detector import (
    detect_duplicates,
    duplicate_summary,
    cleanup_suggestions,
    _slug_of,
    _checkout_of,
    _status_of,
    _url_of,
    _is_better_candidate,
)


def _make_product(slug="test-slug", checkout="https://buy.polar.sh/abc",
                  status="live", url="https://test-slug.vercel.app",
                  **extra):
    p = {"s": slug, "c": checkout, "st": status, "v": url}
    p.update(extra)
    return p


def _write_summary(tmp_path, products):
    summary = {"products": products}
    p = tmp_path / "STATE_SUMMARY.json"
    p.write_text(json.dumps(summary), encoding="utf-8")
    return p


class TestHelperFunctions:
    def test_slug_of_prefers_s(self):
        assert _slug_of({"s": "a", "slug": "b"}) == "a"

    def test_slug_of_fallback_slug(self):
        assert _slug_of({"slug": "b"}) == "b"

    def test_slug_of_fallback_name(self):
        assert _slug_of({"n": "My Product"}) == "My Product"

    def test_slug_of_unknown(self):
        assert _slug_of({}) == "unknown"

    def test_checkout_of_prefers_c(self):
        assert _checkout_of({"c": "https://a", "checkout_url": "https://b"}) == "https://a"

    def test_checkout_of_empty(self):
        assert _checkout_of({}) == ""

    def test_status_of_prefers_st(self):
        assert _status_of({"st": "live", "status": "pending"}) == "live"

    def test_status_of_empty(self):
        assert _status_of({}) == ""

    def test_url_of_prefers_v(self):
        assert _url_of({"v": "https://a", "vercel_url": "https://b"}) == "https://a"

    def test_url_of_empty(self):
        assert _url_of({}) == ""


class TestDetectDuplicates:
    def test_no_duplicates(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="a", checkout="https://buy.polar.sh/1"),
            _make_product(slug="b", checkout="https://buy.polar.sh/2"),
        ])
        assert detect_duplicates(p) == []

    def test_single_duplicate_group(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="a", checkout="https://buy.polar.sh/shared"),
            _make_product(slug="b", checkout="https://buy.polar.sh/shared"),
        ])
        dupes = detect_duplicates(p)
        assert len(dupes) == 1
        assert dupes[0]["count"] == 2
        slugs = {e["slug"] for e in dupes[0]["products"]}
        assert slugs == {"a", "b"}

    def test_multiple_groups_sorted_by_count(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="a1", checkout="https://buy.polar.sh/g1"),
            _make_product(slug="a2", checkout="https://buy.polar.sh/g1"),
            _make_product(slug="b1", checkout="https://buy.polar.sh/g2"),
            _make_product(slug="b2", checkout="https://buy.polar.sh/g2"),
            _make_product(slug="b3", checkout="https://buy.polar.sh/g2"),
        ])
        dupes = detect_duplicates(p)
        assert len(dupes) == 2
        assert dupes[0]["count"] == 3
        assert dupes[1]["count"] == 2

    def test_skips_non_http_checkout(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="a", checkout=""),
            _make_product(slug="b", checkout="not-a-url"),
        ])
        assert detect_duplicates(p) == []

    def test_skips_non_dict_products(self, tmp_path):
        p = _write_summary(tmp_path, ["not_a_dict", 42])
        assert detect_duplicates(p) == []

    def test_missing_file(self, tmp_path):
        assert detect_duplicates(tmp_path / "nonexistent.json") == []

    def test_invalid_json(self, tmp_path):
        bad = tmp_path / "STATE_SUMMARY.json"
        bad.write_text("NOT JSON", encoding="utf-8")
        assert detect_duplicates(bad) == []

    def test_no_products_key(self, tmp_path):
        p = tmp_path / "STATE_SUMMARY.json"
        p.write_text(json.dumps({"other": "data"}), encoding="utf-8")
        assert detect_duplicates(p) == []

    def test_products_not_list(self, tmp_path):
        p = tmp_path / "STATE_SUMMARY.json"
        p.write_text(json.dumps({"products": "not_list"}), encoding="utf-8")
        assert detect_duplicates(p) == []


class TestDuplicateSummary:
    def test_summary_structure(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="a", checkout="https://buy.polar.sh/s"),
            _make_product(slug="b", checkout="https://buy.polar.sh/s"),
            _make_product(slug="c", checkout="https://buy.polar.sh/other"),
        ])
        s = duplicate_summary(p)
        assert s["duplicate_groups"] == 1
        assert s["total_affected_products"] == 2
        assert s["redundant_products"] == 1
        assert "a" in s["slugs"]
        assert "b" in s["slugs"]

    def test_no_duplicates_summary(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="a", checkout="https://buy.polar.sh/1"),
        ])
        s = duplicate_summary(p)
        assert s["duplicate_groups"] == 0
        assert s["total_affected_products"] == 0
        assert s["redundant_products"] == 0


class TestCleanupSuggestions:
    def test_keep_canonical_url(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="foo", checkout="https://buy.polar.sh/s",
                          url="https://foo.vercel.app"),
            _make_product(slug="foo-alt", checkout="https://buy.polar.sh/s",
                          url="https://foo-alt-random.vercel.app"),
        ])
        suggestions = cleanup_suggestions(p)
        assert len(suggestions) == 1
        assert suggestions[0]["keep_slug"] == "foo"
        assert "foo-alt" in suggestions[0]["remove_slugs"]

    def test_keep_live_status(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="a", checkout="https://buy.polar.sh/s",
                          url="https://a-random.vercel.app", status="pending"),
            _make_product(slug="b", checkout="https://buy.polar.sh/s",
                          url="https://b-random.vercel.app", status="live"),
        ])
        suggestions = cleanup_suggestions(p)
        assert suggestions[0]["keep_slug"] == "b"

    def test_tiebreak_alphabetical(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="zebra", checkout="https://buy.polar.sh/s",
                          url="https://z-random.vercel.app", status="live"),
            _make_product(slug="alpha", checkout="https://buy.polar.sh/s",
                          url="https://a-random.vercel.app", status="live"),
        ])
        suggestions = cleanup_suggestions(p)
        assert suggestions[0]["keep_slug"] == "alpha"

    def test_no_suggestions_for_singletons(self, tmp_path):
        p = _write_summary(tmp_path, [
            _make_product(slug="a", checkout="https://buy.polar.sh/1"),
        ])
        assert cleanup_suggestions(p) == []


class TestIsBetterCandidate:
    def test_canonical_beats_noncanonical(self):
        c = {"slug": "x", "url": "https://x.vercel.app", "status": "live"}
        cu = {"slug": "y", "url": "https://y-other.vercel.app", "status": "live"}
        assert _is_better_candidate(c, cu) is True

    def test_noncanonical_loses_to_canonical(self):
        c = {"slug": "x", "url": "https://x-other.vercel.app", "status": "live"}
        cu = {"slug": "y", "url": "https://y.vercel.app", "status": "live"}
        assert _is_better_candidate(c, cu) is False

    def test_live_beats_nonlive(self):
        c = {"slug": "x", "url": "https://x-other.vercel.app", "status": "live"}
        cu = {"slug": "y", "url": "https://y-other.vercel.app", "status": "pending"}
        assert _is_better_candidate(c, cu) is True

    def test_alphabetical_tiebreak(self):
        c = {"slug": "aaa", "url": "https://aaa-other.vercel.app", "status": "live"}
        cu = {"slug": "zzz", "url": "https://zzz-other.vercel.app", "status": "live"}
        assert _is_better_candidate(c, cu) is True
