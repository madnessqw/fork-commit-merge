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

    def test_reject_then_verify_restores_revenue(self):
        sale = p2p_sales_tracker.add_sale("P1", 25, "a@b.com", "TX-1")
        p2p_sales_tracker.reject_sale(sale["id"])
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 0)
        p2p_sales_tracker.verify_sale(sale["id"])
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 25)

    def test_reject_then_reopen_restores_revenue(self):
        sale = p2p_sales_tracker.add_sale("P1", 15, "a@b.com", "TX-1")
        p2p_sales_tracker.reject_sale(sale["id"])
        p2p_sales_tracker.update_sale_status(sale["id"], "pending_verification")
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 15)


class TestSearchSales(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sales_file = os.path.join(self.tmpdir, "p2p_sales.json")
        p2p_sales_tracker.SALES_FILE = self.sales_file

    def tearDown(self):
        if os.path.exists(self.sales_file):
            os.unlink(self.sales_file)
        os.rmdir(self.tmpdir)
        p2p_sales_tracker.SALES_FILE = "/home/gokhan/UniverseCreator/data/p2p_sales.json"

    def test_search_empty_returns_all(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")
        results = p2p_sales_tracker.search_sales()
        self.assertEqual(len(results), 2)

    def test_search_by_product_name(self):
        p2p_sales_tracker.add_sale("SEO Tool", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("Dev Kit", 20, "c@d.com", "TX-2")
        results = p2p_sales_tracker.search_sales(query="seo")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["product"], "SEO Tool")

    def test_search_by_buyer_email(self):
        p2p_sales_tracker.add_sale("P1", 10, "alice@test.com", "TX-1")
        p2p_sales_tracker.add_sale("P2", 20, "bob@test.com", "TX-2")
        results = p2p_sales_tracker.search_sales(query="bob")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["buyer_email"], "bob@test.com")

    def test_search_by_transaction_id(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-ALPHA")
        p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-BETA")
        results = p2p_sales_tracker.search_sales(query="ALPHA")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["transaction_id"], "TX-ALPHA")

    def test_search_by_status(self):
        s1 = p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")
        p2p_sales_tracker.verify_sale(s1["id"])
        results = p2p_sales_tracker.search_sales(status="verified")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "verified")

    def test_search_by_product_exact(self):
        p2p_sales_tracker.add_sale("SEO Tool", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("Dev Kit", 20, "c@d.com", "TX-2")
        results = p2p_sales_tracker.search_sales(product="SEO Tool")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["product"], "SEO Tool")

    def test_search_combined_filters(self):
        s1 = p2p_sales_tracker.add_sale("SEO Tool", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("Dev Kit", 20, "c@d.com", "TX-2")
        p2p_sales_tracker.verify_sale(s1["id"])
        results = p2p_sales_tracker.search_sales(query="seo", status="verified")
        self.assertEqual(len(results), 1)
        results2 = p2p_sales_tracker.search_sales(query="seo", status="pending_verification")
        self.assertEqual(len(results2), 0)

    def test_search_case_insensitive(self):
        p2p_sales_tracker.add_sale("My Product", 10, "a@b.com", "TX-1")
        results = p2p_sales_tracker.search_sales(query="MY PRODUCT")
        self.assertEqual(len(results), 1)
        results2 = p2p_sales_tracker.search_sales(query="my product")
        self.assertEqual(len(results2), 1)

    def test_search_no_match(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        results = p2p_sales_tracker.search_sales(query="nonexistent")
        self.assertEqual(len(results), 0)


class TestDeleteSale(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sales_file = os.path.join(self.tmpdir, "p2p_sales.json")
        p2p_sales_tracker.SALES_FILE = self.sales_file

    def tearDown(self):
        if os.path.exists(self.sales_file):
            os.unlink(self.sales_file)
        os.rmdir(self.tmpdir)
        p2p_sales_tracker.SALES_FILE = "/home/gokhan/UniverseCreator/data/p2p_sales.json"

    def test_delete_sale_removes_entry(self):
        sale = p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        result = p2p_sales_tracker.delete_sale(sale["id"])
        self.assertIsNotNone(result)
        self.assertEqual(result["remaining"], 0)
        self.assertEqual(result["deleted"]["product"], "P1")
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 0)

    def test_delete_sale_deducts_revenue_if_not_rejected(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        sale2 = p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")
        p2p_sales_tracker.delete_sale(sale2["id"])
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 10)

    def test_delete_rejected_sale_no_double_deduct(self):
        sale = p2p_sales_tracker.add_sale("P1", 15, "a@b.com", "TX-1")
        p2p_sales_tracker.reject_sale(sale["id"])
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 0)
        p2p_sales_tracker.delete_sale(sale["id"])
        self.assertEqual(p2p_sales_tracker.load_sales()["total_revenue"], 0)

    def test_delete_nonexistent_returns_none(self):
        result = p2p_sales_tracker.delete_sale(999)
        self.assertIsNone(result)

    def test_delete_sale_preserves_others(self):
        s1 = p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        s2 = p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")
        s3 = p2p_sales_tracker.add_sale("P3", 30, "e@f.com", "TX-3")
        p2p_sales_tracker.delete_sale(s2["id"])
        saved = p2p_sales_tracker.load_sales()
        self.assertEqual(len(saved["sales"]), 2)
        self.assertEqual(saved["total_revenue"], 40)
        ids = [s["id"] for s in saved["sales"]]
        self.assertIn(s1["id"], ids)
        self.assertIn(s3["id"], ids)


class TestSalesByPeriod(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sales_file = os.path.join(self.tmpdir, "p2p_sales.json")
        p2p_sales_tracker.SALES_FILE = self.sales_file

    def tearDown(self):
        if os.path.exists(self.sales_file):
            os.unlink(self.sales_file)
        os.rmdir(self.tmpdir)
        p2p_sales_tracker.SALES_FILE = "/home/gokhan/UniverseCreator/data/p2p_sales.json"

    def _inject_sale_with_date(self, product, amount, email, tx_id, date_str):
        data = p2p_sales_tracker.load_sales()
        sale = {
            "id": len(data["sales"]) + 1,
            "product": product,
            "amount": amount,
            "buyer_email": email,
            "transaction_id": tx_id,
            "date": date_str,
            "status": "pending_verification",
        }
        data["sales"].append(sale)
        data["total_revenue"] += amount
        p2p_sales_tracker.save_sales(data)
        return sale

    def test_empty_returns_empty(self):
        result = p2p_sales_tracker.sales_by_period()
        self.assertEqual(result, [])

    def test_daily_grouping(self):
        self._inject_sale_with_date("P1", 10, "a@b.com", "TX-1", "2026-04-25T10:00:00")
        self._inject_sale_with_date("P2", 20, "c@d.com", "TX-2", "2026-04-25T14:00:00")
        self._inject_sale_with_date("P3", 15, "e@f.com", "TX-3", "2026-04-24T10:00:00")
        result = p2p_sales_tracker.sales_by_period(period="daily")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["period"], "2026-04-24")
        self.assertEqual(result[0]["count"], 1)
        self.assertEqual(result[0]["revenue"], 15)
        self.assertEqual(result[1]["period"], "2026-04-25")
        self.assertEqual(result[1]["count"], 2)
        self.assertEqual(result[1]["revenue"], 30)

    def test_monthly_grouping(self):
        self._inject_sale_with_date("P1", 10, "a@b.com", "TX-1", "2026-04-01T10:00:00")
        self._inject_sale_with_date("P2", 20, "c@d.com", "TX-2", "2026-04-15T10:00:00")
        self._inject_sale_with_date("P3", 30, "e@f.com", "TX-3", "2026-03-20T10:00:00")
        result = p2p_sales_tracker.sales_by_period(period="monthly")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["period"], "2026-03")
        self.assertEqual(result[0]["revenue"], 30)
        self.assertEqual(result[1]["period"], "2026-04")
        self.assertEqual(result[1]["revenue"], 30)

    def test_weekly_grouping(self):
        self._inject_sale_with_date("P1", 10, "a@b.com", "TX-1", "2026-04-20T10:00:00")
        self._inject_sale_with_date("P2", 25, "c@d.com", "TX-2", "2026-04-21T10:00:00")
        result = p2p_sales_tracker.sales_by_period(period="weekly")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["count"], 2)
        self.assertEqual(result[0]["revenue"], 35)

    def test_status_filter(self):
        sale = self._inject_sale_with_date("P1", 10, "a@b.com", "TX-1", "2026-04-25T10:00:00")
        self._inject_sale_with_date("P2", 20, "c@d.com", "TX-2", "2026-04-25T14:00:00")
        p2p_sales_tracker.verify_sale(sale["id"])
        result = p2p_sales_tracker.sales_by_period(status="verified")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["count"], 1)
        self.assertEqual(result[0]["verified_revenue"], 10)

    def test_verified_revenue_per_period(self):
        s1 = self._inject_sale_with_date("P1", 10, "a@b.com", "TX-1", "2026-04-25T10:00:00")
        self._inject_sale_with_date("P2", 20, "c@d.com", "TX-2", "2026-04-25T14:00:00")
        p2p_sales_tracker.verify_sale(s1["id"])
        result = p2p_sales_tracker.sales_by_period(period="daily")
        self.assertEqual(result[0]["revenue"], 30)
        self.assertEqual(result[0]["verified_revenue"], 10)

    def test_invalid_date_skipped(self):
        self._inject_sale_with_date("P1", 10, "a@b.com", "TX-1", "2026-04-25T10:00:00")
        data = p2p_sales_tracker.load_sales()
        data["sales"].append({"id": 2, "product": "X", "amount": 5, "date": "bad-date", "status": "pending_verification"})
        p2p_sales_tracker.save_sales(data)
        result = p2p_sales_tracker.sales_by_period(period="daily")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["revenue"], 10)

    def test_invalid_period_defaults_daily(self):
        self._inject_sale_with_date("P1", 10, "a@b.com", "TX-1", "2026-04-25T10:00:00")
        result = p2p_sales_tracker.sales_by_period(period="yearly")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["period"], "2026-04-25")

    def test_missing_date_skipped(self):
        data = p2p_sales_tracker.load_sales()
        data["sales"].append({"id": 1, "product": "X", "amount": 5, "status": "pending_verification"})
        p2p_sales_tracker.save_sales(data)
        result = p2p_sales_tracker.sales_by_period()
        self.assertEqual(result, [])


class TestExportSalesCSV(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.sales_file = os.path.join(self.tmpdir, "p2p_sales.json")
        p2p_sales_tracker.SALES_FILE = self.sales_file

    def tearDown(self):
        if os.path.exists(self.sales_file):
            os.unlink(self.sales_file)
        p2p_sales_tracker.SALES_FILE = "/home/gokhan/UniverseCreator/data/p2p_sales.json"

    def test_empty_sales_produces_header_only(self):
        result = p2p_sales_tracker.export_sales_csv()
        self.assertEqual(result["row_count"], 0)
        lines = result["csv"].strip().split("\n")
        self.assertEqual(len(lines), 1)
        self.assertIn("id", lines[0])

    def test_export_includes_all_sales(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")
        result = p2p_sales_tracker.export_sales_csv()
        self.assertEqual(result["row_count"], 2)
        lines = result["csv"].strip().split("\n")
        self.assertEqual(len(lines), 3)

    def test_export_filters_by_status(self):
        s1 = p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("P2", 20, "c@d.com", "TX-2")
        p2p_sales_tracker.verify_sale(s1["id"])
        result = p2p_sales_tracker.export_sales_csv(status="verified")
        self.assertEqual(result["row_count"], 1)
        self.assertIn("P1", result["csv"])

    def test_export_filters_by_product(self):
        p2p_sales_tracker.add_sale("SEO Tool", 10, "a@b.com", "TX-1")
        p2p_sales_tracker.add_sale("Dev Kit", 20, "c@d.com", "TX-2")
        result = p2p_sales_tracker.export_sales_csv(product="SEO Tool")
        self.assertEqual(result["row_count"], 1)
        self.assertIn("SEO Tool", result["csv"])

    def test_export_writes_to_file(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        csv_path = os.path.join(self.tmpdir, "export.csv")
        result = p2p_sales_tracker.export_sales_csv(output_path=csv_path)
        self.assertTrue(os.path.exists(csv_path))
        with open(csv_path) as f:
            content = f.read()
        self.assertIn("P1", content)
        self.assertEqual(result["path"], csv_path)

    def test_export_csv_has_correct_columns(self):
        p2p_sales_tracker.add_sale("P1", 10, "a@b.com", "TX-1")
        result = p2p_sales_tracker.export_sales_csv()
        header = result["csv"].split("\n")[0].strip()
        for field in ["id", "product", "amount", "buyer_email", "transaction_id", "date", "status"]:
            self.assertIn(field, header)
