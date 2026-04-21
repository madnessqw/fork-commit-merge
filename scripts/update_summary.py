#!/usr/bin/env python3
"""STATE.json'dan STATE_SUMMARY.json oluşturur (context tasarrufu için)"""
import json

with open('STATE.json') as f:
    state = json.load(f)

# Özet oluştur
summary = {
    "cycle": state.get("cycle"),
    "mode": state.get("mode"),
    "balance": state.get("balance"),
    "active_count": state.get("active_count"),
    "live_count": state.get("live_count"),
    "healthy_count": state.get("healthy_count"),
    "next_action": state.get("next_action"),
    "vercel_auth_issue": state.get("vercel_auth_issue"),
    "last_updated": state.get("last_updated"),
    "products": [
        {
            "n": p.get("name"),
            "s": p.get("slug"),
            "st": p.get("status"),
            "v": p.get("vercel_url"),
            "c": p.get("checkout_url")
        }
        for p in state.get("products", {}).get("active", [])
    ]
}

with open('STATE_SUMMARY.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f"STATE_SUMMARY.json updated: cycle {summary['cycle']}")
