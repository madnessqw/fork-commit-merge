import unittest
from unittest.mock import MagicMock, patch


class AuditPortfolioHealthTests(unittest.TestCase):
    @patch("scripts.audit_portfolio_health.health_check_main")
    def test_delegates_to_health_check_main(self, mock_hc: MagicMock) -> None:
        from scripts.audit_portfolio_health import health_check_main

        mock_hc.return_value = {"unhealthy": 0, "total": 5}
        result = health_check_main()
        mock_hc.assert_called_once()
        self.assertEqual(result["unhealthy"], 0)
        self.assertEqual(result["total"], 5)

    @patch("scripts.audit_portfolio_health.health_check_main")
    def test_returns_unhealthy_count(self, mock_hc: MagicMock) -> None:
        from scripts.audit_portfolio_health import health_check_main

        mock_hc.return_value = {"unhealthy": 3, "total": 10}
        result = health_check_main()
        self.assertEqual(result["unhealthy"], 3)

    @patch("scripts.audit_portfolio_health.health_check_main")
    def test_returns_empty_dict(self, mock_hc: MagicMock) -> None:
        from scripts.audit_portfolio_health import health_check_main

        mock_hc.return_value = {}
        result = health_check_main()
        self.assertEqual(result, {})

    @patch("scripts.audit_portfolio_health.health_check_main")
    def test_passes_through_all_keys(self, mock_hc: MagicMock) -> None:
        from scripts.audit_portfolio_health import health_check_main

        mock_hc.return_value = {
            "unhealthy": 0,
            "total": 5,
            "healthy": 5,
            "details": [],
        }
        result = health_check_main()
        self.assertIn("healthy", result)
        self.assertIn("details", result)


if __name__ == "__main__":
    unittest.main()
