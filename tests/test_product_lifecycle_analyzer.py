"""Tests for product_lifecycle_analyzer module."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.product_lifecycle_analyzer import (
    STAGE_ORDER,
    analyze_portfolio,
    classify_product,
    find_at_risk,
    lifecycle_summary,
    stage_health_score,
)

GOOD = {
    "n": "Good Product",
    "s": "good-product",
    "st": "live",
    "v": "https://good-product.vercel.app",
    "c": "https://buy.polar.sh/polar_cl_abc123",
}

NO_CHECKOUT = {
    "n": "No Checkout",
    "s": "no-checkout",
    "st": "live",
    "v": "https://no-checkout.vercel.app",
    "c": "",
}

NO_URL = {
    "n": "No URL",
    "s": "no-url",
    "st": "live",
    "v": "",
    "c": "https://buy.polar.sh/polar_cl_xyz",
}

ZOMBIE = {
    "n": "Zombie",
    "s": "zombie-prod",
    "st": "draft",
    "v": "https://zombie.vercel.app",
    "c": "https://buy.polar.sh/polar_cl_dead",
}

MOCK_SUMMARY = {"products": [GOOD, NO_CHECKOUT, NO_URL, ZOMBIE]}


class TestClassifyProduct:
    def test_healthy(self):
        assert classify_product(GOOD) == "healthy"

    def test_no_checkout(self):
        assert classify_product(NO_CHECKOUT) == "no_checkout"

    def test_no_url(self):
        assert classify_product(NO_URL) == "no_url"

    def test_zombie(self):
        assert classify_product(ZOMBIE) == "zombie"

    def test_empty_product(self):
        assert classify_product({}) == "zombie"

    def test_live_no_checkout_no_url(self):
        p = {"st": "live", "v": "", "c": ""}
        assert classify_product(p) == "no_url"


class TestAnalyzePortfolio:
    def test_all_stages(self, tmp_path):
        sf = tmp_path / "STATE_SUMMARY.json"
        sf.write_text(json.dumps(MOCK_SUMMARY))
        stages = analyze_portfolio(summary_path=sf)
        assert len(stages["healthy"]) == 1
        assert len(stages["no_checkout"]) == 1
        assert len(stages["no_url"]) == 1
        assert len(stages["zombie"]) == 1

    def test_empty_products(self, tmp_path):
        sf = tmp_path / "STATE_SUMMARY.json"
        sf.write_text(json.dumps({"products": []}))
        stages = analyze_portfolio(summary_path=sf)
        assert all(len(v) == 0 for v in stages.values())


class TestLifecycleSummary:
    def test_counts(self):
        stages = {"healthy": [GOOD, GOOD], "zombie": [ZOMBIE]}
        s = lifecycle_summary(stages)
        assert s["healthy"] == 2
        assert s["zombie"] == 1

    def test_empty(self):
        s = lifecycle_summary({})
        assert s == {}


class TestStageHealthScore:
    def test_100_percent(self):
        stages = {"healthy": [{"slug": "a"}], "no_url": []}
        assert stage_health_score(stages) == 100.0

    def test_50_percent(self):
        stages = {"healthy": [{}], "no_checkout": [{}]}
        assert stage_health_score(stages) == 50.0

    def test_zero(self):
        stages = {"healthy": [], "zombie": [{}]}
        assert stage_health_score(stages) == 0.0

    def test_empty_portfolio(self):
        assert stage_health_score({}) == 0.0


class TestFindAtRisk:
    def test_finds_risk(self):
        stages = {
            "healthy": [GOOD],
            "no_checkout": [NO_CHECKOUT],
            "no_url": [NO_URL],
            "zombie": [ZOMBIE],
        }
        at_risk = find_at_risk(stages)
        assert len(at_risk) == 3

    def test_limit(self):
        stages = {"no_checkout": [{"slug": f"p{i}"} for i in range(20)]}
        at_risk = find_at_risk(stages, limit=5)
        assert len(at_risk) == 5

    def test_no_risk(self):
        stages = {"healthy": [GOOD], "no_checkout": []}
        at_risk = find_at_risk(stages)
        assert at_risk == []
