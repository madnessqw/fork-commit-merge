import json
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch
from scripts.orphan_detector import (
    load_state_slugs,
    get_dir_slugs,
    dir_size,
    format_size,
    scan,
    prune,
    PROTECTED_DIRS,
)


@pytest.fixture
def tmp_products(tmp_path, monkeypatch):
    products_dir = tmp_path / "products"
    products_dir.mkdir()

    for slug in ["alpha-tool", "beta-app", "gamma-dev"]:
        d = products_dir / slug
        d.mkdir()
        (d / "spec.json").write_text("{}")

    state = {
        "products": {
            "active": [
                {"slug": "alpha-tool", "status": "live"},
                {"slug": "beta-app", "status": "live"},
            ],
            "archived": [],
        }
    }
    state_path = tmp_path / "STATE.json"
    state_path.write_text(json.dumps(state))

    import scripts.orphan_detector as mod

    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "STATE_PATH", state_path)
    monkeypatch.setattr(mod, "PRODUCTS_DIR", products_dir)
    monkeypatch.setattr(mod, "ARCHIVE_DIR", products_dir / ".archived")

    return tmp_path, products_dir


class TestLoadStateSlugs:
    def test_basic(self, tmp_products, monkeypatch):
        slugs = load_state_slugs()
        assert "alpha-tool" in slugs
        assert "beta-app" in slugs

    def test_archived_included(self, tmp_products, monkeypatch):
        tmp_path, _ = tmp_products
        state = json.load(open(tmp_path / "STATE.json"))
        state["products"]["archived"] = [{"slug": "old-thing"}]
        (tmp_path / "STATE.json").write_text(json.dumps(state))
        slugs = load_state_slugs()
        assert "old-thing" in slugs

    def test_empty_slug_excluded(self, tmp_path, monkeypatch):
        state = {"products": {"active": [{"slug": ""}], "archived": []}}
        sf = tmp_path / "STATE.json"
        sf.write_text(json.dumps(state))
        import scripts.orphan_detector as mod

        monkeypatch.setattr(mod, "STATE_PATH", sf)
        assert "" not in load_state_slugs()


class TestGetDirSlugs:
    def test_basic(self, tmp_products):
        slugs = get_dir_slugs()
        assert "alpha-tool" in slugs
        assert "beta-app" in slugs
        assert "gamma-dev" in slugs

    def test_protected_excluded(self, tmp_products):
        tmp_path, products_dir = tmp_products
        (products_dir / ".archived").mkdir(exist_ok=True)
        (products_dir / "__pycache__").mkdir(exist_ok=True)
        slugs = get_dir_slugs()
        assert ".archived" not in slugs
        assert "__pycache__" not in slugs


class TestDirSize:
    def test_basic(self, tmp_path):
        d = tmp_path / "testdir"
        d.mkdir()
        (d / "file.txt").write_text("x" * 100)
        size = dir_size(d)
        assert size >= 100

    def test_nested(self, tmp_path):
        d = tmp_path / "nested"
        d.mkdir()
        sub = d / "sub"
        sub.mkdir()
        (sub / "data.bin").write_bytes(b"\x00" * 200)
        size = dir_size(d)
        assert size >= 200

    def test_empty_dir(self, tmp_path):
        d = tmp_path / "empty"
        d.mkdir()
        assert dir_size(d) == 0


class TestFormatSize:
    def test_bytes(self):
        assert "B" in format_size(50)

    def test_kb(self):
        assert "KB" in format_size(2048)

    def test_mb(self):
        assert "MB" in format_size(2 * 1024 * 1024)

    def test_gb(self):
        assert "GB" in format_size(3 * 1024 * 1024 * 1024)


class TestScan:
    def test_finds_orphans(self, tmp_products, capsys):
        results = scan()
        slugs = [r["slug"] for r in results]
        assert "gamma-dev" in slugs
        assert "alpha-tool" not in slugs

    def test_no_orphans(self, tmp_path, monkeypatch):
        products_dir = tmp_path / "products"
        products_dir.mkdir()
        (products_dir / "only-tool").mkdir()
        state = {"products": {"active": [{"slug": "only-tool"}], "archived": []}}
        sf = tmp_path / "STATE.json"
        sf.write_text(json.dumps(state))
        import scripts.orphan_detector as mod

        monkeypatch.setattr(mod, "ROOT", tmp_path)
        monkeypatch.setattr(mod, "STATE_PATH", sf)
        monkeypatch.setattr(mod, "PRODUCTS_DIR", products_dir)
        results = scan()
        assert results == []


class TestPrune:
    def test_dry_run(self, tmp_products, capsys):
        count = prune(dry_run=True)
        assert count == 0
        tmp_path, products_dir = tmp_products
        assert (products_dir / "gamma-dev").exists()

    def test_actual_prune(self, tmp_products, capsys):
        count = prune(dry_run=False)
        assert count == 1
        tmp_path, products_dir = tmp_products
        assert not (products_dir / "gamma-dev").exists()
        assert (products_dir / ".archived" / "gamma-dev").exists()
