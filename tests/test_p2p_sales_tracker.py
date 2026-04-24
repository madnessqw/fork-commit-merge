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
