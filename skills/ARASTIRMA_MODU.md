# 🔬 ARAŞTIRMA & PLANLAMA MODU

**Bu dosyayı okuyan Codex: Şu an ARAŞTIRMA modundasın.**

## 🚫 MUTLAK YASAK — BUNLARI ASLA YAPMA:
- ❌ git commit / git push
- ❌ Vercel deploy
- ❌ Yeni ürün oluşturma
- ❌ STATE.json değiştirme
- ❌ Mevcut kodu değiştirme / production dosyalara yazma
- ❌ npm install / pip install / herhangi bir paket kurma

## ✅ GÖREVİN:
Her cycle'da:
1. `sistem-planlama/counter.txt` dosyasını oku → N sayısını öğren
2. **14** araştırma konusundan birini seç (N % 14 + 1)
3. Derin araştırma yap (aşağıdaki TÜM araçları aktif kullan)
4. `sistem-planlama/arastirma{N}.md` yaz
5. Araştırmaya dayalı `sistem-planlama/planlama{N}.md` yaz
6. `sistem-planlama/counter.txt` içindeki sayıyı N+1 yap
7. **N+1 sayısı 14'ün katıysa** (14, 28, 42...) → `sistem-planlama/sentez{N}.md` yaz (aşağıda format var)

---

## 🔄 SENTEZDOSYASl (Her 14 cycle'da bir — KONU ROTASYONU TAMAMLANDI)

### `sistem-planlama/sentez{N}.md` formatı:
```markdown
# Sentez #{N} — Tam Rotasyon Analizi
**Tarih:** YYYY-MM-DD HH:MM
**Kapsanan Döngüler:** #{N-13} → #{N}

## En Yüksek Potansiyelli 3 Fırsat
[Her birini somut ROI, kurulum süresi, swarm uyumluluğu ile sırala]

## Hemen Yapılabilir (Bu Hafta) — Top 1 Seçim
[En az çaba, en yüksek ilk gelir potansiyeli olan seçimi derinlemesine yaz]

## Swarm Sistemini Nasıl Güçlendirir?
[Mevcut Claude+Codex+GLM sistemi ile hangi bulgu en iyi entegre olur]

## Gözden Kaçan / Sürpriz Bulgu
[Araştırmalarda beklenmedik bir şey çıktıysa yaz]

## Sonraki Rotasyon İçin Öncelik
[Hangi 3 konu bir sonraki 14 döngüde daha derin araştırılmalı]
```

---

## 📁 ÇIKTI FORMATI

### `sistem-planlama/arastirma{N}.md` formatı:
```markdown
# Araştırma #{N} — [Konu Başlığı]
**Tarih:** YYYY-MM-DD HH:MM
**Konu:** [Araştırılan konu]
**Kaynaklar:** [kullanılan kaynaklar listesi]

## Özet Bulgular
[3-5 madde, en kritik bulgular]

## Gerçek Başarı Hikayeleri
[Somut örnekler, gelir rakamları, kullanım alanları]

## Pazar Büyüklüğü & Fırsat
[Rakamsal veriler, büyüme trendi]

## Rakipler & Boşluklar
[Mevcut çözümler ve eksiklikleri]

## Teknik Gereksinimler
[Bu sistemi kurmak için neler lazım]

## Ham Notlar
[Araştırma sırasında bulunan ilginç detaylar]
```

### `sistem-planlama/planlama{N}.md` formatı:
```markdown
# Planlama #{N} — [Konu Başlığı] Uygulama Haritası
**Tarih:** YYYY-MM-DD HH:MM
**Bağlı Araştırma:** arastirma{N}.md

## Swarm Agent ile Nasıl Uygulanır?
[Adım adım sistem tasarımı — mevcut Claude+Codex+GLM swarm'a nasıl eklenir]

## Gerekli Bileşenler
- Script/Bot: [neler lazım]
- MCP/Araç: [hangi araçlar]
- API: [hangi APIler, maliyetleri]
- İnsan Müdahalesi: [nerelerde insan gerekli]

## Workflow Haritası
[Tetikleyici → Adım 1 → Adım 2 → ... → Çıktı]

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**
- En düşük çaba / en yüksek çıktı adımı nedir?
- Hangi mevcut araç/script bu işi kısmen yapar?
- Proof-of-concept için minimum gereksinimler neler?
- Tahmini kurulum süresi ve ilk gelir beklentisi?

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**
- Hangi metric'ler başarıyı gösterir?
- Hangi adımlar paralel çalışabilir?
- Ölçeklendirme için ne gerekiyor (insan, araç, bütçe)?
- Checkpoint'ler ve başarı kriterleri?

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**
- En iyi senaryo: sistem tamamen otomatik çalışırsa ne olur?
- Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?
- Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek nedir?
- White-label veya SaaS olarak satılabilir mi?

## Öncelik & Çaba Tahmini
- Öncelik: Yüksek / Orta / Düşük
- Kurulum Süresi: [gün/hafta]
- Aylık İşletme Maliyeti: [tahmini $]
- Potansiyel Gelir: [tahmini aylık $]
- ROI Beklentisi: [ne zaman break-even?]

## Mevcut Sistemle Entegrasyon
[Şu anki swarm (universe_loop.sh, 113 ürün, Vercel) ile nasıl birleşir]

## Riskler & Dikkat Edilecekler
[Potansiyel sorunlar]

## Önce Yapılacak 3 Adım (Bu Hafta)
1. [Bugün veya yarın yapılabilecek en kritik adım]
2. [İkinci adım — 1. adımın üzerine kurulur]
3. [Üçüncü adım — momentum kazandırır]
```

---

## 🎯 ARAŞTIRMA KONULARI — 14 KONU ROTASYONU

| # | Konu | Odak & Anahtar Sorular |
|---|------|------------------------|
| 1 | AI Calling Agents | Vapi/Retell/Bland/Twilio — gerçek gelir örnekleri, niche vertical ROI'leri, consent-based outreach |
| 2 | Lead Generation Automation | HVAC/solar/roofing/dental — Google Maps → enrichment → email/call, maliyet per lead |
| 3 | Ticari İstihbarat & HS Codes | Trade data scraping, GTIP/HS rapor ürünü, B2B ihracatçı-ithalatçı outreach |
| 4 | Content Factory + SEO | Programmatic SEO, 113 mevcut ürün için organik trafik, blog fabrikası, backlink otomasyonu |
| 5 | Türkiye + MENA Dijital Pazar | Trendyol/Hepsiburada/Sahibinden otomasyon, Türkiye'ye özel SaaS fırsatları, TR lokal boşluklar |
| 6 | White-label Otomasyon Ajansı | Aylık abonelik modeli, hangi sektörler en çok öder, fiyatlama, müşteri edinme |
| 7 | E-commerce Automation | Shopify/Amazon/Etsy/Temu — fiyat takip, stok, listing optimizasyon, review mining |
| 8 | Voice AI + Sales Funnel | Phone qualify bot → randevu → satış, konuşma scriptleri, düşük-budget uygulama |
| 9 | Multi-Agent Architecture Patterns | GitHub'daki gerçek swarm/multi-agent implementasyonları, framework karşılaştırma, production case'ler |
| 10 | Browser Agent + Otomasyon | Browser-use, Skyvern, Stagehand, Playwright — gerçek kazanç hikayeleri, hangi iş türleri otomatize edilir |
| 11 | Micro-SaaS & API-First Data Products | $10-200/mo küçük araçlar — IndieHackers/PH başarıları, hangi veri ürünleri satılıyor, API monetization |
| 12 | Workflow Template Marketplace | n8n/Make template satışı, Zapier alternatif, otomasyon şablonu olarak ürün — kim ne kadar kazanıyor |
| 13 | AI-Powered Recruiting & HR Otomasyon | CV screening, interview scheduler, onboarding — B2B fırsatlar, mevcut platformlar, boşluklar |
| 14 | Swarm Agent Başarı Hikayeleri | Reddit/HN/IH — gerçek case study'ler, gelir rakamları, hangi swarm pattern'ler işe yarıyor |

**Konu seçimi:** `N % 14 + 1` (counter 0 → konu 1, 13 → konu 14, 14 → konu 1, ...)

---

## 📂 MEVCUT PROJE KATALOĞU — projeler.txt

Her araştırmadan önce şunu yap:
```bash
# Araştırma konusuna ilgili keyword'leri projeler.txt'den bul
grep -i "KEYWORD" /home/gokhan/UniverseCreator/projeler.txt | head -20
# Linkleri çıkar
grep -i "KEYWORD" /home/gokhan/UniverseCreator/projeler.txt | grep -oE "https?://[^ ]+" | head -10
```

Örnek kullanım:
- Konu 1: "AI Calling Agents" → `grep -i "vapi\|retell\|twilio\|calling\|voice" projeler.txt`
- Konu 2: "Lead Generation" → `grep -i "lead\|scrape\|outreach\|cold email\|apify" projeler.txt`
- Konu 9: "Multi-Agent" → `grep -i "swarm\|multi.agent\|langchain\|crew\|autogen" projeler.txt`
- Konu 10: "Browser Agent" → `grep -i "browser-use\|skyvern\|stagehand\|playwright" projeler.txt`
- Konu 11: "Micro-SaaS" → `grep -i "saas\|api\|mrr\|indiehackers\|tool" projeler.txt`
- Konu 12: "n8n" → `grep -i "n8n\|make.com\|zapier\|workflow\|template" projeler.txt`
- Konu 14: "Swarm" → `grep -i "swarm\|agent.*agent\|multi.*model\|orchestrat" projeler.txt`

---

## 🔧 ARAŞTIRMA ARAÇLARI — HEPSİNİ KULLAN

### 1️⃣ DuckDuckGo Web Arama — ddgr (Birincil arama motoru)
```bash
# JSON formatında web arama
ddgr --np --json "ai calling agent revenue 2025 case study" 2>/dev/null | \
  python3 -c "
import sys, json
try:
  results = json.load(sys.stdin)
  for r in results[:8]:
    print(r.get('title','')[:80])
    print('  ' + r.get('url','')[:80])
    print('  ' + r.get('abstract','')[:120])
    print()
except: pass
"

# Spesifik site araması
ddgr --np --json "site:indiehackers.com ai automation revenue" 2>/dev/null | \
  python3 -c "import sys,json; [print(r['url']) for r in json.load(sys.stdin)[:5]]"

# Reddit araması (rdt olmadan)
ddgr --np --json "reddit.com ai agent automation mrr 2024" 2>/dev/null | \
  python3 -c "import sys,json; [print(r['title'],'\n ',r['url']) for r in json.load(sys.stdin)[:5] if 'reddit' in r.get('url','')]"
```

### 2️⃣ Reddit JSON API (doğrudan, 403 vermez)
```bash
# Belirli subreddit'te arama (en iyi yöntem)
QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('ai automation revenue'))")
curl -s "https://www.reddit.com/r/SideProject/search.json?q=${QUERY}&sort=top&t=year&limit=10&restrict_sr=1" \
  -H "User-Agent: research-bot/1.0" | python3 -c "
import sys, json
try:
  data = json.load(sys.stdin)
  for item in data['data']['children']:
    d = item['data']
    print(d['title'][:100])
    print('  score:', d.get('score',0), '| comments:', d.get('num_comments',0))
    print('  https://reddit.com' + d.get('permalink',''))
    print()
except Exception as e: print('HATA:', e)
"

# Birden fazla subreddit için arama:
for SUB in SideProject entrepreneur AIAgents automation indiehackers; do
  echo "=== r/$SUB ==="
  QUERY="ai+agent+automation"
  curl -s "https://www.reddit.com/r/${SUB}/search.json?q=${QUERY}&sort=top&t=year&limit=5&restrict_sr=1" \
    -H "User-Agent: research-bot/1.0" | python3 -c "
import sys,json
try:
  data=json.load(sys.stdin)
  for item in data['data']['children'][:3]:
    d=item['data']
    print(' -',d['title'][:90],'(score:'+str(d.get('score',0))+')')
    print('   https://reddit.com'+d.get('permalink',''))
except: pass
" 2>/dev/null
done

# Bir Reddit post'unun yorumlarını oku (değerli bilgi var burada!)
curl -s "https://www.reddit.com/r/SideProject/comments/POST_ID.json" \
  -H "User-Agent: research-bot/1.0" | python3 -c "
import sys,json
data=json.load(sys.stdin)
# İlk post
post = data[0]['data']['children'][0]['data']
print('BAŞLIK:', post.get('title',''))
print('SELFTEXT:', post.get('selftext','')[:500])
print('\nYORUMLAR:')
for c in data[1]['data']['children'][:5]:
  if c['kind'] == 't1':
    print(' -', c['data'].get('body','')[:200])
"
```

### 3️⃣ GitHub Araştırma — gerçek implementasyonlar bul
```bash
# Stars'a göre repo araması
gh search repos "ai calling agent automation" --sort stars --limit 10 \
  --json name,description,stargazerCount,url,createdAt 2>/dev/null | \
  python3 -c "
import sys,json
for r in json.load(sys.stdin):
  print(f\"★{r['stargazerCount']:>5} | {r['name']}: {r.get('description','')[:60]}\")
  print(f\"       {r['url']}\")
"

# Belirli topic'e göre
gh search repos --topic "voice-agent" --sort stars --limit 10 2>/dev/null | head -20
gh search repos --topic "n8n-workflow" --sort stars --limit 10 2>/dev/null | head -20
gh search repos --topic "lead-generation" --sort stars --limit 10 2>/dev/null | head -20

# Yeni repolar (son 3 ay, aktif projeler)
gh search repos "swarm agent business" --created ">2025-01-01" --sort stars --limit 10 2>/dev/null
```

### 4️⃣ ProductHunt — yeni araçlar ve SaaS ürünler
```bash
# ProductHunt search (Jina reader ile)
curl -s --max-time 15 "https://r.jina.ai/https://www.producthunt.com/search?q=ai+calling+agent" | head -100

# ProductHunt günlük trending (AI kategori)
curl -s --max-time 15 "https://r.jina.ai/https://www.producthunt.com/topics/artificial-intelligence" | head -80

# Belirli bir ürünün PH sayfası
curl -s --max-time 10 "https://r.jina.ai/https://www.producthunt.com/products/vapi" | head -60
```

### 5️⃣ Derin Araştırma Skill (Akademik + Video)
```
/derin-arastirma <konu>
```
Bu skill şunları yapar:
- **ArXiv MCP:** Akademik makaleler (`mcp__arxiv__search_papers`)
- **MCPTube:** YouTube transkriptleri — PARALEL kullan:
  ```bash
  python3 /home/gokhan/projects/scrape/mcptube/parallel_add.py \
    "https://youtube.com/watch?v=VIDEO1" \
    "https://youtube.com/watch?v=VIDEO2" \
    "https://youtube.com/watch?v=VIDEO3"
  ```

### 6️⃣ Jina Reader — Hızlı Sayfa Okuma
```bash
# Paralel curl (birden fazla sayfa aynı anda)
curl -s "https://r.jina.ai/https://www.vapi.ai/pricing" &
curl -s "https://r.jina.ai/https://retellai.com/pricing" &
curl -s "https://r.jina.ai/https://www.bland.ai/pricing" &
wait

# IndieHackers arama
curl -s --max-time 15 "https://r.jina.ai/https://www.indiehackers.com/search?q=ai+automation" | head -80

# Hacker News arama (Show HN / Ask HN)
curl -s "https://r.jina.ai/https://hn.algolia.com/api/v1/search?query=ai+automation+revenue&tags=story&numericFilters=points>100" | \
  python3 -c "
import sys,json
data=json.load(sys.stdin)
for hit in data.get('hits',[])[:5]:
  print(hit.get('title','')[:90])
  print('  pts:', hit.get('points',0), '| comments:', hit.get('num_comments',0))
  print('  https://news.ycombinator.com/item?id=' + str(hit.get('objectID','')))
  print()
"
```

### 7️⃣ Playwright MCP — JS gerektiren siteler
```
mcp__playwright__browser_navigate url="https://example.com"
mcp__playwright__browser_snapshot
mcp__playwright__browser_take_screenshot
```
Ne zaman kullan: pricing sayfaları, dashboard'lar, JavaScript ile yüklenen içerikler.

### 8️⃣ Chrome DevTools MCP — gerçek sayfa içeriği
```
mcp__chrome-devtools__*
```
Playwright ile açılan Chrome üzerinde daha derin inceleme için.

---

## 🔬 KONU BAZLI ARAŞTIRMA REHBERI

### Konu 1 — AI Calling Agents
```bash
ddgr --np --json "vapi ai calling agent revenue 2025 case study" 2>/dev/null | python3 -c "import sys,json; [print(r['title'],'\n ',r['url'],'\n') for r in json.load(sys.stdin)[:6]]"
gh search repos "vapi voice agent" --sort stars --limit 8 2>/dev/null
curl -s "https://r.jina.ai/https://www.indiehackers.com/search?q=voice+ai+agency" | head -60
```

### Konu 2 — Lead Generation
```bash
ddgr --np --json "lead generation automation mrr indie hacker 2025" 2>/dev/null | python3 -c "import sys,json; [print(r['title'],'\n ',r['url'],'\n') for r in json.load(sys.stdin)[:6]]"
gh search repos "lead generation automation scraper" --sort stars --limit 8 2>/dev/null
curl -s "https://r.jina.ai/https://www.indiehackers.com/search?q=lead+generation+revenue" | head -60
```

### Konu 9 — Multi-Agent Architecture
```bash
gh search repos "multi agent swarm llm" --sort stars --limit 10 2>/dev/null
gh search repos --topic "multi-agent" --sort stars --limit 10 2>/dev/null
ddgr --np --json "multi agent architecture production case study 2025" 2>/dev/null | python3 -c "import sys,json; [print(r['title'],'\n ',r['url'],'\n') for r in json.load(sys.stdin)[:6]]"
```

### Konu 11 — Micro-SaaS
```bash
curl -s "https://r.jina.ai/https://www.indiehackers.com/search?q=micro+saas+api+revenue" | head -80
ddgr --np --json "micro saas api data product 100 mrr 2025 indiehackers" 2>/dev/null | python3 -c "import sys,json; [print(r['title'],'\n ',r['url'],'\n') for r in json.load(sys.stdin)[:6]]"
curl -s --max-time 15 "https://r.jina.ai/https://www.producthunt.com/topics/developer-tools" | head -60
```

### Konu 12 — Workflow Templates
```bash
gh search repos "n8n workflow template" --sort stars --limit 10 2>/dev/null
ddgr --np --json "sell n8n templates make.com workflow marketplace revenue" 2>/dev/null | python3 -c "import sys,json; [print(r['title'],'\n ',r['url'],'\n') for r in json.load(sys.stdin)[:6]]"
curl -s "https://r.jina.ai/https://n8n.io/workflows/" | head -60
```

### Konu 5 — Türkiye + MENA Pazarı
```bash
ddgr --np --json "saas automation startup Turkey Turkish market 2025" 2>/dev/null | python3 -c "import sys,json; [print(r['title'],'\n ',r['url'],'\n') for r in json.load(sys.stdin)[:6]]"
ddgr --np --json "Trendyol automation API ecommerce seller tools" 2>/dev/null | python3 -c "import sys,json; [print(r['title'],'\n ',r['url'],'\n') for r in json.load(sys.stdin)[:6]]"
curl -s "https://r.jina.ai/https://www.sahibinden.com/ilan-kategorileri" | head -40
```

---

## 📊 COUNTER YÖNETİMİ

```bash
# Counter oku
N=$(cat /home/gokhan/UniverseCreator/sistem-planlama/counter.txt 2>/dev/null || echo "0")
KONU_IDX=$(( N % 14 + 1 ))

# Yazma işleminden sonra counter artır
echo "$((N + 1))" > /home/gokhan/UniverseCreator/sistem-planlama/counter.txt

# Sentez kontrolü (her 14 döngüde bir)
YENI_N=$((N + 1))
if [ $((YENI_N % 14)) -eq 0 ]; then
  echo "14 DÖNGÜ TAMAMLANDI — sentez${YENI_N}.md yaz!"
fi
```

---

## 📝 ÇALIŞMA AKIŞI (Her Cycle)

```
1. Counter oku → N = X, Konu = X%14+1
2. Konu başlığını belirle
3. projeler.txt'den ilgili keyword'leri ve linkleri bul
4. ddgr ile web araması yap (birincil kaynak keşfi)
5. Reddit JSON API ile community intelligence topla (success stories, gelir rakamları)
6. GitHub'da gerçek implementasyonlar bul (gh search repos)
7. derin-arastirma skill'ini çağır: /derin-arastirma <konu>
8. Seçici Jina okuma — sadece en değerli URL'leri oku
9. ProductHunt'ta bu kategorideki yeni araçlara bak
10. arastirma{N}.md yaz (detaylı, kaynak linkli, gerçek rakamlar)
11. planlama{N}.md yaz (swarm ile nasıl yapılır, workflow haritası, kısa/orta/uzun vade)
12. Counter'ı N+1 yap
13. Eğer yeni counter 14'ün katıysa → sentez{N+1}.md yaz
14. Bitti — execute etme, deploy etme, commit atma
```

**Araştırmada kalite kontrolü:**
- En az 3 farklı kaynak türü kullan (web + reddit + github veya arxiv)
- Gerçek gelir/ROI rakamları yoksa "tahmin" olarak etiketle
- Türkiye/MENA konularında Türkçe kaynak da ara

---

## ⚠️ HATIRLATMA

Sen şu an bir **araştırmacısın**, bir uygulayıcı değil.
Yarın insan bu dosyaları okuyacak ve en iyi planı seçecek.
Kaliteli, somut, ölçülebilir bilgiler yaz. Spekülatif değil.
Gerçek gelir rakamları, gerçek kullanım örnekleri, gerçek araç maliyetleri.
