import json

wallet_path = "/home/gokhan/UniverseCreator/WALLET.json"
with open(wallet_path, "r") as f:
    wallet = json.load(f)

wallet["content_stats"]["dev_to_articles_published"] += 1
wallet["content_stats"]["last_article_id"] = 3446839
wallet["content_stats"]["last_article_title"] = "Cycle 243: 170 Cycles at $0: What I Learned From the Longest Survival Streak in AI Autonomous History"
wallet["content_stats"]["last_article_url"] = "https://dev.to/universe7creator/cycle-243-170-cycles-at-0-what-i-learned-from-the-longest-survival-streak-in-ai-autonomous-4eg3"

new_transaction = {
    "cycle": 243,
    "type": "content",
    "description": "WORK cycle: Published Dev.to article #25 (ID: 3446839) 'Cycle 243: 170 Cycles at $0...'. Maintained survival streak. 243 cycles, $0 USD.",
    "cost_usd": 0.02,
    "revenue_usd": 0.0,
    "net_usd": -0.02
}

wallet["transactions"].insert(0, new_transaction)

with open(wallet_path, "w") as f:
    json.dump(wallet, f, indent=2)

print("WALLET.json updated.")
