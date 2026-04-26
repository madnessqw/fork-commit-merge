import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.product_status_timeline import (
    category_status_matrix,
    checkout_readiness,
    generate_timeline,
    ledger_mode_summary,
    load_ledger,
    load_products,
    recent_cycle_health,
    status_snapshot,
)


@pytest.fixture
def sample_products():
    return [
        {"_dir": "slug-a", "status": "live", "category": "dev-tools", "checkout_url": "https://polar.sh/checkout/a", "vercel_url": "https://slug-a.vercel.app"},
        {"_dir": "slug-b", "status": "live", "category": "dev-tools", "checkout_url": "", "vercel_url": "https://slug-b.vercel.app"},
        {"_dir": "slug-c", "status": "building", "category": "utilities", "checkout_url": "", "vercel_url": ""},
        {"_dir": "slug-d", "status": "live", "category": "ai-ml", "checkout_url": "https://polar.sh/checkout/d", "vercel_url": "https://slug-d.vercel.app"},
        {"_dir": "slug-e", "status": "pending", "category": "ai-ml", "checkout_url": "", "vercel_url": ""},
        {"_dir": "slug-f", "status": "inactive", "category": "uncategorized", "checkout_url": "", "vercel_url": ""},
    ]


@pytest.fixture
def sample_ledger(tmp_path):
    ledger_file = tmp_path / "run_ledger.jsonl"
    entries = [
        {"cycle": 1, "mode": "BUILD", "status": "success", "agent": "codex"},
        {"cycle": 2, "mode": "BUILD", "status": "success", "agent": "codex"},
        {"cycle": 3, "mode": "STRATEGY", "status": "fail", "agent": "codex"},
        {"cycle": 4, "mode": "BUILD", "status": "success", "agent": "glm"},
        {"cycle": 5, "mode": "INNOVATE", "status": "success", "agent": "glm"},
    ]
    with open(ledger_file, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")
    return ledger_file


def test_status_snapshot(sample_products):
    snap = status_snapshot(sample_products)
    assert snap["total"] == 6
    assert snap["live"] == 3
    assert snap["building"] == 1
    assert snap["pending"] == 1
    assert snap["inactive"] == 1


def test_status_snapshot_empty():
    assert status_snapshot([]) == {"total": 0, "live": 0, "building": 0, "pending": 0, "inactive": 0}


def test_category_status_matrix(sample_products):
    matrix = category_status_matrix(sample_products)
    assert matrix["dev-tools"]["live"] == 2
    assert matrix["ai-ml"]["live"] == 1
    assert matrix["ai-ml"]["pending"] == 1
    assert matrix["utilities"]["building"] == 1
    assert matrix["uncategorized"]["inactive"] == 1


def test_category_status_matrix_uncategorized():
    products = [{"_dir": "x", "status": "live"}]
    matrix = category_status_matrix(products)
    assert matrix["uncategorized"]["live"] == 1


def test_checkout_readiness(sample_products):
    co = checkout_readiness(sample_products)
    assert co["live_total"] == 3
    assert co["with_checkout"] == 2
    assert co["with_vercel_url"] == 3
    assert co["checkout_pct"] == 66.7
    assert co["url_pct"] == 100.0


def test_checkout_readiness_no_live():
    co = checkout_readiness([])
    assert co["live_total"] == 0
    assert co["checkout_pct"] == 0
    assert co["url_pct"] == 0


def test_checkout_readiness_all_with_checkout():
    products = [
        {"status": "live", "checkout_url": "https://polar.sh/x", "vercel_url": "https://x.vercel.app"},
        {"status": "live", "checkout_url": "https://polar.sh/y", "vercel_url": "https://y.vercel.app"},
    ]
    co = checkout_readiness(products)
    assert co["checkout_pct"] == 100.0
    assert co["url_pct"] == 100.0


def test_ledger_mode_summary(sample_ledger):
    with patch("scripts.product_status_timeline.LEDGER_PATH", sample_ledger):
        entries = load_ledger()
    summary = ledger_mode_summary(entries)
    assert summary["total_runs"] == 5
    assert summary["fail_count"] == 1
    assert summary["modes"]["BUILD"] == 3
    assert summary["modes"]["STRATEGY"] == 1
    assert summary["modes"]["INNOVATE"] == 1


def test_ledger_mode_summary_empty():
    summary = ledger_mode_summary([])
    assert summary["total_runs"] == 0
    assert summary["fail_count"] == 0


def test_recent_cycle_health(sample_ledger):
    with patch("scripts.product_status_timeline.LEDGER_PATH", sample_ledger):
        entries = load_ledger()
    recent = recent_cycle_health(entries, last_n=3)
    assert len(recent) == 3
    assert recent[0]["cycle"] == 3
    assert recent[1]["agent"] == "glm"
    assert recent[2]["mode"] == "INNOVATE"


def test_recent_cycle_health_empty():
    assert recent_cycle_health([]) == []


def test_recent_cycle_health_fewer_than_n(sample_ledger):
    with patch("scripts.product_status_timeline.LEDGER_PATH", sample_ledger):
        entries = load_ledger()
    recent = recent_cycle_health(entries, last_n=100)
    assert len(recent) == 5


def test_load_ledger_malformed(tmp_path):
    ledger_file = tmp_path / "bad.jsonl"
    with open(ledger_file, "w") as f:
        f.write("not json\n")
        f.write('{"cycle": 1}\n')
        f.write("\n")
    with patch("scripts.product_status_timeline.LEDGER_PATH", ledger_file):
        entries = load_ledger()
    assert len(entries) == 1
    assert entries[0]["cycle"] == 1


def test_load_products(tmp_path):
    prod_dir = tmp_path / "products" / "test-prod"
    prod_dir.mkdir(parents=True)
    (prod_dir / "product.json").write_text(json.dumps({"status": "live", "category": "test"}))
    not_prod = tmp_path / "products" / "not-a-product"
    not_prod.mkdir()
    with patch("scripts.product_status_timeline.PRODUCTS_DIR", tmp_path / "products"):
        products = load_products()
    assert len(products) == 1
    assert products[0]["_dir"] == "test-prod"


def test_load_products_bad_json(tmp_path):
    prod_dir = tmp_path / "products" / "bad-prod"
    prod_dir.mkdir(parents=True)
    (prod_dir / "product.json").write_text("NOT JSON!!!")
    with patch("scripts.product_status_timeline.PRODUCTS_DIR", tmp_path / "products"):
        products = load_products()
    assert len(products) == 0


def test_generate_timeline_structure(tmp_path, sample_products, sample_ledger):
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps({"cycle": 42, "mode": "BUILD"}))
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps({"cycle": 42, "mode": "BUILD"}))
    prod_dir = tmp_path / "products"
    prod_dir.mkdir()

    with patch("scripts.product_status_timeline.STATE_PATH", state_file), \
         patch("scripts.product_status_timeline.STATE_SUMMARY_PATH", summary_file), \
         patch("scripts.product_status_timeline.PRODUCTS_DIR", prod_dir), \
         patch("scripts.product_status_timeline.LEDGER_PATH", sample_ledger):
        timeline = generate_timeline()

    assert timeline["current_cycle"] == 42
    assert timeline["current_mode"] == "BUILD"
    assert "status_snapshot" in timeline
    assert "checkout_readiness" in timeline
    assert "ledger_summary" in timeline
    assert "recent_cycles" not in timeline


def test_generate_timeline_with_details(tmp_path, sample_ledger):
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps({"cycle": 99, "mode": "INNOVATE"}))
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps({"cycle": 99}))
    prod_dir = tmp_path / "products"
    prod_dir.mkdir()

    with patch("scripts.product_status_timeline.STATE_PATH", state_file), \
         patch("scripts.product_status_timeline.STATE_SUMMARY_PATH", summary_file), \
         patch("scripts.product_status_timeline.PRODUCTS_DIR", prod_dir), \
         patch("scripts.product_status_timeline.LEDGER_PATH", sample_ledger):
        timeline = generate_timeline(include_details=True)

    assert "recent_cycles" in timeline
    assert len(timeline["recent_cycles"]) == 5


def test_format_timeline_output(tmp_path, sample_products, sample_ledger):
    from scripts.product_status_timeline import format_timeline

    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps({"cycle": 10, "mode": "BUILD"}))
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps({"cycle": 10}))
    prod_dir = tmp_path / "products"
    prod_dir.mkdir()

    with patch("scripts.product_status_timeline.STATE_PATH", state_file), \
         patch("scripts.product_status_timeline.STATE_SUMMARY_PATH", summary_file), \
         patch("scripts.product_status_timeline.PRODUCTS_DIR", prod_dir), \
         patch("scripts.product_status_timeline.LEDGER_PATH", sample_ledger):
        timeline = generate_timeline(include_details=True)

    output = format_timeline(timeline)
    assert "# Status Timeline" in output
    assert "Cycle: 10" in output
    assert "Checkout Readiness" in output
    assert "Category Status Matrix" in output
    assert "Ledger Summary" in output
    assert "Recent Cycles" in output
