import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from scripts.polar_checkout_sync import (
    ensure_checkout_link,
    PolarClient,
    discover_price_from_files,
    find_remote_product,
    load_local_products,
    parse_price_to_cents,
    polar_checkout_requires_link_repair,
    product_needs_update,
    slugify_name,
)


class PolarCheckoutSyncTests(unittest.TestCase):
    def test_polar_client_request_preserves_post_across_307_redirect(self) -> None:
        events: list[tuple[str, str]] = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length") or "0")
                body = self.rfile.read(length).decode("utf-8")
                events.append((self.path, body))

                if self.path == "/products":
                    self.send_response(307)
                    self.send_header("Location", "/v1/products")
                    self.end_headers()
                    return

                if self.path == "/v1/products":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps({"ok": True, "body": json.loads(body)}).encode("utf-8")
                    )
                    return

                self.send_error(404)

            def log_message(self, format: str, *args) -> None:  # noqa: A003
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            client = PolarClient(
                "test-token",
                base_url=f"http://127.0.0.1:{server.server_port}",
            )
            result = client.create_product({"name": "Redirect Tool"})
        finally:
            server.shutdown()
            thread.join(timeout=5)

        self.assertEqual(result["ok"], True)
        self.assertEqual(events[0][0], "/products")
        self.assertEqual(events[1][0], "/v1/products")
        self.assertEqual(events[1][1], json.dumps({"name": "Redirect Tool"}))

    def test_parse_price_to_cents_handles_common_product_formats(self) -> None:
        self.assertEqual(parse_price_to_cents("9"), 900)
        self.assertEqual(parse_price_to_cents("$19"), 1900)
        self.assertEqual(parse_price_to_cents("$12 one-time"), 1200)
        self.assertEqual(parse_price_to_cents(29), 2900)

    def test_slugify_name_normalizes_human_titles(self) -> None:
        self.assertEqual(
            slugify_name("API Spec Validator — Quick Check"),
            "api-spec-validator-quick-check",
        )
        self.assertEqual(
            slugify_name("  Cron Expression Builder  "), "cron-expression-builder"
        )

    def test_product_needs_update_when_remote_price_or_visibility_drift_exists(
        self,
    ) -> None:
        local = type(
            "Local",
            (),
            {
                "name": "Tool X",
                "description": "Desc",
                "price_cents": 1900,
            },
        )()
        remote = {
            "name": "Tool X",
            "description": "Desc",
            "visibility": "private",
            "prices": [
                {"price_amount": 900, "price_currency": "usd", "is_archived": False}
            ],
        }
        self.assertTrue(product_needs_update(remote, local))

    def test_discover_price_from_files_falls_back_to_site_markup(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            product_dir = Path(tmpdir)
            (product_dir / "public").mkdir()
            (product_dir / "public" / "index.html").write_text(
                '<a class="cta">Get Lifetime Access — $19</a>',
                encoding="utf-8",
            )
            found = discover_price_from_files(product_dir)

        self.assertIsNotNone(found)
        cents, source = found
        self.assertEqual(cents, 1900)
        self.assertIn("public/index.html", source)

    def test_polar_checkout_requires_link_repair_without_link_metadata(self) -> None:
        self.assertTrue(
            polar_checkout_requires_link_repair(
                {},
                checkout_url="https://polar.sh/checkout/polar_cs_session",
                payment_provider="polar",
            )
        )
        self.assertFalse(
            polar_checkout_requires_link_repair(
                {
                    "polar_checkout_link_id": "polar_cl_123",
                    "polar_product_id": "prod_123",
                },
                checkout_url="https://polar.sh/checkout/polar_cl_123",
                payment_provider="polar",
            )
        )

    def test_load_local_products_reselects_polar_session_urls_for_link_rollout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            product_dir = root / "products" / "session-tool"
            product_dir.mkdir(parents=True)
            (product_dir / "product.json").write_text(
                """{
  "name": "Session Tool",
  "slug": "session-tool",
  "status": "live",
  "price": "$19",
  "vercel_url": "https://session-tool.vercel.app",
  "checkout_url": "https://polar.sh/checkout/polar_cs_session"
}
""",
                encoding="utf-8",
            )

            with patch("scripts.polar_checkout_sync.PRODUCTS_DIR", root / "products"):
                products = load_local_products(
                    statuses={"live"},
                    include_existing=False,
                    replace_non_polar=False,
                )

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].payment_provider, "polar")
        self.assertEqual(products[0].selection_reason, "repair_polar_link")

    def test_load_local_products_reselects_legacy_non_polar_checkout_without_vercel_url(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            product_dir = root / "products" / "legacy-tool"
            product_dir.mkdir(parents=True)
            (product_dir / "product.json").write_text(
                """{
  "name": "Legacy Tool",
  "slug": "legacy-tool",
  "status": "live",
  "price": "$19",
  "checkout_url": "https://profitbridge.lemonsqueezy.com/checkout/buy/legacy-tool-001",
  "payment_provider": "lemonsqueezy"
}
""",
                encoding="utf-8",
            )

            with patch("scripts.polar_checkout_sync.PRODUCTS_DIR", root / "products"):
                products = load_local_products(
                    statuses={"live"},
                    include_existing=False,
                    replace_non_polar=True,
                )

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].payment_provider, "lemonsqueezy")
        self.assertEqual(products[0].selection_reason, "replace_non_polar")

    def test_ensure_checkout_link_omits_return_urls_without_vercel_url(self) -> None:
        captured: dict[str, dict] = {}

        class FakeClient:
            def create_checkout_link(self, payload: dict) -> dict:
                captured["payload"] = payload
                return {"id": "polar_cl_test", "url": "https://buy.polar.sh/polar_cl_test"}

        local = type(
            "Local",
            (),
            {
                "slug": "legacy-tool",
                "vercel_url": None,
                "price_cents": 1900,
            },
        )()
        remote_product = {
            "id": "polar_pr_test",
            "prices": [
                {
                    "id": "polar_price_test",
                    "price_amount": 1900,
                    "price_currency": "usd",
                    "is_archived": False,
                }
            ],
        }

        ensure_checkout_link(FakeClient(), [], remote_product=remote_product, local=local)

        payload = captured["payload"]
        self.assertNotIn("success_url", payload)
        self.assertNotIn("return_url", payload)
        self.assertEqual(payload["product_price_id"], "polar_price_test")
        self.assertEqual(payload["label"], "universecreator:legacy-tool")

    def test_find_remote_product_matches_by_metadata_slug_first(self) -> None:
        local = type("Local", (), {"name": "My Tool", "slug": "my-tool"})()
        remote_products = [
            {"name": "My Tool", "metadata": {}},
            {"name": "Other", "metadata": {"local_slug": "my-tool"}},
        ]
        result = find_remote_product(remote_products, local)
        self.assertEqual(result["metadata"]["local_slug"], "my-tool")

    def test_find_remote_product_falls_back_to_slugified_name(self) -> None:
        local = type("Local", (), {"name": "My Cool Tool", "slug": "my-tool"})()
        remote_products = [
            {"name": "my-cool-tool", "metadata": {}},
        ]
        result = find_remote_product(remote_products, local)
        self.assertEqual(result["name"], "my-cool-tool")

    def test_find_remote_product_returns_none_when_no_match(self) -> None:
        local = type("Local", (), {"name": "Unique Tool", "slug": "unique-tool"})()
        result = find_remote_product([], local)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
