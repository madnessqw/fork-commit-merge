import json
import tempfile
import unittest
from pathlib import Path

from scripts.fix_product_state_gaps import (
    BATCH_DEPLOY_CYCLE,
    CURRENT_CYCLE,
    DATE_CYCLE_MAP,
    estimate_created_cycle,
    load_json,
    main,
    save_json,
)


class TestEstimateCreatedCycle(unittest.TestCase):
    def test_returns_cycle_for_matching_created_at(self):
        product = {"created_at": "2026-04-22T10:00:00Z"}
        result = estimate_created_cycle(product)
        self.assertEqual(result, DATE_CYCLE_MAP["2026-04-22"])

    def test_returns_cycle_for_matching_seo_optimized_at(self):
        product = {"seo_optimized_at": "2026-04-23T08:00:00Z"}
        result = estimate_created_cycle(product)
        self.assertEqual(result, DATE_CYCLE_MAP["2026-04-23"] + 2)

    def test_returns_none_for_no_dates(self):
        product = {"name": "test"}
        result = estimate_created_cycle(product)
        self.assertIsNone(result)

    def test_created_at_takes_priority_over_seo(self):
        product = {"created_at": "2026-04-21T00:00:00Z", "seo_optimized_at": "2026-04-24T00:00:00Z"}
        result = estimate_created_cycle(product)
        self.assertEqual(result, DATE_CYCLE_MAP["2026-04-21"])

    def test_returns_none_for_non_matching_date(self):
        product = {"created_at": "2025-01-01T00:00:00Z"}
        result = estimate_created_cycle(product)
        self.assertIsNone(result)


class TestLoadSaveJson(unittest.TestCase):
    def test_load_save_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.json"
            data = {"name": "test", "cycle": 100}
            save_json(str(path), data)
            loaded = load_json(str(path))
            self.assertEqual(loaded, data)


class TestMain(unittest.TestCase):
    def _make_product(self, tmpdir, slug, **overrides):
        pdir = Path(tmpdir) / "products" / slug
        pdir.mkdir(parents=True, exist_ok=True)
        product = {"name": slug, "slug": slug, "status": "live"}
        product.update(overrides)
        save_json(str(pdir / "product.json"), product)
        return product

    def test_patches_missing_created_cycle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_product(tmpdir, "test-prod", status="live")
            import scripts.fix_product_state_gaps as mod
            orig = mod.PRODUCTS_DIR
            mod.PRODUCTS_DIR = str(Path(tmpdir) / "products")
            try:
                rc = main()
            finally:
                mod.PRODUCTS_DIR = orig
            self.assertEqual(rc, 0)
            updated = load_json(str(Path(tmpdir) / "products" / "test-prod" / "product.json"))
            self.assertIn("created_cycle", updated)

    def test_patches_deployed_cycle_for_live(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_product(tmpdir, "live-prod", status="live", created_cycle=500)
            import scripts.fix_product_state_gaps as mod
            orig = mod.PRODUCTS_DIR
            mod.PRODUCTS_DIR = str(Path(tmpdir) / "products")
            try:
                main()
            finally:
                mod.PRODUCTS_DIR = orig
            updated = load_json(str(Path(tmpdir) / "products" / "live-prod" / "product.json"))
            self.assertEqual(updated["deployed_cycle"], BATCH_DEPLOY_CYCLE)

    def test_no_deployed_cycle_for_non_live(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_product(tmpdir, "spec-prod", status="spec_ready", created_cycle=500)
            import scripts.fix_product_state_gaps as mod
            orig = mod.PRODUCTS_DIR
            mod.PRODUCTS_DIR = str(Path(tmpdir) / "products")
            try:
                main()
            finally:
                mod.PRODUCTS_DIR = orig
            updated = load_json(str(Path(tmpdir) / "products" / "spec-prod" / "product.json"))
            self.assertNotIn("deployed_cycle", updated)

    def test_skips_already_complete_products(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._make_product(
                tmpdir, "complete-prod",
                status="live", created_cycle=100, deployed_cycle=200
            )
            import scripts.fix_product_state_gaps as mod
            orig = mod.PRODUCTS_DIR
            mod.PRODUCTS_DIR = str(Path(tmpdir) / "products")
            try:
                main()
            finally:
                mod.PRODUCTS_DIR = orig
            updated = load_json(str(Path(tmpdir) / "products" / "complete-prod" / "product.json"))
            self.assertEqual(updated["created_cycle"], 100)
            self.assertEqual(updated["deployed_cycle"], 200)


if __name__ == "__main__":
    unittest.main()
