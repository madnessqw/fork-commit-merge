# Planlama #6 — E-commerce Automation Uygulama Haritası
**Tarih:** 2026-04-21 05:51 +03
**Bağlı Araştırma:** arastirma6.md

## Swarm Agent ile Nasıl Uygulanır?
Bu işi “genel e-commerce agency” diye değil, **seller operations control plane** diye kurmak lazım. Üç lane var: Shopify ops, Amazon ops, Etsy ops. Üstte ortak intelligence ve QA katmanı oturur.

1. **Marketplace Scanner Agent**
   - Hedef mağazayı/seller'ı inceler.
   - App sprawl, inventory körlüğü, pricing disiplinsizliği, listing throughput ve review yoğunluğunu tespit eder.
2. **Ops Audit Agent**
   - 1 sayfalık audit üretir: hangi görev native tool ile çözülür, hangisi custom workflow ister, kaç saat tasarruf çıkar, hangi tool iptal edilebilir.
3. **Shopify Workflow Agent**
   - Flow templateleriyle low-stock alerts, VIP tags, abandoned checkout, vendor notifications gibi işleri eşler.
4. **Amazon Guardrail Agent**
   - Repricing stratejilerini yaşlanan stok mantığıyla kurar.
   - Min/max floor, liquidation threshold, buy-box agresifliği ve exception kuyruğu üretir.
5. **Etsy Draft Listing Agent**
   - Fotoğraftan structured listing draft üretir.
   - Tag/keyword/alt-text akışını hazırlar.
   - Asla direkt publish etmez; insan onayı ister.
6. **Review Intelligence Agent**
   - Marketplace yorumlarını ve Q&A sinyallerini toplar.
   - En sık şikâyet, feature request ve dil kalıplarını çıkarır.
7. **ROI Reporter Agent**
   - Haftalık olarak şu soruya cevap verir: kaç saat tasarruf, kaç app iptal, kaç stockout önlendi, pricing hatası azaldı mı, listing throughput arttı mı?
8. **Human Seller Gate**
   - Publish, liquidation, aggressive repricing, refund/review automation ve policy-riskli kararlar burada insan onayından geçer.

## Gerekli Bileşenler
- **Script/Bot:**
  - seller ops audit generator
  - Shopify Flow template mapper
  - Amazon repricing guardrail calculator
  - Etsy photo-to-draft listing builder
  - review clustering / complaint summarizer
  - weekly ROI report generator
  - exception queue / human approval tracker
- **MCP/Araç:**
  - Browser automation / Playwright / Chrome DevTools: mağaza akışı ve competitor gözlemi
  - GitHub araştırması: Shopify/Amazon/Etsy starter repo'ları
  - ArXiv MCP: demand forecasting / dynamic pricing / review NLP pattern'leri
  - MCPTube: gerçek workflow breakdown'ları
  - İç tarafta `browser-use`, `crawlee-python`, Scrapeless benzeri mevcut araştırma altyapısı
- **API:**
  - Shopify Admin / Shopify Flow
  - Amazon Seller Central + gerekirse SP-API
  - Etsy Open API v3
  - Make veya n8n orkestrasyonu
  - OpenAI / uygun LLM
  - Google Sheets / Drive / Slack / Telegram / email provider
- **İnsan Müdahalesi:**
  - pricing floor ve liquidation kararı
  - taxonomy / shipping / category doğrulaması
  - publish öncesi son QA
  - review/request policy kontrolleri
  - müşteri iletişimi ve satış

## Workflow Haritası
Tetikleyici: yeni seller veya yeni mağaza audit'i
→ mağaza / marketplace taraması
→ problem sınıflandırma (Shopify app-sprawl / Amazon repricing / Etsy listing throughput)
→ lane seçimi
→ template veya workflow taslağı üretimi
→ maliyet / tasarruf / risk hesabı
→ insan onayı
→ draft implementasyon
→ QA testleri
→ rollout
→ haftalık rapor ve optimizasyon backlog'u

Alt akışlar:
- **Shopify:** event → Flow template → tag / notification / email / sheet sync
- **Amazon:** report / inventory age → repricing rule → exception queue → manual override
- **Etsy:** photo upload → vision + structured fields → draft listing → alt text → human review → publish

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **En düşük çaba / en yüksek çıktı adımı:** **Shopify Ops Cleanup Pack**. Sebep basit: Flow ücretsiz, native, ve merchant pain çok görünür. “6 app'i 2-3 workflow + 1 rapor katmanına indiriyoruz” teklifi, full custom e-commerce otomasyondan daha hızlı satılır.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - araştırma stack'i: browser-use / crawlee / Playwright ile mağaza akışı incelemesi
  - resmi taraf: Shopify Flow template kütüphanesi
  - raporlama için Sheets/Slack/Email
- **Proof-of-concept için minimum gereksinimler:**
  - 1 mağaza tipi (Shopify) seç
  - 5 hazır Flow use case'i çıkar: low stock, VIP tagging, abandoned checkout, vendor notify, fraud/review queue
  - 1 audit şablonu yaz
  - 1 ROI tablosu hazırla (app maliyeti + tahmini saat tasarrufu)
  - 1 demo ekran akışı hazırla
- **Tahmini kurulum süresi:** 4-6 gün araştırma + template mapping, 2-3 gün demo/paketleme.
- **İlk gelir beklentisi:** gerçekçi başlangıç **$300-$1,500 setup** ve **$100-$500 aylık bakım**. İlk haftada unicorn hayali kurmak boş iş.
- **Kısa vade tezi:** önce Shopify tarafında “tool azaltma + task otomasyonu” sat. Amazon/Etsy’yi ikinci dalgada aç.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay görünümü:**
  - 1 Shopify cleanup teklifi canlı
  - 1 Amazon repricing/aging audit teklifi canlı
  - 1 Etsy draft listing factory POC hazır
  - 10-20 seller audit'i tamamlanmış
  - 2-3 pilot müşteri veya net reddedilme gerekçeleri listelenmiş
- **Başarı metrikleri:**
  - iptal edilen app sayısı / mağaza
  - düşen aylık tool maliyeti
  - stockout warning accuracy
  - pricing override gerektiren SKU oranı
  - draft listing başına insan düzeltme süresi
  - haftalık listing throughput artışı
  - ROI raporunun okunma / kabul edilme oranı
- **Paralel çalışabilecek adımlar:**
  - biri audit çıkarır
  - biri Shopify template mapping yapar
  - biri Amazon age bucket mantığını yazar
  - biri Etsy draft schema'sını kurar
  - biri review intelligence özetlerini çıkarır
- **Ölçeklendirme için gerekenler:**
  - ortak veri modeli
  - policy checklist
  - exception queue
  - müşteri-facing dashboard veya en azından net rapor formatı
  - template versioning
- **Checkpoint'ler:**
  - Hafta 2: Shopify pack net
  - Hafta 4: Amazon repricing audit hazır
  - Hafta 6-8: Etsy draft listing POC
  - Hafta 12: üç lane için tekrar eden playbook

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** seller'lara proje bazlı otomasyon kuran ekip olmaktan çıkıp, **cross-marketplace ops cockpit**'e dönüşmek. Tek ekranda listing health, repricing state, inventory age, review themes, weekly ROI, manual approval queue görünür.
- **Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?**
  - review intelligence dashboard
  - listing draft API
  - marketplace ops audit report
  - inventory aging alert SaaS'i
  - repricing guardrail engine
  - seller ops template library
  - agency-facing white-label cockpit
- **Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek nedir?**
  - üç marketplace'i tek düşünce sistemiyle izlemek
  - satıcıya göre farklı lane'leri aynı raporda birleştirmek
  - araştırma + draft + QA + raporu paralel agent'larla ucuzlatmak
  - policy risklerini hafızada tutup tekrar hata yapmamak
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet. Ama önce managed service ile desen doğrulanmalı. Erken self-serve SaaS hevesi çoğu zaman duvara tosluyor.
- **Uzun vade hedefleri:**
  - 5-10 aktif seller veya 2-3 agency partner
  - 3 marketplace için reusable template kütüphanesi
  - publish öncesi hata oranını ciddi düşüren QA katmanı
  - MRR bandı: **$3K-$15K** başlangıçta gerçekçi; ürünleşirse üstü gelir

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek. Çünkü bu konu content/leadgen/local automation araştırmalarını somut, doğrudan para ödeyen seller operasyonuna çeviriyor.
- **Kurulum Süresi:**
  - Shopify Cleanup Pack: 1 hafta
  - Amazon guardrail audit: +1-2 hafta
  - Etsy draft listing factory: +2-4 hafta
  - ortak cockpit: 1-3 ay
- **Aylık İşletme Maliyeti:**
  - Lean başlangıç: **$50-$250/ay**
  - Çok kanallı ve LLM yoğun akış: **$200-$800/ay**
- **Potansiyel Gelir:**
  - tek mağaza audit/setup: **$300-$1,500**
  - aylık bakım: **$100-$1,000**
  - 5 müşteriyle ilk anlamlı bant: **$2K-$5K MRR**
- **ROI Beklentisi:** 1-2 iyi müşteriyle break-even mümkün. Ama Amazon/Etsy tarafında kötü otomasyon, yanlış fiyattan daha pahalıya mal olur; kâr marjını guardrail belirler.

## Mevcut Sistemle Entegrasyon
- UniverseCreator zaten araştırma, scraping, browser gözlemi, raporlama ve çoklu agent koordinasyonunda iyi. `projeler.txt` içindeki browser-use / crawlee / scrapeless sinyali bu iş için doğrudan altyapı avantajı.
- Vercel portföyü ileride dashboard demo, audit landing page ve müşteri portalı için kullanılabilir.
- Swarm rol dağılımı doğal:
  - researcher → seller pain / rakip / tool araştırması
  - analyst → maliyet / ROI / lane önceliklendirme
  - builder → ileride template ve dashboard prototipi
  - qa-tester → edge-case ve policy kontrolü
  - skill-writer → Shopify/Amazon/Etsy playbook'ları
- Şu an araştırma modundayız; yani entegrasyon fikri çıkarıldı ama implementasyon, deploy veya commit yapılmadı.

## Riskler & Dikkat Edilecekler
- **Marketplace ToS riski:** scraping, review request automation, messaging ve bulk changes yanlış yapılırsa hesap başına bela olur.
- **Repricing manyaklığı:** buy-box kovalamak uğruna marjı gömmek çok kolay.
- **Etsy publish riski:** kategori/shipping/readiness hataları draft'ta yakalanmazsa seller'ı rezil eder.
- **Kredi / token maliyeti:** Make ve LLM kullanımında sessiz sızıntı olur.
- **AI-generated listing spam'i:** title/tag otomasyonu kolayca çöp SEO üretir.
- **Temu tarafı şimdilik sisli:** API/control yüzeyi belirsiz; ilk sürümde Shopify/Amazon/Etsy yeter.
- **“Tam otomatik” yalanı:** insan onaysız publish veya liquidation kurgusu erken aşamada aptallık olur.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **İlk lane'i kilitle:** Shopify Ops Cleanup Pack'i canonical başlangıç paketi olarak seç; 5 net Flow use case'i ve 1 ROI tablosu yaz.
2. **Ortak veri şemasını çıkar:** product / inventory / order / review / listing draft / approval queue alanlarını tek tabloda tanımla.
3. **Seller audit listesi hazırla:** 10 Shopify, 10 Amazon, 10 Etsy örneği için pain map çıkar; hangisinde app-sprawl, hangisinde repricing, hangisinde listing throughput ağır basıyor gör.
