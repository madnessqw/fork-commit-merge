import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts import update_summary
from scripts.update_summary import build_summary, is_placeholder_product, normalize_product, persist_summary


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
                                }
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

            self.assertEqual(synced_state["canonical_url_drift"], 0)
            self.assertEqual(synced_state["canonical_url_drift_products"], [])
            self.assertEqual(synced_state["products"]["active"][0]["vercel_url"], "https://temporary-tool.vercel.app")
            self.assertEqual(synced_state["products"]["active"][0]["v"], "https://temporary-tool.vercel.app")
            self.assertEqual(synced_summary["canonical_url_drift"], 0)
            self.assertEqual(synced_summary["products"][0]["v"], "https://temporary-tool.vercel.app")

    def test_canonical_url_drift_is_reported_from_ideal_url(self) -> None:
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
        self.assertEqual(summary["unhealthy_count"], 0)
        self.assertEqual(summary["deploy_missing_or_bad_url"], 0)
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
                }
            ],
        )

    def test_last_successful_health_url_can_clear_stale_alias_drift(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "Stale Tool",
                        "slug": "stale-tool",
                        "status": "live",
                        "vercel_url": "https://stale-tool-rose.vercel.app",
                        "health_status": "healthy",
                        "last_health_code": 200,
                        "last_health_url": "https://stale-tool.vercel.app",
                    }
                ]
            }
        }

        summary = build_summary(state)

        self.assertEqual(summary["healthy_count"], 1)
        self.assertEqual(summary["unhealthy_count"], 0)
        self.assertEqual(summary["canonical_url_drift"], 0)
        self.assertEqual(summary["canonical_url_drift_products"], [])
        self.assertEqual(summary["products"][0]["v"], "https://stale-tool.vercel.app")
        self.assertEqual(summary["gaps"]["canonical_url_drift"], [])

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
                    "probe_url": "https://broken-tool.vercel.app",
                }
            ],
        )

    def test_canonical_url_drift_is_reported_from_slug_when_ideal_missing(self) -> None:
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
                }
            ],
        )

    def test_alternate_healthy_counts_as_healthy_when_public_url_is_canonical(self) -> None:
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
        self.assertEqual(summary["gaps"]["unhealthy_live"], [])

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
