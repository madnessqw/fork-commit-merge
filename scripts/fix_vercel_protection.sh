#!/usr/bin/env bash
# fix_vercel_protection.sh
# Vercel SSO/Deployment Protection'ı API ile otomatik kapatır.
# Kullanım:
#   ./fix_vercel_protection.sh           → tüm projeleri düzelt
#   ./fix_vercel_protection.sh --all     → tüm projeleri düzelt
#   ./fix_vercel_protection.sh <slug>    → tek projeyi düzelt

VERCEL_TOKEN="${VERCEL_TOKEN:-vcp_258G92BEBEcaDuAoOgCVMLWsW5ifjcMefXGbWFBMGIbUmlLbH72uKAbg}"
TEAM_ID="team_dvJDRExvJITRGWh3cWs5L44m"
LOG="/home/gokhan/UniverseCreator/logs/vercel_protection_fix.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"; }

disable_protection() {
  local slug="$1"
  local result
  result=$(curl -s -X PATCH \
    -H "Authorization: Bearer $VERCEL_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"ssoProtection": null}' \
    "https://api.vercel.com/v9/projects/${slug}?teamId=${TEAM_ID}")

  local sso_after
  sso_after=$(echo "$result" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('ssoProtection','null'))" 2>/dev/null)
  local err
  err=$(echo "$result" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error',{}).get('message',''))" 2>/dev/null)

  if [ -n "$err" ] && [ "$err" != "None" ] && [ "$err" != "{}" ]; then
    log "  ❌ $slug — ERROR: $err"
    return 1
  else
    log "  ✅ $slug — ssoProtection: $sso_after"
    return 0
  fi
}

fix_all() {
  log "=== Tüm projelerin ssoProtection kapatılıyor ==="
  local page_size=100
  local fixed=0
  local failed=0
  local skipped=0

  local projects_json
  projects_json=$(curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
    "https://api.vercel.com/v9/projects?teamId=${TEAM_ID}&limit=${page_size}")

  local total
  total=$(echo "$projects_json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('projects',[])))" 2>/dev/null)
  log "Toplam proje: $total"

  while IFS= read -r slug; do
    [ -z "$slug" ] && continue
    disable_protection "$slug" && ((fixed++)) || ((failed++))
    sleep 0.2  # rate limit koruması
  done < <(echo "$projects_json" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d.get('projects',[]):
    if p.get('ssoProtection'):
        print(p['name'])
" 2>/dev/null)

  log "=== SONUÇ: $fixed düzeltildi, $failed başarısız ==="
}

fix_single() {
  local slug="$1"
  log "=== $slug için ssoProtection kapatılıyor ==="
  disable_protection "$slug"
}

mkdir -p "$(dirname "$LOG")"

if [ $# -eq 0 ] || [ "$1" = "--all" ]; then
  fix_all
else
  fix_single "$1"
fi
