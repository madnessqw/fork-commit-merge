import unittest

from scripts.product_state_sync import (
    choose_public_vercel_url,
    health_check_url,
    merge_product_record,
    sync_state_products,
    sync_state_snapshot,
)


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

    def test_predeploy_manifest_clears_stale_public_and_health_metadata(self) -> None:
        merged = merge_product_record(
            {
                "name": "Color Contrast Pro",
                "slug": "color-contrast-pro",
                "status": "ready_to_deploy",
                "vercel_url": "https://color-contrast-pro.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://color-contrast-pro.vercel.app",
                "last_health_check": "2026-04-21T00:00:00Z",
                "health_checked_at": "2026-04-21T00:00:00Z",
            },
            {
                "name": "Color Contrast Pro",
                "slug": "color-contrast-pro",
                "status": "ready_to_deploy",
                "vercel_url": "https://color-contrast-pro.vercel.app",
            },
        )

        self.assertEqual(merged["status"], "ready_to_deploy")
        self.assertIsNone(merged["vercel_url"])
        self.assertIsNone(merged["v"])
        self.assertIsNone(merged["health_status"])
        self.assertIsNone(merged["last_health_code"])
        self.assertIsNone(merged["last_health_url"])
        self.assertIsNone(merged["last_health_check"])
        self.assertIsNone(merged["health_checked_at"])
        self.assertIsNone(merged["canonical_health_status"])
        self.assertIsNone(merged["canonical_health_code"])
        self.assertIsNone(merged["canonical_health_url"])
        self.assertIsNone(merged["canonical_probe_url"])
        self.assertIsNone(merged["canonical_health_checked_at"])
        self.assertIsNone(health_check_url(merged))

    def test_predeploy_state_without_manifest_still_clears_public_and_health_metadata(self) -> None:
        merged = merge_product_record(
            {
                "name": "HTML Minifier Pro",
                "slug": "html-minifier-pro",
                "status": "ready_to_deploy",
                "vercel_url": "https://html-minifier-pro.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://html-minifier-pro.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["status"], "ready_to_deploy")
        self.assertIsNone(merged["vercel_url"])
        self.assertIsNone(merged["v"])
        self.assertIsNone(merged["health_status"])
        self.assertIsNone(merged["last_health_code"])
        self.assertIsNone(merged["last_health_url"])
        self.assertIsNone(merged["canonical_health_status"])
        self.assertIsNone(merged["canonical_health_code"])
        self.assertIsNone(merged["canonical_health_url"])
        self.assertIsNone(merged["canonical_probe_url"])
        self.assertIsNone(merged["canonical_health_checked_at"])
        self.assertIsNone(health_check_url(merged))

    def test_live_health_snapshot_mirrors_timestamp_fields(self) -> None:
        merged = merge_product_record(
            {
                "name": "Timestamp Sync Tool",
                "slug": "timestamp-sync-tool",
                "status": "live",
                "vercel_url": "https://timestamp-sync-tool.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://timestamp-sync-tool.vercel.app",
                "last_health_check": "2026-04-22T10:00:00Z",
            },
            None,
        )

        self.assertEqual(merged["last_health_check"], "2026-04-22T10:00:00Z")
        self.assertEqual(merged["health_checked_at"], "2026-04-22T10:00:00Z")
        self.assertEqual(merged["canonical_health_status"], "healthy")
        self.assertEqual(merged["canonical_health_code"], 200)
        self.assertEqual(merged["canonical_health_url"], "https://timestamp-sync-tool.vercel.app")
        self.assertEqual(merged["canonical_probe_url"], "https://timestamp-sync-tool.vercel.app")
        self.assertEqual(merged["canonical_health_checked_at"], "2026-04-22T10:00:00Z")
        self.assertEqual(merged["ideal_vercel_url"], "https://timestamp-sync-tool.vercel.app")
        self.assertEqual(health_check_url(merged), "https://timestamp-sync-tool.vercel.app")

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

    def test_live_manifest_preview_hash_without_state_url_promotes_canonical_slug(self) -> None:
        merged = merge_product_record(
            {
                "slug": "uuid-generator-pro",
                "status": "ready_to_deploy",
                "vercel_url": None,
                "health_status": "healthy",
                "last_health_code": 200,
            },
            {
                "slug": "uuid-generator-pro",
                "status": "live",
                "vercel_url": "https://uuid-generator-glm6h3i1l-madnessqws-projects.vercel.app",
            },
        )

        self.assertEqual(merged["status"], "live")
        self.assertEqual(merged["vercel_url"], "https://uuid-generator-pro.vercel.app")
        self.assertEqual(merged["v"], "https://uuid-generator-pro.vercel.app")
        self.assertEqual(health_check_url(merged), "https://uuid-generator-pro.vercel.app")

    def test_live_preview_alias_without_health_promotes_canonical_slug(self) -> None:
        merged = merge_product_record(
            {
                "slug": "api-mock-generator",
                "status": "live",
                "vercel_url": "https://api-mock-generator-m7lonmii3-madnessqws-projects.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["vercel_url"], "https://api-mock-generator.vercel.app")
        self.assertEqual(merged["v"], "https://api-mock-generator.vercel.app")
        self.assertEqual(merged["ideal_vercel_url"], "https://api-mock-generator.vercel.app")
        self.assertEqual(merged["canonical_health_url"], "https://api-mock-generator.vercel.app")
        self.assertEqual(health_check_url(merged), "https://api-mock-generator.vercel.app")

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
        self.assertEqual(merged["deployment_url"], "https://keyforge-3lj8zc033-madnessqws-projects.vercel.app")

    def test_live_manifest_preview_alias_is_retained_as_probe_fallback(self) -> None:
        merged = merge_product_record(
            {
                "slug": "html-entity-encoder",
                "status": "live",
                "vercel_url": "https://html-entity-encoder.vercel.app",
            },
            {
                "slug": "html-entity-encoder",
                "status": "live",
                "vercel_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
            },
        )

        self.assertEqual(merged["vercel_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(merged["v"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(merged["deployment_url"], "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app")
        self.assertEqual(health_check_url(merged), "https://html-entity-encoder.vercel.app")

    def test_alternate_healthy_fallback_url_beats_stale_canonical_state_url(self) -> None:
        merged = merge_product_record(
            {
                "slug": "temporary-tool",
                "status": "live",
                "vercel_url": "https://temporary-tool.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
                "last_health_url": "https://temporary-tool-preview.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["vercel_url"], "https://temporary-tool-preview.vercel.app")
        self.assertEqual(merged["v"], "https://temporary-tool-preview.vercel.app")
        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["last_health_url"], "https://temporary-tool-preview.vercel.app")
        self.assertEqual(health_check_url(merged), "https://temporary-tool.vercel.app")

    def test_canonical_failure_with_successful_fallback_becomes_alternate_healthy(self) -> None:
        merged = merge_product_record(
            {
                "slug": "canonical-failure-tool",
                "status": "live",
                "vercel_url": "https://canonical-failure-tool.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://canonical-failure-tool-preview.vercel.app",
                "canonical_health_code": 404,
                "canonical_health_status": "not_found",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://canonical-failure-tool-preview.vercel.app")
        self.assertEqual(merged["v"], "https://canonical-failure-tool-preview.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://canonical-failure-tool-preview.vercel.app")
        self.assertEqual(health_check_url(merged), "https://canonical-failure-tool.vercel.app")

    def test_manifest_backed_fallback_keeps_reachable_alias_as_public_url(self) -> None:
        merged = merge_product_record(
            {
                "slug": "manifest-fallback-tool",
                "status": "live",
                "vercel_url": "https://manifest-fallback-tool.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://manifest-fallback-tool-preview.vercel.app",
                "canonical_health_code": 404,
                "canonical_health_status": "not_found",
            },
            {
                "slug": "manifest-fallback-tool",
                "status": "live",
                "vercel_url": "https://manifest-fallback-tool.vercel.app",
            },
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://manifest-fallback-tool-preview.vercel.app")
        self.assertEqual(merged["v"], "https://manifest-fallback-tool-preview.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://manifest-fallback-tool-preview.vercel.app")
        self.assertEqual(health_check_url(merged), "https://manifest-fallback-tool.vercel.app")

    def test_stale_failure_with_successful_fallback_stays_alternate_healthy(self) -> None:
        merged = merge_product_record(
            {
                "slug": "fallback-stale-error",
                "status": "live",
                "vercel_url": "https://fallback-stale-error.vercel.app",
                "health_status": "error_404",
                "last_health_code": 200,
                "last_health_url": "https://fallback-stale-error-preview.vercel.app",
                "canonical_health_code": 404,
                "canonical_health_status": "not_found",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://fallback-stale-error-preview.vercel.app")
        self.assertEqual(merged["v"], "https://fallback-stale-error-preview.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://fallback-stale-error-preview.vercel.app")
        self.assertEqual(merged["canonical_health_code"], 404)
        self.assertEqual(merged["canonical_health_status"], "not_found")

    def test_canonical_success_promotes_stale_fallback_state_back_to_canonical(self) -> None:
        merged = merge_product_record(
            {
                "slug": "temporary-tool",
                "status": "live",
                "vercel_url": "https://temporary-tool-preview.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
                "last_health_url": "https://temporary-tool-preview.vercel.app",
                "canonical_health_status": "healthy",
                "canonical_health_code": 200,
                "canonical_health_url": "https://temporary-tool.vercel.app",
                "canonical_health_checked_at": "2026-04-22T10:00:00Z",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "healthy")
        self.assertEqual(merged["last_health_code"], 200)
        self.assertEqual(merged["last_health_url"], "https://temporary-tool.vercel.app")
        self.assertEqual(merged["vercel_url"], "https://temporary-tool.vercel.app")
        self.assertEqual(merged["v"], "https://temporary-tool.vercel.app")
        self.assertEqual(merged["canonical_health_status"], "healthy")
        self.assertEqual(merged["canonical_health_code"], 200)
        self.assertEqual(merged["canonical_health_url"], "https://temporary-tool.vercel.app")
        self.assertEqual(merged["canonical_health_checked_at"], "2026-04-22T10:00:00Z")

    def test_newer_fallback_snapshot_without_explicit_canonical_probe_keeps_alias_visible(self) -> None:
        merged = merge_product_record(
            {
                "slug": "temporary-tool",
                "status": "live",
                "vercel_url": "https://temporary-tool-preview.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
                "last_health_url": "https://temporary-tool-preview.vercel.app",
                "last_health_check": "2026-04-22T10:05:00Z",
                "canonical_health_status": "healthy",
                "canonical_health_code": 200,
                "canonical_health_url": "https://temporary-tool.vercel.app",
                "canonical_health_checked_at": "2026-04-22T10:00:00Z",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://temporary-tool-preview.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://temporary-tool-preview.vercel.app")
        self.assertEqual(merged["canonical_health_code"], 200)
        self.assertEqual(merged["canonical_health_status"], "healthy")
        self.assertEqual(merged["canonical_health_url"], "https://temporary-tool.vercel.app")
        self.assertEqual(health_check_url(merged), "https://temporary-tool.vercel.app")

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

    def test_effective_health_url_wins_over_legacy_probe_url(self) -> None:
        merged = merge_product_record(
            {
                "slug": "redirect-tool",
                "status": "live",
                "vercel_url": "https://redirect-tool-rose.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://redirect-tool-rose.vercel.app",
                "health_probe_url": "https://redirect-tool-rose.vercel.app",
                "effective_health_url": "https://redirect-tool.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["vercel_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(merged["v"], "https://redirect-tool.vercel.app")
        self.assertEqual(merged["effective_health_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(merged["health_probe_url"], "https://redirect-tool-rose.vercel.app")
        self.assertEqual(health_check_url(merged), "https://redirect-tool.vercel.app")

    def test_healthy_canonical_records_without_canonical_health_code_get_promoted_to_canonical(self) -> None:
        merged = merge_product_record(
            {
                "slug": "drift-tool",
                "status": "live",
                "vercel_url": "https://drift-tool.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://drift-tool.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["vercel_url"], "https://drift-tool.vercel.app")
        self.assertEqual(merged["v"], "https://drift-tool.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://drift-tool.vercel.app")
        self.assertEqual(merged["canonical_health_code"], 200)
        self.assertEqual(merged["canonical_health_status"], "healthy")
        self.assertEqual(health_check_url(merged), "https://drift-tool.vercel.app")

    def test_healthy_preview_alias_without_canonical_probe_stays_alternate_healthy(self) -> None:
        merged = merge_product_record(
            {
                "slug": "drift-tool",
                "status": "live",
                "vercel_url": "https://drift-tool-rose.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://drift-tool-rose.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://drift-tool-rose.vercel.app")
        self.assertEqual(merged["v"], "https://drift-tool-rose.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://drift-tool-rose.vercel.app")
        self.assertIsNone(merged["canonical_health_code"])
        self.assertEqual(merged["canonical_health_status"], "pending")
        self.assertEqual(health_check_url(merged), "https://drift-tool.vercel.app")

    def test_compact_preview_alias_without_health_url_stays_alternate_healthy(self) -> None:
        merged = merge_product_record(
            {
                "slug": "webhook-tester",
                "status": "live",
                "vercel_url": "https://webhook-tester.vercel.app",
                "v": "https://webhook-tester-beryl.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://webhook-tester-beryl.vercel.app")
        self.assertEqual(merged["v"], "https://webhook-tester-beryl.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://webhook-tester-beryl.vercel.app")
        self.assertIsNone(merged["canonical_health_code"])
        self.assertEqual(merged["canonical_health_status"], "pending")
        self.assertEqual(health_check_url(merged), "https://webhook-tester.vercel.app")

    def test_compact_preview_alias_with_alternate_healthy_keeps_fallback_display(self) -> None:
        merged = merge_product_record(
            {
                "slug": "compact-fallback-tool",
                "status": "live",
                "vercel_url": "https://compact-fallback-tool.vercel.app",
                "v": "https://compact-fallback-tool-preview.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://compact-fallback-tool-preview.vercel.app")
        self.assertEqual(merged["v"], "https://compact-fallback-tool-preview.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://compact-fallback-tool-preview.vercel.app")
        self.assertEqual(merged["effective_health_url"], "https://compact-fallback-tool-preview.vercel.app")
        self.assertEqual(health_check_url(merged), "https://compact-fallback-tool.vercel.app")

    def test_stale_effective_canonical_url_does_not_shadow_fallback_alias(self) -> None:
        merged = merge_product_record(
            {
                "slug": "shadowed-fallback-tool",
                "status": "live",
                "vercel_url": "https://shadowed-fallback-tool.vercel.app",
                "deployment_url": "https://shadowed-fallback-tool-preview.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
                "last_health_url": "https://shadowed-fallback-tool-preview.vercel.app",
                "effective_health_url": "https://shadowed-fallback-tool.vercel.app",
                "canonical_health_code": 404,
                "canonical_health_status": "not_found",
                "canonical_health_url": "https://shadowed-fallback-tool.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://shadowed-fallback-tool-preview.vercel.app")
        self.assertEqual(merged["v"], "https://shadowed-fallback-tool-preview.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://shadowed-fallback-tool-preview.vercel.app")
        self.assertEqual(health_check_url(merged), "https://shadowed-fallback-tool.vercel.app")

    def test_alternate_healthy_preview_alias_without_explicit_health_url_keeps_fallback_display(self) -> None:
        public_url = choose_public_vercel_url(
            slug="preview-only-tool",
            state_status="live",
            state_url="https://preview-only-tool.vercel.app",
            manifest_url=None,
            deployment_url="https://preview-only-tool-rose.vercel.app",
            status="live",
            health_status="alternate_healthy",
            last_health_code=200,
            health_url=None,
        )

        self.assertEqual(public_url, "https://preview-only-tool-rose.vercel.app")

    def test_healthy_preview_alias_without_explicit_health_url_keeps_fallback_display(self) -> None:
        public_url = choose_public_vercel_url(
            slug="preview-only-tool",
            state_status="live",
            state_url="https://preview-only-tool-rose.vercel.app",
            manifest_url=None,
            deployment_url=None,
            status="live",
            health_status="healthy",
            last_health_code=200,
            health_url=None,
        )

        self.assertEqual(public_url, "https://preview-only-tool-rose.vercel.app")

    def test_healthy_preview_alias_with_explicit_health_url_keeps_fallback_display(self) -> None:
        public_url = choose_public_vercel_url(
            slug="preview-only-tool",
            state_status="live",
            state_url="https://preview-only-tool.vercel.app",
            manifest_url=None,
            deployment_url=None,
            status="live",
            health_status="healthy",
            last_health_code=200,
            health_url="https://preview-only-tool-rose.vercel.app",
        )

        self.assertEqual(public_url, "https://preview-only-tool-rose.vercel.app")

    def test_deployment_alias_without_explicit_health_url_stays_alternate_healthy(self) -> None:
        merged = merge_product_record(
            {
                "slug": "deployment-alias-tool",
                "status": "live",
                "vercel_url": "https://deployment-alias-tool.vercel.app",
                "deployment_url": "https://deployment-alias-tool-rose.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://deployment-alias-tool-rose.vercel.app")
        self.assertEqual(merged["v"], "https://deployment-alias-tool-rose.vercel.app")
        self.assertEqual(merged["deployment_url"], "https://deployment-alias-tool-rose.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://deployment-alias-tool-rose.vercel.app")
        self.assertEqual(health_check_url(merged), "https://deployment-alias-tool.vercel.app")

    def test_deployment_alias_with_health_timestamp_keeps_fallback_display(self) -> None:
        merged = merge_product_record(
            {
                "slug": "deployment-timestamp-tool",
                "status": "live",
                "vercel_url": "https://deployment-timestamp-tool.vercel.app",
                "deployment_url": "https://deployment-timestamp-tool-rose.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_check": "2026-04-23T10:00:00Z",
                "health_checked_at": "2026-04-23T10:00:00Z",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://deployment-timestamp-tool-rose.vercel.app")
        self.assertEqual(merged["v"], "https://deployment-timestamp-tool-rose.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://deployment-timestamp-tool-rose.vercel.app")
        self.assertEqual(health_check_url(merged), "https://deployment-timestamp-tool.vercel.app")

    def test_deployment_alias_without_health_timestamp_stays_visible(self) -> None:
        merged = merge_product_record(
            {
                "slug": "deployment-no-timestamp-tool",
                "status": "live",
                "vercel_url": "https://deployment-no-timestamp-tool.vercel.app",
                "deployment_url": "https://deployment-no-timestamp-tool-rose.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(merged["vercel_url"], "https://deployment-no-timestamp-tool-rose.vercel.app")
        self.assertEqual(merged["v"], "https://deployment-no-timestamp-tool-rose.vercel.app")
        self.assertEqual(merged["deployment_url"], "https://deployment-no-timestamp-tool-rose.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://deployment-no-timestamp-tool-rose.vercel.app")
        self.assertEqual(health_check_url(merged), "https://deployment-no-timestamp-tool.vercel.app")

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

    def test_stale_canonical_failure_refreshed_from_current_live_outage(self) -> None:
        merged = merge_product_record(
            {
                "slug": "html-entity-encoder",
                "status": "live",
                "vercel_url": "https://html-entity-encoder.vercel.app",
                "health_status": "deployment_disabled",
                "last_health_code": 402,
                "last_health_url": "https://html-entity-encoder.vercel.app",
                "canonical_health_code": 0,
                "canonical_health_status": "timeout",
                "canonical_health_url": "https://html-entity-encoder.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "deployment_disabled")
        self.assertEqual(merged["last_health_code"], 402)
        self.assertEqual(merged["canonical_health_code"], 402)
        self.assertEqual(merged["canonical_health_status"], "deployment_disabled")
        self.assertEqual(merged["canonical_health_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(health_check_url(merged), "https://html-entity-encoder.vercel.app")

    def test_newer_canonical_success_overrides_stale_canonical_failure(self) -> None:
        merged = merge_product_record(
            {
                "slug": "redirect-tool",
                "status": "live",
                "vercel_url": "https://redirect-tool.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
                "last_health_url": "https://redirect-tool.vercel.app",
                "last_health_check": "2026-04-23T10:05:00Z",
                "canonical_health_status": "not_found",
                "canonical_health_code": 404,
                "canonical_health_url": "https://redirect-tool.vercel.app",
                "canonical_health_checked_at": "2026-04-23T10:00:00Z",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "healthy")
        self.assertEqual(merged["vercel_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(merged["last_health_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(merged["canonical_health_code"], 200)
        self.assertEqual(merged["canonical_health_status"], "healthy")
        self.assertEqual(merged["canonical_health_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(merged["canonical_health_checked_at"], "2026-04-23T10:05:00Z")

    def test_redirected_canonical_success_keeps_fallback_alias_visible(self) -> None:
        merged = merge_product_record(
            {
                "slug": "html-entity-encoder",
                "status": "live",
                "vercel_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
                "health_probe_url": "https://html-entity-encoder.vercel.app",
                "last_health_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "effective_health_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "canonical_health_code": 200,
                "canonical_health_status": "healthy",
                "canonical_health_url": "https://html-entity-encoder.vercel.app",
                "canonical_health_checked_at": "2026-04-23T10:05:00Z",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(
            merged["vercel_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(
            merged["last_health_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(merged["canonical_health_code"], 200)
        self.assertEqual(merged["canonical_health_status"], "redirected_preview_alias")
        self.assertEqual(merged["canonical_health_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(merged["canonical_probe_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(health_check_url(merged), "https://html-entity-encoder.vercel.app")

    def test_stale_effective_canonical_url_still_keeps_fallback_alias_visible(self) -> None:
        merged = merge_product_record(
            {
                "slug": "html-entity-encoder",
                "status": "live",
                "vercel_url": "https://html-entity-encoder.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
                "last_health_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "effective_health_url": "https://html-entity-encoder.vercel.app",
                "canonical_health_code": 200,
                "canonical_health_status": "healthy",
                "canonical_health_url": "https://html-entity-encoder.vercel.app",
                "canonical_health_checked_at": "2026-04-23T10:05:00Z",
                "canonical_probe_url": "https://html-entity-encoder.vercel.app",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(
            merged["vercel_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(
            merged["last_health_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(
            merged["effective_health_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(merged["canonical_health_code"], 200)
        self.assertEqual(merged["canonical_health_status"], "redirected_preview_alias")
        self.assertEqual(merged["canonical_health_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(merged["canonical_probe_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(health_check_url(merged), "https://html-entity-encoder.vercel.app")

    def test_canonical_probe_url_preserves_redirected_fallback_when_health_probe_is_fallback(self) -> None:
        merged = merge_product_record(
            {
                "slug": "html-entity-encoder",
                "status": "live",
                "vercel_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
                "health_probe_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "canonical_probe_url": "https://html-entity-encoder.vercel.app",
                "last_health_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "effective_health_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "canonical_health_code": 200,
                "canonical_health_status": "healthy",
                "canonical_health_url": "https://html-entity-encoder.vercel.app",
                "canonical_health_checked_at": "2026-04-23T10:05:00Z",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "alternate_healthy")
        self.assertEqual(
            merged["vercel_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(merged["health_probe_url"], "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app")
        self.assertEqual(merged["canonical_probe_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(merged["canonical_health_status"], "redirected_preview_alias")
        self.assertEqual(health_check_url(merged), "https://html-entity-encoder.vercel.app")

    def test_newer_canonical_failure_beats_stale_fallback_success(self) -> None:
        merged = merge_product_record(
            {
                "slug": "stale-fallback-tool",
                "status": "live",
                "vercel_url": "https://stale-fallback-tool-preview.vercel.app",
                "deployment_url": "https://stale-fallback-tool-preview.vercel.app",
                "health_status": "alternate_healthy",
                "last_health_code": 200,
                "last_health_url": "https://stale-fallback-tool-preview.vercel.app",
                "effective_health_url": "https://stale-fallback-tool-preview.vercel.app",
                "last_health_check": "2026-04-23T10:00:00Z",
                "canonical_health_code": 404,
                "canonical_health_status": "not_found",
                "canonical_health_url": "https://stale-fallback-tool.vercel.app",
                "canonical_health_checked_at": "2026-04-23T10:05:00Z",
            },
            None,
        )

        self.assertEqual(merged["health_status"], "not_found")
        self.assertEqual(merged["last_health_code"], 404)
        self.assertEqual(merged["last_health_url"], "https://stale-fallback-tool.vercel.app")
        self.assertEqual(merged["canonical_health_code"], 404)
        self.assertEqual(merged["canonical_health_status"], "not_found")
        self.assertEqual(merged["vercel_url"], "https://stale-fallback-tool.vercel.app")
        self.assertEqual(merged["deployment_url"], "https://stale-fallback-tool-preview.vercel.app")

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

    def test_sync_state_snapshot_reconciles_alternate_health_fallback_url(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Webhook Tester",
                        "slug": "webhook-tester",
                        "status": "live",
                        "vercel_url": "https://webhook-tester.vercel.app",
                        "v": "https://webhook-tester-beryl.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://webhook-tester-beryl.vercel.app",
                    }
                ],
                "spec_ready": [],
            }
        }

        synced = sync_state_snapshot(state)
        product = synced["products"]["active"][0]

        self.assertEqual(product["vercel_url"], "https://webhook-tester-beryl.vercel.app")
        self.assertEqual(product["v"], "https://webhook-tester-beryl.vercel.app")
        self.assertEqual(product["last_health_url"], "https://webhook-tester-beryl.vercel.app")
        self.assertEqual(product["health_status"], "alternate_healthy")

    def test_sync_state_snapshot_without_manifest_promotes_canonical_health_url(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Orphan Tool",
                        "slug": "orphan-tool",
                        "status": "live",
                        "vercel_url": "https://orphan-tool-rose.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://orphan-tool.vercel.app",
                    }
                ],
                "spec_ready": [],
            }
        }

        synced = sync_state_snapshot(state, product_catalog={})
        product = synced["products"]["active"][0]

        self.assertEqual(product["vercel_url"], "https://orphan-tool.vercel.app")
        self.assertEqual(product["v"], "https://orphan-tool.vercel.app")
        self.assertEqual(product["last_health_url"], "https://orphan-tool.vercel.app")

    def test_sync_state_products_deduplicates_duplicate_slugs(self) -> None:
        products = [
            {
                "name": "Duplicate Tool",
                "slug": "duplicate-tool",
                "status": "live",
                "vercel_url": "https://duplicate-tool.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
            },
            {
                "name": "Duplicate Tool",
                "slug": "duplicate-tool",
                "status": "live",
                "vercel_url": "https://duplicate-tool.vercel.app",
                "health_status": "healthy",
                "last_health_code": 200,
            },
        ]

        synced = sync_state_products(products)

        self.assertEqual(len(synced), 1)
        self.assertEqual(synced[0]["slug"], "duplicate-tool")
        self.assertEqual(synced[0]["vercel_url"], "https://duplicate-tool.vercel.app")


if __name__ == "__main__":
    unittest.main()
