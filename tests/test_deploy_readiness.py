import json
import tempfile
import unittest
from pathlib import Path

from scripts.deploy_readiness import collect_spec_ready_deploy_readiness


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
                "lemonsqueezy_product_id",
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


if __name__ == "__main__":
    unittest.main()
