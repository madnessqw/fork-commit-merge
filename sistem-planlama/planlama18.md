# Planlama #18 — Türkiye + MENA Dijital Pazar Uygulama Haritası
**Tarih:** 2026-04-21 14:15 +03
**Bağlı Araştırma:** arastirma18.md

## Swarm Agent ile Nasıl Uygulanır?
Bu sistemin doğru adı “Türkiye e-ticaret SaaS'ı” değil. O laf fazla geniş ve gevşek. Doğru wedge: **TR/MENA Marketplace Ops Copilot** — Trendyol/Hepsiburada/Sahibinden/MENA satıcı operasyonundaki para kaçaklarını bulup aksiyona çeviren agent sistemi.

### Sistem Haritası
1. **Data Intake Agent**
   - İlk POC'de API yazmadan satıcıdan CSV/XLS export, ekran görüntüsü veya örnek order/question/return verisi alır.
   - Sonraki aşamada Trendyol/Hepsiburada API credential ile read-only bağlanır.
2. **Normalization Agent**
   - Ürün, SKU, stok, fiyat, sipariş, iade, kargo, soru, fatura ve ödeme kesintilerini ortak şemaya indirger.
3. **Leak Detection Agent**
   - Kargo deadline, geç cevap, stok/fiyat sapması, düşük marj SKU, iade riski, ödeme/kargo maliyeti ve kampanya zararını puanlar.
4. **Localization Agent**
   - Türkçe/İngilizce/Arapça müşteri mesajı taslakları üretir; tone/politeness ve lehçe riskini işaretler.
5. **Compliance Agent**
   - İYS/KVKK, pazaryeri API/ToS, sahibinden yetkili API, müşteri verisi ve outbound/transactional ayrımını kontrol eder.
6. **Human Gate**
   - Fiyat değiştirme, iade onayı, müşteriye mesaj, resmi cevap ve hukuki/ödeme etkili aksiyonlarda onay ister.
7. **Report & Sales Agent**
   - Günlük “bugün para kaybetmemen için 7 aksiyon” listesi ve haftalık “kâr kaçağı raporu” üretir.
8. **Growth Agent**
   - Aynı rapordan anonymized case study, landing page copy, cold outreach snippet ve demo hazırlığı çıkarır.

## Gerekli Bileşenler
- **Script/Bot:**
  - CSV/XLS importer
  - Marketplace data normalizer
  - Order/return/question/margin risk scorer
  - Daily action report generator
  - Turkish/Arabic customer answer drafter
  - Compliance checklist generator
  - Prospect list + personalized outreach draft generator
- **MCP/Araç:**
  - Jina Reader: pazaryeri dokümanı, rakip sayfaları, resmi kaynak okuma
  - Reddit JSON API: satıcı pain mining
  - GitHub/gh: connector ve SDK implementasyon sinyali
  - ArXiv MCP: Turkish/Arabic NLP ve agent localization araştırması
  - MCPTube: yerel satıcı/entegrasyon eğitimleri ve case study başlıkları
  - chrome-devtools-axi / Playwright: izinli satıcı panelinde gözlem ve QA
- **API:**
  - Trendyol Marketplace API
  - Hepsiburada Merchant API
  - sahibinden.com API: sadece yetkili kurumsal emlak/vasıta mağaza + EİDS entegre firma koşuluyla
  - iyzico Link / PayTR / Shopier / Param / Vepara vb. ödeme alma seçenekleri; ilk satışta manuel link daha gerçekçi
  - Kargo/e-fatura sağlayıcıları: ikinci fazda
- **İnsan Müdahalesi:**
  - İlk müşteri verisini alma ve gizlilik/onay kontrolü
  - API credential kurulumu
  - İlk 2 hafta rapor doğrulaması
  - Müşteri mesajları ve iade/fiyat aksiyonlarında onay
  - KVKK/İYS metni ve sözleşme taslağı için hukuki kontrol

## Workflow Haritası
Tetikleyici: haftalık / günlük marketplace ops cycle
→ satıcı export/API verisi alınır
→ ürün/sipariş/iade/soru/fatura/ödeme verisi normalize edilir
→ risk skorları hesaplanır
→ kâr kaçağı ve operasyon darboğazı bulunur
→ aksiyon listesi oluşturulur
→ müşteri soru/cevap taslakları hazırlanır
→ compliance gate çalışır
→ insan onayı gerekenler ayrılır
→ günlük rapor satıcıya teslim edilir
→ haftalık ROI/kayıp önleme raporu çıkarılır
→ case study/outreach materyali üretilir
→ sonraki müşteri için template iyileştirilir

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen hayata geçirilecek bulgu:** Entegrasyon paneli kurmadan **Pazaryeri Kâr Kaçağı Audit'i** sat. Satıcıdan son 30 gün CSV/XLS/screenshot al; ürün, sipariş, iade, müşteri soru ve kargo verisini elle/yarı otomatik analiz et; 24-48 saatte rapor teslim et.
- **En düşük çaba / en yüksek çıktı:** “Trendyol/Hepsiburada satıcıları için 10 maddelik para kaçağı raporu” landing + örnek PDF. Ücret: ilk validasyon için 1,500-3,000 TL tek seferlik veya ücretsiz ilk 3 audit + başarı hikayesi karşılığı.
- **Mevcut araç/script bu işi kısmen yapar mı?** Evet. UniverseCreator'ın araştırma/raporlama disiplini, browser/Jina/GitHub/Reddit kaynak taraması ve 113 ürünlük product-led dokümantasyon kası var. Kod yazmadan Google Sheets/Markdown raporuyla POC yapılabilir.
- **Minimum POC gereksinimleri:**
  1. 1 sayfalık “Pazaryeri Kâr Kaçağı Audit” teklif metni
  2. Satıcıdan istenecek veri listesi: ürün listesi, sipariş export, iade/claim export, müşteri soru export, kargo/fatura durumu, ödeme kesintisi örneği
  3. Rapor şablonu: en riskli 10 SKU, geciken 10 sipariş, cevaplanmamış 10 soru, iade/kargo/fatura riskleri, net aksiyonlar
  4. KVKK/İYS notu: müşteri kişisel verisi maskelensin; outbound mesaj yok; sadece satıcı operasyon raporu
- **Tahmini kurulum süresi:** 2 gün teklif + rapor şablonu; 2-3 gün ilk örnek rapor; 1 hafta içinde ilk gerçek satıcı audit'i yapılabilir.
- **İlk gelir beklentisi:** 1 müşteri × 1,500-3,000 TL audit mümkün. Aylık retainer'a dönüşirse 2,990-5,990 TL/ay aralığı, Pazaryeri Bot/Sopyo pricing envelope'ına göre gerçekçi. Bu tahmindir; satış yapılmadan gelir diye yazılmaz.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonu hedefi:**
  - 5-10 satıcıyla audit görüşmesi
  - 2-3 gerçek audit teslimi
  - En az 1 ücretli müşteri veya güçlü testimonial
  - Standart veri şeması ve rapor template'i
  - Trendyol read-only API POC veya export parser
  - “Günlük 7 aksiyon” raporu demo çıktısı
- **Başarı metric'leri:**
  - Audit teslim süresi <48 saat
  - Rapor başına en az 5 uygulanabilir aksiyon
  - Satıcının onayladığı somut kaçak/iyileştirme sayısı
  - Ücretli dönüşüm: ücretsiz/indirimli audit alanların %20+ retainer ilgisi
  - Support workload: rapor başına <2 saat manuel düzeltme
- **Paralel çalışabilecek adımlar:**
  - Bir agent pazar/lead listesi toplar.
  - Bir agent rapor şablonunu iyileştirir.
  - Bir agent Trendyol/Hepsiburada API dokümanını şema haritasına çevirir.
  - Bir agent Türkçe/Arapça Q&A prompt/eval seti hazırlar.
  - Bir agent compliance checklist üretir.
- **Ölçeklendirme için gerekenler:**
  - 1 read-only connector veya sağlam export parser
  - Düşük maliyetli hosting / cron / storage
  - Gizlilik ve veri işleme sözleşmesi
  - Satıcı onboarding formu
  - Basit müşteri paneli veya haftalık e-posta/Notion/Google Docs teslimatı
- **Checkpoint'ler:**
  - 2. hafta: örnek audit PDF tamam
  - 4. hafta: 2 gerçek audit
  - 6. hafta: read-only connector veya parser stabil
  - 8. hafta: 1 retainer müşteri
  - 12. hafta: 3-5 retainer veya wedge pivot kararı

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** Sistem Trendyol/Hepsiburada satıcısının operasyonunu her sabah tarar; kargo/iade/soru/stok/fiyat/fatura/kâr risklerini puanlar; düşük riskli aksiyonları otomatik yapar; yüksek riskli aksiyonları human approval'a yollar; haftalık ROI raporu üretir.
- **Yan ürünler / gelir kolları:**
  - TR Marketplace Ops Copilot SaaS
  - White-label pazaryeri audit ajansı
  - MENA localization audit: Arabic/Turkish customer ops + KSA/UAE address/payment/shipping checklist
  - Authorized Sahibinden emlak/vasıta portfolio analytics
  - E-ihracat readiness report: ürün, fiyat, ödeme, kargo, dil, iade, gümrük
  - Turkish/Arabic customer question answer QA dataset/eval pack
- **Swarm yaklaşımının farkı:** Rakipler tek panel + entegrasyon satıyor; swarm sistemi connector, risk scoring, localization, compliance, reporting, sales enablement ve measurement agentlarını ayrı ayrı çalıştırabilir. Bu “operasyon danışmanı + otomasyon” karışımıdır; düz SaaS'tan daha hızlı satılır.
- **White-label veya SaaS olur mu?** Evet, ama SaaS'a acele etmek kötü fikir. Önce service/audit ile problem doğrulanmalı. 10+ audit ve 3+ retainer olmadan panel inşa etmek ürün mezarlığına yeni mezar taşı dikmek olur.
- **MENA evrimi:** KSA/UAE için harita pin/adres normalizasyonu, Arabic politeness/tone gate, local payment/wallet/BNPL, cross-border delivery ve return workflow eklendikçe ürün “Türkiye satıcı ops”tan “regional commerce ops copilot”a büyüyebilir.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek. `sentez14.md` bu konuyu eksik tur diye işaretlemişti; pazar verisi ve yerel boşluk bunu doğruladı.
- **Kurulum Süresi:**
  - Audit-only POC: 3-7 gün
  - Export parser + rapor otomasyonu: 2-4 hafta
  - API connector + human-gated action system: 1-3 ay
- **Aylık İşletme Maliyeti:**
  - POC: $0-20
  - 1-5 müşteri: $10-50 LLM/hosting/tooling
  - Ödeme komisyonu: provider'a göre, community anekdotlarında TR sanal POS için genelde %2.5-4+ konuşuluyor; kesin teklif alınmadan sabit yazma.
- **Potansiyel Gelir:**
  - Tek sefer audit: 1,500-3,000 TL
  - Retainer: 2,990-5,990 TL/ay başlangıç
  - Daha büyük satıcı: 9,990-19,990 TL/ay danışmanlık + otomasyon
  - Bunlar tahmin; gerçek gelir yalnızca tahsilatla yazılır.
- **ROI Beklentisi:** 1 ücretli audit, POC maliyetini kapatır. Retainer modelinde 1 müşteri bile hosting/LLM maliyetini rahat karşılar; müşteri edinme süresi asıl darboğaz.

## Mevcut Sistemle Entegrasyon
- **UniverseCreator state:** `STATE_SUMMARY.json` / `STATE.json` cycle 1025'te **113 active / 113 healthy / balance 0.0**. Para harcamadan başlayan rapor-first model bu yüzden doğru.
- **113 ürünle birleşim:** Mevcut devtool portföyü doğrudan pazaryeri ops ürünü değil; ama landing page, report generator, CSV analyzer, invoice/checklist generator, API wrapper, prompt/eval tool gibi reusable asset'ler çıkarılabilir.
- **Swarm rol dağılımı:**
  - Researcher: satıcı segmenti, rakip, mevzuat, Reddit/YouTube pain toplar.
  - Codex: uygulama döngüsünde parser/rapor script'i yazar; bu turda yazmaz.
  - GLM/Analyst: fiyatlandırma, ROI, müşteri segmenti ve rapor kalitesi değerlendirir.
  - QA: veri maskelenmesi, hukuki risk, supported claim ve API ToS kontrolü yapar.
- **Satış kanalı:** Payment blocker çözülene kadar ilk satış manuel invoice/iyzico Link/PayPal/direct yöntemle planlanmalı; kullanıcı onayı olmadan dış outreach yok.

## Riskler & Dikkat Edilecekler
- **Generic entegrasyon paneli yapma.** Sopyo/ikas/Dopigo/Entegra/Pazaryeri Bot zaten burada. Connector commodity; karar/aksiyon katmanı sat.
- **Sahibinden scraping mayını.** Cloudflare koruması, resmi API şartları ve kurumsal/EİDS koşulu var. Public scraping'i ticari ürün omurgası yapma.
- **KVKK/İYS riski.** Müşteri verisi, çerez, pazarlama, ticari ileti ve açık rıza konuları net ayrılmalı. Rapor-first modelde kişisel veriyi maskele; outbound mesaj atma.
- **Repricing/collusion riski.** Otomatik fiyat önerisi kurarken rakip verisiyle fiyat sabitleme, buybox manipülasyonu veya platform taahhütlerine ters patternlerden uzak dur.
- **MENA localization'ı hafife alma.** Arabic dialect, politeness, address format, payment preference ve delivery behavior farklı. “Google Translate + WhatsApp bot” çöp olur.
- **Satıcı verisi kalitesi.** Export formatları dağınık; ilk sprintte robust parser değil, kontrollü template ve manuel normalize daha hızlıdır.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Audit teklifini yaz:** “Trendyol/Hepsiburada satıcıları için 24-48 saatte Kâr Kaçağı Raporu” — kapsam, veri listesi, örnek çıktı, gizlilik notu, fiyat aralığı.
2. **Rapor şablonunu üret:** SKU riski, kargo deadline, müşteri soru bekleme, iade/claim, fatura, ödeme komisyonu, net aksiyon ve tahmini etki bölümleri.
3. **10 prospect segmenti belirle:** moda/aksesuar, elektronik aksesuar, ev-bahçe, kozmetik, bebek/anne, araç aksesuarı, küçük üretici, Instagram+Trendyol satan marka, Dubai/UAE açılımı düşünen Türk marka, kurumsal emlak/vasıta mağazası. Her segment için farklı pain cümlesi yaz.
