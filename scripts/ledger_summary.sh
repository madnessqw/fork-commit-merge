#!/bin/bash
# Run Ledger özeti — son N kayıt
N=${1:-20}
LEDGER="/home/gokhan/UniverseCreator/logs/run_ledger.jsonl"

if [ ! -f "$LEDGER" ]; then
    echo "Run ledger yok: $LEDGER"
    exit 1
fi

echo "=== Son $N Run ==="
tail -n "$N" "$LEDGER" | python3 -c "
import json, sys
from collections import Counter
lines = [json.loads(l) for l in sys.stdin if l.strip()]
modes = Counter(l.get('mode') for l in lines)
statuses = Counter(l.get('status') for l in lines)
total_cost = sum(l.get('cost_est', 0) for l in lines)
print(f'Toplam: {len(lines)} run')
print(f'Modlar: {dict(modes)}')
print(f'Durumlar: {dict(statuses)}')
print(f'Tahmini maliyet: \${total_cost:.3f}')
if lines:
    last = lines[-1]
    print(f'Son run: {last.get(\"run_id\")} — {last.get(\"mode\")} — {last.get(\"status\")}')
"
