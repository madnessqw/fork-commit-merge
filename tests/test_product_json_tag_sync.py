#!/usr/bin/env python3
"""Tests for product_json_tag_sync.py"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.product_json_tag_sync import sync_tags


@pytest.fixture
def tmp_repo(tmp_path, monkeypatch):
    import scripts.product_json_tag_sync as mod

    state_dir = tmp_path / "state"
    products_dir = tmp_path / "products"
    state_dir.mkdir()
    products_dir.mkdir()

    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "STATE_FILE", state_dir / "STATE.json")
    monkeypatch.setattr(mod, "PRODUCTS_DIR", products_dir)

    return tmp_path, state_dir, products_dir


def _write_state(state_dir, products):
    state = {"products": {"active": products}}
    (state_dir / "STATE.json").write_text(json.dumps(state))


def _write_product(products_dir, slug, data):
    p = products_dir / slug
    p.mkdir(exist_ok=True)
    (p / "product.json").write_text(json.dumps(data))


def test_sync_adds_category_and_tags(tmp_repo):
    tmp, state_dir, products_dir = tmp_repo

    _write_state(state_dir, [
        {"slug": "test-prod", "category": "developer-tools", "tags": ["json", "converter"]},
    ])
    _write_product(products_dir, "test-prod", {"name": "Test Prod", "slug": "test-prod"})

    result = sync_tags(
        [{"slug": "test-prod", "category": "developer-tools", "tags": ["json", "converter"]}],
        dry_run=False,
    )

    assert result["updated_count"] == 1
    pj = json.loads((products_dir / "test-prod" / "product.json").read_text())
    assert pj["category"] == "developer-tools"
    assert pj["tags"] == ["json", "converter"]


def test_sync_dry_run_no_write(tmp_repo):
    tmp, state_dir, products_dir = tmp_repo

    _write_product(products_dir, "dry-prod", {"name": "Dry Prod", "slug": "dry-prod"})

    result = sync_tags(
        [{"slug": "dry-prod", "category": "security", "tags": ["hash"]}],
        dry_run=True,
    )

    assert result["updated_count"] == 1
    pj = json.loads((products_dir / "dry-prod" / "product.json").read_text())
    assert "category" not in pj
    assert "tags" not in pj


def test_sync_skips_already_synced(tmp_repo):
    tmp, state_dir, products_dir = tmp_repo

    _write_product(products_dir, "synced-prod", {
        "name": "Synced",
        "slug": "synced-prod",
        "category": "devops",
        "tags": ["docker"],
    })

    result = sync_tags(
        [{"slug": "synced-prod", "category": "devops", "tags": ["docker"]}],
    )

    assert result["updated_count"] == 0
    assert result["skipped_count"] == 1


def test_sync_handles_missing_product_json(tmp_repo):
    tmp, state_dir, products_dir = tmp_repo

    result = sync_tags(
        [{"slug": "ghost-prod", "category": "utilities", "tags": ["tool"]}],
    )

    assert result["updated_count"] == 0
    assert result["skipped_count"] == 1


def test_sync_handles_invalid_json(tmp_repo):
    tmp, state_dir, products_dir = tmp_repo

    p = products_dir / "bad-prod"
    p.mkdir(exist_ok=True)
    (p / "product.json").write_text("{invalid json")

    result = sync_tags(
        [{"slug": "bad-prod", "category": "utilities", "tags": ["tool"]}],
    )

    assert result["error_count"] == 1
    assert result["updated_count"] == 0


def test_sync_empty_tags_does_not_overwrite(tmp_repo):
    tmp, state_dir, products_dir = tmp_repo

    _write_product(products_dir, "no-tags-prod", {
        "name": "No Tags",
        "slug": "no-tags-prod",
    })

    result = sync_tags(
        [{"slug": "no-tags-prod", "category": "utilities", "tags": []}],
    )

    assert result["updated_count"] == 1
    pj = json.loads((products_dir / "no-tags-prod" / "product.json").read_text())
    assert pj["category"] == "utilities"
    assert "tags" not in pj
