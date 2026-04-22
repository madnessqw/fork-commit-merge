import json
import tempfile
import unittest
from pathlib import Path

from scripts.standardize_checkout_fields import normalize_file


ROOT = Path(__file__).resolve().parents[1]


class StandardizeCheckoutFieldsTests(unittest.TestCase):
    def test_write_mode_prunes_legacy_checkout_aliases_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            product_path = Path(tmpdir) / "product.json"
            product_path.write_text(
                json.dumps(
                    {
                        "slug": "legacy-tool",
                        "checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/legacy-tool-001",
                        "payment_provider": "lemonsqueezy",
                        "lemon_checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/legacy-tool-001",
                        "lemonsqueezy_checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/legacy-tool-001",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            changed = normalize_file(product_path, write=True)

            self.assertTrue(changed)
            normalized = json.loads(product_path.read_text(encoding="utf-8"))
            self.assertEqual(
                normalized["checkout_url"],
                "https://profitbridge.lemonsqueezy.com/checkout/buy/legacy-tool-001",
            )
            self.assertEqual(normalized["payment_provider"], "lemonsqueezy")
            self.assertNotIn("lemon_checkout_url", normalized)
            self.assertNotIn("lemonsqueezy_checkout_url", normalized)

    def test_repo_product_manifests_use_canonical_checkout_contract(self) -> None:
        legacy_paths: list[str] = []
        missing_provider_paths: list[str] = []

        for path in sorted((ROOT / "products").glob("*/product.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            if "lemon_checkout_url" in data or "lemonsqueezy_checkout_url" in data:
                legacy_paths.append(str(path.relative_to(ROOT)))

            checkout_url = data.get("checkout_url")
            if checkout_url and not data.get("payment_provider"):
                missing_provider_paths.append(str(path.relative_to(ROOT)))

        self.assertEqual(legacy_paths, [])
        self.assertEqual(missing_provider_paths, [])


if __name__ == "__main__":
    unittest.main()
