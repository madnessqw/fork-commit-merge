#!/usr/bin/env python3
import json
import datetime

# Read current STATE
with open('STATE.json', 'r') as f:
    s = json.load(f)

# Update for Cycle 279
s['cycle'] = 279
s['timestamp'] = datetime.datetime.utcnow().isoformat() + '+00:00'
s['message'] = 'Cycle 279 - Deploying agents for emergency income generation'
s['next_priority'] = '1) Execute highest priority quick win, 2) Check PR statuses, 3) Deploy backup tasks'

# Update agent statuses
for agent in s['team']['agents']:
    if agent['name'] in ['planner', 'executor-2', 'quick-executor', 'researcher-3', 'bounty-finder']:
        agent['status'] = 'working'

# Add learning
s.setdefault('learnings', []).append('Cycle 279: Deploying agents for emergency income - 9 PRs pending ($170), 10 opportunities ready')

# Write back
with open('STATE.json', 'w') as f:
    json.dump(s, f, indent=2)

print('STATE.json updated for Cycle 279')
print(f'Cycle: {s["cycle"]}')
print(f'Balance: ${s["balance"]}')
print(f'Pending PRs: {len(s.get("pending_prs", []))}')
print(f'Active agents: {len([a for a in s["team"]["agents"] if a["status"] == "working"])}')
