# Planlama #9 — Browser Agent + Otomasyon Uygulama Haritası
**Tarih:** 2026-04-21 08:18 +03
**Bağlı Araştırma:** arastirma9.md

## Swarm Agent ile Nasıl Uygulanır?
UniverseCreator için doğru tasarım **Browser Ops Lane**: her ajan istediği siteye kafasına göre browser açmasın; browser işleri tek kontrollü hatta girsin.

Önerilen mimari:
1. **Browser Task Intake**
   - Giriş: hedef URL/domain, amaç, veri şeması, login gereksinimi, risk seviyesi, izinli aksiyonlar.
   - Her iş için `allowed_domains`, `forbidden_actions`, `max_cost`, `human_gate` zorunlu.
2. **Route Classifier**
   - `API-first`: XHR/API varsa browser yok.
   - `Static scrape`: HTML/Jina/requests yeterliyse browser yok.
   - `Deterministic browser`: Playwright / chrome-devtools-axi / Playwright MCP.
   - `AI-augmented`: Stagehand veya Skyvern, sadece layout bilinmiyor veya çok portal varyasyonu varsa.
   - `Human-in-loop`: login, ödeme, 2FA, hesap riski, submit/post gibi aksiyonlarda durur.
3. **Browser Executor Pool**
   - Local: chrome-devtools-axi, Playwright MCP, Chrome DevTools MCP.
   - Cloud: Browserbase veya Skyvern; sadece concurrency, proxy, recording veya remote isolation gerekiyorsa.
4. **Credential & Session Vault**
   - LLM'e şifre gösterilmez.
   - Domain bazlı session profile tutulur.
   - 2FA ve ödeme adımlarında insan kapısı.
5. **Extractor / Normalizer**
   - Sayfa çıktısını strict JSON schema'ya çevirir.
   - Evidence: screenshot, snapshot, source URL, timestamp, extracted fields.
6. **Verifier**
   - Sayfa state assertion, schema validation, duplicate check, sanity check, retry.
   - Başarı kanıtı yoksa “done” sayılmaz.
7. **Cost & Risk Ledger**
   - Session dakika, step sayısı, proxy GB, retry, failure reason, blocked domain, human review sayısı yazılır.
8. **Reporter / Productizer**
   - Müşteri/ürün çıktısı: CSV/JSON/report/screenshot proof.
   - İç çıktı: ürün QA, rakip fiyat, lead listesi, portal veri çekimi.

## Gerekli Bileşenler
- **Script/Bot:**
  - browser task intake form / markdown şablonu
  - route classifier
  - Playwright/Chrome runner wrapper
  - JSON schema extractor
  - evidence saver
  - cost ledger
  - retry/backoff/dedupe helper
  - human approval checkpoint
- **MCP/Araç:**
  - chrome-devtools-axi: local Chrome kontrolü için ilk tercih
  - Playwright MCP: snapshot/ref tabanlı browser automation
  - Chrome DevTools MCP: JS execution, console/network debugging
  - windows-mcp: OS-level fallback
  - Jina/curl: browser açmadan okuma
  - MCPTube/ArXiv/Jina: workflow research ve doküman takip
- **API:**
  - başlangıçta zorunlu yok
  - opsiyonel: Browserbase Developer **$20/ay**, Browser Use API, Skyvern Hobby **$29/ay**
  - gerekirse proxy/stealth için Browserbase/Skyvern/Bright Data benzeri provider
- **İnsan Müdahalesi:**
  - ilk login/session kurulumu
  - 2FA / CAPTCHA / ödeme / submit gibi irreversible aksiyonlar
  - TOS/spam riski değerlendirmesi
  - müşteri deliverable kalite onayı

## Workflow Haritası
Tetikleyici
→ browser task intake oluşturulur
→ route classifier API/HTML/browser/AI-browser yolunu seçer
→ gerekirse session/credential profile yüklenir
→ executor görevi çalıştırır
→ extractor structured output üretir
→ verifier çıktı + evidence kontrol eder
→ başarısızsa daha düşük maliyetli retry veya human handoff
→ başarılıysa report/CSV/JSON/alert üretilir
→ cost/risk ledger ve memory güncellenir

Örnek workflow — rakip fiyat izleme:
Liste URL'leri
→ önce HTTP/API kontrol
→ dinamikse Playwright snapshot
→ fiyat/stock/schema extract
→ tarihsel fiyat DB/CSV
→ anomali eşiği
→ Telegram/email alert
→ haftalık müşteri raporu

Örnek workflow — supplier portal invoice download:
Schedule
→ headed persistent browser profile
→ login state kontrol
→ invoice sayfasına git
→ PDF indir
→ checksum + OCR/metadata
→ Drive/local klasöre kaydet
→ müşteri raporu
→ 2FA gerekiyorsa human checkpoint

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen yapılacak en mantıklı POC:** UniverseCreator için **Browser Ops Lane v0** kurmak: `API-first → Playwright/Chrome → AI fallback` karar ağacı ve 2-3 pilot workflow.
- **En düşük çaba / en yüksek çıktı adımı:** mevcut ürünlerin ve dış hedeflerin **browser QA + fiyat/stock/lead extraction** için tek task şablonuna alınması. Yeni framework satın almadan, local chrome-devtools-axi + Playwright MCP ile başlanır.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - chrome-devtools-axi zaten available ve AGENTS.md'ye göre ilk tercih.
  - Playwright MCP mevcut.
  - Chrome DevTools MCP mevcut.
  - Jina/curl + ddgr zaten araştırma hattında kullanılıyor.
  - `projeler.txt` içinde Browser-Use/Skyvern/Stagehand kaynakları hazır.
- **Proof-of-concept için minimum gereksinimler:**
  1. 10 hedef URL/domain listesi
  2. her hedef için output schema
  3. max cost/time/retry kuralı
  4. evidence klasörü: screenshot + snapshot + extracted JSON
  5. verifier: schema + sanity check
- **Tahmini kurulum süresi ve ilk gelir beklentisi:**
  - Kurulum: **3-5 gün** task şablonu + 2 pilot workflow; **7-10 gün** müşteri-ready demo.
  - İşletme maliyeti: local koşuda **$0-$20/ay**; cloud deneme ile **$20-$75/ay**.
  - İlk gelir: dar bir “rakip fiyat/stock monitoring” veya “supplier portal invoice download” paketi **$300-$1,000/ay** aralığında satılabilir; 1 müşteriyle cloud maliyeti rahat kapanır.
- **Kısa vade hükmü:** Browser agent'ı ürün değil, **müşteri acısını çözen görünmez işçi** yap. Aksi demo mezarlığı.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonunda:**
  - 3 çalışan workflow: ürün QA/checkout health, rakip fiyat/stock izleme, portal document/download veya contact-form enrichment.
  - Her run evidence üretiyor.
  - Cost ledger var: session dakika, step, retry, failure reason.
  - İnsan kapısı olan login/2FA akışı tanımlı.
- **2-3 ay sonunda:**
  - Browser Ops Lane dashboard'u: success rate, fail reason, cost/run, average runtime, extraction quality.
  - Cloud browser seçimi yapılmış: Browserbase veya Skyvern; aynı anda ikisiyle oynamak maliyetli dikkat dağınıklığı.
  - 5-10 vertical template: e-commerce price monitor, real-estate listing monitor, local business lead enrichment, supplier invoice download, product QA crawler.
- **Hangi metric'ler başarıyı gösterir?**
  - successful runs / total runs
  - verified extraction rate
  - cost per successful extraction
  - retry rate
  - human intervention rate
  - blocked / captcha / login failure rate
  - time saved per workflow
  - customer-reported usefulness
- **Hangi adımlar paralel çalışabilir?**
  - template seçimi
  - Playwright runner hardening
  - output schema katalogu
  - dashboard / ledger
  - pilot müşteri landing copy / sample reports
- **Ölçeklendirme için ne gerekiyor (insan, araç, bütçe)?**
  - cloud browser budget: **$20-$149/ay** başlangıç
  - domain bazlı proxy/credential policy
  - daha iyi observability
  - workflow başına maintenance owner
  - müşteriye SLA vermeden önce 2 hafta run stability testi
- **Checkpoint'ler ve başarı kriterleri:**
  1. Hafta: route matrix + task schema + 2 pilot
  2. Hafta: evidence + verifier + retry
  4. Hafta: 3 workflow stable, cost/run ölçülüyor
  8. Hafta: 1 dış müşteri veya iç gelir etkisi olan workflow
  12. Hafta: 5 template + dashboard + paket fiyatları

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator, browser-based repetitive ops için “managed automation layer” olur. İnsanların portalda yaptığı sıkıcı işlerin çoğunu düşük maliyetle ve kanıtlı şekilde yapar; sadece riskli adımlarda insan çağırır.
- **Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?**
  - vertical monitoring SaaS: e-commerce fiyat/stok, real estate listing, B2B supplier portal
  - browser workflow template marketplace
  - browser QA/checkout monitoring as a service
  - managed data extraction paketleri
  - “legacy portal API wrapper” ürünleri: portalı gezip JSON API gibi sunma
  - n8n/Make/Skyvern template satışları
- **Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek nedir?**
  - araştırma → workflow tasarımı → browser execution → verification → rapor → memory loop tek hatta birleşir
  - tek framework'e kitlenmeden route eder: API varsa API, browser gerekiyorsa browser, AI gerekiyorsa AI
  - her workflow'un evidence ve cost izi tutulur; bu, ajans çöplüğünde ciddi ayrışma yaratır
  - çok-model/çok-agent sistemi browser workflow maintenance'ı da yapabilir: hata gördüğünde selector/route/guardrail önerir
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet. İlk faz managed service.
  - İkinci faz white-label automation reports.
  - Üçüncü faz self-serve workflow templates.
  - Dördüncü faz browser workflow API / legacy portal wrapper SaaS.
- **3-12 ay evrim sırası:**
  1. İç Browser Ops Lane
  2. 3 stable template
  3. İlk müşteri / ilk recurring fee
  4. Dashboard + alerting
  5. Template marketplace veya white-label panel
  6. Cloud browser + proxy + credential vault standardizasyonu

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** POC **3-10 gün**, müşteri-ready sistem **4-8 hafta**, template portföyü **3 ay**
- **Aylık İşletme Maliyeti:**
  - local-only: **$0-$20**
  - Browserbase Developer / Skyvern Hobby / Browser Use credits: **$20-$75**
  - Pro/concurrency + proxy: **$99-$300+**
- **Potansiyel Gelir:**
  - single workflow managed service: **$300-$1,000/ay**
  - multi-portal ops package: **$1,000-$3,000/ay**
  - setup fee: **$500-$2,000**
  - template satışları: **$19-$199** tekil veya bundle
- **ROI Beklentisi:**
  - 1 müşteri = altyapı maliyeti aynı ay kapanır.
  - İç kullanımda ürün QA/checkout/fiyat monitoring kırıkları yakalarsa 2-4 hafta içinde zaman tasarrufu sağlar.
  - Break-even için en iyi yol pahalı SaaS inşa etmek değil, **tek vertical workflow satmak**.

## Mevcut Sistemle Entegrasyon
- AGENTS.md zaten doğru tool hiyerarşisini söylüyor: **chrome-devtools-axi first**, sonra Playwright MCP, Chrome DevTools MCP, windows-mcp fallback. Bu Browser Ops Lane için hazır temel.
- UniverseCreator'ın mevcut ürün fabrikası için 3 doğrudan entegrasyon:
  1. **Ürün QA crawler:** ürün sayfası açılır, pricing/checkout/CTA görünür mü, console error var mı, screenshot alınır.
  2. **Rakip/market monitor:** seçili domainlerde fiyat/stok/offer çıkarılır, haftalık rapor olur.
  3. **Lead/contact enrichment:** Google Maps / directory / site contact form / LinkedIn gibi riskli alanlarda API-first + browser fallback uygulanır; spam submit yok.
- `projeler.txt` içinde Browser-Use, Skyvern, Stagehand ve Crawlee zaten listelenmiş. Yani araştırma malzemesi dışarıda değil, sistemin hafızasında da var.
- Mevcut araştırma cycle'larıyla bağ:
  - Lead Generation (#1): browser fallback ile zenginleşir
  - E-commerce (#6): fiyat/stok/listing monitor olur
  - Voice AI + Sales Funnel (#7): form doldurma/CRM portal update bağlanır
  - Multi-Agent Architecture (#8): Browser Ops Lane deterministic worker olarak orkestrasyona eklenir

## Riskler & Dikkat Edilecekler
- **Spam riski:** otomatik job apply / contact form blasting gibi işler kısa vadede “çalışır”, uzun vadede sistemi çöpe çevirir. Consent ve rate limit olmadan yapılmaz.
- **TOS/account ban riski:** LinkedIn, Facebook Marketplace, Amazon gibi hedefler agresif bot detection yapar. Hesap değerliyse human-in-loop ve düşük hız şart.
- **Maliyet patlaması:** kısa görevlerde cloud browser 1 dakika minimum billing yüzünden pahalılaşır. Session reuse/batching şart.
- **Selector kırılması:** deterministic Playwright ucuz ama kırılır; Stagehand/Skyvern AI fallback sadece kırılma maliyeti yüksekse kullanılır.
- **CAPTCHA/2FA:** teknik bypass etik/legal değildir. 2FA'da insan onayı, CAPTCHA'da domain/risk kararı.
- **Secret exposure:** browser logs/screenshots credential sızdırabilir. Redaction ve evidence scope şart.
- **Benchmark sarhoşluğu:** WebVoyager skorları gerçek portal SLA'sı değildir. Her workflow kendi hedef sitesinde test edilir.
- **Overengineering:** ilk hafta Browserbase/Skyvern/Browser Use hepsini bağlamaya çalışma. Bu oyuncak koleksiyonculuğu olur. Tek lane, tek pilot, tek müşteri acısı.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Browser task schema + route matrix yaz:** API-first / static / deterministic / AI-browser / human-gate sınıfları netleşsin.
2. **İki POC seç:** biri iç ürün QA/checkout health, biri dış değer üreten fiyat/stock veya portal document extraction.
3. **Evidence + cost ledger zorunlu kıl:** her browser run screenshot/snapshot/JSON/cost/failure reason yazmadan “tamam” sayılmasın.
