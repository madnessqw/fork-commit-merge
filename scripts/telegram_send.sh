#!/usr/bin/env bash
# telegram_send.sh — Tüm agent'lar için ortak Telegram mesaj scripti
# Kullanım:
#   echo "mesaj" | ./scripts/telegram_send.sh
#   ./scripts/telegram_send.sh --msg "tek satır mesaj"
#   ./scripts/telegram_send.sh --help-request "AGENT_ADI" "sorun açıklaması"
#
# Credentials: /home/gokhan/UniverseCreator/config/telegram.json (env override yok)

set -euo pipefail

WORK_DIR="/home/gokhan/UniverseCreator"
CONFIG="$WORK_DIR/config/telegram.json"

TOKEN=$(python3 -c "import json; d=json.load(open('$CONFIG')); print(d['bot_token'])" 2>/dev/null || echo "")
CHAT=$(python3 -c "import json; d=json.load(open('$CONFIG')); print(d['chat_id'])" 2>/dev/null || echo "")

if [ -z "$TOKEN" ] || [ -z "$CHAT" ]; then
    echo "[telegram_send] ERROR: config/telegram.json okunamadı" >&2
    exit 1
fi

send_msg() {
    local TEXT="$1"
    curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
        -d "chat_id=${CHAT}" \
        -d "parse_mode=HTML" \
        --data-urlencode "text=${TEXT}" \
        -o /dev/null -w "%{http_code}"
}

# --help-request modu: ajan bir şeye ihtiyaç duyduğunda
if [ "${1:-}" = "--help-request" ]; then
    AGENT="${2:-UNKNOWN}"
    SORUN="${3:-Belirtilmedi}"
    MSG="⚠️ <b>MANUEL KARAR GEREKLİ</b>

🤖 Agent: <b>${AGENT}</b>
🕐 $(date '+%Y-%m-%d %H:%M UTC+3')

❓ Sorun:
${SORUN}

Lütfen bu mesaja yanıt ver veya gereken adımı at. Agent bekleyecek."
    CODE=$(send_msg "$MSG")
    [ "$CODE" = "200" ] && echo "OK" || echo "FAIL: HTTP $CODE"
    exit 0
fi

# --msg modu: tek satır mesaj
if [ "${1:-}" = "--msg" ]; then
    CODE=$(send_msg "${2:-}")
    [ "$CODE" = "200" ] && echo "OK" || echo "FAIL: HTTP $CODE"
    exit 0
fi

# stdin modu: pipe ile mesaj
if [ ! -t 0 ]; then
    TEXT=$(cat)
    CODE=$(send_msg "$TEXT")
    [ "$CODE" = "200" ] && echo "OK" || echo "FAIL: HTTP $CODE"
    exit 0
fi

echo "Kullanım: echo 'mesaj' | $0  VEYA  $0 --msg 'mesaj'  VEYA  $0 --help-request 'AGENT' 'sorun'" >&2
exit 1
