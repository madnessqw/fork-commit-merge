import json
import tempfile
import unittest
from pathlib import Path

from scripts.deploy_readiness import (
    auto_fix_suggestions,
    batch_suggest_vercel_urls,
    collect_spec_ready_deploy_readiness,
    ready_for_payment_audit,
    readiness_summary,
    suggest_vercel_url,
)


class DeployReadinessTests(unittest.TestCase):
    def test_missing_manifest_reports_all_required_fields(self) -> None:
        state = {
            "products": {
                "spec_ready": [
                    {
                        "name": "SQL Query Builder Pro",
                        "slug": "sql-query-builder-pro",
                        "status": "spec_ready",
                    }
                ]
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = collect_spec_ready_deploy_readiness(state, root=root)

        self.assertEqual(report["count"], 1)
        self.assertEqual(report["manifest_gap_count"], 1)
        self.assertEqual(report["url_gap_count"], 1)
        self.assertEqual(report["state_gap_count"], 1)

        issue = report["issues"][0]
        self.assertEqual(issue["slug"], "sql-query-builder-pro")
        self.assertEqual(issue["manifest_problem"], "missing")
        self.assertIn("name", issue["missing_manifest_fields"])
        self.assertIn("status", issue["missing_manifest_fields"])
        self.assertIn("vercel_url", issue["missing_url_fields"])
        self.assertIn("checkout_url", issue["missing_url_fields"])
        self.assertIn("payment_provider", issue["missing_state_fields"])
        self.assertIn("created_cycle", issue["missing_state_fields"])

    def test_existing_manifest_reports_url_and_state_gaps(self) -> None:
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

        manifest = {
            "name": "Agent Prompt Engineer",
            "slug": "agent-prompt-engineer",
            "tagline": "Optimize prompts for AI agents",
            "description": "Engineer and optimize prompts for AI agents.",
            "price": "19",
            "features": ["Prompt templates"],
            "tech_stack": "Vercel + Node.js",
            "status": "spec_ready",
            "category": "ai_tools",
            "spec_version": "1.0",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            product_path = root / "products" / "agent-prompt-engineer" / "product.json"
            product_path.parent.mkdir(parents=True, exist_ok=True)
            product_path.write_text(json.dumps(manifest), encoding="utf-8")

            report = collect_spec_ready_deploy_readiness(state, root=root)

        self.assertEqual(report["count"], 1)
        self.assertEqual(report["manifest_gap_count"], 0)
        self.assertEqual(report["url_gap_count"], 1)
        self.assertEqual(report["state_gap_count"], 1)

        issue = report["issues"][0]
        self.assertEqual(issue["slug"], "agent-prompt-engineer")
        self.assertIsNone(issue["manifest_problem"])
        self.assertEqual(issue["missing_manifest_fields"], [])
        self.assertCountEqual(
            issue["missing_url_fields"],
            [
                "vercel_url",
                "deployment_url",
                "github_url",
                "webhook_url",
                "checkout_url",
            ],
        )
        self.assertCountEqual(
            issue["missing_state_fields"],
            [
                "payment_provider",
                "created_cycle",
                "deployed_cycle",
            ],
        )

    def test_ready_to_deploy_products_are_included(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "name": "HTTP Load Tester Pro",
                        "slug": "http-load-tester-pro",
                        "status": "ready_to_deploy",
                    }
                ]
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = collect_spec_ready_deploy_readiness(state, root=root)

        self.assertEqual(report["count"], 1)
        issue = report["issues"][0]
        self.assertEqual(issue["slug"], "http-load-tester-pro")
        self.assertEqual(issue["manifest_problem"], "missing")

    def test_other_statuses_excluded(self) -> None:
        state = {
            "products": {
                "active": [
                    {"name": "Live Product", "slug": "live-prod", "status": "live"},
                    {
                        "name": "Building Product",
                        "slug": "building-prod",
                        "status": "building",
                    },
                    {
                        "name": "Spec Product",
                        "slug": "spec-prod",
                        "status": "spec_ready",
                    },
                    {
                        "name": "Deploy Product",
                        "slug": "deploy-prod",
                        "status": "ready_to_deploy",
                    },
                ]
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = collect_spec_ready_deploy_readiness(state, root=root)

        slugs = [i["slug"] for i in report["issues"]]
        self.assertIn("spec-prod", slugs)
        self.assertIn("deploy-prod", slugs)
        self.assertNotIn("live-prod", slugs)
        self.assertNotIn("building-prod", slugs)


class ReadinessSummaryTests(unittest.TestCase):
    """Tests for the readiness_summary shortcut function."""

    def _write_json(self, path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_summary_merges_state_and_summary(self) -> None:
        state = {
            "products": {
                "spec_ready": [
                    {"slug": "alpha-tool", "status": "spec_ready"},
                    {"slug": "beta-tool", "status": "spec_ready"},
                ]
            }
        }
        summary = {
            "live_count": 80,
            "healthy_count": 78,
            "spec_ready_count": 2,
            "deploy_missing_or_bad_url": 12,
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            state_path = root / "STATE.json"
            summary_path = root / "STATE_SUMMARY.json"
            self._write_json(state_path, state)
            self._write_json(summary_path, summary)

            result = readiness_summary(state_path, summary_path, root=root)

        self.assertEqual(result["live_count"], 80)
        self.assertEqual(result["healthy_count"], 78)
        self.assertAlmostEqual(result["health_pct"], 97.5)
        self.assertEqual(result["total_spec_ready"], 2)
        self.assertEqual(result["deploy_missing_or_bad_url"], 12)
        self.assertEqual(result["issues_count"], 2)
        self.assertEqual(result["url_gap"], 2)
        self.assertEqual(result["state_gap"], 2)

    def test_health_pct_zero_when_no_live(self) -> None:
        state = {"products": {"spec_ready": []}}
        summary = {"live_count": 0, "healthy_count": 0, "spec_ready_count": 0}

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            state_path = root / "STATE.json"
            summary_path = root / "STATE_SUMMARY.json"
            self._write_json(state_path, state)
            self._write_json(summary_path, summary)

            result = readiness_summary(state_path, summary_path, root=root)

        self.assertEqual(result["health_pct"], 0.0)
        self.assertEqual(result["issues_count"], 0)
        self.assertEqual(result["top_url_gap_slugs"], [])

    def test_top_url_gap_slugs_limited_to_five(self) -> None:
        spec_ready = [
            {"slug": f"tool-{i}", "status": "spec_ready"} for i in range(8)
        ]
        state = {"products": {"spec_ready": spec_ready}}
        summary = {"live_count": 10, "healthy_count": 10, "spec_ready_count": 8}

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            state_path = root / "STATE.json"
            summary_path = root / "STATE_SUMMARY.json"
            self._write_json(state_path, state)
            self._write_json(summary_path, summary)

            result = readiness_summary(state_path, summary_path, root=root)

        self.assertLessEqual(len(result["top_url_gap_slugs"]), 5)
        self.assertEqual(result["issues_count"], 8)

    def test_missing_files_returns_zeros(self) -> None:
        """When STATE/STATE_SUMMARY don't exist, returns safe defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            state_path = root / "STATE.json"
            summary_path = root / "STATE_SUMMARY.json"

            result = readiness_summary(state_path, summary_path, root=root)

        self.assertEqual(result["live_count"], 0)
        self.assertEqual(result["healthy_count"], 0)
        self.assertEqual(result["health_pct"], 0.0)
        self.assertEqual(result["issues_count"], 0)


class SuggestVercelUrlTests(unittest.TestCase):
    """Tests for suggest_vercel_url and batch_suggest_vercel_urls."""

    def test_basic_slug(self) -> None:
        self.assertEqual(
            suggest_vercel_url("my-cool-tool"), "https://my-cool-tool.vercel.app"
        )

    def test_slug_whitespace_stripped(self) -> None:
        self.assertEqual(
            suggest_vercel_url("  fancy-tool  "), "https://fancy-tool.vercel.app"
        )

    def test_slug_lowercased(self) -> None:
        self.assertEqual(
            suggest_vercel_url("My-Cool-Tool"), "https://my-cool-tool.vercel.app"
        )

    def test_batch_returns_mapping(self) -> None:
        result = batch_suggest_vercel_urls(["tool-a", "tool-b"])
        self.assertEqual(
            result,
            {
                "tool-a": "https://tool-a.vercel.app",
                "tool-b": "https://tool-b.vercel.app",
            },
        )

    def test_batch_empty_list(self) -> None:
        self.assertEqual(batch_suggest_vercel_urls([]), {})


class AutoFixSuggestionsTests(unittest.TestCase):
    """Tests for auto_fix_suggestions."""

    def test_suggests_vercel_url_for_url_gaps(self) -> None:
        state = {
            "products": {
                "spec_ready": [
                    {"slug": "cool-tool", "status": "spec_ready"},
                ]
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            result = auto_fix_suggestions(state, root=root)

        self.assertEqual(len(result), 1)
        fix = result[0]
        self.assertEqual(fix["slug"], "cool-tool")
        self.assertEqual(fix["suggested_vercel_url"], "https://cool-tool.vercel.app")
        self.assertIn("vercel_url", fix["auto_fillable"])
        self.assertEqual(fix["auto_fillable"]["vercel_url"], "https://cool-tool.vercel.app")

    def test_auto_fills_from_manifest(self) -> None:
        state = {
            "products": {
                "spec_ready": [
                    {"slug": "paid-tool", "status": "spec_ready"},
                ]
            }
        }
        manifest = {
            "name": "Paid Tool",
            "slug": "paid-tool",
            "tagline": "t",
            "description": "d",
            "price": "9",
            "features": [],
            "tech_stack": "Vercel",
            "category": "tools",
            "status": "spec_ready",
            "spec_version": "1.0",
            "github_url": "https://github.com/example/paid-tool",
            "checkout_url": "https://buy.polar.sh/test",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            product_path = root / "products" / "paid-tool" / "product.json"
            product_path.parent.mkdir(parents=True, exist_ok=True)
            product_path.write_text(json.dumps(manifest), encoding="utf-8")

            result = auto_fix_suggestions(state, root=root)

        self.assertEqual(len(result), 1)
        fix = result[0]
        self.assertTrue(fix["manifest_ok"])
        self.assertIn("checkout_url", fix["auto_fillable"])
        self.assertEqual(fix["auto_fillable"]["checkout_url"], "https://buy.polar.sh/test")

    def test_skips_products_with_no_gaps(self) -> None:
        state = {
            "products": {
                "active": [
                    {
                        "slug": "complete-tool",
                        "status": "spec_ready",
                        "payment_provider": "polar",
                        "created_cycle": 100,
                        "deployed_cycle": 101,
                        "vercel_url": "https://complete-tool.vercel.app",
                        "deployment_url": "https://complete-tool.vercel.app",
                        "github_url": "https://github.com/test",
                        "webhook_url": "https://hook.test",
                        "checkout_url": "https://buy.polar.sh/test",
                    },
                ]
            }
        }
        manifest = {
            "name": "Complete Tool",
            "slug": "complete-tool",
            "tagline": "t",
            "description": "d",
            "price": "9",
            "features": [],
            "tech_stack": "Vercel",
            "category": "tools",
            "status": "spec_ready",
            "spec_version": "1.0",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            product_path = root / "products" / "complete-tool" / "product.json"
            product_path.parent.mkdir(parents=True, exist_ok=True)
            product_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = auto_fix_suggestions(state, root=root)

        self.assertEqual(len(result), 0)

    def test_manifest_ok_false_when_manifest_problem(self) -> None:
        state = {
            "products": {
                "spec_ready": [
                    {"slug": "broken-tool", "status": "spec_ready"},
                ]
            }
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            result = auto_fix_suggestions(state, root=root)

        self.assertEqual(len(result), 1)
        self.assertFalse(result[0]["manifest_ok"])


class ReadyForPaymentAuditTests(unittest.TestCase):
    def _write_state(self, tmpdir: str, products: list[dict]) -> Path:
        state_path = Path(tmpdir) / "STATE.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state = {"products": {"active": products}}
        state_path.write_text(json.dumps(state), encoding="utf-8")
        return state_path

    def test_no_ready_for_payment(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {"slug": "live-prod", "status": "live", "vercel_url": "https://x.vercel.app"},
            ])
            result = ready_for_payment_audit(sp)
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["live_ready"], [])
        self.assertEqual(result["blocked"], [])

    def test_live_ready_product(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {
                    "slug": "ready-prod",
                    "status": "ready_for_payment",
                    "vercel_url": "https://ready-prod.vercel.app",
                    "checkout_url": "https://buy.polar.sh/test",
                    "last_health_code": 200,
                },
            ])
            result = ready_for_payment_audit(sp)
        self.assertEqual(result["total"], 1)
        self.assertEqual(len(result["live_ready"]), 1)
        self.assertEqual(result["live_ready"][0]["slug"], "ready-prod")
        self.assertEqual(result["live_ready"][0]["blockers"], [])
        self.assertEqual(result["blocked"], [])

    def test_blocked_missing_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {
                    "slug": "no-checkout",
                    "status": "ready_for_payment",
                    "vercel_url": "https://no-checkout.vercel.app",
                    "last_health_code": 200,
                },
            ])
            result = ready_for_payment_audit(sp)
        self.assertEqual(result["total"], 1)
        self.assertEqual(len(result["blocked"]), 1)
        self.assertIn("missing_checkout_url", result["blocked"][0]["blockers"])
        self.assertEqual(result["blocker_counts"]["missing_checkout_url"], 1)

    def test_blocked_unhealthy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {
                    "slug": "sick-prod",
                    "status": "ready_for_payment",
                    "vercel_url": "https://sick-prod.vercel.app",
                    "checkout_url": "https://buy.polar.sh/test",
                    "last_health_code": 500,
                },
            ])
            result = ready_for_payment_audit(sp)
        self.assertEqual(len(result["blocked"]), 1)
        self.assertIn("unhealthy", result["blocked"][0]["blockers"])

    def test_blocked_missing_vercel_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {
                    "slug": "no-deploy",
                    "status": "ready_for_payment",
                    "checkout_url": "https://buy.polar.sh/test",
                    "last_health_code": 200,
                },
            ])
            result = ready_for_payment_audit(sp)
        self.assertEqual(len(result["blocked"]), 1)
        self.assertIn("missing_vercel_url", result["blocked"][0]["blockers"])

    def test_blocked_missing_health_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {
                    "slug": "no-hc",
                    "status": "ready_for_payment",
                    "vercel_url": "https://no-hc.vercel.app",
                    "checkout_url": "https://buy.polar.sh/test",
                },
            ])
            result = ready_for_payment_audit(sp)
        self.assertIn("missing_health_check", result["blocked"][0]["blockers"])

    def test_multiple_blockers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {
                    "slug": "bad-prod",
                    "status": "ready_for_payment",
                    "last_health_code": 500,
                },
            ])
            result = ready_for_payment_audit(sp)
        blocked = result["blocked"][0]
        self.assertIn("missing_checkout_url", blocked["blockers"])
        self.assertIn("missing_vercel_url", blocked["blockers"])
        self.assertIn("unhealthy", blocked["blockers"])

    def test_mixed_products(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {
                    "slug": "good",
                    "status": "ready_for_payment",
                    "vercel_url": "https://good.vercel.app",
                    "checkout_url": "https://buy.polar.sh/test",
                    "last_health_code": 200,
                },
                {
                    "slug": "bad",
                    "status": "ready_for_payment",
                    "last_health_code": 500,
                },
                {
                    "slug": "live-prod",
                    "status": "live",
                    "vercel_url": "https://live.vercel.app",
                },
            ])
            result = ready_for_payment_audit(sp)
        self.assertEqual(result["total"], 2)
        self.assertEqual(len(result["live_ready"]), 1)
        self.assertEqual(len(result["blocked"]), 1)

    def test_missing_file_returns_empty(self) -> None:
        result = ready_for_payment_audit(Path("/nonexistent/STATE.json"))
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["live_ready"], [])
        self.assertEqual(result["blocked"], [])

    def test_deduplication(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sp = self._write_state(tmpdir, [
                {
                    "slug": "dup-prod",
                    "status": "ready_for_payment",
                    "vercel_url": "https://dup.vercel.app",
                    "checkout_url": "https://buy.polar.sh/test",
                    "last_health_code": 200,
                },
                {
                    "slug": "dup-prod",
                    "status": "ready_for_payment",
                    "vercel_url": "https://dup.vercel.app",
                    "checkout_url": "https://buy.polar.sh/test",
                    "last_health_code": 200,
                },
            ])
            result = ready_for_payment_audit(sp)
        self.assertEqual(result["total"], 1)

    def test_shorthand_fields_recognized(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "STATE.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state = {"products": {"active": [
                {
                    "s": "shorthand-prod",
                    "st": "ready_for_payment",
                    "v": "https://shorthand-prod.vercel.app",
                    "c": "https://buy.polar.sh/test",
                    "last_health_code": 200,
                },
            ]}}
            state_path.write_text(json.dumps(state), encoding="utf-8")
            result = ready_for_payment_audit(state_path)
        self.assertEqual(result["total"], 1)
        self.assertEqual(len(result["live_ready"]), 1)


if __name__ == "__main__":
    unittest.main()
