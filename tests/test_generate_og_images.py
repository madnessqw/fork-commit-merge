import json
import os
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_og_images import (
    GRADIENTS,
    HEIGHT,
    WIDTH,
    blend_color,
    generate_og_image,
    generate_svg,
    get_top_products,
    hex_to_rgb,
    load_product,
)


class TestHexToRgb:
    def test_basic(self):
        assert hex_to_rgb("#ff0000") == (255, 0, 0)

    def test_green(self):
        assert hex_to_rgb("#00ff00") == (0, 255, 0)

    def test_blue(self):
        assert hex_to_rgb("#0000ff") == (0, 0, 255)

    def test_without_hash(self):
        assert hex_to_rgb("aabbcc") == (170, 187, 204)

    def test_white(self):
        assert hex_to_rgb("#ffffff") == (255, 255, 255)

    def test_black(self):
        assert hex_to_rgb("#000000") == (0, 0, 0)


class TestBlendColor:
    def test_start_color(self):
        result = blend_color("#000000", "#ffffff", 0)
        assert result == "#000000"

    def test_end_color(self):
        result = blend_color("#000000", "#ffffff", 1)
        assert result == "#ffffff"

    def test_midpoint(self):
        result = blend_color("#000000", "#ffffff", 0.5)
        r, g, b = int(result[1:3], 16), int(result[3:5], 16), int(result[5:7], 16)
        assert abs(r - 128) <= 1
        assert abs(g - 128) <= 1
        assert abs(b - 128) <= 1

    def test_same_color(self):
        result = blend_color("#ff0000", "#ff0000", 0.5)
        assert result == "#ff0000"


class TestGenerateSvg:
    def test_contains_product_name(self):
        svg = generate_svg("MyTool", "A great tool", 9, 0)
        assert "MyTool" in svg

    def test_contains_tagline(self):
        svg = generate_svg("MyTool", "A great tool", 9, 0)
        assert "A great tool" in svg

    def test_contains_price(self):
        svg = generate_svg("MyTool", "tag", 29, 0)
        assert "$29" in svg

    def test_dimensions(self):
        svg = generate_svg("X", "Y", 0, 0)
        assert f'width="{WIDTH}"' in svg
        assert f'height="{HEIGHT}"' in svg

    def test_escapes_special_chars(self):
        svg = generate_svg('A&B<>"', "tag", 0, 0)
        assert "&amp;" in svg
        assert "&lt;" in svg
        assert "&gt;" in svg
        assert "&quot;" in svg

    def test_gradient_index_wraps(self):
        svg0 = generate_svg("X", "Y", 0, 0)
        svg10 = generate_svg("X", "Y", 0, len(GRADIENTS))
        assert svg0 == svg10


class TestLoadProduct:
    def test_existing_product(self, tmp_path, monkeypatch):
        import scripts.generate_og_images as mod
        prod_dir = tmp_path / "myslug"
        prod_dir.mkdir()
        (prod_dir / "product.json").write_text(json.dumps({"name": "My Slug", "price": 5}))
        monkeypatch.setattr(mod, "PRODUCTS_DIR", tmp_path)
        result = load_product("myslug")
        assert result is not None
        assert result["name"] == "My Slug"

    def test_missing_product(self, tmp_path, monkeypatch):
        import scripts.generate_og_images as mod
        monkeypatch.setattr(mod, "PRODUCTS_DIR", tmp_path)
        result = load_product("nonexistent")
        assert result is None


class TestGetTopProducts:
    def test_sorted_by_price_desc(self, tmp_path, monkeypatch):
        import scripts.generate_og_images as mod
        state = {
            "products": {
                "active": [
                    {"s": "cheap", "price": 5},
                    {"s": "pricy", "price": 99},
                    {"s": "mid", "price": 29},
                ]
            }
        }
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(state))
        monkeypatch.setattr(mod, "STATE_FILE", state_file)
        result = get_top_products(2)
        assert result == ["pricy", "mid"]

    def test_string_price(self, tmp_path, monkeypatch):
        import scripts.generate_og_images as mod
        state = {
            "products": {
                "active": [
                    {"s": "strprice", "price": "$50"},
                    {"s": "intprice", "price": 30},
                ]
            }
        }
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(state))
        monkeypatch.setattr(mod, "STATE_FILE", state_file)
        result = get_top_products(1)
        assert result == ["strprice"]

    def test_invalid_string_price(self, tmp_path, monkeypatch):
        import scripts.generate_og_images as mod
        state = {
            "products": {
                "active": [
                    {"s": "bad", "price": "free"},
                    {"s": "good", "price": 10},
                ]
            }
        }
        state_file = tmp_path / "STATE.json"
        state_file.write_text(json.dumps(state))
        monkeypatch.setattr(mod, "STATE_FILE", state_file)
        result = get_top_products(1)
        assert result == ["good"]


class TestGenerateOgImage:
    def test_skip_no_product_json(self, tmp_path, monkeypatch, capsys):
        import scripts.generate_og_images as mod
        monkeypatch.setattr(mod, "PRODUCTS_DIR", tmp_path)
        result = generate_og_image("nosuchslug")
        assert result is False
        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_skip_already_has_og_image(self, tmp_path, monkeypatch, capsys):
        import scripts.generate_og_images as mod
        prod_dir = tmp_path / "slug1"
        prod_dir.mkdir()
        (prod_dir / "product.json").write_text(json.dumps({
            "name": "Slug1",
            "tagline": "Test",
            "price": 5,
            "og_image": "/og-image.png",
        }))
        monkeypatch.setattr(mod, "PRODUCTS_DIR", tmp_path)
        result = generate_og_image("slug1")
        assert result is False
        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_dry_run(self, tmp_path, monkeypatch, capsys):
        import scripts.generate_og_images as mod
        prod_dir = tmp_path / "slug2"
        prod_dir.mkdir()
        (prod_dir / "product.json").write_text(json.dumps({
            "name": "Slug2",
            "tagline": "Dry run test",
            "price": 9,
        }))
        monkeypatch.setattr(mod, "PRODUCTS_DIR", tmp_path)
        result = generate_og_image("slug2", dry_run=True)
        assert result is True
        captured = capsys.readouterr()
        assert "DRY" in captured.out

    def test_missing_imagemagick(self, tmp_path, monkeypatch, capsys):
        import scripts.generate_og_images as mod
        prod_dir = tmp_path / "slug3"
        prod_dir.mkdir()
        (prod_dir / "product.json").write_text(json.dumps({
            "name": "Slug3",
            "tagline": "No convert",
            "price": 7,
        }))
        public_dir = prod_dir / "public"
        public_dir.mkdir()
        monkeypatch.setattr(mod, "PRODUCTS_DIR", tmp_path)

        def fake_run(*a, **kw):
            rc = mock.MagicMock()
            rc.returncode = 1
            rc.stderr = "convert: command not found"
            return rc

        monkeypatch.setattr(mod.subprocess, "run", fake_run)
        result = generate_og_image("slug3")
        assert result is False
