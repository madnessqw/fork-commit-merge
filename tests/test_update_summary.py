import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts import update_summary
from scripts.update_summary import (
    build_summary,
    canonical_url_drift_entry,
    is_placeholder_product,
    normalize_product,
    persist_summary,
)


class UpdateSummaryTests(unittest.TestCase):
    def test_manual_dashboard_next_action_is_replaced_with_live_gap_summary(self) -> None:
        state = {
            "next_action": "html-entity-encoder Vercel Dashboard manuel kontrol",
            "products": {
                "active": [
                    {
                        "name": "Broken Tool",
                        "slug": "broken-tool",
                        "status": "live",
                        "vercel_url": "https://broken-tool.vercel.app",
                        "health_status": "error_500",
                        "last_health_code": 500,
                    },
                    {
                        "name": "Fallback Tool",
                        "slug": "fallback-tool",
                        "status": "live",
                        "vercel_url": "https://fallback-tool.vercel.app",
                        "deployment_url": "https://fallback-tool-preview.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://fallback-tool-preview.vercel.app",
                        "effective_health_url": "https://fallback-tool-preview.vercel.app",
                    },
                ]
            },
        }

        summary = build_summary(state)

        self.assertEqual(summary["unhealthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["next_action"], "1 canlı ürünü düzelt; 1 fallback alias'ı görünür tut")

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

    def test_newer_fallback_duplicate_preserves_visibility_and_checkout_metadata(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Duplicate Tool",
                        "slug": "duplicate-tool",
                        "status": "live",
                        "vercel_url": "https://duplicate-tool.vercel.app",
                        "checkout_url": "https://checkout.example/duplicate-tool",
                        "health_status": "healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://duplicate-tool.vercel.app",
                        "last_health_check": "2026-04-23T10:00:00Z",
                        "canonical_health_code": 404,
                        "canonical_health_status": "not_found",
                    },
                    {
                        "name": "Duplicate Tool",
                        "slug": "duplicate-tool",
                        "status": "live",
                        "vercel_url": "https://duplicate-tool-preview.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://duplicate-tool-preview.vercel.app",
                        "effective_health_url": "https://duplicate-tool-preview.vercel.app",
                        "health_checked_at": "2026-04-23T11:00:00Z",
                    },
                ],
                "spec_ready": [],
            },
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["fallback_healthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["duplicate-tool"])
        self.assertEqual(summary["products"][0]["v"], "https://duplicate-tool-preview.vercel.app")
        self.assertEqual(summary["products"][0]["c"], "https://checkout.example/duplicate-tool")

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

    def test_legacy_checkout_field_counts_as_checkout(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Legacy Checkout Tool",
                        "slug": "legacy-checkout-tool",
                        "status": "live",
                        "vercel_url": "https://legacy-checkout-tool.vercel.app",
                        "lemonsqueezy_checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/legacy-checkout-tool-001",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["checkout_gap_count"], 0)
        self.assertEqual(summary["products"][0]["c"], "https://profitbridge.lemonsqueezy.com/checkout/buy/legacy-checkout-tool-001")

    def test_product_catalog_reclassifies_stale_live_records(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "SSL Cert Checker",
                        "slug": "ssl-cert-checker",
                        "status": "live",
                        "vercel_url": "https://ssl-cert-checker.vercel.app",
                    }
                ]
            }
        }
        product_catalog = {
            "ssl-cert-checker": {
                "name": "SSL Cert Checker",
                "slug": "ssl-cert-checker",
                "status": "spec_ready",
                "vercel_url": None,
            }
        }

        summary = build_summary(state, product_catalog=product_catalog)

        self.assertEqual(summary["live_count"], 0)
        self.assertEqual(summary["spec_ready_count"], 1)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 1)
        self.assertEqual(summary["gaps"]["missing_url"], ["ssl-cert-checker"])
        self.assertEqual(summary["gaps"]["unhealthy_live"], [])

    def test_product_catalog_keeps_canonical_state_url_for_live_products(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Table to CSV",
                        "slug": "table-to-csv",
                        "status": "live",
                        "vercel_url": "https://table-to-csv.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }
        product_catalog = {
            "table-to-csv": {
                "name": "Table to CSV",
                "slug": "table-to-csv",
                "status": "live",
                "vercel_url": None,
            }
        }

        summary = build_summary(state, product_catalog=product_catalog)

        self.assertEqual(summary["live_count"], 1)
        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 0)
        self.assertEqual(summary["products"][0]["v"], "https://table-to-csv.vercel.app")

    def test_missing_product_catalog_still_promotes_canonical_health_url(self) -> None:
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
                ]
            }
        }

        summary = build_summary(state, product_catalog={})

        self.assertEqual(summary["live_count"], 1)
        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["products"][0]["v"], "https://orphan-tool.vercel.app")
        self.assertEqual(summary["canonical_url_drift"], 0)
        self.assertEqual(summary["canonical_url_drift_products"], [])
        self.assertEqual(summary["gaps"]["canonical_url_drift"], [])

    def test_healthy_alias_record_without_canonical_probe_counts_drift(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Drift Tool",
                        "slug": "drift-tool",
                        "status": "live",
                        "vercel_url": "https://drift-tool-rose.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://drift-tool-rose.vercel.app",
                    }
                ]
            }
        }

        summary = build_summary(state, product_catalog={})

        self.assertEqual(summary["live_count"], 1)
        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["products"][0]["v"], "https://drift-tool-rose.vercel.app")
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["drift-tool"])
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "drift-tool",
                    "url": "https://drift-tool-rose.vercel.app",
                    "ideal_url": "https://drift-tool.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://drift-tool-rose.vercel.app",
                    "canonical_url": "https://drift-tool.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )

    def test_live_state_keeps_fallback_aliases_separate_from_unhealthy_count(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Fallback A",
                        "slug": "fallback-a",
                        "status": "live",
                        "vercel_url": "https://fallback-a.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://fallback-a-preview.vercel.app",
                        "effective_health_url": "https://fallback-a-preview.vercel.app",
                        "canonical_health_code": 404,
                        "canonical_health_status": "not_found",
                        "canonical_health_url": "https://fallback-a.vercel.app",
                        "canonical_probe_url": "https://fallback-a.vercel.app",
                    },
                    {
                        "name": "Fallback B",
                        "slug": "fallback-b",
                        "status": "live",
                        "vercel_url": "https://fallback-b.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://fallback-b-preview.vercel.app",
                        "effective_health_url": "https://fallback-b-preview.vercel.app",
                        "canonical_health_code": 404,
                        "canonical_health_status": "not_found",
                        "canonical_health_url": "https://fallback-b.vercel.app",
                        "canonical_probe_url": "https://fallback-b.vercel.app",
                    },
                    {
                        "name": "Fallback C",
                        "slug": "fallback-c",
                        "status": "live",
                        "vercel_url": "https://fallback-c.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://fallback-c-preview.vercel.app",
                        "effective_health_url": "https://fallback-c-preview.vercel.app",
                        "canonical_health_code": 402,
                        "canonical_health_status": "deployment_disabled",
                        "canonical_health_url": "https://fallback-c.vercel.app",
                        "canonical_probe_url": "https://fallback-c.vercel.app",
                    },
                    {
                        "name": "Fallback D",
                        "slug": "fallback-d",
                        "status": "live",
                        "vercel_url": "https://fallback-d.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://fallback-d-preview.vercel.app",
                        "effective_health_url": "https://fallback-d-preview.vercel.app",
                        "canonical_health_code": 404,
                        "canonical_health_status": "not_found",
                        "canonical_health_url": "https://fallback-d.vercel.app",
                        "canonical_probe_url": "https://fallback-d.vercel.app",
                    },
                    {
                        "name": "Broken A",
                        "slug": "broken-a",
                        "status": "live",
                        "vercel_url": "https://broken-a.vercel.app",
                        "health_status": "error_500",
                        "last_health_code": 500,
                        "last_health_url": "https://broken-a.vercel.app",
                    },
                    {
                        "name": "Broken B",
                        "slug": "broken-b",
                        "status": "live",
                        "vercel_url": "https://broken-b.vercel.app",
                        "health_status": "unauthorized",
                        "last_health_code": 401,
                        "last_health_url": "https://broken-b.vercel.app",
                    },
                    {
                        "name": "Broken C",
                        "slug": "broken-c",
                        "status": "live",
                        "vercel_url": "https://broken-c.vercel.app",
                        "health_status": "error_451",
                        "last_health_code": 451,
                        "last_health_url": "https://broken-c.vercel.app",
                    },
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 4)
        self.assertEqual(summary["canonical_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 4)
        self.assertEqual(summary["unhealthy_count"], 3)
        self.assertEqual(summary["canonical_url_drift"], 4)
        self.assertEqual(summary["needs_fix_count"], 7)
        self.assertEqual(summary["next_action"], "3 canlı ürünü düzelt; 4 fallback alias'ı görünür tut")
        self.assertEqual(summary["canonical_url_drift_products"], ["fallback-a", "fallback-b", "fallback-c", "fallback-d"])
        self.assertEqual(summary["fallback_healthy_products"], ["fallback-a", "fallback-b", "fallback-c", "fallback-d"])

    def test_pending_health_records_are_reported_separately(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Healthy Tool",
                        "slug": "healthy-tool",
                        "status": "live",
                        "vercel_url": "https://healthy-tool.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    },
                    {
                        "name": "Pending Tool",
                        "slug": "pending-tool",
                        "status": "live",
                        "vercel_url": "https://pending-tool.vercel.app",
                    },
                    {
                        "name": "Broken Tool",
                        "slug": "broken-tool",
                        "status": "live",
                        "vercel_url": "https://broken-tool.vercel.app",
                        "health_status": "timeout",
                        "last_health_code": 0,
                        "last_health_url": "https://broken-tool.vercel.app",
                    },
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["pending_health_count"], 1)
        self.assertEqual(summary["unhealthy_count"], 1)
        self.assertEqual(summary["needs_fix_count"], 2)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 2)
        self.assertEqual(
            summary["gaps"]["pending_health"],
            [
                {
                    "slug": "pending-tool",
                    "url": "https://pending-tool.vercel.app",
                    "code": None,
                    "health_status": "pending",
                }
            ],
        )
        self.assertEqual(summary["gaps"]["unhealthy_live"][0]["slug"], "broken-tool")

    def test_product_catalog_preview_hash_without_state_url_uses_canonical_display(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "UUID Generator Pro",
                        "slug": "uuid-generator-pro",
                        "status": "ready_to_deploy",
                        "vercel_url": None,
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }
        product_catalog = {
            "uuid-generator-pro": {
                "name": "UUID Generator Pro",
                "slug": "uuid-generator-pro",
                "status": "live",
                "vercel_url": "https://uuid-generator-glm6h3i1l-madnessqws-projects.vercel.app",
            }
        }

        summary = build_summary(state, product_catalog=product_catalog)

        self.assertEqual(summary["live_count"], 1)
        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["products"][0]["v"], "https://uuid-generator-pro.vercel.app")
        self.assertEqual(summary["canonical_url_drift"], 0)
        self.assertEqual(summary["canonical_url_drift_products"], [])
        self.assertEqual(summary["gaps"]["canonical_url_drift"], [])

    def test_deploy_readiness_report_is_included_in_summary(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Agent Prompt Engineer",
                        "slug": "agent-prompt-engineer",
                        "status": "spec_ready",
                    }
                ]
            }
        }
        readiness = {
            "count": 1,
            "manifest_gap_count": 1,
            "url_gap_count": 1,
            "state_gap_count": 1,
            "issues": [
                {
                    "slug": "agent-prompt-engineer",
                    "name": "Agent Prompt Engineer",
                    "manifest_problem": "missing",
                    "missing_manifest_fields": ["tagline"],
                    "missing_url_fields": ["vercel_url"],
                    "missing_state_fields": ["payment_provider"],
                }
            ],
        }

        with patch.object(update_summary, "collect_spec_ready_deploy_readiness", return_value=readiness) as readiness_mock:
            summary = build_summary(state)

        readiness_mock.assert_called_once()
        self.assertEqual(summary["deploy_readiness_count"], 1)
        self.assertEqual(summary["deploy_readiness_manifest_gap_count"], 1)
        self.assertEqual(summary["deploy_readiness_url_gap_count"], 1)
        self.assertEqual(summary["deploy_readiness_state_gap_count"], 1)
        self.assertEqual(summary["gaps"]["deploy_readiness"], readiness["issues"])

    def test_live_product_without_explicit_url_uses_slug_canonical_display(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Ideal Only Tool",
                        "slug": "ideal-only-tool",
                        "status": "live",
                        "vercel_url": None,
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["live_count"], 1)
        self.assertEqual(summary["products"][0]["v"], "https://ideal-only-tool.vercel.app")
        self.assertEqual(summary["gaps"]["missing_url"], [])
        self.assertEqual(summary["deploy_missing_or_bad_url"], 0)

    def test_predeploy_product_hides_public_url_even_when_state_keeps_one(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Color Contrast Pro",
                        "slug": "color-contrast-pro",
                        "status": "ready_to_deploy",
                        "vercel_url": "https://color-contrast-pro.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }
        product_catalog = {
            "color-contrast-pro": {
                "name": "Color Contrast Pro",
                "slug": "color-contrast-pro",
                "status": "ready_to_deploy",
                "vercel_url": "https://color-contrast-pro.vercel.app",
            }
        }

        summary = build_summary(state, product_catalog=product_catalog)

        self.assertEqual(summary["products"][0]["st"], "ready_to_deploy")
        self.assertIsNone(summary["products"][0]["v"])

    def test_main_persists_normalized_state_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            state_file = tmp_path / "STATE.json"
            summary_file = tmp_path / "STATE_SUMMARY.json"
            state_file.write_text(
                json.dumps(
                    {
                        "cycle": 999,
                        "mode": "BUILD",
                        "balance": 0,
                        "products": {
                            "active": [
                                {
                                    "name": "Temporary Tool",
                                    "slug": "temporary-tool",
                                    "status": "live",
                                    "vercel_url": "https://temporary-tool.vercel.app",
                                    "v": "https://temporary-tool-preview.vercel.app",
                                    "health_status": "alternate_healthy",
                                    "last_health_code": 200,
                                    "last_health_url": "https://temporary-tool-preview.vercel.app",
                                },
                                {
                                    "name": "Temporary Tool",
                                    "slug": "temporary-tool",
                                    "status": "live",
                                    "vercel_url": "https://temporary-tool.vercel.app",
                                    "v": "https://temporary-tool-preview.vercel.app",
                                    "health_status": "alternate_healthy",
                                    "last_health_code": 200,
                                    "last_health_url": "https://temporary-tool-preview.vercel.app",
                                },
                            ],
                            "spec_ready": [],
                        },
                    }
                ),
                encoding="utf-8",
            )

            with patch.object(update_summary, "STATE_FILE", state_file), patch.object(
                update_summary, "SUMMARY_FILE", summary_file
            ), patch.object(update_summary, "load_product_catalog", return_value={}):
                exit_code = update_summary.main()

            self.assertEqual(exit_code, 0)

            synced_state = json.loads(state_file.read_text(encoding="utf-8"))
            synced_summary = json.loads(summary_file.read_text(encoding="utf-8"))

            self.assertEqual(synced_state["canonical_url_drift"], 1)
            self.assertEqual(synced_state["canonical_url_drift_products"], ["temporary-tool"])
            self.assertEqual(
                synced_state["next_action"],
                "1 canonical URL drift'ini düzelt; fallback alias'ı ezme",
            )
            self.assertEqual(len(synced_state["products"]["active"]), 1)
            self.assertEqual(
                synced_state["products"]["active"][0]["vercel_url"],
                "https://temporary-tool-preview.vercel.app",
            )
            self.assertEqual(
                synced_state["products"]["active"][0]["v"],
                "https://temporary-tool-preview.vercel.app",
            )
            self.assertEqual(synced_summary["canonical_url_drift"], 1)
            self.assertEqual(
                synced_summary["products"][0]["v"],
                "https://temporary-tool-preview.vercel.app",
            )

    def test_live_preview_alias_without_canonical_probe_stays_visible(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "DiffMaster Pro",
                        "slug": "diffmaster",
                        "status": "live",
                        "vercel_url": "https://diffmaster-rose.vercel.app",
                        "ideal_vercel_url": "https://diffmaster.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 1)
        self.assertEqual(summary["unhealthy_count"], 0)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 0)
        self.assertEqual(summary["products"][0]["v"], "https://diffmaster-rose.vercel.app")
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["diffmaster"])
        self.assertEqual(summary["gaps"]["unhealthy_live"], [])
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "diffmaster",
                    "url": "https://diffmaster-rose.vercel.app",
                    "ideal_url": "https://diffmaster.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://diffmaster-rose.vercel.app",
                    "canonical_url": "https://diffmaster.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )

    def test_custom_domain_without_health_still_reports_drift(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Webhook Tester",
                        "slug": "webhook-tester",
                        "status": "live",
                        "vercel_url": "https://webhook-tester.example.com",
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 0)
        self.assertEqual(summary["pending_health_count"], 1)
        self.assertEqual(summary["unhealthy_count"], 0)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["webhook-tester"])
        self.assertEqual(summary["products"][0]["v"], "https://webhook-tester.example.com")
        self.assertEqual(
            summary["gaps"]["pending_health"],
            [
                {
                    "slug": "webhook-tester",
                    "url": "https://webhook-tester.example.com",
                    "code": None,
                    "health_status": "pending",
                }
            ],
        )
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "webhook-tester",
                    "url": "https://webhook-tester.example.com",
                    "ideal_url": "https://webhook-tester.vercel.app",
                    "canonical_url": "https://webhook-tester.vercel.app",
                }
            ],
        )

    def test_unhealthy_live_gap_uses_resolved_public_url_and_failure_status(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Broken Tool",
                        "slug": "broken-tool",
                        "status": "live",
                        "vercel_url": "https://broken-tool-rose.vercel.app",
                        "deployment_url": "https://broken-tool.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 401,
                        "last_health_url": "https://broken-tool.vercel.app",
                    }
                ]
            }
        }

        summary = build_summary(state, product_catalog={"dummy": {"slug": "dummy"}})

        self.assertEqual(summary["healthy_count"], 0)
        self.assertEqual(summary["unhealthy_count"], 1)
        self.assertEqual(summary["products"][0]["v"], "https://broken-tool.vercel.app")
        self.assertEqual(
            summary["gaps"]["unhealthy_live"],
            [
                {
                    "slug": "broken-tool",
                    "url": "https://broken-tool.vercel.app",
                    "code": 401,
                    "health_status": "unauthorized",
                    "canonical_url": "https://broken-tool.vercel.app",
                    "canonical_code": 401,
                    "canonical_status": "unauthorized",
                    "probe_url": "https://broken-tool.vercel.app",
                }
            ],
        )

    def test_live_preview_alias_without_last_health_url_stays_visible(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Webhook Tester",
                        "slug": "webhook-tester",
                        "status": "live",
                        "vercel_url": "https://webhook-tester-beryl.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["unhealthy_count"], 0)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 0)
        self.assertEqual(summary["products"][0]["v"], "https://webhook-tester-beryl.vercel.app")
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["webhook-tester"])
        self.assertEqual(summary["gaps"]["unhealthy_live"], [])
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "webhook-tester",
                    "url": "https://webhook-tester-beryl.vercel.app",
                    "ideal_url": "https://webhook-tester.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://webhook-tester-beryl.vercel.app",
                    "canonical_url": "https://webhook-tester.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )

    def test_compact_preview_alias_without_last_health_url_stays_visible(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Webhook Tester",
                        "slug": "webhook-tester",
                        "status": "live",
                        "vercel_url": "https://webhook-tester.vercel.app",
                        "v": "https://webhook-tester-beryl.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["unhealthy_count"], 0)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 0)
        self.assertEqual(summary["products"][0]["v"], "https://webhook-tester-beryl.vercel.app")
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["webhook-tester"])
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "webhook-tester",
                    "url": "https://webhook-tester-beryl.vercel.app",
                    "ideal_url": "https://webhook-tester.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://webhook-tester-beryl.vercel.app",
                    "canonical_url": "https://webhook-tester.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )

    def test_alternate_healthy_records_actual_fallback_url_as_public_display(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Fallback Tool",
                        "slug": "fallback-tool",
                        "status": "live",
                        "vercel_url": "https://fallback-tool.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://fallback-tool-preview.vercel.app",
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["unhealthy_count"], 0)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 0)
        self.assertEqual(summary["needs_fix_count"], 1)
        self.assertEqual(summary["products"][0]["v"], "https://fallback-tool-preview.vercel.app")
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["fallback-tool"])
        self.assertEqual(summary["fallback_healthy_products"], ["fallback-tool"])
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "fallback-tool",
                    "url": "https://fallback-tool-preview.vercel.app",
                    "ideal_url": "https://fallback-tool.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://fallback-tool-preview.vercel.app",
                    "canonical_url": "https://fallback-tool.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )
        self.assertEqual(
            summary["gaps"]["fallback_healthy"],
            [
                {
                    "slug": "fallback-tool",
                    "url": "https://fallback-tool-preview.vercel.app",
                    "ideal_url": "https://fallback-tool.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://fallback-tool-preview.vercel.app",
                    "canonical_url": "https://fallback-tool.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )
        self.assertEqual(summary["gaps"]["unhealthy_live"], [])

    def test_healthy_canonical_url_with_preview_alias_and_missing_canonical_probe_keeps_fallback_visible(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Fallback Tool",
                        "slug": "fallback-tool",
                        "status": "live",
                        "vercel_url": "https://fallback-tool.vercel.app",
                        "deployment_url": "https://fallback-tool-preview.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://fallback-tool.vercel.app",
                        "effective_health_url": "https://fallback-tool.vercel.app",
                        "canonical_health_url": "https://fallback-tool.vercel.app",
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["products"][0]["v"], "https://fallback-tool-preview.vercel.app")
        self.assertEqual(summary["gaps"]["canonical_url_drift"][0]["health_status"], "alternate_healthy")
        self.assertEqual(summary["gaps"]["canonical_url_drift"][0]["canonical_status"], "pending")

    def test_canonical_drift_entry_marks_stale_healthy_alias_as_fallback(self) -> None:
        product = {
            "name": "Stale Healthy Tool",
            "slug": "stale-healthy-tool",
            "status": "live",
            "vercel_url": "https://stale-healthy-tool.vercel.app",
            "health_status": "healthy",
            "last_health_code": 200,
            "last_health_url": "https://stale-healthy-tool-rose.vercel.app",
        }

        entry = canonical_url_drift_entry(product)

        self.assertEqual(entry["url"], "https://stale-healthy-tool-rose.vercel.app")
        self.assertEqual(entry["ideal_url"], "https://stale-healthy-tool.vercel.app")
        self.assertEqual(entry["health_status"], "alternate_healthy")
        self.assertEqual(entry["health_code"], 200)

    def test_stale_effective_canonical_url_still_counts_as_fallback_drift(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Shadowed Fallback Tool",
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
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["shadowed-fallback-tool"])
        self.assertEqual(summary["products"][0]["v"], "https://shadowed-fallback-tool-preview.vercel.app")
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "shadowed-fallback-tool",
                    "url": "https://shadowed-fallback-tool-preview.vercel.app",
                    "ideal_url": "https://shadowed-fallback-tool.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://shadowed-fallback-tool-preview.vercel.app",
                    "canonical_url": "https://shadowed-fallback-tool.vercel.app",
                    "canonical_code": 404,
                    "canonical_status": "not_found",
                }
            ],
        )

    def test_deployment_alias_without_explicit_health_url_keeps_fallback_public_display(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Deployment Alias Tool",
                        "slug": "deployment-alias-tool",
                        "status": "live",
                        "vercel_url": "https://deployment-alias-tool.vercel.app",
                        "deployment_url": "https://deployment-alias-tool-rose.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["deployment-alias-tool"])
        self.assertEqual(summary["products"][0]["v"], "https://deployment-alias-tool-rose.vercel.app")
        self.assertEqual(summary["fallback_healthy_products"], ["deployment-alias-tool"])
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "deployment-alias-tool",
                    "url": "https://deployment-alias-tool-rose.vercel.app",
                    "ideal_url": "https://deployment-alias-tool.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://deployment-alias-tool-rose.vercel.app",
                    "canonical_url": "https://deployment-alias-tool.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )

    def test_deployment_alias_with_health_timestamp_counts_as_fallback_drift(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Deployment Timestamp Tool",
                        "slug": "deployment-timestamp-tool",
                        "status": "live",
                        "vercel_url": "https://deployment-timestamp-tool.vercel.app",
                        "deployment_url": "https://deployment-timestamp-tool-rose.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                        "last_health_check": "2026-04-23T10:00:00Z",
                        "health_checked_at": "2026-04-23T10:00:00Z",
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["deployment-timestamp-tool"])
        self.assertEqual(summary["products"][0]["v"], "https://deployment-timestamp-tool-rose.vercel.app")
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "deployment-timestamp-tool",
                    "url": "https://deployment-timestamp-tool-rose.vercel.app",
                    "ideal_url": "https://deployment-timestamp-tool.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://deployment-timestamp-tool-rose.vercel.app",
                    "canonical_url": "https://deployment-timestamp-tool.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )

    def test_deployment_alias_without_health_timestamp_counts_as_fallback_drift(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Deployment No Timestamp Tool",
                        "slug": "deployment-no-timestamp-tool",
                        "status": "live",
                        "vercel_url": "https://deployment-no-timestamp-tool.vercel.app",
                        "deployment_url": "https://deployment-no-timestamp-tool-rose.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["deployment-no-timestamp-tool"])
        self.assertEqual(summary["products"][0]["v"], "https://deployment-no-timestamp-tool-rose.vercel.app")
        self.assertEqual(summary["fallback_healthy_products"], ["deployment-no-timestamp-tool"])
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "deployment-no-timestamp-tool",
                    "url": "https://deployment-no-timestamp-tool-rose.vercel.app",
                    "ideal_url": "https://deployment-no-timestamp-tool.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://deployment-no-timestamp-tool-rose.vercel.app",
                    "canonical_url": "https://deployment-no-timestamp-tool.vercel.app",
                    "canonical_status": "pending",
                }
            ],
        )

    def test_stale_alternate_label_without_drift_does_not_count_as_fallback(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Stale Label Tool",
                        "slug": "stale-label-tool",
                        "status": "live",
                        "vercel_url": "https://stale-label-tool.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                    }
                ]
            }
        }

        with patch.object(update_summary, "canonical_url_drift_entry", return_value=None):
            summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_products"], [])

    def test_newer_canonical_success_drops_stale_drift_record(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Redirect Tool",
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
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_healthy_count"], 1)
        self.assertEqual(summary["fallback_healthy_count"], 0)
        self.assertEqual(summary["canonical_url_drift"], 0)
        self.assertEqual(summary["canonical_url_drift_products"], [])
        self.assertEqual(summary["gaps"]["canonical_url_drift"], [])

    def test_redirected_canonical_success_still_counts_as_drift(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "HTML Entity Encoder/Decoder Pro",
                        "slug": "html-entity-encoder",
                        "status": "live",
                        "vercel_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                        "health_status": "alternate_healthy",
                        "last_health_code": 200,
                        "health_probe_url": "https://html-entity-encoder.vercel.app",
                        "last_health_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                        "effective_health_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                        "canonical_health_status": "redirected_preview_alias",
                        "canonical_health_code": 200,
                        "canonical_health_url": "https://html-entity-encoder.vercel.app",
                        "canonical_health_checked_at": "2026-04-23T10:05:00Z",
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["canonical_healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["html-entity-encoder"])
        self.assertEqual(summary["products"][0]["v"], "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app")
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "html-entity-encoder",
                    "url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                    "ideal_url": "https://html-entity-encoder.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://html-entity-encoder.vercel.app",
                    "effective_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                    "canonical_url": "https://html-entity-encoder.vercel.app",
                    "canonical_code": 200,
                    "canonical_status": "redirected_preview_alias",
                }
            ],
        )

    def test_stale_failure_with_successful_fallback_records_actual_fallback_url(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Fallback Tool",
                        "slug": "fallback-stale-error",
                        "status": "live",
                        "vercel_url": "https://fallback-stale-error.vercel.app",
                        "checkout_url": "https://checkout.example/fallback-stale-error",
                        "health_status": "error_404",
                        "last_health_code": 200,
                        "last_health_url": "https://fallback-stale-error-preview.vercel.app",
                        "canonical_health_code": 404,
                        "canonical_health_status": "not_found",
                    }
                ]
            }
        }

        summary = build_summary(state, product_catalog={})

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["unhealthy_count"], 0)
        self.assertEqual(summary["checkout_gap_count"], 0)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 0)
        self.assertEqual(summary["products"][0]["v"], "https://fallback-stale-error-preview.vercel.app")
        self.assertEqual(summary["canonical_url_drift"], 1)
        self.assertEqual(summary["canonical_url_drift_products"], ["fallback-stale-error"])
        self.assertEqual(
            summary["gaps"]["canonical_url_drift"],
            [
                {
                    "slug": "fallback-stale-error",
                    "url": "https://fallback-stale-error-preview.vercel.app",
                    "ideal_url": "https://fallback-stale-error.vercel.app",
                    "health_status": "alternate_healthy",
                    "health_code": 200,
                    "probe_url": "https://fallback-stale-error-preview.vercel.app",
                    "canonical_url": "https://fallback-stale-error.vercel.app",
                    "canonical_code": 404,
                    "canonical_status": "not_found",
                }
            ],
        )
        self.assertEqual(summary["gaps"]["unhealthy_live"], [])


    def test_newer_canonical_failure_does_not_count_stale_fallback_as_healthy(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Stale Fallback Tool",
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
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 0)
        self.assertEqual(summary["fallback_healthy_count"], 0)
        self.assertEqual(summary["unhealthy_count"], 1)
        self.assertEqual(summary["canonical_url_drift"], 0)
        self.assertEqual(summary["fallback_healthy_products"], [])
        self.assertEqual(summary["gaps"]["unhealthy_live"][0]["slug"], "stale-fallback-tool")
        self.assertEqual(summary["gaps"]["unhealthy_live"][0]["code"], 404)
        self.assertEqual(summary["products"][0]["v"], "https://stale-fallback-tool.vercel.app")

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

    def test_persist_summary_writes_json_file(self) -> None:
        summary = {"cycle": 1, "healthy_count": 2}

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "STATE_SUMMARY.json"
            persist_summary(summary, summary_file=path)

            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), summary)


if __name__ == "__main__":
    unittest.main()
