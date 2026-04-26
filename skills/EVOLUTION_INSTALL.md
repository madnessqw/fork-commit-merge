# EVOLUTION INSTALL — MCP Kataloğu ve Kurulum Prosedürleri
**Sadece gap>0 ise oku.** Gap tespiti için: `cat skills/EVOLUTION_SCAN.md`

## BİLİNEN YARARLI MCP KATALOĞU

### ŞU AN KURULU (Hazır Kullan)

| MCP | Komut | Ne Yapar |
|-----|-------|----------|
| `council` | `/home/gokhan/projects/agents-council/dist/council mcp` | Multi-agent orchestration |
| `arxiv` | `uv tool run arxiv-mcp-server` | Akademik makale arama |
| `mcptube` | `/home/gokhan/projects/scrape/mcptube/venv/bin/mcptube serve --stdio` | YouTube analiz |

### NPM İLE YÜKLENMEYE HAZIR (Global Install Mevcut)

```bash
# Zaten yüklü, sadece settings.json'a ekle:
ls /home/gokhan/.npm-global/lib/node_modules/ | grep mcp
# → arxiv-query-mcp, duckduckgo-mcp-server, mcporter, one-search-mcp, webclaw-mcp
```

| Paket | Komut | Ne Yapar | Öncelik |
|-------|-------|----------|---------|
| `duckduckgo-mcp-server` | `node /home/gokhan/.npm-global/lib/node_modules/duckduckgo-mcp-server/dist/index.js` | Ücretsiz web araması | YÜKSEK |
| `one-search-mcp` | `node /home/gokhan/.npm-global/lib/node_modules/one-search-mcp/dist/index.js` | Birleşik arama | YÜKSEK |
| `webclaw-mcp` | `node /home/gokhan/.npm-global/lib/node_modules/webclaw-mcp/dist/index.js` | Web scraping | ORTA |
| `arxiv-query-mcp` | `node /home/gokhan/.npm-global/lib/node_modules/arxiv-query-mcp/dist/index.js` | Arxiv alternatifi | DÜŞÜK |
| `mcporter` | `node /home/gokhan/.npm-global/lib/node_modules/mcporter/dist/index.js` | MCP management | ORTA |

### YENİ KURULACAK MCP'LER (Öncelik Sırasıyla)

#### Web Arama (Kritik — Araştırma için gerekli)
```bash
# Brave Search MCP (API key gerekir: https://api.search.brave.com)
npm install -g @modelcontextprotocol/server-brave-search

# Exa Search (API key: https://exa.ai)
npm install -g exa-mcp-server

# Tavily (API key: https://tavily.com)
npm install -g tavily-mcp
```

#### Tarayıcı Otomasyonu (Yüksek Değer)
```bash
# Playwright MCP — headless browser, screenshot, form doldurma
npm install -g @executeautomation/playwright-mcp-server
# VEYA (resmi):
npm install -g @playwright/mcp

# Puppeteer MCP
npm install -g @modelcontextprotocol/server-puppeteer
```

#### GitHub Entegrasyonu
```bash
# GitHub MCP — repo okuma, issue/PR yönetimi
npm install -g @modelcontextprotocol/server-github
# ENV: GITHUB_PERSONAL_ACCESS_TOKEN gerekir
```

#### Dosya ve Sistem
```bash
# Filesystem MCP — güvenli dosya erişimi
npm install -g @modelcontextprotocol/server-filesystem

# Memory/KV Store
npm install -g @modelcontextprotocol/server-memory
```

#### Veritabanı
```bash
# SQLite MCP
npm install -g @modelcontextprotocol/server-sqlite

# PostgreSQL MCP
npm install -g @modelcontextprotocol/server-postgres
```

#### Ödeme ve E-ticaret
```bash
# Stripe MCP (API key gerekir)
npm install -g @stripe/mcp
# ENV: STRIPE_SECRET_KEY
```

#### Analitik ve İzleme
```bash
# Sentry MCP
npm install -g @sentry/mcp-server
# ENV: SENTRY_AUTH_TOKEN, SENTRY_ORG

# Cloudflare Workers & Analytics
npm install -g @cloudflare/mcp-server-cloudflare
```

#### Üretkenlik
```bash
# Slack MCP
npm install -g @modelcontextprotocol/server-slack

# Notion MCP
npm install -g @notionhq/notion-mcp-server
```

---

## MCP KURULUM PROSEDÜRÜ

### Adım 1 — Paketi Kur

**npm ile:**
```bash
npm install -g <paket-adı>
# Verify:
ls /home/gokhan/.npm-global/lib/node_modules/<paket-adı>/
```

**pip ile:**
```bash
pip3 install <paket-adı>
# Verify:
pip3 show <paket-adı>
```

**uv ile:**
```bash
uv tool install <paket-adı>
uv tool list  # doğrula
```

**GitHub'dan (kaynak):**
```bash
git clone https://github.com/<org>/<repo> /home/gokhan/projects/<repo>
cd /home/gokhan/projects/<repo>
npm install && npm run build
# Sonra dist/ veya bin/ içindeki çalıştırılabiliri kullan
```

### Adım 2 — ~/.claude/settings.json'a Ekle

```bash
# Önce mevcut settings'i oku:
cat /home/gokhan/.claude/settings.json | python3 -m json.tool

# JSON'u düzenle — mcpServers bölümüne yeni giriş ekle:
python3 << 'EOF'
import json, sys
with open('/home/gokhan/.claude/settings.json', 'r') as f:
    cfg = json.load(f)

# Yeni MCP ekle:
cfg['mcpServers']['<mcp-adı>'] = {
    "command": "node",
    "args": ["/home/gokhan/.npm-global/lib/node_modules/<paket-adı>/dist/index.js"],
    "env": {
        "API_KEY": "<key-varsa>"
    }
}

with open('/home/gokhan/.claude/settings.json', 'w') as f:
    json.dump(cfg, f, indent=4, ensure_ascii=False)
print("OK: settings.json güncellendi")
EOF
```

**ENV gerektiren MCP için env bölümü şablonu:**
```json
"env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_...",
    "BRAVE_API_KEY": "BSA...",
    "STRIPE_SECRET_KEY": "sk_live_...",
    "SENTRY_AUTH_TOKEN": "sntrys_..."
}
```

> ⚠️ **API key yoksa:** `USER.md` veya `WALLET.json` kontrol et. Yoksa gap'i `"status": "blocked"` olarak işaretle ve note'a yaz.

### Adım 3 — Smoke Test

Her MCP kurulumundan sonra temel bir test çalıştır:

```bash
# MCP'nin çalıştırılabilir dosyasını doğrudan test et:
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  node /home/gokhan/.npm-global/lib/node_modules/<paket>/dist/index.js 2>/dev/null | \
  python3 -m json.tool | head -30

# Başarı: "tools" listesi dönmeli
# Başarısız: stderr'e hata yazıyor, kurulum başarısız
```

### Adım 4 — capabilities.json'u Güncelle

```python
import json
from datetime import datetime, timezone

path = '/home/gokhan/UniverseCreator/config/capabilities.json'
with open(path, 'r') as f:
    caps = json.load(f)

# Yeni MCP'yi mcp_servers'a ekle:
caps['mcp_servers']['<mcp-adı>'] = {
    "status": "healthy",
    "owner": "toolsmith",
    "installed": datetime.now(timezone.utc).strftime('%Y-%m-%d')
}

# Gap varsa kapat:
caps['gaps'] = [
    {**g, "status": "healthy", "resolved_at": datetime.now(timezone.utc).isoformat()}
    if g['id'] == '<gap-id>'
    else g
    for g in caps.get('gaps', [])
]

caps['last_updated'] = datetime.now(timezone.utc).isoformat()

with open(path, 'w') as f:
    json.dump(caps, f, indent=2)
print("capabilities.json güncellendi")
```

### Adım 5 — Restart Kaydet

```python
# restart_required listesine ekle (Claude Code yeniden başlatılana kadar eski config çalışır):
caps['restart_required'].append('<mcp-adı>')
```

---

## SKİLL YAZMA REHBERİ

Tekrar eden görevler için yeni `.md` skill dosyası yaz. Skill dosyaları Claude'a "bu görev nasıl yapılır" öğretir.

### Skill Dosyası Yapısı

```markdown
# <GÖREV ADI> SKILL — <Hangi agent kullanır>
**Version:** 1.0 | **Owner:** <agent-adı> | **Güven skoru:** Temel/Orta/Yüksek

## Amaç
[Bu skill ne zaman okunur, ne yapar]

## Ön Koşullar
- [Gerekli credentials, tools, configs]

## Adım Adım Prosedür

### Adım 1 — [İlk adım]
```bash
[Komut]
```

### Adım 2 — [İkinci adım]
...

## Doğrulama
[Nasıl test edilir, başarı kriterleri]

## Bilinen Hatalar
[Sık karşılaşılan sorunlar ve çözümleri]

## Cycle Güncellemeleri
[skill-writer tarafından doldurulur]
```

### Skill Dosyası Nereye Yazılır?

```
/home/gokhan/UniverseCreator/skills/<görev-adı>.md
```

Yazıldıktan sonra `capabilities.json` skills bölümüne ekle:
```json
"skills": {
    "<skill-adı>": {
        "status": "configured",
        "owner": "<agent>",
        "path": "/home/gokhan/UniverseCreator/skills/<dosya>.md"
    }
}
```

### İyi Skill Dosyası Kriterleri
- [ ] Sadece bu göreve odaklı (fazla kapsamlı olmayacak)
- [ ] Çalıştırılabilir bash komutları içeriyor (gerçek komutlar)
- [ ] Doğrulama/test bölümü var
- [ ] Bilinen hata ve çözümleri var
- [ ] Okuyunca ne yapacağını anlayabiliyorsun

---

## CAPABILITIES.JSON PROTOKOLÜ

**Dosya:** `/home/gokhan/UniverseCreator/config/capabilities.json`

### Zorunlu Alanlar

```json
{
  "version": "1.1",
  "last_updated": "<ISO timestamp>",
  "cycle": <mevcut cycle>,
  "mcp_servers": {
    "<ad>": { "status": "healthy|degraded|down", "owner": "<agent>", "installed": "<tarih>" }
  },
  "plugins": {
    "<ad>@<kaynak>": { "status": "enabled|disabled", "owner": "<agent>" }
  },
  "skills": {
    "<ad>": { "status": "available|configured|deprecated", "owner": "<agent>", "path": "<yol>" }
  },
  "scripts": {
    "<dosya.sh>": { "status": "working|broken" }
  },
  "gaps": [
    {
      "id": "<benzersiz-id>",
      "status": "pending|blocked|healthy|wont_fix",
      "owner": "<agent>",
      "note": "<açıklama>",
      "resolved_at": "<ISO timestamp veya null>"
    }
  ],
  "restart_required": [],
  "agent_capabilities": {
    "researcher": [],
    "builder": [],
    "optimizer": [],
    "toolsmith": []
  }
}
```

### Güncelleme Kuralları
1. Her yeni kurulum/değişiklik → `last_updated` güncelle
2. Gap çözüldüğünde → status `"healthy"`, `resolved_at` ekle
3. Yeni gap bulunduğunda → gaps listesine ekle, benzersiz id ver
4. Hiçbir zaman var olan healthy kaydı silme, sadece güncelle

---

## KENDİ KENDİNE ARAŞTIRMA METODOLOJİSİ

Yeni bir capability gerektiğinde araştırma sırası:

### 1. Önce Yerel Kontrol
```bash
# Zaten kurulu mu?
npm list -g --depth=0 2>/dev/null | grep -i "<araç>"
pip3 list 2>/dev/null | grep -i "<araç>"
uv tool list 2>/dev/null
ls /home/gokhan/.npm-global/lib/node_modules/ | grep -i "<araç>"

# settings.json'da var mı?
cat /home/gokhan/.claude/settings.json | grep -i "<araç>"
```

### 2. Web Araması (council MCP veya curl)
```bash
# Jina Reader ile web araması:
curl -s "https://r.jina.ai/https://www.google.com/search?q=mcp+server+<konu>+site:github.com" | head -100

# npm kayıt araması:
curl -s "https://registry.npmjs.org/-/v1/search?text=mcp+<konu>&size=10" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); [print(p['package']['name'], p['package']['description'][:80]) for p in d['objects']]"

# GitHub araması (gh CLI ile):
gh search repos "mcp server <konu>" --limit 5 --json fullName,description,stargazerCount | python3 -m json.tool
```

### 3. Bilinen Güvenilir MCP Kaynakları
- **Resmi:** https://github.com/modelcontextprotocol/servers
- **Topluluk:** https://github.com/punkpeye/awesome-mcp-servers
- **npm:** https://www.npmjs.com/search?q=%40modelcontextprotocol
- **PyPI:** https://pypi.org/search/?q=mcp+server

### 4. Bir MCP'yi Değerlendirme Kriterleri
Kurmadan önce kontrol et:
- [ ] Son commit ne zaman? (90 günden eski → riskli)
- [ ] Stars > 50 mi?
- [ ] README'de `npm install` veya `pip install` komutu var mı?
- [ ] ENV gereksinimleri karşılanabilir mi?
- [ ] TypeScript/Node.js mı Python mı? (Node.js tercih et, daha stabil)

---

## YENİ PLUGIN EKLEME PROSEDÜRÜ

Claude Code plugin'leri `~/.claude/settings.json`'daki `enabledPlugins` ile yönetilir.

### Marketplace'ten Plugin Yükleme
```python
import json

with open('/home/gokhan/.claude/settings.json', 'r') as f:
    cfg = json.load(f)

# Yeni plugin ekle:
cfg['enabledPlugins']['<plugin-adı>@<marketplace>'] = True

# Yeni marketplace ekle (gerekirse):
cfg['extraKnownMarketplaces']['<marketplace-adı>'] = {
    "source": {
        "source": "git",
        "url": "https://github.com/<org>/<repo>.git"
    }
}

with open('/home/gokhan/.claude/settings.json', 'w') as f:
    json.dump(cfg, f, indent=4, ensure_ascii=False)
```

---

## SCRIPT YAZMA REHBERİ

Otomasyon scriptleri `/home/gokhan/UniverseCreator/scripts/` altında tutulur.

### Script Şablonu
```bash
#!/bin/bash
# <Script Adı> — <Amaç>
# Version: 1.0 | Cycle: <N>
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(dirname "$SCRIPT_DIR")"
CAPS="$WORKSPACE/config/capabilities.json"
LOG="$WORKSPACE/logs/<script-adı>.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

log "Başladı"
# ... iş mantığı ...
log "Tamamlandı"
```

Yazıldıktan sonra:
```bash
chmod +x /home/gokhan/UniverseCreator/scripts/<script>.sh
```

Ve `capabilities.json`'a ekle:
```json
"scripts": {
    "<script>.sh": { "status": "working" }
}
```

---

## BÜTÜNLÜK KONTROLÜ — YENİ CAPABILITY EKLERKEN

Her yeni kurulumdan önce şu listeyi geç:

```
PRE-KURULUM:
[ ] capabilities.json'daki tüm sağlıklı MCP'ler hâlâ çalışıyor mu?
    → Kontrol: settings.json'daki path'ler mevcut mu?
[ ] Çakışan port/kaynak var mı? (MCP'ler stdio kullanır, çakışmaz)
[ ] ENV var ekleyeceksem güvenli mi? (secret, ortak yerde değil)

POST-KURULUM:
[ ] Smoke test geçti mi?
[ ] capabilities.json güncellendi mi?
[ ] gap varsa kapatıldı mı?
[ ] restart_required listesine eklendi mi?
[ ] Hangi agent kullanacak, biliyor mu? (agent_capabilities güncelle)
```

---

## HATA AYIKLAMA

### "MCP tool not found" Hatası
```bash
# 1. settings.json path'i kontrol et:
cat /home/gokhan/.claude/settings.json | python3 -c "import json,sys; cfg=json.load(sys.stdin); [print(k, v) for k,v in cfg['mcpServers'].items()]"

# 2. Binary'nin varlığını doğrula:
ls -la <path/to/mcp/binary>

# 3. Manuel test:
<mcp-command> <<< '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### "npm install" Başarısız
```bash
# npm cache temizle:
npm cache clean --force
# Tekrar dene global prefix ile:
npm install -g --prefix /home/gokhan/.npm-global <paket>
```

### "uv tool run" Başarısız
```bash
# uv tool'u yeniden kur:
uv tool uninstall <paket> 2>/dev/null; uv tool install <paket>
uv tool list
```

### capabilities.json Bozuldu
```bash
# Backup'tan geri yükle:
cp /home/gokhan/UniverseCreator/config/capabilities.json.bak \
   /home/gokhan/UniverseCreator/config/capabilities.json
# Veya validate et:
python3 -c "import json; json.load(open('/home/gokhan/UniverseCreator/config/capabilities.json')); print('VALID')"
```

---

## EVRIM DÖNGÜSÜ ÖZET AKIŞI

```
Her Cycle:
  0. projeler.txt tara  → [***]/[**] listele, yeni gap fikirleri al
  1. cat config/capabilities.json → gaps listesini bul
  2. pending gap var mı?
     HAYIR → HEARTBEAT_OK, başka işe geç
     EVET  → sınıflandır
  3. capability gap mı?
     HAYIR → doğru owner'a yönlendir (builder/researcher/etc.)
     EVET  → araştır
  4. Çözüm bulundu mu?
     HAYIR → gap'i "blocked" yap, note yaz
     EVET  → kur (npm/pip/uv/git clone)
  5. Smoke test:
     BAŞARISIZ → kurulumu sil, gap "blocked" yap
     BAŞARILI  → settings.json + capabilities.json güncelle
  6. restart_required kaydı üret
  7. issues/issues.jsonl'a kayıt yaz
  8. self_improvement_log.md güncelle
  9. TEAM-LEAD'E RAPOR → Teammate() ile bildir
```

---

## 📡 TEAM-LEAD'E RAPORLAMA PROTOKOLÜ

**Her MCP kurulumu, skill yazımı veya dosya değişikliği sonrası ZORUNLU:**

```javascript
Teammate({
  operation: "write",
  target_agent_id: "team-lead",
  value: JSON.stringify({
    type: "toolsmith_report",
    cycle: <mevcut cycle>,
    installed: ["<paket-adi-1>", "<paket-adi-2>"],          // kurduğun MCP'ler
    updated_files: [                                          // değiştirdiğin dosyalar
      "~/.claude/settings.json",
      "config/capabilities.json",
      "skills/EVOLUTION.md"
    ],
    usage_notes: {                                            // nasıl kullanılır
      "duckduckgo": "web araması için: /duckduckgo search <query>",
      "playwright": "browser automation: /playwright screenshot <url>"
    },
    agent_actions: [                                          // agent yönetim eylemleri
      "researcher yeniden spawn edildi",
      "stale builder durduruldu"
    ],
    gaps_resolved: ["<gap-id-1>"],                           // çözülen gap'ler
    new_gaps_found: ["<gap-id-2>"],                          // yeni bulunan gap'ler
    restart_required: true,                                   // Claude Code restart gerekiyor mu
    notes: "DuckDuckGo ve One-Search MCP kuruldu. İkisi de web araması için kullanılabilir."
  })
})
```

**Ne zaman rapor gönderilmez:**
- Gap yoksa ve hiçbir şey değişmediyse → `HEARTBEAT_OK` yeter

---

## 🤖 AGENT YÖNETİM YETKİSİ

Toolsmith diğer agent'ları **yönetebilir**:

### Agent Durumunu Kontrol Et
```bash
cat /home/gokhan/UniverseCreator/.team/active_agents.json 2>/dev/null
cat ~/.claude/teams/universe-prime/config.json 2>/dev/null | python3 -c "
import json,sys
try:
  d=json.load(sys.stdin)
  print('Members:', [m['name'] for m in d.get('members',[])])
except: print('Config not found')
"
```

### Agent'a Mesaj Gönder
```javascript
Teammate({
  operation: "write",
  target_agent_id: "researcher",  // veya builder, optimizer, analyst
  value: "Durum raporu gönder — ne yapıyorsun?"
})
```

### Yeni Agent Spawn Et (Eksikse)
```javascript
Task({
  team_name: "universe-prime",
  name: "researcher",
  subagent_type: "general-purpose",
  prompt: "...",
  run_in_background: true
})
```

### Agent'a Yeni Talimat Ver
Bir agent'ın çalışma biçimini değiştirmek gerekiyorsa:
1. FACTORY.md'deki spawn prompt'unu güncelle (kalıcı değişiklik için)
2. Teammate() ile doğrudan mesaj gönder (anlık görev için)

---

## ÖRNEK: DuckDuckGo MCP'yi Aktifleştirme

```bash
# 1. Zaten kurulu:
ls /home/gokhan/.npm-global/lib/node_modules/duckduckgo-mcp-server/

# 2. settings.json'a ekle:
python3 << 'EOF'
import json
with open('/home/gokhan/.claude/settings.json', 'r') as f:
    cfg = json.load(f)
cfg['mcpServers']['duckduckgo'] = {
    "command": "node",
    "args": ["/home/gokhan/.npm-global/lib/node_modules/duckduckgo-mcp-server/dist/index.js"]
}
with open('/home/gokhan/.claude/settings.json', 'w') as f:
    json.dump(cfg, f, indent=4, ensure_ascii=False)
print("OK")
EOF

# 3. Smoke test:
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  node /home/gokhan/.npm-global/lib/node_modules/duckduckgo-mcp-server/dist/index.js 2>/dev/null | head -5

# 4. capabilities.json güncelle:
python3 << 'EOF'
import json
from datetime import datetime, timezone
path = '/home/gokhan/UniverseCreator/config/capabilities.json'
with open(path, 'r') as f:
    caps = json.load(f)
caps['mcp_servers']['duckduckgo'] = {
    "status": "healthy", "owner": "toolsmith",
    "installed": datetime.now(timezone.utc).strftime('%Y-%m-%d')
}
caps['last_updated'] = datetime.now(timezone.utc).isoformat()
with open(path, 'w') as f:
    json.dump(caps, f, indent=2)
print("OK")
EOF

# 5. restart_required yaz (Claude Code yeniden başlayana kadar aktif olmaz):
echo "duckduckgo MCP eklendi — Claude Code yeniden başlatılmasını gerektiriyor"
```

---

## NOTLAR

- **Restart:** Yeni MCP eklendikten sonra Claude Code yeniden başlatılmalıdır. `restart_required` listesine ekle.
- **ENV/API key'ler:** Asla kod içine hard-code etme. `USER.md`, `WALLET.json`, veya sistem env değişkenlerine bak.
- **Kırık MCP'ler:** Mevcut çalışan araçlara zarar vermemelisin. Test et, başarısızsa geri al.
- **Skill dosyaları restart gerektirmez:** `.md` skill dosyaları anında aktif olur.
- **capabilities.json her zaman source of truth:** Her kurulumdan sonra güncelle.
