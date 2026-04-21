#!/bin/bash
# check_evolution.sh — Capability Gap Tarayıcı ve Otomatik Çözücü
# Version: 1.0 | Owner: toolsmith
# Kullanım: bash /home/gokhan/UniverseCreator/scripts/check_evolution.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(dirname "$SCRIPT_DIR")"
CAPS="$WORKSPACE/config/capabilities.json"
LOG="$WORKSPACE/logs/evolution_report.txt"
SETTINGS="/home/gokhan/.claude/settings.json"
NPM_ROOT="/home/gokhan/.npm-global/lib/node_modules"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }
section() { echo "" | tee -a "$LOG"; echo "═══════════════════════════════════════" | tee -a "$LOG"; echo "  $*" | tee -a "$LOG"; echo "═══════════════════════════════════════" | tee -a "$LOG"; }

mkdir -p "$(dirname "$LOG")"
echo "# Evolution Check Report — $(date '+%Y-%m-%d %H:%M:%S')" > "$LOG"

# ──────────────────────────────────────────────
section "1. CAPABILITIES.JSON DURUM"
# ──────────────────────────────────────────────

if [ ! -f "$CAPS" ]; then
    log "HATA: $CAPS bulunamadı!"
    exit 1
fi

python3 - <<'EOF' | tee -a "$LOG"
import json, sys

caps = json.load(open('/home/gokhan/UniverseCreator/config/capabilities.json'))
print(f"  Version : {caps.get('version', '?')}")
print(f"  Cycle   : {caps.get('cycle', '?')}")
print(f"  Updated : {caps.get('last_updated', '?')[:19]}")

gaps = caps.get('gaps', [])
pending = [g for g in gaps if g.get('status') == 'pending']
blocked = [g for g in gaps if g.get('status') == 'blocked']
healthy = [g for g in gaps if g.get('status') in ('healthy', 'resolved')]

print(f"\n  Gaps    : {len(gaps)} toplam")
print(f"  Pending : {len(pending)}")
print(f"  Blocked : {len(blocked)}")
print(f"  Çözüldü : {len(healthy)}")

if pending:
    print("\n  [PENDING GAPS]")
    for g in pending:
        print(f"    - {g['id']} : {g.get('note', '-')[:80]}")

if blocked:
    print("\n  [BLOCKED GAPS]")
    for g in blocked:
        print(f"    - {g['id']} : {g.get('note', '-')[:80]}")
EOF

# ──────────────────────────────────────────────
section "2. MCP SUNUCU SAĞLIK KONTROLÜ"
# ──────────────────────────────────────────────

python3 - <<'EOF' | tee -a "$LOG"
import json, os, subprocess

settings = json.load(open('/home/gokhan/.claude/settings.json'))
mcps = settings.get('mcpServers', {})

print(f"  Kayıtlı MCP: {len(mcps)}")
for name, cfg in mcps.items():
    cmd = cfg.get('command', '')
    args = cfg.get('args', [])
    # Binary varlık kontrolü
    if cmd in ('node', 'uv', 'python3', 'python'):
        binary = args[0] if args else ''
        exists = os.path.exists(binary) if binary and not binary.startswith('-') else True
        status = "✓" if exists else "✗ PATH YOK"
    else:
        exists = os.path.exists(cmd)
        status = "✓" if exists else "✗ BINARY YOK"
    print(f"  [{status}] {name}")
EOF

# ──────────────────────────────────────────────
section "3. NPM'DE HAZIR MCP'LER (KAYITLI DEĞİL)"
# ──────────────────────────────────────────────

log "npm global'de kurulu ama settings.json'a eklenmemiş MCP'ler:"

python3 - <<'EOF' | tee -a "$LOG"
import json, os

npm_root = '/home/gokhan/.npm-global/lib/node_modules'
settings = json.load(open('/home/gokhan/.claude/settings.json'))
registered_cmds = set()
for v in settings.get('mcpServers', {}).values():
    if v.get('args'):
        registered_cmds.update(v['args'])

mcp_packages = {
    'duckduckgo-mcp-server': 'dist/index.js',
    'one-search-mcp':        'dist/index.js',
    'webclaw-mcp':           'dist/index.js',
    'arxiv-query-mcp':       'dist/index.js',
    'mcporter':              'dist/index.js',
}

unregistered = []
for pkg, entry in mcp_packages.items():
    path = os.path.join(npm_root, pkg, entry)
    if os.path.exists(path) and path not in registered_cmds:
        unregistered.append((pkg, path))

if unregistered:
    for pkg, path in unregistered:
        print(f"  [HAZIR-KAYITSIZ] {pkg}")
        print(f"    Eklemek için:")
        print(f'    "command": "node", "args": ["{path}"]')
else:
    print("  Tüm kurulu MCP'ler settings.json'da kayıtlı.")
EOF

# ──────────────────────────────────────────────
section "4. OTOMATİK GAP ÇÖZÜMLEME (DENEME)"
# ──────────────────────────────────────────────

# Bilinen basit çözümler için auto-resolve dene
python3 - <<'PYEOF' | tee -a "$LOG"
import json, os
from datetime import datetime, timezone

caps_path = '/home/gokhan/UniverseCreator/config/capabilities.json'
caps = json.load(open(caps_path))
gaps = caps.get('gaps', [])
now_iso = datetime.now(timezone.utc).isoformat()
resolved = []

# Bilinen auto-resolvable gaps
auto_resolutions = {
    'capability-loop': {
        'note': 'Evolution loop integrated into FACTORY.md and EVOLUTION.md skills',
        'condition': lambda: os.path.exists('/home/gokhan/UniverseCreator/skills/EVOLUTION.md')
    }
}

for i, gap in enumerate(gaps):
    gid = gap.get('id', '')
    if gap.get('status') == 'pending' and gid in auto_resolutions:
        res = auto_resolutions[gid]
        if res['condition']():
            gaps[i] = {**gap, 'status': 'healthy', 'note': res['note'], 'resolved_at': now_iso}
            resolved.append(gid)
            print(f"  [AUTO-RESOLVED] {gid}")
        else:
            print(f"  [KOŞUL KARŞILANMADI] {gid} — atlanıyor")

if resolved:
    caps['gaps'] = gaps
    caps['last_updated'] = now_iso
    with open(caps_path, 'w') as f:
        json.dump(caps, f, indent=2)
    print(f"  {len(resolved)} gap otomatik çözüldü ve kaydedildi.")
else:
    print("  Otomatik çözülecek gap yok.")
PYEOF

# ──────────────────────────────────────────────
section "5. SKİLL DOSYASI DURUMU"
# ──────────────────────────────────────────────

SKILLS_DIR="$WORKSPACE/skills"
log "Skills dizini: $SKILLS_DIR"
skill_count=$(ls "$SKILLS_DIR"/*.md 2>/dev/null | wc -l)
log "Toplam skill dosyası: $skill_count"
ls "$SKILLS_DIR"/*.md 2>/dev/null | while read f; do
    fname=$(basename "$f")
    lines=$(wc -l < "$f")
    echo "  ✓ $fname ($lines satır)" | tee -a "$LOG"
done

# ──────────────────────────────────────────────
section "6. SCRIPT DURUMU"
# ──────────────────────────────────────────────

SCRIPTS_DIR="$WORKSPACE/scripts"
for s in "$SCRIPTS_DIR"/*.sh "$SCRIPTS_DIR"/*.py; do
    [ -f "$s" ] || continue
    fname=$(basename "$s")
    if [ -x "$s" ]; then
        echo "  [x] $fname (çalıştırılabilir)" | tee -a "$LOG"
    else
        echo "  [-] $fname (chmod +x eksik)" | tee -a "$LOG"
    fi
done

# ──────────────────────────────────────────────
section "7. SONUÇ ÖZETİ"
# ──────────────────────────────────────────────

python3 - <<'EOF' | tee -a "$LOG"
import json

caps = json.load(open('/home/gokhan/UniverseCreator/config/capabilities.json'))
gaps = caps.get('gaps', [])
pending = [g for g in gaps if g.get('status') == 'pending']
blocked = [g for g in gaps if g.get('status') == 'blocked']

healthy_mcps = sum(1 for v in caps.get('mcp_servers', {}).values() if v.get('status') == 'healthy')
total_mcps   = len(caps.get('mcp_servers', {}))
total_skills = len(caps.get('skills', {}))

print(f"  MCP Sunucuları  : {healthy_mcps}/{total_mcps} healthy")
print(f"  Skill Dosyaları : {total_skills} kayıtlı")
print(f"  Pending Gaps    : {len(pending)}")
print(f"  Blocked Gaps    : {len(blocked)}")

if not pending and not blocked:
    print("\n  ✅ Sistem SAĞLIKLI — Aktif gap yok.")
else:
    print("\n  ⚠️  Çözülmesi gereken gap'ler mevcut.")
    print("  → EVOLUTION.md'yi oku ve toolsmith prosedürünü uygula.")
EOF

log "Rapor tamamlandı: $LOG"
echo ""
echo "Tam rapor: $LOG"
