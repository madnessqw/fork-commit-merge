#!/usr/bin/env bash
# Codex Research Loop — UniverseCodex tmux session
# codex exec (non-interactive) kullanır — her cycle fresh context + MCPs
# Cron: */35 * * * * /home/gokhan/UniverseCreator/scripts/codex_loop.sh >> /home/gokhan/UniverseCreator/logs/codex_loop.log 2>&1

set -euo pipefail

WORK_DIR="/home/gokhan/UniverseCreator"
PROMPT_FILE="$WORK_DIR/prompts/codex_prompt.txt"
LOCK_FILE="/tmp/codex_loop.lock"
RUNNING_FLAG="/tmp/codex_research_running.flag"
LOG_FILE="$WORK_DIR/logs/codex_loop.log"
SESSION="UniverseCodex"
CODEX_BIN="/home/gokhan/.local/bin/codex"
RUN_SCRIPT="/tmp/codex_run.sh"
COUNTER_FILE="$WORK_DIR/sistem-planlama/counter.txt"

mkdir -p "$(dirname "$LOG_FILE")" "$WORK_DIR/sistem-planlama" "$WORK_DIR/analysis"

# Singleton — önceki çalışma devam ediyorsa atla
exec 9>"$LOCK_FILE"
flock -n 9 || { echo "[CODEX $(date '+%Y-%m-%d %H:%M:%S')] Already running, skipping."; exit 0; }

log() { echo "[CODEX $(date '+%Y-%m-%d %H:%M:%S')] $*"; }

log "=== Codex Cycle START ==="

# Önceki araştırma hâlâ devam ediyorsa skip
if [[ -f "$RUNNING_FLAG" ]]; then
    FLAG_AGE=$(( $(date +%s) - $(stat -c %Y "$RUNNING_FLAG" 2>/dev/null || echo 0) ))
    if (( FLAG_AGE < 3600 )); then
        log "Önceki araştırma hâlâ devam ediyor (${FLAG_AGE}s geçti) — skip."
        exit 0
    else
        log "UYARI: Flag dosyası 1 saatten eski, süresi dolmuş sayılıyor — temizleniyor."
        rm -f "$RUNNING_FLAG"
    fi
fi

[[ -f "$PROMPT_FILE" ]] || { log "ERROR: Prompt file missing: $PROMPT_FILE"; exit 1; }

# Counter durumu
if [[ -f "$COUNTER_FILE" ]]; then
    N=$(cat "$COUNTER_FILE")
    log "Counter: $N (arastirma${N}.md hedef)"
else
    log "INFO: counter.txt yok — ilk çalışma"
    N=0
fi

# Tmux session yoksa oluştur (fresh start = MCPler aktif olur)
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux new-session -d -s "$SESSION" -x 220 -y 50
    log "Created tmux session $SESSION (fresh — MCPs will load)"
    sleep 2
fi

# Temp script — prompt içeriği komut satırına girmez, quoting sorunu yok
cat > "$RUN_SCRIPT" << 'RUNEOF'
#!/usr/bin/env bash
set -euo pipefail
WORK_DIR="/home/gokhan/UniverseCreator"
LOG_FILE="$WORK_DIR/logs/codex_loop.log"
CODEX_BIN="/home/gokhan/.local/bin/codex"
CMA_BIN="$HOME/bin/cma"
RUNNING_FLAG="/tmp/codex_research_running.flag"

run_codex() {
    local account="$1"
    CMA_DISABLE_KEYRING=1 "$CMA_BIN" activate "$account" 2>&1 | tee -a "$LOG_FILE"
    sleep 1
    local output
    output=$("$CODEX_BIN" exec \
        --config "approval_policy=never" \
        --config "sandbox_mode=danger-full-access" \
        "$PROMPT_CONTENT" 2>&1)
    echo "$output" | tee -a "$LOG_FILE"
    if echo "$output" | grep -qE "usage limit|high demand|Reconnecting"; then
        return 1
    fi
    return 0
}

# Running flag koy — başka cycle bizi geçemesin
touch "$RUNNING_FLAG"
trap 'rm -f "$RUNNING_FLAG"; echo "[CODEX] Flag temizlendi." | tee -a "$LOG_FILE"' EXIT

cd "$WORK_DIR"
python3 scripts/update_summary.py | tee -a "$LOG_FILE"
python3 scripts/refresh_codex_context.py | tee -a "$LOG_FILE"
PROMPT_CONTENT=$(cat prompts/codex_prompt.txt)

echo "--- codex exec START $(date '+%Y-%m-%d %H:%M:%S') ---" | tee -a "$LOG_FILE"

# Hesap 1 dene, limit/hata alırsa hesap 2'ye geç
if ! run_codex 1; then
    echo "[CODEX] hesap1 başarısız (usage limit / high demand) — hesap2 deneniyor..." | tee -a "$LOG_FILE"
    if ! run_codex 2; then
        echo "[CODEX] Her iki hesap da başarısız — bir sonraki cycle'a ertelendi." | tee -a "$LOG_FILE"
        EXIT_CODE=1
    else
        EXIT_CODE=0
    fi
else
    EXIT_CODE=0
fi

echo "--- codex exec END $(date '+%Y-%m-%d %H:%M:%S') exit=$EXIT_CODE ---" | tee -a "$LOG_FILE"
RUNEOF
chmod +x "$RUN_SCRIPT"

tmux send-keys -t "${SESSION}:0" "bash $RUN_SCRIPT" Enter

log "Dispatched: bash $RUN_SCRIPT → tmux $SESSION:0"
log "Counter: $N | Monitor: tmux attach -t $SESSION | Logs: $LOG_FILE"
log "=== Codex Cycle END ==="
