#!/usr/bin/env python3
"""
P2P Sales Tracker - UniverseCreator
Direct payment tracking for PayPal/Akbank
"""

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SALES_FILE = str(ROOT / "data" / "p2p_sales.json")
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


def load_sales():
    try:
        with open(SALES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"sales": [], "total_revenue": 0}


def save_sales(data):
    with open(SALES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_sale(product, amount, buyer_email, transaction_id):
    data = load_sales()
    sale = {
        "id": len(data["sales"]) + 1,
        "product": product,
        "amount": amount,
        "buyer_email": buyer_email,
        "transaction_id": transaction_id,
        "date": datetime.now().isoformat(),
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


if __name__ == "__main__":
    print(PAYMENT_INFO)
    print("\nAvailable Products:")
    for p in list_products():
        print(f"  {p['id']}. {p['name']} - ${p['price']}")

    print(f"\nTotal Sales: ${load_sales()['total_revenue']}")
