#!/usr/bin/env bash
# GLM Analyst Loop — UniverseGLM tmux session
# opencode run (permission.allow ile yolo mode) kullanır — her cycle fresh context
# Cron: */20 * * * * /home/gokhan/UniverseCreator/scripts/glm_loop.sh >> /home/gokhan/UniverseCreator/logs/glm_loop.log 2>&1

set -euo pipefail

WORK_DIR="/home/gokhan/UniverseCreator"
PROMPT_FILE="$WORK_DIR/prompts/glm_prompt.txt"
LOCK_FILE="/tmp/glm_loop.lock"
LOG_FILE="$WORK_DIR/logs/glm_loop.log"
SESSION="UniverseGLM"
OPENCODE_BIN="/home/gokhan/.opencode/bin/opencode"
RUN_SCRIPT="/tmp/glm_run.sh"
ONERI_FILE="$WORK_DIR/analysis/oneri.md"

mkdir -p "$(dirname "$LOG_FILE")" "$WORK_DIR/analysis"

# Singleton — önceki çalışma devam ediyorsa atla
exec 9>"$LOCK_FILE"
flock -n 9 || { echo "[GLM $(date '+%Y-%m-%d %H:%M:%S')] Already running, skipping."; exit 0; }

# log() sadece stdout'a yazar — cron redirect'i log dosyasına yönlendirir (no duplicates)
log() { echo "[GLM $(date '+%Y-%m-%d %H:%M:%S')] $*"; }

log "=== GLM Cycle START ==="

[[ -f "$PROMPT_FILE" ]] || { log "ERROR: Prompt file missing: $PROMPT_FILE"; exit 1; }

# oneri.md yaşı kontrolü
if [[ -f "$ONERI_FILE" ]]; then
    AGE=$(( $(date +%s) - $(stat -c %Y "$ONERI_FILE") ))
    log "Last oneri.md: $(( AGE / 60 ))min ago"
    [[ $(( AGE / 60 )) -gt 25 ]] && log "WARNING: oneri.md stale (>25min) — previous run may have failed"
else
    log "INFO: oneri.md does not exist yet (first run)"
fi

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
        log "Killing stale pane child PID $CPID ($(ps -p $CPID -o cmd --no-headers 2>/dev/null || echo unknown))"
        kill -9 "$CPID" 2>/dev/null || true
    done
    [[ -n "$CHILDREN" ]] && sleep 2
fi

# Temp script — quoting sorununu tamamen çözer, prompt içeriği komut satırına hiç girmez
cat > "$RUN_SCRIPT" << 'RUNEOF'
#!/usr/bin/env bash
set -euo pipefail
WORK_DIR="/home/gokhan/UniverseCreator"
LOG_FILE="$WORK_DIR/logs/glm_loop.log"
OPENCODE_BIN="/home/gokhan/.opencode/bin/opencode"

cd "$WORK_DIR"
PROMPT_CONTENT=$(cat prompts/glm_prompt.txt)

echo "--- opencode run START $(date '+%Y-%m-%d %H:%M:%S') ---" | tee -a "$LOG_FILE"
set +e
"$OPENCODE_BIN" run --model zai-coding-plan/glm-5.1 "$PROMPT_CONTENT" 2>&1 | tee -a "$LOG_FILE"
GLM_EXIT=${PIPESTATUS[0]}
set -e
echo "--- opencode run END $(date '+%Y-%m-%d %H:%M:%S') exit=$GLM_EXIT ---" | tee -a "$LOG_FILE"

# ─── Shell-level Telegram (ZORUNLU — LLM atlasa da tetiklenir) ──────────
ONERI_HEAD=$(head -15 "$WORK_DIR/analysis/oneri.md" 2>/dev/null | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g' | cut -c1-300 || echo "(oneri.md yok)")
EXIT_TAG=""
[[ "$GLM_EXIT" != "0" ]] && EXIT_TAG=" ❌exit=$GLM_EXIT"
printf '🔍 <b>GLM Cycle Bitti</b>%s\n🕐 %s\n\n%s' \
    "$EXIT_TAG" "$(date '+%d.%m %H:%M')" "$ONERI_HEAD" \
    | "$WORK_DIR/scripts/telegram_send.sh" || true
# ─────────────────────────────────────────────────────────────────────────
RUNEOF
chmod +x "$RUN_SCRIPT"

tmux send-keys -t "${SESSION}:0" "bash $RUN_SCRIPT" Enter

log "Dispatched: bash $RUN_SCRIPT → tmux $SESSION:0"
log "Monitor: tmux attach -t $SESSION | Logs: $LOG_FILE"
log "=== GLM Cycle END ==="
