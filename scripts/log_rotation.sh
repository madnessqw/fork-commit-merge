#!/bin/bash
MAX_SIZE=$((10 * 1024 * 1024))
KEEP=3

for log in logs/codex_loop.log logs/structured.jsonl logs/glm_loop.log; do
    [ ! -f "$log" ] && continue
    size=$(stat -c%s "$log" 2>/dev/null || echo 0)
    if [ "$size" -gt "$MAX_SIZE" ]; then
        ts=$(date +%Y%m%d%H%M%S)
        mv "$log" "${log}.${ts}.old"
        gzip "${log}.${ts}.old" &
        touch "$log"
        count=$(ls -1 "${log}."*.old.gz 2>/dev/null | wc -l)
        if [ "$count" -gt "$KEEP" ]; then
            ls -1t "${log}."*.old.gz | tail -n +$((KEEP + 1)) | xargs rm -f
        fi
        echo "Rotated: $log (${ts})"
    fi
done
wait
