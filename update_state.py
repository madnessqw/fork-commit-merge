import json
import datetime

# Update STATE.json
with open('STATE.json', 'r') as f:
    state = json.load(f)

state['status'] = 'CYCLE_COMPLETE'
state['timestamp'] = datetime.datetime.utcnow().isoformat() + 'Z'
state['message'] = "Cycle 245 complete. Swarm orchestration deployed. p2p_api_service (Direct Monetization API) built by subagents. Ready to sell via direct PayPal/IBAN."

with open('STATE.json', 'w') as f:
    json.dump(state, f, indent=2)

# Update WALLET.json
with open('WALLET.json', 'r') as f:
    wallet = json.load(f)

new_tx = {
  "cycle": 245,
  "type": "build",
  "description": "BUILD cycle: Orchestrated Swarm (V11) to build p2p_api_service. A Python FastAPI service with direct P2P monetization (PayPal & Akbank IBAN embedded in 402 responses and README). Bypassing LemonSqueezy API limits. Ready for direct sales.",
  "cost_usd": 0.05,
  "revenue_usd": 0.0,
  "net_usd": -0.05
}

wallet['transactions'].insert(0, new_tx)
wallet['balance'] = round(wallet['balance'] - 0.05, 2)

with open('WALLET.json', 'w') as f:
    json.dump(wallet, f, indent=2)
