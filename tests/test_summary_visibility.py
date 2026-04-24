"""Tests for scripts.summary_visibility — canonical drift & fallback helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.summary_visibility import (
    apply_drift_fix_to_state,
    canonical_drift_count,
    canonical_drift_entries,
    drift_products_from_state,
    fallback_healthy_count,
    fallback_healthy_entries,
    _has_value,
    _ideal_url,
    _normalize_url,
    _summary_products_by_slug,
    _visible_public_url,
)


class TestHasValue:
    def test_none_is_false(self):
        assert _has_value(None) is False

    def test_empty_string_is_false(self):
        assert _has_value("") is False

    def test_whitespace_string_is_false(self):
        assert _has_value("   ") is False

    def test_nonempty_string_is_true(self):
        assert _has_value("hello") is True

    def test_zero_is_true(self):
        assert _has_value(0) is True

    def test_list_is_true(self):
        assert _has_value([]) is True


class TestNormalizeUrl:
    def test_none_returns_none(self):
        assert _normalize_url(None) is None

    def test_empty_returns_none(self):
        assert _normalize_url("") is None

    def test_whitespace_returns_none(self):
        assert _normalize_url("   ") is None

    def test_trailing_slash_stripped(self):
        assert _normalize_url("https://example.com/") == "https://example.com"

    def test_clean_url_unchanged(self):
        assert _normalize_url("https://example.com") == "https://example.com"


class TestIdealUrl:
    def test_slug_produces_vercel_url(self):
        assert _ideal_url("jwt-generator") == "https://jwt-generator.vercel.app"

    def test_none_returns_none(self):
        assert _ideal_url(None) is None

    def test_empty_returns_none(self):
        assert _ideal_url("") is None


class TestSummaryProductsBySlug:
    def test_empty_list(self):
        assert _summary_products_by_slug({}) == {}
        assert _summary_products_by_slug({"products": []}) == {}

    def test_indexed_by_s_key(self):
        summary = {"products": [{"s": "foo", "v": "http://a"}, {"s": "bar"}]}
        result = _summary_products_by_slug(summary)
        assert "foo" in result
        assert "bar" in result
        assert result["foo"]["v"] == "http://a"

    def test_indexed_by_slug_key(self):
        summary = {"products": [{"slug": "baz"}]}
        result = _summary_products_by_slug(summary)
        assert "baz" in result

    def test_skips_non_dict_items(self):
        summary = {"products": ["not-a-dict", 42, {"s": "ok"}]}
        result = _summary_products_by_slug(summary)
        assert len(result) == 1
        assert "ok" in result


class TestVisiblePublicUrl:
    def test_none_input(self):
        assert _visible_public_url(None) is None

    def test_non_dict_input(self):
        assert _visible_public_url("string") is None

    def test_v_key_preferred(self):
        assert _visible_public_url({"v": "https://a.com"}) == "https://a.com"

    def test_fallback_to_vercel_url(self):
        assert (
            _visible_public_url({"vercel_url": "https://b.com"})
            == "https://b.com"
        )

    def test_all_empty_returns_none(self):
        assert _visible_public_url({"v": "", "vercel_url": None}) is None


class TestCanonicalDriftEntries:
    def test_from_gaps_key(self):
        summary = {
            "gaps": {
                "canonical_url_drift": [
                    {"slug": "pdf-forge", "url": "https://alt.vercel.app", "ideal_url": "https://pdf-forge.vercel.app"}
                ]
            }
        }
        entries = canonical_drift_entries(summary)
        assert len(entries) == 1
        assert entries[0]["slug"] == "pdf-forge"

    def test_from_canonical_drift_products(self):
        summary = {
            "canonical_url_drift_products": ["webhook-tester"],
            "products": [{"s": "webhook-tester", "v": "https://webhook-tester-beryl.vercel.app"}],
        }
        entries = canonical_drift_entries(summary)
        assert len(entries) == 1
        assert entries[0]["slug"] == "webhook-tester"

    def test_empty_summary_returns_empty(self):
        assert canonical_drift_entries({}) == []


class TestCanonicalDriftCount:
    def test_from_numeric_field(self):
        assert canonical_drift_count({"canonical_url_drift": 7}) == 7

    def test_from_list_field(self):
        assert canonical_drift_count({"canonical_url_drift": [1, 2, 3]}) == 3

    def test_from_entries_fallback(self):
        summary = {
            "gaps": {
                "canonical_url_drift": [
                    {"slug": "a"},
                    {"slug": "b"},
                ]
            }
        }
        assert canonical_drift_count(summary) == 2

    def test_empty_is_zero(self):
        assert canonical_drift_count({}) == 0


class TestFallbackHealthyEntries:
    def test_from_gaps_fallback_healthy(self):
        summary = {
            "gaps": {
                "fallback_healthy": [
                    {"slug": "pdf-forge", "health_status": "alternate_healthy"}
                ]
            }
        }
        entries = fallback_healthy_entries(summary)
        assert len(entries) == 1

    def test_falls_through_to_canonical_drift(self):
        summary = {
            "gaps": {"canonical_url_drift": [{"slug": "x"}]},
        }
        entries = fallback_healthy_entries(summary)
        assert len(entries) == 1

    def test_empty_returns_empty_list(self):
        assert fallback_healthy_entries({}) == []


class TestFallbackHealthyCount:
    def test_from_numeric_field(self):
        assert fallback_healthy_count({"fallback_healthy_count": 4}) == 4

    def test_from_entries_fallback(self):
        summary = {
            "gaps": {"fallback_healthy": [{"slug": "a"}, {"slug": "b"}]},
        }
        assert fallback_healthy_count(summary) == 2

    def test_empty_is_zero(self):
        assert fallback_healthy_count({}) == 0


class TestDriftProductsFromState:
    def test_finds_alternate_healthy_drift(self):
        state = {
            "products": {
                "active": [
                    {
                        "slug": "jwt-gen",
                        "health_status": "alternate_healthy",
                        "ideal_vercel_url": "https://jwt-gen.vercel.app",
                        "deployment_url": "https://jwt-gen-rho.vercel.app",
                    }
                ]
            }
        }
        result = drift_products_from_state(state)
        assert len(result) == 1
        assert result[0]["slug"] == "jwt-gen"
        assert result[0]["ideal_url"] == "https://jwt-gen.vercel.app"
        assert result[0]["deployment_url"] == "https://jwt-gen-rho.vercel.app"

    def test_ignores_healthy_products(self):
        state = {
            "products": {
                "active": [
                    {
                        "slug": "ok-prod",
                        "health_status": "healthy",
                        "ideal_vercel_url": "https://ok-prod.vercel.app",
                        "deployment_url": "https://ok-prod.vercel.app",
                    }
                ]
            }
        }
        assert drift_products_from_state(state) == []

    def test_ignores_when_urls_match(self):
        state = {
            "products": {
                "active": [
                    {
                        "slug": "no-drift",
                        "health_status": "alternate_healthy",
                        "ideal_vercel_url": "https://no-drift.vercel.app",
                        "deployment_url": "https://no-drift.vercel.app",
                    }
                ]
            }
        }
        assert drift_products_from_state(state) == []

    def test_handles_missing_products_key(self):
        assert drift_products_from_state({}) == []

    def test_handles_non_dict_product(self):
        state = {"products": {"active": ["not-a-dict"]}}
        assert drift_products_from_state(state) == []


class TestApplyDriftFixToState:
    def _sample_state(self):
        return {
            "products": {
                "active": [
                    {
                        "slug": "jwt-gen",
                        "health_status": "alternate_healthy",
                        "ideal_vercel_url": "https://jwt-gen.vercel.app",
                        "deployment_url": "https://jwt-gen-rho.vercel.app",
                        "canonical_health_status": "error_500",
                    },
                    {
                        "slug": "pdf-forge",
                        "health_status": "alternate_healthy",
                        "ideal_vercel_url": "https://pdf-forge.vercel.app",
                        "deployment_url": "https://pdf-forge-five.vercel.app",
                        "canonical_health_status": "error_500",
                    },
                    {
                        "slug": "ok-prod",
                        "health_status": "healthy",
                        "ideal_vercel_url": "https://ok-prod.vercel.app",
                        "deployment_url": "https://ok-prod.vercel.app",
                    },
                ]
            }
        }

    def test_dry_run_does_not_modify_state(self):
        state = self._sample_state()
        report = apply_drift_fix_to_state(state, dry_run=True)
        assert report["dry_run"] is True
        assert report["checked"] == 2
        assert report["fixed"] == 0
        assert len(report["fixes"]) == 2
        assert state["products"]["active"][0]["ideal_vercel_url"] == "https://jwt-gen.vercel.app"

    def test_applies_fix_to_state(self):
        state = self._sample_state()
        report = apply_drift_fix_to_state(state)
        assert report["checked"] == 2
        assert report["fixed"] == 2
        assert state["products"]["active"][0]["ideal_vercel_url"] == "https://jwt-gen-rho.vercel.app"
        assert state["products"]["active"][1]["ideal_vercel_url"] == "https://pdf-forge-five.vercel.app"

    def test_slug_filter(self):
        state = self._sample_state()
        report = apply_drift_fix_to_state(state, slugs=["jwt-gen"])
        assert report["checked"] == 1
        assert report["fixed"] == 1
        assert state["products"]["active"][1]["ideal_vercel_url"] == "https://pdf-forge.vercel.app"

    def test_no_drift_returns_empty(self):
        state = {
            "products": {
                "active": [
                    {
                        "slug": "ok-prod",
                        "health_status": "healthy",
                        "ideal_vercel_url": "https://ok-prod.vercel.app",
                        "deployment_url": "https://ok-prod.vercel.app",
                    }
                ]
            }
        }
        report = apply_drift_fix_to_state(state)
        assert report["checked"] == 0
        assert report["fixed"] == 0
