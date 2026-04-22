import unittest

from scripts.product_state_sync import health_check_url, merge_product_record


class ProductStateSyncTests(unittest.TestCase):
    def test_manifest_status_overrides_stale_live_state_and_clears_url(self) -> None:
        merged = merge_product_record(
            {
                "name": "SSL Cert Checker",
                "slug": "ssl-cert-checker",
                "status": "live",
                "vercel_url": "https://ssl-cert-checker.vercel.app",
            },
            {
                "name": "SSL Cert Checker",
                "slug": "ssl-cert-checker",
                "status": "spec_ready",
                "vercel_url": None,
            },
        )

        self.assertEqual(merged["status"], "spec_ready")
        self.assertIsNone(merged["vercel_url"])
        self.assertIsNone(health_check_url(merged))

    def test_live_manifest_with_missing_url_keeps_state_canonical_url(self) -> None:
        merged = merge_product_record(
            {
                "slug": "table-to-csv",
                "status": "live",
                "vercel_url": "https://table-to-csv.vercel.app",
            },
            {
                "slug": "table-to-csv",
                "status": "live",
                "vercel_url": None,
            },
        )

        self.assertEqual(merged["vercel_url"], "https://table-to-csv.vercel.app")
        self.assertEqual(health_check_url(merged), "https://table-to-csv.vercel.app")

    def test_state_canonical_alias_beats_manifest_preview_hash(self) -> None:
        merged = merge_product_record(
            {
                "slug": "keyforge",
                "status": "live",
                "vercel_url": "https://keyforge.vercel.app",
            },
            {
                "slug": "keyforge",
                "status": "live",
                "vercel_url": "https://keyforge-3lj8zc033-madnessqws-projects.vercel.app",
            },
        )

        self.assertEqual(merged["vercel_url"], "https://keyforge.vercel.app")
        self.assertEqual(merged["v"], "https://keyforge.vercel.app")
        self.assertEqual(health_check_url(merged), "https://keyforge.vercel.app")

    def test_live_manifest_canonical_url_beats_stale_state_alias(self) -> None:
        merged = merge_product_record(
            {
                "slug": "diffmaster",
                "status": "live",
                "vercel_url": "https://diffmaster-rose.vercel.app",
                "ideal_vercel_url": "https://diffmaster.vercel.app",
            },
            {
                "slug": "diffmaster",
                "status": "live",
                "vercel_url": "https://diffmaster.vercel.app",
            },
        )

        self.assertEqual(merged["vercel_url"], "https://diffmaster.vercel.app")
        self.assertEqual(merged["v"], "https://diffmaster.vercel.app")
        self.assertEqual(merged["ideal_vercel_url"], "https://diffmaster.vercel.app")
        self.assertEqual(health_check_url(merged), "https://diffmaster.vercel.app")

    def test_live_deployment_url_canonical_beats_stale_state_alias(self) -> None:
        merged = merge_product_record(
            {
                "slug": "pdf-forge",
                "status": "live",
                "vercel_url": "https://pdf-forge-five.vercel.app",
                "ideal_vercel_url": "https://pdf-forge.vercel.app",
            },
            {
                "slug": "pdf-forge",
                "status": "live",
                "vercel_url": "https://pdf-forge-five.vercel.app",
                "deployment_url": "https://pdf-forge.vercel.app",
            },
        )

        self.assertEqual(merged["vercel_url"], "https://pdf-forge.vercel.app")
        self.assertEqual(merged["v"], "https://pdf-forge.vercel.app")
        self.assertEqual(merged["ideal_vercel_url"], "https://pdf-forge.vercel.app")
        self.assertEqual(health_check_url(merged), "https://pdf-forge.vercel.app")

    def test_last_successful_health_url_can_promote_stale_state_alias_back_to_canonical(self) -> None:
        merged = merge_product_record(
            {
                "slug": "stale-tool",
                "status": "live",
                "vercel_url": "https://stale-tool-rose.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://stale-tool.vercel.app",
            },
            {
                "slug": "stale-tool",
                "status": "live",
                "vercel_url": "https://stale-tool-rose.vercel.app",
            },
        )

        self.assertEqual(merged["vercel_url"], "https://stale-tool.vercel.app")
        self.assertEqual(merged["v"], "https://stale-tool.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://stale-tool.vercel.app")
        self.assertEqual(health_check_url(merged), "https://stale-tool.vercel.app")

    def test_failure_codes_normalize_stale_healthy_health_status(self) -> None:
        merged = merge_product_record(
            {
                "slug": "broken-tool",
                "status": "live",
                "vercel_url": "https://broken-tool-rose.vercel.app",
                "health_status": "healthy",
                "last_health_code": 401,
                "last_health_url": "https://broken-tool.vercel.app",
            },
            {
                "slug": "broken-tool",
                "status": "live",
                "vercel_url": "https://broken-tool.vercel.app",
                "deployment_url": "https://broken-tool.vercel.app",
            },
        )

        self.assertEqual(merged["health_status"], "unauthorized")
        self.assertEqual(merged["last_health_code"], 401)
        self.assertEqual(merged["vercel_url"], "https://broken-tool.vercel.app")
        self.assertEqual(health_check_url(merged), "https://broken-tool.vercel.app")

    def test_live_product_without_explicit_url_probes_slug_canonical(self) -> None:
        self.assertEqual(
            health_check_url(
                {
                    "slug": "ideal-only-tool",
                    "status": "live",
                }
            ),
            "https://ideal-only-tool.vercel.app",
        )

    def test_live_preview_alias_still_probes_slug_canonical_first(self) -> None:
        self.assertEqual(
            health_check_url(
                {
                    "slug": "webhook-tester",
                    "status": "live",
                    "vercel_url": "https://webhook-tester-beryl.vercel.app",
                }
            ),
            "https://webhook-tester.vercel.app",
        )


if __name__ == "__main__":
    unittest.main()
