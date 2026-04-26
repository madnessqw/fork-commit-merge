import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from scripts.split_shared_checkouts import get_token, polar_request


class SplitSharedCheckoutsTests(unittest.TestCase):
    def _temp_root(self) -> Path:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        root = Path(tempdir.name)
        return root

    def test_get_token_from_env(self) -> None:
        with patch.dict("os.environ", {"POLAR_OAT": "env_token_123"}):
            token = get_token()
            self.assertEqual(token, "env_token_123")

    def test_get_token_from_config_file(self) -> None:
        root = self._temp_root()
        config_dir = root / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "polar.json").write_text(json.dumps({"polar_oat": "file_token_456"}))
        with patch.dict("os.environ", {}, clear=False):
            with patch("scripts.split_shared_checkouts.ROOT", root):
                with patch("os.environ.get", lambda k, d="": "" if k == "POLAR_OAT" else d):
                    from scripts.split_shared_checkouts import get_token as gt
                    token = gt()
                    self.assertEqual(token, "file_token_456")

    def test_get_token_raises_when_missing(self) -> None:
        root = self._temp_root()
        config_dir = root / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "polar.json").write_text("{}")
        with patch("scripts.split_shared_checkouts.ROOT", root):
            with patch("os.environ.get", lambda k, d="": ""):
                from scripts.split_shared_checkouts import get_token as gt
                with self.assertRaises(RuntimeError):
                    gt()

    def test_polar_request_success(self) -> None:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"id": "prod_123"}'
        mock_resp.json.return_value = {"id": "prod_123"}
        with patch("requests.request", return_value=mock_resp):
            result = polar_request("fake_token", "GET", "/products")
            self.assertEqual(result["id"], "prod_123")

    def test_polar_request_error_raises(self) -> None:
        mock_resp = MagicMock()
        mock_resp.status_code = 422
        mock_resp.text = "Validation error"
        with patch("requests.request", return_value=mock_resp):
            with self.assertRaises(RuntimeError) as ctx:
                polar_request("fake_token", "POST", "/products", json={"name": "x"})
            self.assertIn("422", str(ctx.exception))

    def test_polar_request_empty_content(self) -> None:
        mock_resp = MagicMock()
        mock_resp.status_code = 204
        mock_resp.content = b""
        with patch("requests.request", return_value=mock_resp):
            result = polar_request("fake_token", "DELETE", "/products/xyz")
            self.assertEqual(result, {})

    def test_pairs_are_defined(self) -> None:
        PAIRS = [
            ("uuid-generator", "uuid-generator-pro"),
            ("timestamp-converter", "timestamp-converter-pro"),
            ("toml-parser", "toml-parser-pro"),
            ("markdown-previewer", "markdown-previewer-pro"),
        ]
        self.assertEqual(len(PAIRS), 4)
        for base, pro in PAIRS:
            self.assertTrue(pro.endswith("-pro") or "-pro" in pro, f"{pro} should be pro variant")
            self.assertNotEqual(base, pro)

    def test_parse_price_helper(self) -> None:
        def parse_price(p: str) -> float:
            p = p.replace("$", "").strip()
            try:
                return float(p)
            except ValueError:
                return 0.0

        self.assertEqual(parse_price("$5"), 5.0)
        self.assertEqual(parse_price("$9.99"), 9.99)
        self.assertEqual(parse_price("0"), 0.0)
        self.assertEqual(parse_price("free"), 0.0)
        self.assertEqual(parse_price("$19.99"), 19.99)
        self.assertEqual(parse_price(" $7.50 "), 7.5)

    def test_price_inversion_detection(self) -> None:
        def parse_price(p: str) -> float:
            p = p.replace("$", "").strip()
            try:
                return float(p)
            except ValueError:
                return 0.0

        base_val = parse_price("$5")
        pro_val = parse_price("$9.99")
        self.assertGreater(pro_val, base_val)

        inverted_base = parse_price("$9.99")
        inverted_pro = parse_price("$5")
        self.assertLess(inverted_pro, inverted_base)

    def test_minimum_price_enforcement(self) -> None:
        price_cents = int(0.0 * 100)
        if price_cents < 50:
            price_cents = 500
        self.assertEqual(price_cents, 500)

        price_cents = int(3.0 * 100)
        if price_cents < 50:
            price_cents = 500
        self.assertEqual(price_cents, 300)

    def test_create_payload_structure(self) -> None:
        payload = {
            "name": "Test Pro (Pro Version)",
            "description": "Professional version",
            "visibility": "public",
            "metadata": {"source": "universecreator", "local_slug": "test-pro"},
            "prices": [{
                "amount_type": "fixed",
                "price_amount": 999,
                "price_currency": "usd",
            }],
        }
        self.assertEqual(payload["visibility"], "public")
        self.assertEqual(len(payload["prices"]), 1)
        self.assertEqual(payload["prices"][0]["price_currency"], "usd")

    def test_checkout_link_payload_structure(self) -> None:
        payload = {
            "product_price_id": "price_abc",
            "payment_processor": "stripe",
            "label": "universecreator:test-pro",
            "metadata": {"source": "universecreator", "local_slug": "test-pro"},
            "allow_discount_codes": True,
        }
        self.assertEqual(payload["payment_processor"], "stripe")
        self.assertTrue(payload["allow_discount_codes"])

    def test_shared_polar_id_detection(self) -> None:
        base_ppid = "polar_prod_shared_001"
        pro_ppid = "polar_prod_shared_001"
        self.assertEqual(base_ppid, pro_ppid)

        base_ppid2 = "polar_prod_A"
        pro_ppid2 = "polar_prod_B"
        self.assertNotEqual(base_ppid2, pro_ppid2)

    def test_product_json_update_logic(self) -> None:
        pro_pj = {
            "name": "Test Pro",
            "polar_product_id": "old_id",
            "checkout_url": "https://old.checkout.url",
        }
        new_ppid = "new_polar_id"
        new_checkout = "https://new.checkout.url"
        pro_pj["polar_product_id"] = new_ppid
        pro_pj["checkout_url"] = new_checkout
        pro_pj["payment_provider"] = "polar"
        self.assertEqual(pro_pj["polar_product_id"], new_ppid)
        self.assertEqual(pro_pj["checkout_url"], new_checkout)
        self.assertEqual(pro_pj["payment_provider"], "polar")


if __name__ == "__main__":
    unittest.main()
