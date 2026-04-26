#!/usr/bin/env bash
# Kimi Loop — UniverseKimi tmux session
# kimi-k2.6 / OpenCode ile otonom sistem analizi
# Cron: */25 * * * * /home/gokhan/UniverseCreator/scripts/kimi_loop.sh >> /home/gokhan/UniverseCreator/logs/kimi_loop.log 2>&1

set -euo pipefail

WORK_DIR="/home/gokhan/UniverseCreator"
PROMPT_FILE="$WORK_DIR/prompts/kimi_prompt.txt"
LOCK_FILE="/tmp/kimi_loop.lock"
LOG_FILE="$WORK_DIR/logs/kimi_loop.log"
SESSION="UniverseKimi"
OPENCODE_BIN="/home/gokhan/.opencode/bin/opencode"
RUN_SCRIPT="/tmp/kimi_run.sh"

mkdir -p "$(dirname "$LOG_FILE")" "$WORK_DIR/analysis"

# Singleton — önceki çalışma devam ediyorsa atla
exec 9>"$LOCK_FILE"
flock -n 9 || { echo "[Kimi $(date '+%Y-%m-%d %H:%M:%S')] Already running, skipping."; exit 0; }

log() { echo "[Kimi $(date '+%Y-%m-%d %H:%M:%S')] $*"; }

log "=== Kimi Cycle START ==="

[[ -f "$PROMPT_FILE" ]] || { log "ERROR: Prompt file missing: $PROMPT_FILE"; exit 1; }

# Tmux session yoksa oluştur
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux new-session -d -s "$SESSION" -x 220 -y 50
    log "Created tmux session $SESSION"
fi

# Panede çalışan opencode TUI (veya başka süreç) varsa SIGKILL ile öldür
PANE_PID=$(tmux display-message -t "${SESSION}:0" -p "#{pane_pid}" 2>/dev/null || true)
if [[ -n "$PANE_PID" ]]; then
    CHILDREN=$(ps --ppid "$PANE_PID" --no-headers -o pid 2>/dev/null || true)
    for CPID in $CHILDREN; do
        log "Killing stale pane child PID $CPID"
        kill -9 "$CPID" 2>/dev/null || true
    done
    [[ -n "$CHILDREN" ]] && sleep 2
fi

# Temp script — prompt içeriği komut satırına hiç girmez
cat > "$RUN_SCRIPT" << 'RUNEOF'
#!/usr/bin/env bash
set -euo pipefail
WORK_DIR="/home/gokhan/UniverseCreator"
LOG_FILE="$WORK_DIR/logs/kimi_loop.log"
OPENCODE_BIN="/home/gokhan/.opencode/bin/opencode"

cd "$WORK_DIR"

# POLAR_OAT yükle (polar_checkout_sync.py için)
if [[ -f "$WORK_DIR/config/polar.json" ]]; then
    export POLAR_OAT=$(python3 -c "import json; print(json.load(open('$WORK_DIR/config/polar.json'))['polar_oat'])" 2>/dev/null || true)
fi

PROMPT_CONTENT=$(cat prompts/kimi_prompt.txt)

echo "--- kimi run START $(date '+%Y-%m-%d %H:%M:%S') ---" | tee -a "$LOG_FILE"

# Model: kimi-k2.6 via OpenCode Go
set +e
"$OPENCODE_BIN" run --model opencode-go/kimi-k2.6 --dir "$WORK_DIR" "$PROMPT_CONTENT" 2>&1 | tee -a "$LOG_FILE"
KIMI_EXIT=${PIPESTATUS[0]}
set -e

echo "--- kimi run END $(date '+%Y-%m-%d %H:%M:%S') exit=$KIMI_EXIT ---" | tee -a "$LOG_FILE"

# ─── Telegram Raporu (ZORUNLU) ─────────────────────────
KIMI_RAPOR=$(ls -t "$WORK_DIR"/analysis/kimi_rapor_*.md 2>/dev/null | head -1)
if [[ -n "$KIMI_RAPOR" && -f "$KIMI_RAPOR" ]]; then
    # İlk 15 satır + son 10 satır = özet
    HEAD=$(head -15 "$KIMI_RAPOR" | tr '\n' ' ' | cut -c1-200)
    TAIL=$(tail -10 "$KIMI_RAPOR" | grep -E "Sağlık|Tespit|Öneri" | head -3 | tr '\n' '|' | cut -c1-150)
    RAPOR_SUMMARY="${HEAD:0:150}... [${TAIL}"
else
    RAPOR_SUMMARY="Rapor dosyası bulunamadı"
fi

EXIT_TAG=""
[[ "$KIMI_EXIT" != "0" ]] && EXIT_TAG=" ❌exit=$KIMI_EXIT"
printf '🔬 <b>Kimi Cycle Bitti</b>%s\n🕐 %s\n\n📋 %s' \
    "$EXIT_TAG" "$(date '+%d.%m %H:%M')" "$RAPOR_SUMMARY" \
    | "$WORK_DIR/scripts/telegram_send.sh" || true
# ──────────────────────────────────────────────────────
RUNEOF
chmod +x "$RUN_SCRIPT"

tmux send-keys -t "${SESSION}:0" "bash $RUN_SCRIPT" Enter

log "Dispatched: bash $RUN_SCRIPT → tmux $SESSION:0"
log "Monitor: tmux attach -t $SESSION | Logs: $LOG_FILE"
log "=== Kimi Cycle END ==="
