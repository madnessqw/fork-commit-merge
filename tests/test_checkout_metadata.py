import unittest

from scripts.checkout_metadata import (
    get_checkout_url,
    merge_checkout_metadata,
    normalize_checkout_metadata,
)


class CheckoutMetadataTests(unittest.TestCase):
    def test_legacy_lemonsqueezy_field_normalizes_into_canonical_contract(self) -> None:
        record = {
            "slug": "mock-data-pro",
            "lemonsqueezy_checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/mock-data-pro-001",
        }

        normalized = normalize_checkout_metadata(record, force_canonical_key=True)

        self.assertEqual(
            normalized["checkout_url"],
            "https://profitbridge.lemonsqueezy.com/checkout/buy/mock-data-pro-001",
        )
        self.assertEqual(normalized["payment_provider"], "lemonsqueezy")
        self.assertEqual(normalized["lemon_checkout_url"], normalized["checkout_url"])
        self.assertEqual(normalized["lemonsqueezy_checkout_url"], normalized["checkout_url"])

    def test_existing_non_lemonsqueezy_provider_is_preserved(self) -> None:
        record = {
            "checkout_url": "https://gumroad.com/l/tool",
            "payment_provider": "gumroad",
            "lemon_checkout_url": "https://old.example/ignore-me",
        }

        normalized = normalize_checkout_metadata(record, force_canonical_key=True)

        self.assertEqual(normalized["payment_provider"], "gumroad")
        self.assertEqual(normalized["checkout_url"], "https://gumroad.com/l/tool")
        self.assertEqual(normalized["lemon_checkout_url"], "https://old.example/ignore-me")

    def test_prune_legacy_drops_duplicate_checkout_aliases(self) -> None:
        record = {
            "checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/tool-001",
            "payment_provider": "lemonsqueezy",
            "lemon_checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/tool-001",
            "lemonsqueezy_checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/tool-001",
        }

        normalized = normalize_checkout_metadata(
            record,
            force_canonical_key=True,
            prune_legacy=True,
        )

        self.assertEqual(
            normalized["checkout_url"],
            "https://profitbridge.lemonsqueezy.com/checkout/buy/tool-001",
        )
        self.assertEqual(normalized["payment_provider"], "lemonsqueezy")
        self.assertNotIn("lemon_checkout_url", normalized)
        self.assertNotIn("lemonsqueezy_checkout_url", normalized)

    def test_get_checkout_url_reads_compact_and_legacy_keys(self) -> None:
        self.assertEqual(
            get_checkout_url({"c": "https://checkout.example/tool"}),
            "https://checkout.example/tool",
        )
        self.assertEqual(
            get_checkout_url({"lemonsqueezy_checkout_url": "https://checkout.example/tool"}),
            "https://checkout.example/tool",
        )

    def test_merge_checkout_metadata_preserves_existing_checkout_when_overlay_clears_it(self) -> None:
        existing = {
            "checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/tool-001",
            "payment_provider": "lemonsqueezy",
            "lemon_checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/tool-001",
            "lemonsqueezy_checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/tool-001",
        }
        overlay = {
            "checkout_url": None,
            "payment_provider": "lemonsqueezy",
            "lemon_checkout_url": None,
            "lemonsqueezy_checkout_url": None,
        }

        merged = merge_checkout_metadata(
            overlay,
            existing,
            force_canonical_key=True,
            prune_legacy=True,
        )

        self.assertEqual(
            merged["checkout_url"],
            "https://profitbridge.lemonsqueezy.com/checkout/buy/tool-001",
        )
        self.assertEqual(merged["payment_provider"], "lemonsqueezy")
        self.assertNotIn("lemon_checkout_url", merged)
        self.assertNotIn("lemonsqueezy_checkout_url", merged)


if __name__ == "__main__":
    unittest.main()
