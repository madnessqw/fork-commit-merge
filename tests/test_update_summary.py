import unittest

from scripts.update_summary import build_summary, is_placeholder_product, normalize_product


class UpdateSummaryTests(unittest.TestCase):
    def test_placeholder_records_are_ignored(self) -> None:
        state = {
            "cycle": 1060,
            "mode": "INNOVATE",
            "balance": 0.0,
            "products": {
                "active": [
                    {
                        "name": "Live Tool",
                        "slug": "live-tool",
                        "status": "live",
                        "vercel_url": "https://live-tool.vercel.app",
                        "checkout_url": "https://checkout.example/live-tool",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    },
                    {
                        "name": "Spec Tool",
                        "slug": "spec-tool",
                        "status": "spec_ready",
                    },
                    {
                        "name": None,
                        "slug": None,
                        "status": None,
                        "vercel_url": None,
                        "checkout_url": None,
                    },
                    {},
                ],
                "spec_ready": [],
            },
        }

        summary = build_summary(state)

        self.assertEqual(summary["active_count"], 2)
        self.assertEqual(summary["live_count"], 1)
        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 1)
        self.assertEqual(summary["products"], [
            {
                "n": "Live Tool",
                "s": "live-tool",
                "st": "live",
                "v": "https://live-tool.vercel.app",
                "c": "https://checkout.example/live-tool",
            },
            {
                "n": "Spec Tool",
                "s": "spec-tool",
                "st": "spec_ready",
                "v": None,
                "c": None,
            },
        ])

    def test_compact_records_are_normalized_before_counting(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Compact Spec Tool",
                        "slug": "compact-spec-tool",
                        "status": "spec_ready",
                        "created_at": "2026-04-21T20:39:38.509746Z",
                        "health_status": "pending",
                    },
                    {"n": "Compact Spec Tool", "s": "compact-spec-tool", "st": "spec_ready", "v": None, "c": None},
                    {"name": "Live Tool", "slug": "live-tool", "status": "live", "vercel_url": "https://live-tool.vercel.app"},
                ],
                "spec_ready": [
                    {"name": "Compact Spec Tool", "slug": "compact-spec-tool", "status": "spec_ready"},
                    {"name": "External Spec Tool", "slug": "external-spec-tool", "status": "spec_ready"},
                ],
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["spec_ready_count"], 2)
        self.assertEqual(summary["active_count"], 2)
        self.assertEqual(summary["products"][0]["s"], "compact-spec-tool")
        self.assertEqual(summary["products"][0]["st"], "spec_ready")
        self.assertEqual(summary["products"][0]["n"], "Compact Spec Tool")
        self.assertEqual(summary["gaps"]["missing_url"], ["compact-spec-tool"])

    def test_placeholder_detector_treats_whitespace_as_empty(self) -> None:
        self.assertTrue(
            is_placeholder_product(
                {
                    "name": "   ",
                    "slug": "\n",
                    "status": "\t",
                    "vercel_url": "",
                    "checkout_url": None,
                }
            )
        )
        self.assertFalse(
            is_placeholder_product(
                {
                    "name": "Tool",
                    "slug": "tool",
                    "status": None,
                }
            )
        )

    def test_normalize_product_maps_compact_fields(self) -> None:
        self.assertEqual(
            normalize_product(
                {
                    "n": "Tool",
                    "s": "tool",
                    "st": "live",
                    "v": "https://tool.vercel.app",
                    "c": "https://checkout.example/tool",
                }
            ),
            {
                "n": "Tool",
                "s": "tool",
                "st": "live",
                "v": "https://tool.vercel.app",
                "c": "https://checkout.example/tool",
                "name": "Tool",
                "slug": "tool",
                "status": "live",
                "vercel_url": "https://tool.vercel.app",
                "checkout_url": "https://checkout.example/tool",
            },
        )


if __name__ == "__main__":
    unittest.main()
