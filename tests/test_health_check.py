import unittest
from unittest.mock import Mock, patch

from scripts.health_check import check_product_health


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
        self.assertEqual(run_mock.call_count, 2)


if __name__ == "__main__":
    unittest.main()
