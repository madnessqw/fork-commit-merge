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
AUTH_STATE_FILE="$WORK_DIR/.signals/codex_auth_state.json"
RUNNING_FLAG="/tmp/codex_research_running.flag"
AUTH_SWITCH_PATTERNS='usage limit|high demand|Reconnecting|429|rate limit'

run_codex() {
    local account="$1"
    local activate_output activate_exit
    set +e
    activate_output=$(CMA_DISABLE_KEYRING=1 "$CMA_BIN" activate "$account" 2>&1)
    activate_exit=$?
    set -e
    echo "$activate_output" | tee -a "$LOG_FILE"
    if (( activate_exit != 0 )); then
        LAST_RUN_ERROR="activate_exit=$activate_exit"
        LAST_RUN_KIND="activate_failed"
        return 3
    fi
    sleep 1
    local output
    local exit_code
    set +e
    output=$("$CODEX_BIN" exec \
        --config "approval_policy=never" \
        --config "sandbox_mode=danger-full-access" \
        "$PROMPT_CONTENT" 2>&1)
    exit_code=$?
    set -e
    echo "$output" | tee -a "$LOG_FILE"
    if echo "$output" | grep -qiE "$AUTH_SWITCH_PATTERNS"; then
        LAST_RUN_ERROR="$(echo "$output" | tail -3 | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g')"
        LAST_RUN_KIND="auth_switch"
        return 1
    fi
    if (( exit_code != 0 )); then
        LAST_RUN_ERROR="exit_code=$exit_code"
        LAST_RUN_KIND="exec_failed"
        return "$exit_code"
    fi
    LAST_RUN_ERROR=""
    LAST_RUN_KIND="success"
    return 0
}

# Running flag koy — başka cycle bizi geçemesin
touch "$RUNNING_FLAG"
trap 'rm -f "$RUNNING_FLAG"; echo "[CODEX] Flag temizlendi." | tee -a "$LOG_FILE"' EXIT

cd "$WORK_DIR"
python3 scripts/update_summary.py | tee -a "$LOG_FILE"
python3 scripts/refresh_codex_context.py | tee -a "$LOG_FILE"

# Polar OAT — config/polar.json'dan oku, varsa export et
if [[ -f "$WORK_DIR/config/polar.json" ]]; then
    POLAR_OAT_VAL=$(python3 -c "import json,sys; d=json.load(open('$WORK_DIR/config/polar.json')); print(d.get('polar_oat',''))" 2>/dev/null || true)
    if [[ -n "$POLAR_OAT_VAL" ]]; then
        export POLAR_OAT="$POLAR_OAT_VAL"
        echo "[CODEX] POLAR_OAT yüklendi (config/polar.json)" | tee -a "$LOG_FILE"
    fi
fi

PROMPT_CONTENT=$(cat prompts/codex_prompt.txt)

echo "--- codex exec START $(date '+%Y-%m-%d %H:%M:%S') ---" | tee -a "$LOG_FILE"

python3 "$WORK_DIR/scripts/codex_auth_manager.py" init --state-file "$AUTH_STATE_FILE" | tee -a "$LOG_FILE"

AUTH_INFO=$(python3 "$WORK_DIR/scripts/codex_auth_manager.py" choose --state-file "$AUTH_STATE_FILE" --format shell)
read -r PRIMARY_ACCOUNT FALLBACK_ACCOUNT <<< "$AUTH_INFO"
echo "[CODEX] Auth preference: first=$PRIMARY_ACCOUNT fallback=$FALLBACK_ACCOUNT state=$AUTH_STATE_FILE" | tee -a "$LOG_FILE"

if echo "$FALLBACK_ACCOUNT" | grep -q "BLOCKED"; then
    echo "[CODEX] SKIP: All accounts blocked — skipping codex exec this cycle." | tee -a "$LOG_FILE"
    python3 "$WORK_DIR/scripts/codex_auth_manager.py" record \
        --state-file "$AUTH_STATE_FILE" \
        --preferred-account "$PRIMARY_ACCOUNT" \
        --active-account "$PRIMARY_ACCOUNT" \
        --outcome "skipped_all_blocked" \
        --cycle "__CYCLE_N__" \
        --exit-code 0 \
        --last-error "Both accounts usage-limited" \
        --attempted-accounts "$PRIMARY_ACCOUNT" "$FALLBACK_ACCOUNT" \
        | tee -a "$LOG_FILE"
    rm -f "$RUNNING_FLAG"
    exit 0
fi

AUTH_ATTEMPTS=()
AUTH_OUTCOME="failure"
AUTH_ACTIVE_ACCOUNT="$PRIMARY_ACCOUNT"
AUTH_ERROR=""
EXIT_CODE=0

if run_codex "$PRIMARY_ACCOUNT"; then
    AUTH_ATTEMPTS=("$PRIMARY_ACCOUNT")
    AUTH_OUTCOME="success"
    AUTH_ACTIVE_ACCOUNT="$PRIMARY_ACCOUNT"
    EXIT_CODE=0
else
    PRIMARY_RC=$?
    AUTH_ATTEMPTS=("$PRIMARY_ACCOUNT")
    AUTH_ERROR="$LAST_RUN_ERROR"

    if (( PRIMARY_RC == 1 )); then
        echo "[CODEX] account $PRIMARY_ACCOUNT auth/limit issue — switching to $FALLBACK_ACCOUNT" | tee -a "$LOG_FILE"
        AUTH_ATTEMPTS=("$PRIMARY_ACCOUNT" "$FALLBACK_ACCOUNT")
        if run_codex "$FALLBACK_ACCOUNT"; then
            AUTH_OUTCOME="auth_switch_success"
            AUTH_ACTIVE_ACCOUNT="$FALLBACK_ACCOUNT"
            EXIT_CODE=0
            AUTH_ERROR="${AUTH_ERROR:-$LAST_RUN_ERROR}"
        else
            SECONDARY_RC=$?
            SECONDARY_ERROR="$LAST_RUN_ERROR"
            AUTH_OUTCOME="auth_switch_failure"
            AUTH_ACTIVE_ACCOUNT="$FALLBACK_ACCOUNT"
            AUTH_ERROR="${AUTH_ERROR:-$SECONDARY_ERROR}"
            AUTH_ERROR="$AUTH_ERROR | fallback=$SECONDARY_ERROR"
            if (( SECONDARY_RC == 1 )); then
                EXIT_CODE=1
                echo "[CODEX] both accounts hit auth/limit signals — next cycle will start from $FALLBACK_ACCOUNT" | tee -a "$LOG_FILE"
            else
                EXIT_CODE=$SECONDARY_RC
                echo "[CODEX] fallback account $FALLBACK_ACCOUNT failed with exit=$SECONDARY_RC — auth state still rotated" | tee -a "$LOG_FILE"
            fi
        fi
    else
        AUTH_OUTCOME="failure"
        AUTH_ACTIVE_ACCOUNT="$PRIMARY_ACCOUNT"
        EXIT_CODE=$PRIMARY_RC
        echo "[CODEX] account $PRIMARY_ACCOUNT failed without auth signature — no account switch" | tee -a "$LOG_FILE"
    fi
fi

python3 "$WORK_DIR/scripts/codex_auth_manager.py" record \
    --state-file "$AUTH_STATE_FILE" \
    --preferred-account "$PRIMARY_ACCOUNT" \
    --active-account "$AUTH_ACTIVE_ACCOUNT" \
    --outcome "$AUTH_OUTCOME" \
    --cycle "__CYCLE_N__" \
    --exit-code "$EXIT_CODE" \
    --last-error "$AUTH_ERROR" \
    --attempted-accounts "${AUTH_ATTEMPTS[@]}" \
    | tee -a "$LOG_FILE"

echo "--- codex exec END $(date '+%Y-%m-%d %H:%M:%S') exit=$EXIT_CODE ---" | tee -a "$LOG_FILE"

# ─── Shell-level Telegram (ZORUNLU — LLM atlasa da tetiklenir) ──────────
RESULT_HEAD=$(head -12 "$WORK_DIR/analysis/codex_result.md" 2>/dev/null | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g' | cut -c1-300 || echo "(codex_result.md yok)")
AUTH_TAG=""
[[ "$AUTH_OUTCOME" == auth_switch_success ]] && AUTH_TAG=" 🔁 hesap geçildi"
[[ "$AUTH_OUTCOME" == auth_switch_failure ]] && AUTH_TAG=" ⚠️ auth sorun"
[[ "$EXIT_CODE" != "0" ]] && AUTH_TAG="$AUTH_TAG ❌exit=$EXIT_CODE"
CYCLE_LABEL="__CYCLE_N__"
printf '🤖 <b>Codex Cycle %s Bitti</b>%s\n🕐 %s\n\n%s' \
    "$CYCLE_LABEL" "$AUTH_TAG" "$(date '+%d.%m %H:%M')" "$RESULT_HEAD" \
    | "$WORK_DIR/scripts/telegram_send.sh" || true
# ─────────────────────────────────────────────────────────────────────────
RUNEOF
# Inject real cycle counter (heredoc is single-quoted, $N not expanded at write time)
sed -i "s/__CYCLE_N__/${N}/g" "$RUN_SCRIPT"
chmod +x "$RUN_SCRIPT"

tmux send-keys -t "${SESSION}:0" "bash $RUN_SCRIPT" Enter

log "Dispatched: bash $RUN_SCRIPT → tmux $SESSION:0"
log "Counter: $N | Monitor: tmux attach -t $SESSION | Logs: $LOG_FILE"
log "=== Codex Cycle END ==="
