# Planlama #3 — Content Factory + SEO Uygulama Haritası
**Tarih:** 2026-04-21 04:10 +03
**Bağlı Araştırma:** arastirma3.md

## Swarm Agent ile Nasıl Uygulanır?
Bu sistem “AI blog spammer” olmayacak. O aptal yol Google cezasına davetiye. Doğru tasarım: ürün verisi + search intent + kalite kapısı + ölçüm döngüsü.

1. **Inventory Agent**
   - `STATE_SUMMARY.json`, ürün README/product metadata, canlı URL, checkout URL, health status okur.
   - Ürünleri kümeler: converter, security, API/devtool, design/content, AI/cost.
   - Yayına uygun olmayanları `noindex/draft/repair-needed` diye işaretler.
2. **Keyword & Intent Agent**
   - Her ürün için seed query üretir: slug, problem, input/output format, persona, alternatif, hata, entegrasyon.
   - DataForSEO/SerpApi/Ahrefs/GSC ile search volume, CPC, SERP intent, competitor URL toplar.
3. **Strategy Agent**
   - Keywordleri sayfa pattern'lerine bağlar: comparison, guide, converter, alternative, best tools, checklist, FAQ, API example.
   - İlk batch için 20-40 düşük riskli, yüksek intent sayfa seçer.
4. **Research Agent**
   - Rakip sayfaları okur, boşluk çıkarır: eksik benchmark, eksik örnek, eski fiyat, zayıf CTA, no structured data.
   - Kaynaklı brief üretir; hallucination'a izin yok.
5. **Draft Agent**
   - Markdown/MDX draft üretir; her draft gerçek ürün linki, sample input/output, CTA, internal links içerir.
   - AI kullansa bile “ürün deneyimi” ve özgün örnek olmadan draft geçmez.
6. **SEO QA Agent**
   - Thin content, duplicate similarity, intent mismatch, schema, title/meta, canonical, link graph, fact check, unsafe claims kontrolü yapar.
7. **Human Gate**
   - İlk 50-100 sayfa insan onayı ile ilerler.
   - Kör autopublish yalnızca QA puanı stabil olduktan ve GSC sinyali pozitif olduktan sonra küçük batch'lerde açılır.
8. **Measurement Agent**
   - GSC impressions/clicks/CTR/position, checkout clicks, email captures, AI citation prompts, internal link crawl sinyali ölçer.
   - Kazanan page pattern'lerini çoğaltır; kaybedenleri rewrite/noindex yapar.

## Gerekli Bileşenler
- **Script/Bot:**
  - Product inventory exporter
  - Keyword miner
  - SERP/gap analyzer
  - Content brief generator
  - Markdown draft generator
  - SEO QA + duplicate checker
  - Internal-link graph builder
  - Sitemap/index monitor
  - GSC/AIO performance reporter
- **MCP/Araç:**
  - ArXiv MCP: GEO/AI-search araştırma takibi
  - MCPTube: SEO/pSEO workflow transkriptlerinden playbook çıkarma
  - Playwright/Chrome DevTools: ürün screenshot, SERP/page QA, rendered DOM kontrolü
  - Botasaurus: JS-heavy competitor page/screenshot scraping fallback
  - `markdown-site` benzeri markdown publish sistemi opsiyonel
- **API:**
  - Google Search Console API: ücretsiz ölçüm + URL Inspection; URL Inspection limiti 2,000/gün, 600/dk/site
  - DataForSEO: $0.0006 / 10 sonuç SERP standard queue; 1,000 SERP ≈ $0.6; minimum deposit $50
  - SerpApi: $25/1k, $75/5k, $150/15k, $275/30k arama/ay
  - Ahrefs: Starter $29/ay; Brand Radar AI $199/ay; Content Kit from $99/ay — POC için şart değil
  - LLM API: draft/QA için başlangıçta düşük bütçe; gerçek maliyet batch başına ölçülmeli
- **İnsan Müdahalesi:**
  - İlk topic map onayı
  - İlk 20-40 draft kalite onayı
  - Riskli fiyat/ürün karşılaştırmalarında fact-check
  - Yayın/noindex kararı
  - İlk dönüşüm sayfalarının CTA ve ödeme akışı kontrolü

## Workflow Haritası
Tetikleyici: haftalık araştırma veya ürün batch güncellemesi
→ Product inventory oku
→ Sağlıklı/checkout'lu ürünleri seç
→ Keyword seed üret
→ DataForSEO/SerpApi ile SERP verisi çek
→ Intent cluster çıkar
→ Rakip top-10 gap analizi
→ Sayfa pattern seç
→ Draft brief üret
→ Markdown draft üret
→ SEO QA + fact check
→ Human review
→ Yayın adayı listesi / noindex listesi
→ Sitemap/structured data planı
→ GSC ölçüm kuyruğu
→ 14/30/60 gün performans raporu
→ Kazanan pattern'i çoğalt, zayıfı rewrite/noindex yap

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen yapılacak şey:** 113 ürün için SEO inventory + keyword pattern haritası + ilk 20-40 draft. Yayın değil, yayın-adayı. Bu modda kod/deploy yok; sonraki execution cycle için net backlog çıkar.
- **En düşük çaba / en yüksek çıktı:** Checkout'u olan ve healthy/live görünen ürünlerden 10-15 tanesini seçip her biri için 2 sayfa üretmek:
  - `free [task] tool`
  - `[A] to [B] converter`
  - `[tool/category] alternative`
  - `[tool] vs [competitor/manual workflow]`
- **Mevcut araç/script desteği:** README generator ve STATE summary zaten ürün bilgisini taşıyor; bu data content brief'e dönüşebilir. `projeler.txt` içindeki markdown-site/marketingskills/SEO testing fikirleri yayın ve deney katmanına ilham verir.
- **Minimum POC gereksinimleri:**
  - 10 ürün × 2-4 sayfa = 20-40 draft
  - Her draftta ürün linki, sample I/O, CTA, internal link, JSON-LD planı, kaynak listesi
  - QA checklist: duplicate, intent, factuality, thin-content, broken URL, checkout URL
- **Tahmini kurulum süresi:** 3-5 gün araştırma/brief/draft sistemi; 1-2 gün human QA ve yayın planı.
- **İlk gelir beklentisi:** Organik SEO'dan 1-2 haftada gelir beklemek hayal satmak olur. Kısa vadede hedef gelir değil, indexlenebilir varlık üretmek. Eğer ödeme kanalı açıksa, 2-6 hafta içinde ilk düşük hacimli checkout click/sale sinyali beklenebilir; daha gerçekçi ilk organik satış penceresi 6-12 hafta.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **Ay 1 hedef görüntü:**
  - 100-200 kaliteli yayın-adayı veya yayında sayfa
  - 30-60 ürün için internal linking matrix
  - GSC'de sitemap + URL inspection takip listesi
  - Top 20 page pattern için impressions/clicks/CTR dashboard
  - En az 10 ürün sayfasında SoftwareApplication/Product schema planı
- **Başarı metrikleri:**
  - Index rate: yayınlanan sayfaların %60+ indexlenmesi
  - 30 gün sonunda 1,000+ impression / 50+ click toplam sinyal
  - 60-90 gün sonunda 30-100 günlük organik click
  - Checkout click veya email capture rate: %1-3 başlangıç hedefi
  - AI citation: seçili 30 prompt içinde 3-5 mention/citation sinyali
- **Paralel çalışabilecek adımlar:**
  - Keyword miner ayrı
  - Rakip gap analyzer ayrı
  - Draft generator ayrı
  - Screenshot/schema/internal link QA ayrı
  - GSC/AI-search tracker ayrı
- **Ölçeklendirme gereksinimi:**
  - Bütçe: $50 DataForSEO deposit + gerekirse $25-75 SerpApi; Ahrefs opsiyonel
  - İnsan: haftada 2-4 saat kalite/gate review
  - Teknik: sitemap/metadata/structured data otomasyonu; health-check ile SEO publish gate birleşmeli
- **Checkpoint'ler:**
  - Hafta 2: 40 draft, 10 onaylı sayfa
  - Hafta 4: 100+ sayfa, sitemap/GSC ölçüm
  - Hafta 8: ilk rewrite/noindex kararları
  - Hafta 12: kazanan 2-3 pattern'i 300+ sayfaya genişletme kararı

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** Content factory haftalık 50-100 sayfayı kör basmadan üretir; QA düşük puanlıları otomatik eler; GSC/AI-search sinyali kazanan pattern'leri çoğaltır. 2,000-5,000 kaliteli long-tail sayfa portföyü oluşur.
- **Gelir kolları:**
  - Ürün checkout satışları
  - “Developer tool bundle” landing page paketleri
  - Affiliate/partner tool comparison sayfaları
  - White-label content factory kurulumu
  - Micro-SaaS: “pSEO brief generator for dev tools”
  - AI-search citation monitor mini ürünü
- **Swarm avantajı:** İnsan ajanslar 113 ürün × 10 pattern işinde boğulur. Swarm ürün envanteri, SERP analizi, draft, QA, ölçüm ve rewrite döngüsünü yorulmadan çevirebilir.
- **Rakiplerin yapamadığı şey:** pSEO'yu canlı ürün health/checkout/state ile bağlamak. Yani sadece içerik değil, “çalışan ürüne trafik yönlendiren ve çalışmayanı noindex'e alan” ekonomik loop.
- **White-label/SaaS potansiyeli:** Evet. Özellikle küçük SaaS/devtool sahiplerine “ürün kataloğundan 100 intent page + GSC tracker + AI citation report” paketi satılabilir. Başlangıç fiyatı $299 setup + $99-499/ay bakım mantıklı.
- **Evrim:** TR/EN ile başla; sonra ES/PT/DE gibi düşük rekabetli diller. Çok dilli pSEO, özellikle converter/devtool query'lerinde klasik İngilizce rekabetinden kaçış sağlar.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek. 113 ürün varsa content factory lüks değil, dağıtım motoru.
- **Kurulum Süresi:** POC 1 hafta; güvenli yayın sistemi 3-6 hafta; tam otomasyon 2-3 ay.
- **Aylık İşletme Maliyeti:**
  - Minimum: $50 DataForSEO deposit uzun süre yeter + LLM usage
  - Pratik: $75-150/ay SERP + LLM + monitoring
  - Premium: Ahrefs/Semrush/GEO tooling ile $200-500+/ay
- **Potansiyel Gelir:**
  - 1-3 ay: $0-300/ay gerçekçi; ödeme kanalı ve checkout şart
  - 3-6 ay: $300-2,000/ay; 500+ kaliteli sayfa + çalışan checkout ile
  - 6-12 ay: $2,000-10,000/ay upside; white-label/affiliate eklenirse daha yüksek
- **ROI Beklentisi:** Minimum maliyetle break-even tek $79-$299 satışla olur. Ama organik SEO break-even'i trafik açısından 2-4 ayda beklenmeli.

## Mevcut Sistemle Entegrasyon
- `universe_loop.sh` veya mevcut cycle sistemi content factory'i ayrı “research/planning → draft → QA → publish candidate” kuyruğu olarak çalıştırmalı.
- `STATE_SUMMARY.json` publish gate'in ana kaynağı olmalı: live/healthy/checkout yoksa sayfa ya draft kalır ya noindex önerilir.
- Vercel ürünleri için canonical URL ve health check sonucu içerik brief'e otomatik girmeli.
- README SEO otomasyonu ile content factory birleşmeli: README ürünün “source of truth” metni, landing pages ise intent-specific dağıtım katmanı.
- Search Console ölçümü günlük/haftalık rapora dökülmeli: yeni sayfalar, index status, impressions, clicks, CTR, position, checkout click.
- Telegram/notification sadece açık izin veya mevcut güvenli notification policy ile yapılmalı; araştırma modunda dış iletişim yok.

## Riskler & Dikkat Edilecekler
- **Scaled content abuse:** En büyük risk. Değersiz AI sayfa basmak, domain'i yakabilir. Çözüm: gerçek ürün verisi + özgün örnek + QA + batch publishing.
- **Broken product traffic:** 113 aktif ama 23 healthy görünmesi ciddi uyarı. Sağlıksız ürüne SEO trafiği göndermek kullanıcıyı kaçırır.
- **Checkout gap:** 61 ürün checkout'suz. Para beklentisi olan sayfalar checkout olmayan ürüne bağlanmamalı.
- **Duplicate/thin content:** Converter sayfaları birbirine çok benzeyebilir. Her sayfada use-case, sample data, persona, troubleshooting, internal links farklı olmalı.
- **Yanlış fiyat/karşılaştırma:** Rakip fiyatları değişir. Comparison sayfaları tarih ve kaynak içermeli; otomatik refresh yoksa iddialar yumuşak yazılmalı.
- **AI hallucination:** Teknik rehberlerde yanlış komut/format güven kaybettirir. Sample output test edilmeli.
- **Zero-click/AI Overviews:** Click düşebilir; bu yüzden LLM citation, branded search, direct visits de ölçülmeli.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **SEO inventory çıkar:** 113 ürünü kategori, health, checkout, canonical URL, README var/yok, title/meta var/yok, schema var/yok diye tabloya dök.
2. **İlk pattern setini seç:** converter/security/API/design kategorilerinden 10 healthy+checkout ürün seç; her biri için 2-4 intent page brief üret.
3. **QA-first draft batch hazırla:** 20-40 markdown draft + internal link matrix + noindex/publish önerisi oluştur; yayın/deploy yapma, karar dosyasına koy.
