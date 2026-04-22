import unittest
from datetime import datetime, timezone

from scripts.refresh_codex_context import determine_focus, render_codex_task


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

    def test_focus_uses_checkout_field_issue_when_live_portfolio_is_healthy(self) -> None:
        summary = {
            "live_count": 113,
            "healthy_count": 113,
            "pending_health_count": 0,
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

    def test_rendered_codex_task_mentions_generated_guardrails(self) -> None:
        summary = {
            "cycle": 1063,
            "live_count": 113,
            "healthy_count": 113,
            "pending_health_count": 0,
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

        rendered = render_codex_task(summary, focus, datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc))

        self.assertIn("Generated 2026-04-22 12:00 UTC", rendered)
        self.assertIn("Canonical drift: 0", rendered)
        self.assertIn("Manual Vercel/LemonSqueezy", rendered)
        self.assertIn("analysis/codex_result.md", rendered)
        self.assertIn("Health pending: 0", rendered)


if __name__ == "__main__":
    unittest.main()
