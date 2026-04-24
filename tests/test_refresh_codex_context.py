import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch

from scripts import refresh_codex_context
from scripts.refresh_codex_context import (
    determine_focus,
    effective_next_action,
    render_codex_task,
    render_oneri,
    render_sorun_analizi,
)


class RefreshCodexContextTests(unittest.TestCase):
    def test_focus_prefers_live_health_over_other_signals(self) -> None:
        summary = {
            "live_count": 10,
            "healthy_count": 9,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 1,
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "broken-live-tool",
                        "code": 401,
                        "health_status": "unauthorized",
                        "url": "https://broken-live-tool.vercel.app",
                    }
                ],
                "missing_checkout": [],
                "missing_url": [],
            },
        }
        issues = [
            {
                "issue_type": "checkout_field_inconsistency",
                "severity": "medium",
                "status": "open",
                "description": "Multiple checkout fields",
            }
        ]

        focus = determine_focus(summary, issues)

        self.assertEqual(focus.key, "live_health")
        self.assertIn("broken-live-tool", focus.summary)

    def test_focus_live_health_mentions_pending_health_when_present(self) -> None:
        summary = {
            "live_count": 10,
            "healthy_count": 8,
            "pending_health_count": 2,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 2,
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "broken-live-tool",
                        "code": 401,
                        "health_status": "unauthorized",
                        "url": "https://broken-live-tool.vercel.app",
                    }
                ],
                "pending_health": [
                    {
                        "slug": "pending-tool-a",
                        "code": None,
                        "health_status": "pending",
                        "url": "https://pending-tool-a.vercel.app",
                    },
                    {
                        "slug": "pending-tool-b",
                        "code": None,
                        "health_status": "pending",
                        "url": "https://pending-tool-b.vercel.app",
                    },
                ],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [],
            },
        }

        focus = determine_focus(summary, [])

        self.assertEqual(focus.key, "live_health")
        self.assertIn("2 canlı ürün health snapshot bekliyor", focus.summary)
        self.assertIn("health snapshot bekliyor", focus.codex_task_body)

    def test_focus_uses_pending_health_when_no_outages_exist(self) -> None:
        summary = {
            "live_count": 10,
            "healthy_count": 8,
            "pending_health_count": 2,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 2,
            "gaps": {
                "unhealthy_live": [],
                "pending_health": [
                    {
                        "slug": "pending-tool-a",
                        "code": None,
                        "health_status": "pending",
                        "url": "https://pending-tool-a.vercel.app",
                    },
                    {
                        "slug": "pending-tool-b",
                        "code": None,
                        "health_status": "pending",
                        "url": "https://pending-tool-b.vercel.app",
                    },
                ],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [],
            },
        }

        focus = determine_focus(summary, [])

        self.assertEqual(focus.key, "health_pending")
        self.assertIn("health snapshot bekliyor", focus.summary)

    def test_focus_prefers_deploy_readiness_over_generic_url_gaps(self) -> None:
        summary = {
            "live_count": 10,
            "healthy_count": 10,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 0,
            "deploy_readiness_count": 1,
            "gaps": {
                "unhealthy_live": [],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": ["agent-prompt-engineer"],
                "canonical_url_drift": [],
                "deploy_readiness": [
                    {
                        "slug": "agent-prompt-engineer",
                        "manifest_problem": "missing",
                        "missing_manifest_fields": ["tagline", "description"],
                        "missing_url_fields": ["vercel_url", "checkout_url"],
                        "missing_state_fields": ["payment_provider"],
                    }
                ],
            },
        }

        focus = determine_focus(summary, [])

        self.assertEqual(focus.key, "deploy_readiness")
        self.assertIn("manifest=missing", focus.summary)
        self.assertIn(
            "Eksik manifest/URL/state alanlarını raporla", focus.codex_task_body
        )

    def test_focus_live_health_mentions_canonical_drift_when_present(self) -> None:
        summary = {
            "live_count": 10,
            "healthy_count": 8,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 2,
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "broken-live-tool",
                        "code": 500,
                        "health_status": "error_500",
                        "url": "https://broken-live-tool.vercel.app",
                    }
                ],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [
                    {
                        "slug": "fallback-tool",
                        "url": "https://fallback-tool-preview.vercel.app",
                        "ideal_url": "https://fallback-tool.vercel.app",
                    }
                ],
            },
        }

        focus = determine_focus(summary, [])

        self.assertEqual(focus.key, "live_health")
        self.assertIn("fallback alias", focus.summary)
        self.assertIn("fallback alias", focus.codex_task_body)

    def test_focus_live_health_uses_outage_title_when_canonical_drift_absent(
        self,
    ) -> None:
        summary = {
            "live_count": 4,
            "healthy_count": 3,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 1,
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "broken-live-tool",
                        "code": 404,
                        "health_status": "not_found",
                        "url": "https://broken-live-tool.vercel.app",
                    }
                ],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [],
            },
        }

        focus = determine_focus(summary, [])

        self.assertEqual(focus.key, "live_health")
        self.assertEqual(focus.codex_task_title, "Canlı sağlık açığını düzelt")
        self.assertIn("Canonical drift yok", focus.codex_task_body)

    def test_focus_uses_checkout_field_issue_when_live_portfolio_is_healthy(
        self,
    ) -> None:
        summary = {
            "live_count": 113,
            "healthy_count": 113,
            "pending_health_count": 0,
            "fallback_healthy_count": 3,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 18,
            "gaps": {
                "unhealthy_live": [],
                "missing_checkout": [],
                "missing_url": ["ssl-cert-checker", "security-headers-checker"],
            },
        }
        issues = [
            {
                "issue_type": "checkout_field_inconsistency",
                "severity": "medium",
                "status": "open",
                "description": "Multiple checkout fields",
            }
        ]

        focus = determine_focus(summary, issues)

        self.assertEqual(focus.key, "checkout_field_inconsistency")
        self.assertIn("metadata", focus.summary)

    def test_load_summary_rebuilds_from_state_even_if_stale_summary_exists(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            state_file = tmp_path / "STATE.json"
            summary_file = tmp_path / "STATE_SUMMARY.json"

            state_file.write_text(
                json.dumps(
                    {
                        "cycle": 1108,
                        "products": {
                            "active": [
                                {
                                    "name": "Fallback Tool",
                                    "slug": "fallback-tool",
                                    "status": "live",
                                    "vercel_url": "https://fallback-tool-preview.vercel.app",
                                    "health_status": "alternate_healthy",
                                    "last_health_code": 200,
                                    "last_health_url": "https://fallback-tool-preview.vercel.app",
                                    "canonical_health_url": "https://fallback-tool.vercel.app",
                                    "canonical_health_status": "not_found",
                                    "canonical_health_code": 404,
                                }
                            ]
                        },
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            summary_file.write_text(
                json.dumps(
                    {
                        "healthy_count": 999,
                        "canonical_url_drift": 0,
                        "fallback_healthy_count": 0,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            with (
                patch.object(refresh_codex_context, "STATE_FILE", state_file),
                patch.object(refresh_codex_context, "SUMMARY_FILE", summary_file),
                patch.object(
                    refresh_codex_context, "refresh_live_health", return_value=None
                ),
                patch.object(
                    refresh_codex_context, "load_product_catalog", return_value={}
                ),
            ):
                summary = refresh_codex_context.load_summary()

            self.assertEqual(summary["healthy_count"], 1)
            self.assertEqual(summary["canonical_healthy_count"], 0)
            self.assertEqual(summary["fallback_healthy_count"], 1)
            self.assertEqual(summary["canonical_url_drift"], 1)
            self.assertEqual(summary["canonical_url_drift_products"], ["fallback-tool"])
            self.assertEqual(
                summary["gaps"]["canonical_url_drift"][0]["slug"], "fallback-tool"
            )

            persisted = json.loads(summary_file.read_text(encoding="utf-8"))
            self.assertEqual(persisted["healthy_count"], 1)
            self.assertEqual(persisted["canonical_url_drift"], 1)
            self.assertEqual(persisted["fallback_healthy_count"], 1)

    def test_rendered_deploy_readiness_sections_include_missing_fields(self) -> None:
        summary = {
            "cycle": 1108,
            "mode": "OPTIMIZE",
            "live_count": 10,
            "healthy_count": 10,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 0,
            "deploy_readiness_count": 1,
            "deploy_readiness_manifest_gap_count": 1,
            "deploy_readiness_url_gap_count": 1,
            "deploy_readiness_state_gap_count": 1,
            "spec_ready_count": 11,
            "next_action": "html-entity-encoder Vercel Dashboard manuel kontrol",
            "gaps": {
                "unhealthy_live": [],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [],
                "deploy_readiness": [
                    {
                        "slug": "agent-prompt-engineer",
                        "manifest_problem": "missing",
                        "missing_manifest_fields": ["tagline", "description"],
                        "missing_url_fields": ["vercel_url", "checkout_url"],
                        "missing_state_fields": ["payment_provider"],
                    }
                ],
            },
        }

        focus = determine_focus(summary, [])
        rendered_oneri = render_oneri(
            summary, [], focus, datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc)
        )
        rendered_task = render_codex_task(
            summary, focus, datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc)
        )

        self.assertIn("Deploy readiness gap", rendered_oneri)
        self.assertIn("Deploy Readiness Issues", rendered_oneri)
        self.assertIn("agent-prompt-engineer", rendered_oneri)
        self.assertIn("Deploy readiness gap", rendered_task)
        self.assertIn("manifest/URL/state", rendered_task)

    def test_rendered_sorun_analizi_shows_canonical_health_details_for_outages(
        self,
    ) -> None:
        summary = {
            "cycle": 1110,
            "live_count": 2,
            "healthy_count": 1,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 1,
            "deploy_readiness_count": 0,
            "spec_ready_count": 0,
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "fallback-stale-error",
                        "code": 401,
                        "health_status": "unauthorized",
                        "url": "https://fallback-stale-error-preview.vercel.app",
                        "probe_url": "https://fallback-stale-error.vercel.app",
                        "effective_url": "https://fallback-stale-error-final.vercel.app",
                        "canonical_url": "https://fallback-stale-error.vercel.app",
                        "canonical_code": 404,
                        "canonical_status": "not_found",
                    }
                ],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [],
                "deploy_readiness": [],
            },
        }

        focus = determine_focus(summary, [])
        rendered = render_sorun_analizi(
            summary,
            [],
            focus,
            datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc),
        )

        self.assertIn("canonical_url=https://fallback-stale-error.vercel.app", rendered)
        self.assertIn(
            "effective_url=https://fallback-stale-error-final.vercel.app", rendered
        )
        self.assertIn("canonical_code=404", rendered)
        self.assertIn("canonical_status=not_found", rendered)

    def test_focus_prefers_canonical_drift_when_health_is_clean(self) -> None:
        summary = {
            "live_count": 77,
            "healthy_count": 77,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 24,
            "canonical_url_drift": 1,
            "gaps": {
                "unhealthy_live": [],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [
                    {
                        "slug": "diffmaster",
                        "url": "https://diffmaster-rose.vercel.app",
                        "ideal_url": "https://diffmaster.vercel.app",
                    }
                ],
            },
        }

        focus = determine_focus(summary, [])

        self.assertEqual(focus.key, "canonical_url_drift")
        self.assertIn("diffmaster", focus.summary)

    def test_rendered_sorun_analizi_shows_canonical_drift_health_details(self) -> None:
        summary = {
            "cycle": 1111,
            "live_count": 1,
            "healthy_count": 1,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 0,
            "deploy_readiness_count": 0,
            "spec_ready_count": 0,
            "gaps": {
                "unhealthy_live": [],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [
                    {
                        "slug": "fallback-tool",
                        "url": "https://fallback-tool-preview.vercel.app",
                        "ideal_url": "https://fallback-tool.vercel.app",
                        "health_status": "alternate_healthy",
                        "health_code": 200,
                        "probe_url": "https://fallback-tool-preview.vercel.app",
                        "canonical_url": "https://fallback-tool.vercel.app",
                        "canonical_code": 404,
                        "canonical_status": "not_found",
                    }
                ],
                "deploy_readiness": [],
            },
        }

        focus = determine_focus(summary, [])
        rendered = render_sorun_analizi(
            summary,
            [],
            focus,
            datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc),
        )

        self.assertIn("health=alternate_healthy", rendered)
        self.assertIn("code=200", rendered)
        self.assertIn("canonical_code=404", rendered)
        self.assertIn("canonical_status=not_found", rendered)

    def test_rendered_codex_task_mentions_generated_guardrails(self) -> None:
        summary = {
            "cycle": 1063,
            "live_count": 113,
            "healthy_count": 113,
            "canonical_healthy_count": 110,
            "pending_health_count": 0,
            "fallback_healthy_count": 3,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 18,
            "spec_ready_count": 27,
            "next_action": "prepare_new_products_wait_deploy",
        }
        focus = determine_focus(
            {
                **summary,
                "gaps": {
                    "unhealthy_live": [],
                    "missing_checkout": [],
                    "missing_url": [],
                },
            },
            [],
        )

        rendered = render_codex_task(
            summary, focus, datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc)
        )

        self.assertIn("Generated 2026-04-22 12:00 UTC", rendered)
        self.assertIn("Canonical drift: 0", rendered)
        self.assertIn("Canonical healthy: 110/113", rendered)
        self.assertIn("Manual Vercel/ödeme-provider", rendered)
        self.assertIn("analysis/codex_result.md", rendered)
        self.assertIn("Health pending: 0", rendered)
        self.assertIn("Fallback healthy: 3", rendered)

    def test_manual_vercel_next_action_is_replaced_by_live_health_action(self) -> None:
        summary = {
            "cycle": 1108,
            "mode": "OPTIMIZE",
            "live_count": 88,
            "healthy_count": 85,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 7,
            "deploy_readiness_count": 20,
            "deploy_readiness_manifest_gap_count": 3,
            "deploy_readiness_url_gap_count": 20,
            "deploy_readiness_state_gap_count": 20,
            "canonical_url_drift": 1,
            "fallback_healthy_count": 4,
            "spec_ready_count": 26,
            "next_action": "html-entity-encoder Vercel Dashboard manuel kontrol",
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "jwt-generator",
                        "code": 500,
                        "health_status": "error_500",
                        "url": "https://jwt-generator.vercel.app",
                    }
                ],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [
                    {
                        "slug": "html-entity-encoder",
                        "url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                        "ideal_url": "https://html-entity-encoder.vercel.app",
                        "health_status": "alternate_healthy",
                        "health_code": 200,
                    }
                ],
                "fallback_healthy": [
                    {
                        "slug": "html-entity-encoder",
                        "url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                        "ideal_url": "https://html-entity-encoder.vercel.app",
                        "health_status": "alternate_healthy",
                        "health_code": 200,
                        "probe_url": "https://html-entity-encoder.vercel.app",
                        "canonical_url": "https://html-entity-encoder.vercel.app",
                        "canonical_code": 200,
                        "canonical_status": "redirected_preview_alias",
                    }
                ],
                "deploy_readiness": [],
            },
        }

        focus = determine_focus(summary, [])
        rendered_oneri = render_oneri(
            summary, [], focus, datetime(2026, 4, 23, 6, 42, tzinfo=timezone.utc)
        )
        rendered_task = render_codex_task(
            summary, focus, datetime(2026, 4, 23, 6, 42, tzinfo=timezone.utc)
        )

        self.assertEqual(focus.key, "live_health")
        self.assertNotIn("manuel kontrol", rendered_oneri)
        self.assertNotIn("manuel kontrol", rendered_task)
        self.assertIn("canlı ürünü düzelt", rendered_oneri)
        self.assertIn("fallback alias'ı görünür tut", rendered_task)
        self.assertIn("- Fallback healthy slugs: `html-entity-encoder`", rendered_task)
        self.assertIn("## Fallback Alias Ürünleri", rendered_oneri)
        self.assertIn(
            "- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app health=alternate_healthy code=200 probe=https://html-entity-encoder.vercel.app canonical_code=200 canonical_status=redirected_preview_alias",
            rendered_oneri,
        )

    def test_stale_non_manual_next_action_is_replaced_by_live_gap_summary(self) -> None:
        summary = {
            "cycle": 1109,
            "mode": "OPTIMIZE",
            "live_count": 89,
            "healthy_count": 86,
            "pending_health_count": 0,
            "checkout_gap_count": 1,
            "deploy_missing_or_bad_url": 16,
            "deploy_readiness_count": 27,
            "deploy_readiness_manifest_gap_count": 0,
            "deploy_readiness_url_gap_count": 27,
            "deploy_readiness_state_gap_count": 24,
            "canonical_url_drift": 4,
            "fallback_healthy_count": 4,
            "spec_ready_count": 22,
            "next_action": "prepare_new_products_wait_deploy",
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "jwt-generator",
                        "code": 500,
                        "health_status": "error_500",
                        "url": "https://jwt-generator.vercel.app",
                    }
                ],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [
                    {
                        "slug": "html-entity-encoder",
                        "url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                        "ideal_url": "https://html-entity-encoder.vercel.app",
                        "health_status": "alternate_healthy",
                        "health_code": 200,
                    }
                ],
                "fallback_healthy": [
                    {
                        "slug": "html-entity-encoder",
                        "url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                        "ideal_url": "https://html-entity-encoder.vercel.app",
                        "health_status": "alternate_healthy",
                        "health_code": 200,
                        "probe_url": "https://html-entity-encoder.vercel.app",
                        "canonical_url": "https://html-entity-encoder.vercel.app",
                        "canonical_code": 200,
                        "canonical_status": "redirected_preview_alias",
                    }
                ],
                "deploy_readiness": [],
            },
        }

        focus = determine_focus(summary, [])
        self.assertEqual(
            effective_next_action(summary, focus),
            "1 canlı ürünü düzelt; 1 fallback alias'ı görünür tut",
        )

        rendered_task = render_codex_task(
            summary, focus, datetime(2026, 4, 24, 5, 0, tzinfo=timezone.utc)
        )
        rendered_oneri = render_oneri(
            summary, [], focus, datetime(2026, 4, 24, 5, 0, tzinfo=timezone.utc)
        )

        self.assertNotIn("prepare_new_products_wait_deploy", rendered_task)
        self.assertNotIn("prepare_new_products_wait_deploy", rendered_oneri)
        self.assertIn("1 canlı ürünü düzelt; 1 fallback alias'ı görünür tut", rendered_task)
        self.assertIn("1 canlı ürünü düzelt; 1 fallback alias'ı görünür tut", rendered_oneri)

    def test_compact_state_still_surfaces_canonical_drift_slugs_when_gap_details_are_missing(
        self,
    ) -> None:
        summary = {
            "cycle": 1109,
            "mode": "OPTIMIZE",
            "live_count": 2,
            "healthy_count": 1,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 1,
            "deploy_readiness_count": 0,
            "deploy_readiness_manifest_gap_count": 0,
            "deploy_readiness_url_gap_count": 0,
            "deploy_readiness_state_gap_count": 0,
            "canonical_url_drift": 1,
            "fallback_healthy_count": 1,
            "spec_ready_count": 0,
            "next_action": "prepare_new_products_wait_deploy",
            "products": [
                {
                    "n": "Broken Tool",
                    "s": "broken-tool",
                    "st": "live",
                    "v": "https://broken-tool.vercel.app",
                    "c": None,
                },
                {
                    "n": "Fallback Tool",
                    "s": "fallback-tool",
                    "st": "live",
                    "v": "https://fallback-tool-preview.vercel.app",
                    "c": None,
                },
            ],
            "fallback_healthy_products": ["fallback-tool"],
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "broken-tool",
                        "code": 500,
                        "health_status": "error_500",
                        "url": "https://broken-tool.vercel.app",
                    }
                ],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": [],
                "fallback_healthy": [],
                "deploy_readiness": [],
            },
        }

        focus = determine_focus(summary, [])
        rendered_oneri = render_oneri(
            summary, [], focus, datetime(2026, 4, 24, 5, 0, tzinfo=timezone.utc)
        )
        rendered_task = render_codex_task(
            summary, focus, datetime(2026, 4, 24, 5, 0, tzinfo=timezone.utc)
        )

        self.assertEqual(focus.key, "live_health")
        self.assertEqual(
            effective_next_action(summary, focus),
            "1 canlı ürünü düzelt; 1 fallback alias'ı görünür tut",
        )
        self.assertIn("## Canonical Drift Ürünleri", rendered_oneri)
        self.assertIn(
            "- `fallback-tool` — current=https://fallback-tool-preview.vercel.app ideal=https://fallback-tool.vercel.app",
            rendered_oneri,
        )
        self.assertIn("- Canonical drift slugs: `fallback-tool`", rendered_task)
        self.assertIn("- Fallback healthy slugs: `fallback-tool`", rendered_task)

    def test_compact_state_rebuilds_fallback_alias_visibility_without_explicit_lists(
        self,
    ) -> None:
        summary = {
            "cycle": 1110,
            "mode": "OPTIMIZE",
            "live_count": 2,
            "healthy_count": 1,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 1,
            "deploy_readiness_count": 0,
            "deploy_readiness_manifest_gap_count": 0,
            "deploy_readiness_url_gap_count": 0,
            "deploy_readiness_state_gap_count": 0,
            "canonical_url_drift": 1,
            "fallback_healthy_count": 1,
            "spec_ready_count": 0,
            "next_action": "prepare_new_products_wait_deploy",
            "products": [
                {
                    "n": "Broken Tool",
                    "s": "broken-tool",
                    "st": "live",
                    "v": "https://broken-tool.vercel.app",
                    "c": None,
                },
                {
                    "n": "Fallback Tool",
                    "s": "fallback-tool",
                    "st": "live",
                    "v": "https://fallback-tool-preview.vercel.app",
                    "c": None,
                },
            ],
            "gaps": {
                "unhealthy_live": [
                    {
                        "slug": "broken-tool",
                        "code": 500,
                        "health_status": "error_500",
                        "url": "https://broken-tool.vercel.app",
                    }
                ],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [],
                "fallback_healthy": [],
                "deploy_readiness": [],
            },
        }

        focus = determine_focus(summary, [])
        rendered_oneri = render_oneri(
            summary, [], focus, datetime(2026, 4, 24, 5, 0, tzinfo=timezone.utc)
        )
        rendered_task = render_codex_task(
            summary, focus, datetime(2026, 4, 24, 5, 0, tzinfo=timezone.utc)
        )

        self.assertEqual(focus.key, "live_health")
        self.assertIn("## Fallback Alias Ürünleri", rendered_oneri)
        self.assertIn(
            "- `fallback-tool` — current=https://fallback-tool-preview.vercel.app ideal=https://fallback-tool.vercel.app",
            rendered_oneri,
        )
        self.assertIn("- Canonical drift slugs: `fallback-tool`", rendered_task)
        self.assertIn("- Fallback healthy slugs: `fallback-tool`", rendered_task)

    def test_load_summary_refreshes_live_health_before_rebuilding_context(self) -> None:
        summary = {
            "cycle": 1103,
            "live_count": 1,
            "healthy_count": 1,
            "pending_health_count": 0,
            "checkout_gap_count": 0,
            "deploy_missing_or_bad_url": 0,
            "gaps": {
                "unhealthy_live": [],
                "pending_health": [],
                "missing_checkout": [],
                "missing_url": [],
                "canonical_url_drift": [],
            },
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            state_file = tmp_path / "STATE.json"
            summary_file = tmp_path / "STATE_SUMMARY.json"
            state_file.write_text(
                json.dumps(
                    {
                        "cycle": 1103,
                        "mode": "OPTIMIZE",
                        "balance": 0,
                        "products": {"active": [], "spec_ready": []},
                    }
                ),
                encoding="utf-8",
            )
            summary_file.write_text(json.dumps(summary), encoding="utf-8")

            with (
                patch.object(refresh_codex_context, "STATE_FILE", state_file),
                patch.object(refresh_codex_context, "SUMMARY_FILE", summary_file),
                patch.object(
                    refresh_codex_context.subprocess,
                    "run",
                    return_value=Mock(returncode=1),
                ) as run_mock,
                patch.object(
                    refresh_codex_context, "build_summary", return_value=summary
                ) as build_mock,
            ):
                loaded = refresh_codex_context.load_summary()

            self.assertEqual(loaded, summary)
            build_mock.assert_called_once()
            self.assertTrue(run_mock.called)
            audit_args = run_mock.call_args[0][0]
            self.assertIn("audit_portfolio_health.py", audit_args[1])
            self.assertEqual(
                run_mock.call_args.kwargs["cwd"], refresh_codex_context.ROOT
            )
            self.assertEqual(
                json.loads(summary_file.read_text(encoding="utf-8")), summary
            )


if __name__ == "__main__":
    unittest.main()
