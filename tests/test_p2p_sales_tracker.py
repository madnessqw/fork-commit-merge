import json
import os
import tempfile
import unittest
from unittest.mock import patch

from scripts import p2p_sales_tracker


class P2PSalesTrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sales_file = os.path.join(self.tmpdir, "p2p_sales.json")
        p2p_sales_tracker.SALES_FILE = self.sales_file

    def tearDown(self):
        if os.path.exists(self.sales_file):
            os.unlink(self.sales_file)
        os.rmdir(self.tmpdir)
        p2p_sales_tracker.SALES_FILE = (
            "/home/gokhan/UniverseCreator/data/p2p_sales.json"
        )

    def test_load_sales_returns_default_when_file_missing(self):
        result = p2p_sales_tracker.load_sales()
        self.assertEqual(result, {"sales": [], "total_revenue": 0})

    def test_load_sales_returns_default_on_invalid_json(self):
        with open(self.sales_file, "w") as f:
            f.write("{invalid json")
        result = p2p_sales_tracker.load_sales()
        self.assertEqual(result, {"sales": [], "total_revenue": 0})

    def test_load_sales_reads_valid_file(self):
        data = {
            "sales": [{"id": 1, "product": "test", "amount": 10}],
            "total_revenue": 10,
        }
        with open(self.sales_file, "w") as f:
            json.dump(data, f)
        result = p2p_sales_tracker.load_sales()
        self.assertEqual(result["total_revenue"], 10)
        self.assertEqual(len(result["sales"]), 1)

    def test_add_sale_appends_and_saves(self):
        sale = p2p_sales_tracker.add_sale(
            "Test Product", 29, "buyer@test.com", "TX-001"
        )
        self.assertEqual(sale["product"], "Test Product")
        self.assertEqual(sale["amount"], 29)
        self.assertEqual(sale["buyer_email"], "buyer@test.com")
        self.assertEqual(sale["transaction_id"], "TX-001")
        self.assertEqual(sale["status"], "pending_verification")

        saved = p2p_sales_tracker.load_sales()
        self.assertEqual(len(saved["sales"]), 1)
        self.assertEqual(saved["total_revenue"], 29)

    def test_add_sale_accumulates_revenue(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")

        saved = p2p_sales_tracker.load_sales()
        self.assertEqual(len(saved["sales"]), 2)
        self.assertEqual(saved["total_revenue"], 30)

    def test_list_products_returns_list(self):
        products = p2p_sales_tracker.list_products()
        self.assertIsInstance(products, list)
        self.assertTrue(len(products) > 0)
        for p in products:
            self.assertIn("id", p)
            self.assertIn("name", p)
            self.assertIn("price", p)

    def test_add_sale_increments_id(self):
        s1 = p2p_sales_tracker.add_sale("P1", 5, "a@b.com", "TX-1")
        s2 = p2p_sales_tracker.add_sale("P2", 10, "c@d.com", "TX-2")
        self.assertEqual(s1["id"], 1)
        self.assertEqual(s2["id"], 2)


class TestParsePriceInt(unittest.TestCase):
    def test_none_returns_none(self):
        self.assertIsNone(p2p_sales_tracker._parse_price_int(None))

    def test_int_returns_int(self):
        self.assertEqual(p2p_sales_tracker._parse_price_int(19), 19)

    def test_float_string_returns_int(self):
        self.assertEqual(p2p_sales_tracker._parse_price_int("19.99"), 19)

    def test_dollar_prefix_stripped(self):
        self.assertEqual(p2p_sales_tracker._parse_price_int("$29"), 29)

    def test_dollar_float_stripped(self):
        self.assertEqual(p2p_sales_tracker._parse_price_int("$9.99"), 9)

    def test_whitespace_stripped(self):
        self.assertEqual(p2p_sales_tracker._parse_price_int("  15  "), 15)

    def test_invalid_string_returns_none(self):
        self.assertIsNone(p2p_sales_tracker._parse_price_int("free"))

    def test_zero_price(self):
        self.assertEqual(p2p_sales_tracker._parse_price_int(0), 0)

    def test_negative_price(self):
        self.assertEqual(p2p_sales_tracker._parse_price_int(-5), -5)


class TestListProductsEdgeCases(unittest.TestCase):
    def test_custom_state_path_nonexistent(self):
        result = p2p_sales_tracker.list_products(
            state_path="/nonexistent/STATE.json"
        )
        self.assertEqual(result, p2p_sales_tracker._FALLBACK_PRODUCTS)

    def test_custom_state_path_empty_active(self):
        tmpdir = tempfile.mkdtemp()
        state_file = os.path.join(tmpdir, "STATE.json")
        with open(state_file, "w") as f:
            json.dump({"products": {"active": []}}, f)
        result = p2p_sales_tracker.list_products(state_path=state_file)
        self.assertEqual(result, p2p_sales_tracker._FALLBACK_PRODUCTS)
        os.unlink(state_file)
        os.rmdir(tmpdir)

    def test_custom_state_path_live_no_price(self):
        tmpdir = tempfile.mkdtemp()
        state_file = os.path.join(tmpdir, "STATE.json")
        with open(state_file, "w") as f:
            json.dump(
                {
                    "products": {
                        "active": [
                            {"slug": "free-tool", "status": "live", "price": None}
                        ]
                    }
                },
                f,
            )
        result = p2p_sales_tracker.list_products(state_path=state_file)
        self.assertEqual(result, p2p_sales_tracker._FALLBACK_PRODUCTS)
        os.unlink(state_file)
        os.rmdir(tmpdir)

    def test_custom_state_path_live_with_price(self):
        tmpdir = tempfile.mkdtemp()
        state_file = os.path.join(tmpdir, "STATE.json")
        with open(state_file, "w") as f:
            json.dump(
                {
                    "products": {
                        "active": [
                            {
                                "slug": "paid-tool",
                                "name": "Paid Tool",
                                "status": "live",
                                "price": "$25",
                                "category": "dev",
                            }
                        ]
                    }
                },
                f,
            )
        result = p2p_sales_tracker.list_products(state_path=state_file)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["price"], 25)
        self.assertEqual(result[0]["name"], "Paid Tool")
        self.assertEqual(result[0]["slug"], "paid-tool")
        os.unlink(state_file)
        os.rmdir(tmpdir)

    def test_invalid_json_triggers_fallback(self):
        tmpdir = tempfile.mkdtemp()
        state_file = os.path.join(tmpdir, "STATE.json")
        with open(state_file, "w") as f:
            f.write("{bad json")
        result = p2p_sales_tracker.list_products(state_path=state_file)
        self.assertEqual(result, p2p_sales_tracker._FALLBACK_PRODUCTS)
        os.unlink(state_file)
        os.rmdir(tmpdir)


class TestGetSalesSummary(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sales_file = os.path.join(self.tmpdir, "p2p_sales.json")
        p2p_sales_tracker.SALES_FILE = self.sales_file

    def tearDown(self):
        if os.path.exists(self.sales_file):
            os.unlink(self.sales_file)
        os.rmdir(self.tmpdir)
        p2p_sales_tracker.SALES_FILE = "/home/gokhan/UniverseCreator/data/p2p_sales.json"

    def test_empty_sales(self):
        summary = p2p_sales_tracker.get_sales_summary()
        self.assertEqual(summary["total_sales"], 0)
        self.assertEqual(summary["total_revenue"], 0)
        self.assertEqual(summary["verified_revenue"], 0)
        self.assertIsNone(summary["last_sale_date"])

    def test_with_sales(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")
        summary = p2p_sales_tracker.get_sales_summary()
        self.assertEqual(summary["total_sales"], 2)
        self.assertEqual(summary["total_revenue"], 30)
        self.assertEqual(summary["verified_revenue"], 0)
        self.assertEqual(summary["by_status"]["pending_verification"], 2)
        self.assertIsNotNone(summary["last_sale_date"])


class TestVerifyRejectSale(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sales_file = os.path.join(self.tmpdir, "p2p_sales.json")
        p2p_sales_tracker.SALES_FILE = self.sales_file

    def tearDown(self):
        if os.path.exists(self.sales_file):
            os.unlink(self.sales_file)
        os.rmdir(self.tmpdir)
        p2p_sales_tracker.SALES_FILE = "/home/gokhan/UniverseCreator/data/p2p_sales.json"

    def test_verify_sale_updates_status(self):
        sale = p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        result = p2p_sales_tracker.verify_sale(sale["id"])
        self.assertEqual(result["status"], "verified")
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 10)

    def test_reject_sale_deducts_revenue(self):
        sale = p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        result = p2p_sales_tracker.reject_sale(sale["id"])
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 0)

    def test_verify_nonexistent_returns_none(self):
        result = p2p_sales_tracker.verify_sale(999)
        self.assertIsNone(result)

    def test_reject_nonexistent_returns_none(self):
        result = p2p_sales_tracker.reject_sale(999)
        self.assertIsNone(result)

    def test_verified_revenue_only_counts_verified(self):
        s1 = p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")
        p2p_sales_tracker.verify_sale(s1["id"])
        summary = p2p_sales_tracker.get_sales_summary()
        self.assertEqual(summary["verified_revenue"], 10)
        self.assertEqual(summary["total_revenue"], 30)

    def test_reject_does_not_go_negative(self):
        sale = p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.reject_sale(sale["id"])
        p2p_sales_tracker.reject_sale(sale["id"])
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 0)
