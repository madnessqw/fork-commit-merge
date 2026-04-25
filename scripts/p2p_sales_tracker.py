#!/usr/bin/env python3
"""
P2P Sales Tracker - UniverseCreator
Direct payment tracking for PayPal/Akbank
"""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SALES_DIR = ROOT / "data"
SALES_FILE = SALES_DIR / "p2p_sales.json"
STATE_FILE = ROOT / "STATE.json"

_FALLBACK_PRODUCTS = [
    {"id": 1, "name": "SEO Analyzer API", "price": 19, "description": "Full SEO analysis service"},
    {"id": 2, "name": "Invoice Generator API", "price": 5, "description": "Invoice management system"},
    {"id": 3, "name": "Content Distributor", "price": 15, "description": "Multi-platform content tool"},
    {"id": 4, "name": "Dev Tools Bundle", "price": 49, "description": "All tools + future updates"},
]
PAYMENT_INFO = """
💰 DIRECT PAYMENT OPTIONS:

PayPal: chaotikss@gmail.com
Akbank IBAN: TR38 0004 6002 0088 8000 1791 88

Send payment and email universe7creator@gmail.com with:
- Product name
- Transaction ID
- Your email for API key delivery
"""


def _ensure_data_dir():
    SALES_DIR.mkdir(parents=True, exist_ok=True)


def load_sales():
    try:
        with open(SALES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"sales": [], "total_revenue": 0}


def save_sales(data):
    _ensure_data_dir()
    with open(SALES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_sale(product, amount, buyer_email, transaction_id):
    data = load_sales()
    sale = {
        "id": len(data["sales"]) + 1,
        "product": product,
        "amount": amount,
        "buyer_email": buyer_email,
        "transaction_id": transaction_id,
        "date": datetime.now(timezone.utc).isoformat(),
        "status": "pending_verification",
    }
    data["sales"].append(sale)
    data["total_revenue"] += amount
    save_sales(data)
    return sale


def _parse_price_int(raw) -> int | None:
    if raw is None:
        return None
    s = str(raw).strip().lstrip("$")
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def list_products(state_path: Path | None = None):
    path = state_path or STATE_FILE
    try:
        with open(path, encoding="utf-8") as f:
            state = json.load(f)
        active = state.get("products", {}).get("active", [])
        live = [p for p in active if p.get("status") == "live"]
        if not live:
            return _FALLBACK_PRODUCTS
        result = []
        for idx, p in enumerate(live, start=1):
            price = _parse_price_int(p.get("price"))
            if price is None:
                continue
            result.append({
                "id": idx,
                "name": p.get("name", p.get("slug", f"Product {idx}")),
                "price": price,
                "slug": p.get("slug", ""),
                "description": p.get("category", ""),
            })
        return result if result else _FALLBACK_PRODUCTS
    except (OSError, json.JSONDecodeError, KeyError):
        return _FALLBACK_PRODUCTS


def get_sales_summary():
    data = load_sales()
    sales = data.get("sales", [])
    by_status = {}
    for s in sales:
        st = s.get("status", "unknown")
        by_status[st] = by_status.get(st, 0) + 1
    verified_revenue = sum(s["amount"] for s in sales if s.get("status") == "verified")
    last_date = max((s["date"] for s in sales if s.get("date")), default=None)
    return {
        "total_sales": len(sales),
        "total_revenue": data.get("total_revenue", 0),
        "verified_revenue": verified_revenue,
        "by_status": by_status,
        "last_sale_date": last_date,
    }


def update_sale_status(sale_id, new_status):
    data = load_sales()
    for s in data["sales"]:
        if s["id"] == sale_id:
            old_status = s.get("status")
            s["status"] = new_status
            if old_status != "rejected" and new_status == "rejected":
                data["total_revenue"] = max(0, data["total_revenue"] - s["amount"])
            elif old_status == "rejected" and new_status != "rejected":
                data["total_revenue"] += s["amount"]
            save_sales(data)
            return s
    return None


def sales_by_period(period="daily", status=None):
    data = load_sales()
    sales = data.get("sales", [])
    if status:
        sales = [s for s in sales if s.get("status") == status]
    buckets: dict[str, list] = {}
    for s in sales:
        try:
            dt = datetime.fromisoformat(s["date"])
        except (KeyError, ValueError, TypeError):
            continue
        if period == "daily":
            key = dt.strftime("%Y-%m-%d")
        elif period == "weekly":
            key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
        elif period == "monthly":
            key = dt.strftime("%Y-%m")
        else:
            key = dt.strftime("%Y-%m-%d")
        buckets.setdefault(key, []).append(s)
    result = []
    for key in sorted(buckets):
        bucket = buckets[key]
        revenue = sum(s["amount"] for s in bucket)
        verified = sum(s["amount"] for s in bucket if s.get("status") == "verified")
        result.append({
            "period": key,
            "count": len(bucket),
            "revenue": revenue,
            "verified_revenue": verified,
        })
    return result


def search_sales(query="", status=None, product=None):
    data = load_sales()
    results = data.get("sales", [])
    if query:
        q = query.lower()
        results = [
            s
            for s in results
            if q in s.get("product", "").lower()
            or q in s.get("buyer_email", "").lower()
            or q in s.get("transaction_id", "").lower()
        ]
    if status:
        results = [s for s in results if s.get("status") == status]
    if product:
        results = [s for s in results if s.get("product") == product]
    return results


def verify_sale(sale_id):
    return update_sale_status(sale_id, "verified")


def reject_sale(sale_id):
    return update_sale_status(sale_id, "rejected")


if __name__ == "__main__":
    print(PAYMENT_INFO)
    print("\nAvailable Products:")
    for p in list_products():
        print(f"  {p['id']}. {p['name']} - ${p['price']}")

    summary = get_sales_summary()
    print(f"\nTotal Sales: {summary['total_sales']}")
    print(f"Total Revenue: ${summary['total_revenue']}")
    print(f"Verified Revenue: ${summary['verified_revenue']}")
    if summary["by_status"]:
        print(f"By Status: {summary['by_status']}")
