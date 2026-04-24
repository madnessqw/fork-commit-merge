import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.polar_checkout_sync import (
    discover_price_from_files,
    find_remote_product,
    load_local_products,
    parse_price_to_cents,
    polar_checkout_requires_link_repair,
    product_needs_update,
    slugify_name,
)


class PolarCheckoutSyncTests(unittest.TestCase):
    def test_parse_price_to_cents_handles_common_product_formats(self) -> None:
        self.assertEqual(parse_price_to_cents("9"), 900)
        self.assertEqual(parse_price_to_cents("$19"), 1900)
        self.assertEqual(parse_price_to_cents("$12 one-time"), 1200)
        self.assertEqual(parse_price_to_cents(29), 2900)

    def test_slugify_name_normalizes_human_titles(self) -> None:
        self.assertEqual(
            slugify_name("API Spec Validator — Quick Check"),
            "api-spec-validator-quick-check",
        )
        self.assertEqual(
            slugify_name("  Cron Expression Builder  "), "cron-expression-builder"
        )

    def test_product_needs_update_when_remote_price_or_visibility_drift_exists(
        self,
    ) -> None:
        local = type(
            "Local",
            (),
            {
                "name": "Tool X",
                "description": "Desc",
                "price_cents": 1900,
            },
        )()
        remote = {
            "name": "Tool X",
            "description": "Desc",
            "visibility": "private",
            "prices": [
                {"price_amount": 900, "price_currency": "usd", "is_archived": False}
            ],
        }
        self.assertTrue(product_needs_update(remote, local))

    def test_discover_price_from_files_falls_back_to_site_markup(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            product_dir = Path(tmpdir)
            (product_dir / "public").mkdir()
            (product_dir / "public" / "index.html").write_text(
                '<a class="cta">Get Lifetime Access — $19</a>',
                encoding="utf-8",
            )
            found = discover_price_from_files(product_dir)

        self.assertIsNotNone(found)
        cents, source = found
        self.assertEqual(cents, 1900)
        self.assertIn("public/index.html", source)

    def test_polar_checkout_requires_link_repair_without_link_metadata(self) -> None:
        self.assertTrue(
            polar_checkout_requires_link_repair(
                {},
                checkout_url="https://polar.sh/checkout/polar_cs_session",
                payment_provider="polar",
            )
        )
        self.assertFalse(
            polar_checkout_requires_link_repair(
                {
                    "polar_checkout_link_id": "polar_cl_123",
                    "polar_product_id": "prod_123",
                },
                checkout_url="https://polar.sh/checkout/polar_cl_123",
                payment_provider="polar",
            )
        )

    def test_load_local_products_reselects_polar_session_urls_for_link_rollout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            product_dir = root / "products" / "session-tool"
            product_dir.mkdir(parents=True)
            (product_dir / "product.json").write_text(
                """{
  "name": "Session Tool",
  "slug": "session-tool",
  "status": "live",
  "price": "$19",
  "vercel_url": "https://session-tool.vercel.app",
  "checkout_url": "https://polar.sh/checkout/polar_cs_session"
}
""",
                encoding="utf-8",
            )

            with patch("scripts.polar_checkout_sync.PRODUCTS_DIR", root / "products"):
                products = load_local_products(
                    statuses={"live"},
                    include_existing=False,
                    replace_non_polar=False,
                )

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].payment_provider, "polar")
        self.assertEqual(products[0].selection_reason, "repair_polar_link")

    def test_find_remote_product_matches_by_metadata_slug_first(self) -> None:
        local = type("Local", (), {"name": "My Tool", "slug": "my-tool"})()
        remote_products = [
            {"name": "My Tool", "metadata": {}},
            {"name": "Other", "metadata": {"local_slug": "my-tool"}},
        ]
        result = find_remote_product(remote_products, local)
        self.assertEqual(result["metadata"]["local_slug"], "my-tool")

    def test_find_remote_product_falls_back_to_slugified_name(self) -> None:
        local = type("Local", (), {"name": "My Cool Tool", "slug": "my-tool"})()
        remote_products = [
            {"name": "my-cool-tool", "metadata": {}},
        ]
        result = find_remote_product(remote_products, local)
        self.assertEqual(result["name"], "my-cool-tool")

    def test_find_remote_product_returns_none_when_no_match(self) -> None:
        local = type("Local", (), {"name": "Unique Tool", "slug": "unique-tool"})()
        result = find_remote_product([], local)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
