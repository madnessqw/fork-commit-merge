import json

with open('WALLET.json', 'r') as f:
    wallet = json.load(f)

# Fix the last transaction
wallet['transactions'][0]['cost_usd'] = 0.0
wallet['transactions'][0]['net_usd'] = 0.0
wallet['balance'] = 0.0
wallet['mode'] = "EMERGENCY"

with open('WALLET.json', 'w') as f:
    json.dump(wallet, f, indent=2)
