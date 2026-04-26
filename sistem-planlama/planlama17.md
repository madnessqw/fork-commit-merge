# Planlama #17 — Content Factory + SEO Uygulama Haritası
**Tarih:** 2026-04-21 13:51 +03
**Bağlı Araştırma:** arastirma17.md

## Swarm Agent ile Nasıl Uygulanır?
Bu sistemin adı “content factory” olabilir ama fabrikadan çıkan şey spam olmayacak. Doğru tasarım: **ürün verisi → intent map → evidence-backed brief → draft → QA → human gate → ölçüm → rewrite/noindex**.

1. **Inventory Agent**
   - `STATE.json` / `STATE_SUMMARY.json` okur.
   - 113 ürünü kategori, health, checkout, canonical URL, README varlığı, schema uygunluğu, sample input/output varlığına göre skorlar.
   - Health veya checkout bozuksa sayfayı “traffic-ready değil” diye işaretler.
2. **Intent & Keyword Agent**
   - Her ürün için seed query üretir: problem, format dönüşümü, alternatif, hata, persona, API, template.
   - DataForSEO ile volume/CPC/competition toplar; düşük hacimli ama yüksek intent query'leri kaçırmaz.
3. **SERP Gap Agent**
   - Top result'ları okur: eksik örnek, zayıf CTA, eski fiyat, eksik schema, açıklanmamış use-case, zayıf internal link.
   - “Biz neden daha iyi sayfa üretiriz?” cevabı yoksa sayfa üretmez.
4. **Page Architect Agent**
   - Sayfa family seçer: converter, comparison, alternative, fix guide, API snippet, checklist.
   - Her sayfaya unique data block zorunlu koyar: canlı ürün linki, sample input/output, screenshot, timing, limitations, related tools.
5. **Draft Agent**
   - Markdown/MDX draft üretir; AI kullansa da kaynaklı, kısa, gerçek örnekli ve CTA'lı yazar.
6. **SEO QA / Judge Agent**
   - Thin content, duplicate similarity, hallucination, unsupported claim, broken link, schema, title/meta, canonical, internal-link graph kontrolü yapar.
   - Skor düşükse publish değil rewrite/noindex verir.
7. **Human Gate**
   - İlk 50-100 sayfada insan onayı şart. Sonra bile yüksek-risk comparison/pricing sayfaları insan görmeli.
8. **Measurement Agent**
   - GSC impressions/clicks/CTR/position, checkout click, email capture, AI mention/citation ve direct/branded search sinyalini takip eder.
9. **Earned Media Agent**
   - GitHub README, HN/Reddit/IndieHackers anlatıları, ProductHunt/listing fırsatları ve third-party mention üretir. GEO papers earned-media bias dediği için sadece own-site yetmez.

## Gerekli Bileşenler
- **Script/Bot:**
  - SEO inventory exporter
  - Keyword seed generator
  - DataForSEO batch keyword checker
  - SERP/gap analyzer
  - Page brief generator
  - Draft generator
  - Duplicate/thin-content/evidence QA
  - Internal-link graph builder
  - Sitemap/noindex planner
  - GSC + AI citation report generator
- **MCP/Araç:**
  - ArXiv MCP: GEO/AI-search gelişmelerini takip
  - MCPTube: pSEO/content workflow transkriptlerinden playbook çıkarma
  - Playwright/Chrome DevTools/chrome-devtools-axi: screenshot/rendered-page QA
  - Jina Reader: rakip/dokümantasyon okuma
  - Reddit JSON API: community pain/gain ve gerçek case mining
- **API:**
  - DataForSEO Google Ads Keywords: Standard Queue $0.05/task, 1M keyword ≈ $50; Live Mode 1M keyword ≈ $75.
  - Google Search Console: ölçüm için ücretsiz; URL inspection yayın sonrası izleme için.
  - Ahrefs Lite: $129/ay; POC için lüks, büyüme sonrası gap/backlink için düşünülür.
  - Semrush AI Visibility Toolkit: $99/ay; POC'de değil, GEO monitoring gelir üretince.
  - LLM API: brief/draft/QA; maliyet batch başına ölçülmeli.
- **İnsan Müdahalesi:**
  - İlk topic map ve sayfa family onayı
  - İlk 40-80 draft kalite inceleme
  - Pricing/comparison/factual claim review
  - Publish/noindex/rewrite kararları
  - İlk conversion/CTA metni kontrolü

## Workflow Haritası
Tetikleyici: haftalık content-growth cycle
→ 113 ürün inventory oku
→ Traffic-ready ürünleri filtrele
→ Ürün başına query seed üret
→ DataForSEO volume/CPC/intent çek
→ Query cluster + page family map
→ SERP gap analizi
→ Evidence-backed brief
→ Draft
→ SEO QA / fact-check / duplicate check
→ Human gate
→ Publish candidate listesi veya noindex/rewrite listesi
→ Sitemap/internal-link planı
→ GSC + AI-search ölçüm kuyruğu
→ 14/30/60 gün raporu
→ Kazanan pattern scale, kaybeden pattern kill/rewrite

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen yapılabilir çıktı:** 113 sağlıklı ürün için **SEO inventory + first 40 publish-candidate briefs**. Bu turda kod/deploy yok; ama uygulama cycle'ı için backlog net olur.
- **En düşük çaba / en yüksek çıktı:** 10 ürün seç, her biri için 4 sayfa family çıkar:
  1. `free [task] tool`
  2. `[A] to [B] converter`
  3. `[tool/category] alternative`
  4. `[error/use-case] fix guide`
- **Mevcut araç/script ile yapılabilecekler:** `STATE.json`, README/product metadata ve mevcut health status source-of-truth olarak yeterli. `projeler.txt` içindeki marketing/SEO skill fikirleri prompt/QA tarafına taşınabilir.
- **Minimum POC gereksinimleri:**
  - 10 ürün
  - 40 brief
  - Her briefte keyword intent, SERP gap, sample input/output, internal links, CTA, schema önerisi, noindex/publish önerisi
  - 5 örnek final draft human review için hazırlanır
- **Tahmini kurulum süresi:** 2-3 gün inventory/keyword map; 2-3 gün brief/draft; 1 gün QA rubric. Toplam 1 hafta civarı.
- **İlk gelir beklentisi:** 1-2 haftada organik gelir beklemek masal. Kısa vadede hedef: indexlenebilir asset ve ölçüm kuyruğu. İlk checkout click sinyali 2-6 hafta; anlamlı satış sinyali 6-12 hafta daha gerçekçi.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonu hedefi:**
  - 100-150 publish-ready sayfa brief/draft
  - 40-80 human-approved sayfa
  - Ürünler arası internal link graph
  - GSC ölçüm paneli: index, impression, click, CTR, avg position
  - AI-search prompt paneli: 30-50 prompt, ChatGPT/Perplexity/Gemini mention/citation kontrolü
- **Başarı metric'leri:**
  - Index rate: 30 gün içinde %60+ hedef
  - Impression: ilk 30-45 günde 1,000+ toplam impression
  - CTR: low-volume intent pages için %1-3 başlangıç
  - Checkout/email capture: %0.5-2 ilk sinyal
  - AI mention: 50 prompt içinde 3-5 brand/tool mention
- **Paralel çalışacak adımlar:**
  - Keyword mining ayrı agent
  - SERP gap ayrı agent
  - Draft ayrı agent
  - QA/fact-check ayrı agent
  - GSC/AI-search tracker ayrı agent
- **Ölçeklendirme gereksinimi:**
  - DataForSEO için başlangıç $50 deposit yeterli olabilir.
  - Haftada 2-4 saat insan review.
  - Yayın sistemi içinde noindex/sitemap/canonical/lastmod kontrolü.
  - Checkout/health bozulursa ilgili SEO sayfası rewrite veya noindex kuyruğuna düşmeli.
- **Checkpoint'ler:**
  - Hafta 1: 40 brief + 5 final draft
  - Hafta 2: 20-40 onaylı sayfa adayı
  - Hafta 4: GSC + AI-search tracking başladı
  - Hafta 8: ilk rewrite/noindex kararları
  - Hafta 12: 2-3 kazanan pattern'i 300+ sayfaya genişletme kararı

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** 12 ay içinde UniverseCreator 1,000-3,000 arası kaliteli, ürün bağlantılı, ölçülen long-tail sayfaya sahip olur. Her sayfa gerçek aracı, örneği, internal link'i ve CTA'sı olan küçük satış temsilcisi gibi çalışır.
- **Evrim rotası:**
  - Aşama 1: EN devtool pSEO
  - Aşama 2: AI-search/GEO citation monitoring
  - Aşama 3: ES/PT/DE/TR çok dilli low-competition sayfalar
  - Aşama 4: “content refresh” agent: fiyat, rakip, broken link, outdated info günceller
  - Aşama 5: white-label content factory OS
- **Yan ürünler / gelir kolları:**
  - Product-led SEO setup paketi: $299-$999 one-time
  - Monthly refresh/monitoring retainer: $99-$499/ay
  - “AI citation monitor for micro-SaaS” mini-SaaS
  - Developer-tool comparison affiliate pages
  - SEO inventory/brief generator API
- **Rakiplerin yapamadığı swarm avantajı:** Human agency 113 ürün × 8 page family × rewrite loop işinde yorulur. Swarm her hafta keyword, SERP, draft, QA, GSC, AI citation ve internal link'i döndürür. Sıkıcı işi robot yapar; insan sadece karar verir.
- **White-label/SaaS olarak satılabilir mi?** Evet, ama “AI blog generator” olarak değil. O kategori çöplük. Doğru pozisyon: **Product-led Programmatic SEO OS for small SaaS/devtool portfolios**.

## Öncelik & Çaba Tahmini
- **Öncelik:** Çok yüksek. 113 healthy ürün varsa organik dağıtım sistemi kurmamak para gömmek.
- **Kurulum Süresi:** POC 1 hafta; güvenli publish workflow 3-6 hafta; tam measurement/rewrite loop 2-3 ay.
- **Aylık İşletme Maliyeti:**
  - Minimum: $20-75 LLM + DataForSEO usage
  - Pratik: $75-150/ay LLM + SERP + monitoring
  - Premium: Ahrefs/Semrush/GEO tooling ile $250-600+/ay
- **Potansiyel Gelir:**
  - 1-3 ay: $0-500/ay; daha çok trafik/checkout sinyali
  - 3-6 ay: $500-2,000/ay; organik + affiliate + setup offers
  - 6-12 ay: $2,000-10,000/ay upside; white-label/retainer eklenirse daha yüksek
- **ROI Beklentisi:** Teknik maliyet düşük olduğu için tek $299 setup satışı bile tool maliyetini kapatır. SEO trafik ROI'si için gerçekçi pencere 8-16 hafta.

## Mevcut Sistemle Entegrasyon
- `universe_loop.sh` content-growth lane olarak ayrı çalışmalı: research → brief → draft → QA → publish candidate.
- `STATE.json` ana publish gate olmalı: active/healthy/checkout/canonical yoksa sayfa publish değil draft/noindex.
- README SEO otomasyonu source copy üretir; content factory ise intent-specific landing dağıtımı yapar.
- GSC/AI-search raporu günlük değil haftalık yeterli; SEO sabır ister, panik butonu değil.
- Product health bozulursa ilgili SEO sayfaları “traffic risk” listesine düşmeli.
- Dış paylaşım/backlink/outreach için explicit izin gerekir; bu planlama turunda dış aksiyon yok.

## Riskler & Dikkat Edilecekler
- **Scaled content abuse:** Asıl ölüm sebebi. Aynı template'le yüzlerce değersiz sayfa basma.
- **Duplicate pages:** Converter ve alternative sayfaları kolay kopya kokar. Unique sample, persona, troubleshooting, screenshot şart.
- **AI hallucination:** Teknik rehberlerde yanlış komut, yanlış fiyat, yanlış API bilgisi güven yakar.
- **Indexing hack yanılgısı:** Google Indexing API devtool/blog sayfaları için genel index hack'i değil.
- **Zero-click / AI Overviews:** Trafik düşebilir; citation/direct/branded metrics de izlenmeli.
- **Competitor pricing drift:** Comparison sayfaları tarih/source ve update loop olmadan riskli.
- **Autopublish cazibesi:** Autopublish kısa vadede ego okşar, uzun vadede domain yakar. Human gate olmadan scale yok.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **SEO inventory dosyası çıkar:** 113 ürün için kategori, canonical, checkout, README, schema readiness, sample availability, internal-link candidates.
2. **10 ürünlük POC seç:** Healthy + checkout + clear search intent + low factual risk kriteriyle.
3. **40 brief üret:** Her briefte keyword intent, source links, SERP gap, unique data block, internal links, CTA, QA checklist ve publish/noindex önerisi olsun.
