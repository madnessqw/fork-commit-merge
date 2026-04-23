import json
import os
import unittest
from pathlib import Path
import tempfile
from unittest.mock import Mock, patch

from scripts import health_check
from scripts.health_check import apply_health_result, check_product_health, is_synced_health_result


class HealthCheckTests(unittest.TestCase):
    @patch("scripts.health_check.subprocess.run")
    def test_primary_url_success_is_reported_as_healthy(self, run_mock) -> None:
        run_mock.return_value = Mock(stdout="200")

        result = check_product_health(
            {
                "name": "Primary Tool",
                "slug": "primary-tool",
                "status": "live",
                "vercel_url": "https://primary-tool.vercel.app",
            }
        )

        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["url"], "https://primary-tool.vercel.app")
        self.assertEqual(run_mock.call_count, 1)

    @patch("scripts.health_check.subprocess.run")
    def test_health_probe_uses_ipv4_and_follows_redirects(self, run_mock) -> None:
        run_mock.return_value = Mock(stdout="200")

        check_product_health(
            {
                "name": "Redirect Tool",
                "slug": "redirect-tool",
                "status": "live",
                "vercel_url": "https://redirect-tool.vercel.app",
            }
        )

        command = run_mock.call_args[0][0]
        self.assertIn("-4", command)
        self.assertIn("-L", command)
        self.assertIn("-sS", command)
        self.assertTrue(any("%{url_effective}" in part for part in command))

    @patch("scripts.health_check.subprocess.run")
    def test_health_probe_captures_effective_url_from_redirects(self, run_mock) -> None:
        run_mock.return_value = Mock(stdout="200 https://redirect-tool.vercel.app")

        result = check_product_health(
            {
                "name": "Redirect Tool",
                "slug": "redirect-tool",
                "status": "live",
                "vercel_url": "https://redirect-tool-rose.vercel.app",
            }
        )

        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["url"], "https://redirect-tool.vercel.app")
        self.assertEqual(result["effective_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(result["canonical_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(run_mock.call_count, 1)

    @patch("scripts.health_check.subprocess.run")
    def test_canonical_redirect_to_preview_alias_stays_alternate_healthy(self, run_mock) -> None:
        run_mock.return_value = Mock(
            stdout="200 https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app"
        )

        result = check_product_health(
            {
                "name": "HTML Entity Encoder/Decoder Pro",
                "slug": "html-entity-encoder",
                "status": "live",
                "vercel_url": "https://html-entity-encoder.vercel.app",
            }
        )

        self.assertEqual(result["status"], "alternate_healthy")
        self.assertEqual(result["code"], 200)
        self.assertEqual(
            result["url"],
            "https://html-entity-encoder.vercel.app",
        )
        self.assertEqual(
            result["effective_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(result["canonical_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(result["canonical_status"], "redirected_preview_alias")
        self.assertEqual(result["canonical_code"], 200)
        self.assertEqual(run_mock.call_count, 1)

    @patch("scripts.health_check.subprocess.run")
    def test_ideal_url_is_probed_before_stale_alias(self, run_mock) -> None:
        seen_urls = []

        def side_effect(*args, **kwargs):
            seen_urls.append(args[0][-1])
            return Mock(stdout="200")

        run_mock.side_effect = side_effect

        result = check_product_health(
            {
                "name": "Ideal Tool",
                "slug": "ideal-tool",
                "status": "live",
                "vercel_url": "https://ideal-tool-rose.vercel.app",
                "ideal_vercel_url": "https://ideal-tool.vercel.app",
            }
        )

        self.assertEqual(seen_urls[0], "https://ideal-tool.vercel.app")
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["url"], "https://ideal-tool.vercel.app")
        self.assertEqual(run_mock.call_count, 1)

    @patch("scripts.health_check.subprocess.run")
    def test_fallback_url_success_is_marked_as_alternate_healthy(self, run_mock) -> None:
        run_mock.side_effect = [Mock(stdout="500"), Mock(stdout="200")]

        result = check_product_health(
            {
                "name": "Fallback Tool",
                "slug": "fallback-tool",
                "status": "live",
                "vercel_url": "https://fallback-tool.vercel.app",
                "deployment_url": "https://fallback-tool-preview.vercel.app",
            }
        )

        self.assertEqual(result["status"], "alternate_healthy")
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["url"], "https://fallback-tool-preview.vercel.app")
        self.assertEqual(result["canonical_status"], "error_500")
        self.assertEqual(result["canonical_code"], 500)
        self.assertEqual(result["canonical_url"], "https://fallback-tool.vercel.app")
        self.assertEqual(run_mock.call_count, 2)

    @patch("scripts.health_check.subprocess.run")
    def test_previous_effective_health_url_is_retried_as_fallback_candidate(self, run_mock) -> None:
        seen_urls = []

        def side_effect(*args, **kwargs):
            seen_urls.append(args[0][-1])
            if args[0][-1] == "https://fallback-tool-preview.vercel.app":
                return Mock(stdout="200")
            return Mock(stdout="404")

        run_mock.side_effect = side_effect

        result = check_product_health(
            {
                "name": "Fallback Tool",
                "slug": "fallback-tool",
                "status": "live",
                "vercel_url": "https://fallback-tool.vercel.app",
                "effective_health_url": "https://fallback-tool-preview.vercel.app",
                "last_health_url": "https://fallback-tool-preview.vercel.app",
            }
        )

        self.assertEqual(
            seen_urls,
            [
                "https://fallback-tool.vercel.app",
                "https://fallback-tool-preview.vercel.app",
            ],
        )
        self.assertEqual(result["status"], "alternate_healthy")
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["url"], "https://fallback-tool-preview.vercel.app")
        self.assertEqual(result["effective_url"], "https://fallback-tool-preview.vercel.app")
        self.assertEqual(result["canonical_status"], "not_found")
        self.assertEqual(result["canonical_code"], 404)
        self.assertEqual(result["canonical_url"], "https://fallback-tool.vercel.app")
        self.assertEqual(result["canonical_probe_url"], "https://fallback-tool.vercel.app")

    @patch("scripts.health_check.subprocess.run")
    def test_manifest_preview_alias_probe_success_is_marked_as_alternate_healthy(self, run_mock) -> None:
        run_mock.side_effect = [Mock(stdout="402"), Mock(stdout="200")]

        result = check_product_health(
            {
                "name": "HTML Entity Encoder",
                "slug": "html-entity-encoder",
                "status": "live",
                "vercel_url": "https://html-entity-encoder.vercel.app",
                "deployment_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
            }
        )

        self.assertEqual(result["status"], "alternate_healthy")
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["url"], "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app")
        self.assertEqual(result["canonical_status"], "deployment_disabled")
        self.assertEqual(result["canonical_code"], 402)
        self.assertEqual(result["canonical_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(result["canonical_probe_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(run_mock.call_count, 2)

    @patch("scripts.health_check.subprocess.run")
    def test_non_standard_http_failure_code_is_preserved(self, run_mock) -> None:
        run_mock.return_value = Mock(stdout="451")

        result = check_product_health(
            {
                "name": "Failure Tool",
                "slug": "failure-tool",
                "status": "live",
                "vercel_url": "https://failure-tool.vercel.app",
            }
        )

        self.assertEqual(result["status"], "error_451")
        self.assertEqual(result["code"], 451)
        self.assertIn("checked_at", result)

    @patch("scripts.health_check.subprocess.run")
    def test_deployment_disabled_http_402_is_reported_explicitly(self, run_mock) -> None:
        run_mock.return_value = Mock(stdout="402")

        result = check_product_health(
            {
                "name": "Blocked Tool",
                "slug": "blocked-tool",
                "status": "live",
                "vercel_url": "https://blocked-tool.vercel.app",
            }
        )

        self.assertEqual(result["status"], "deployment_disabled")
        self.assertEqual(result["code"], 402)
        self.assertEqual(result["url"], "https://blocked-tool.vercel.app")
        self.assertEqual(run_mock.call_count, 1)

    def test_alternate_healthy_result_syncs_public_url(self) -> None:
        product = {
            "name": "Fallback Tool",
            "slug": "fallback-tool",
            "status": "live",
            "vercel_url": "https://fallback-tool.vercel.app",
            "v": "https://fallback-tool.vercel.app",
        }

        apply_health_result(
            product,
            {
                "status": "alternate_healthy",
                "code": 200,
                "url": "https://fallback-tool-preview.vercel.app",
                "checked_at": "2026-04-22T10:00:00Z",
                "canonical_status": "not_found",
                "canonical_code": 404,
                "canonical_url": "https://fallback-tool.vercel.app",
            },
        )

        self.assertEqual(product["health_status"], "alternate_healthy")
        self.assertEqual(product["last_health_code"], 200)
        self.assertEqual(product["last_health_url"], "https://fallback-tool-preview.vercel.app")
        self.assertEqual(product["last_health_check"], "2026-04-22T10:00:00Z")
        self.assertEqual(product["health_checked_at"], "2026-04-22T10:00:00Z")
        self.assertEqual(product["canonical_health_status"], "not_found")
        self.assertEqual(product["canonical_health_code"], 404)
        self.assertEqual(product["canonical_health_url"], "https://fallback-tool.vercel.app")
        self.assertEqual(product["canonical_probe_url"], "https://fallback-tool.vercel.app")
        self.assertEqual(product["canonical_health_checked_at"], "2026-04-22T10:00:00Z")
        self.assertEqual(product["ideal_vercel_url"], "https://fallback-tool.vercel.app")
        self.assertEqual(product["vercel_url"], "https://fallback-tool-preview.vercel.app")
        self.assertEqual(product["v"], "https://fallback-tool-preview.vercel.app")

    def test_effective_health_url_is_preserved_for_redirected_successes(self) -> None:
        product = {
            "name": "Redirect Tool",
            "slug": "redirect-tool",
            "status": "live",
            "vercel_url": "https://redirect-tool-rose.vercel.app",
        }

        apply_health_result(
            product,
            {
                "status": "healthy",
                "code": 200,
                "url": "https://redirect-tool-rose.vercel.app",
                "effective_url": "https://redirect-tool.vercel.app",
                "checked_at": "2026-04-22T11:00:00Z",
                "canonical_status": "healthy",
                "canonical_code": 200,
                "canonical_url": "https://redirect-tool.vercel.app",
            },
        )

        self.assertEqual(product["health_probe_url"], "https://redirect-tool-rose.vercel.app")
        self.assertEqual(product["effective_health_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(product["last_health_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(product["vercel_url"], "https://redirect-tool.vercel.app")
        self.assertEqual(product["v"], "https://redirect-tool.vercel.app")

    def test_redirected_preview_alias_keeps_probe_and_effective_urls_distinct(self) -> None:
        product = {
            "name": "HTML Entity Encoder/Decoder Pro",
            "slug": "html-entity-encoder",
            "status": "live",
            "vercel_url": "https://html-entity-encoder.vercel.app",
            "v": "https://html-entity-encoder.vercel.app",
        }

        apply_health_result(
            product,
            {
                "status": "alternate_healthy",
                "code": 200,
                "url": "https://html-entity-encoder.vercel.app",
                "effective_url": "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
                "checked_at": "2026-04-23T10:05:00Z",
                "canonical_status": "redirected_preview_alias",
                "canonical_code": 200,
                "canonical_url": "https://html-entity-encoder.vercel.app",
            },
        )

        self.assertEqual(product["health_probe_url"], "https://html-entity-encoder.vercel.app")
        self.assertEqual(
            product["effective_health_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(
            product["last_health_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(
            product["vercel_url"],
            "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app",
        )
        self.assertEqual(product["canonical_health_status"], "redirected_preview_alias")
        self.assertEqual(product["canonical_health_code"], 200)
        self.assertEqual(product["canonical_probe_url"], "https://html-entity-encoder.vercel.app")

    def test_synced_health_results_include_alternate_healthy(self) -> None:
        self.assertTrue(is_synced_health_result({"status": "healthy"}))
        self.assertTrue(is_synced_health_result({"status": "alternate_healthy"}))
        self.assertFalse(is_synced_health_result({"status": "not_found"}))

    def test_main_keeps_raw_state_pristine_while_mutating_working_copy(self) -> None:
        original_cwd = os.getcwd()
        captured = {}

        def fake_build_summary(state, product_catalog=None, raw_state=None):
            captured["state"] = state
            captured["raw_state"] = raw_state
            return {
                "healthy_count": 1,
                "unhealthy_count": 0,
                "live_count": 1,
                "canonical_url_drift": 0,
            }

        def identity_apply_summary_fields(state, summary):
            return state

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            tmp_path.joinpath("STATE.json").write_text(
                json.dumps(
                    {
                        "cycle": 1,
                        "mode": "OPTIMIZE",
                        "products": {
                            "active": [
                                {
                                    "name": "Raw State Tool",
                                    "slug": "raw-state-tool",
                                    "status": "live",
                                    "vercel_url": "https://raw-state-tool.vercel.app",
                                }
                            ],
                            "spec_ready": [],
                        },
                    }
                ),
                encoding="utf-8",
            )

            try:
                os.chdir(tmpdir)
                with patch.object(health_check, "check_product_health", return_value={
                    "name": "Raw State Tool",
                    "slug": "raw-state-tool",
                    "status": "healthy",
                    "code": 200,
                    "url": "https://raw-state-tool.vercel.app",
                    "canonical_url": "https://raw-state-tool.vercel.app",
                    "canonical_status": "healthy",
                    "canonical_code": 200,
                    "checked_at": "2026-04-22T10:00:00Z",
                }), patch.object(health_check, "load_product_catalog", return_value={}), patch.object(
                    health_check, "build_summary", side_effect=fake_build_summary
                ), patch.object(health_check, "apply_summary_fields", side_effect=identity_apply_summary_fields), patch.object(
                    health_check, "persist_summary"
                ):
                    result = health_check.main()
            finally:
                os.chdir(original_cwd)

        self.assertEqual(result["unhealthy"], 0)
        self.assertEqual(captured["raw_state"]["products"]["active"][0], {
            "name": "Raw State Tool",
            "slug": "raw-state-tool",
            "status": "live",
            "vercel_url": "https://raw-state-tool.vercel.app",
        })
        self.assertIn("ideal_vercel_url", captured["state"]["products"]["active"][0])
        self.assertIn("health_status", captured["state"]["products"]["active"][0])


if __name__ == "__main__":
    unittest.main()
