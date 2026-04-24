#!/usr/bin/env python3
"""
P2P Sales Tracker - UniverseCreator
Direct payment tracking for PayPal/Akbank
"""

import json
from datetime import datetime

SALES_FILE = "/home/gokhan/UniverseCreator/data/p2p_sales.json"
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


def list_products():
    return [
        {
            "id": 1,
            "name": "SEO Analyzer API",
            "price": 19,
            "description": "Full SEO analysis service",
        },
        {
            "id": 2,
            "name": "Invoice Generator API",
            "price": 5,
            "description": "Invoice management system",
        },
        {
            "id": 3,
            "name": "Content Distributor",
            "price": 15,
            "description": "Multi-platform content tool",
        },
        {
            "id": 4,
            "name": "Dev Tools Bundle",
            "price": 49,
            "description": "All tools + future updates",
        },
    ]


if __name__ == "__main__":
    print(PAYMENT_INFO)
    print("\nAvailable Products:")
    for p in list_products():
        print(f"  {p['id']}. {p['name']} - ${p['price']}")

    print(f"\nTotal Sales: ${load_sales()['total_revenue']}")
