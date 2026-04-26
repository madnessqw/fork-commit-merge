# Planlama #16 — Ticari İstihbarat & HS Codes Uygulama Haritası
**Tarih:** 2026-04-21 12:19
**Bağlı Araştırma:** arastirma16.md

## Swarm Agent ile Nasıl Uygulanır?

Bu sistemin doğru ilk versiyonu **dashboard değil, karar raporu fabrikası**. Trade-intelligence SaaS yapmak ilk günden güzel görünen ama para yakan fikir. Doğru wedge: **GTIP/HS Opportunity Snapshot + Tariff Shock Note + Buyer Map**.

### Önerilen swarm rolleri
1. **Lead Intake Agent**
   - Ürün adı, açıklama, mevcut GTIP/HS, hedef ülke ve kullanım amacı alır.
   - Kullanıcıyı üç lane'den birine sokar: `pazar fırsatı`, `tarife şoku`, `buyer/supplier bulma`.

2. **HS Hypothesis Agent**
   - 2/4/6 haneli adayları çıkarır.
   - Belirsizlik varsa 3 alternatif verir; tek kod dayatmaz.
   - Confidence ve açıklama üretir.

3. **Official Source Agent**
   - WCO, Türkiye Ticaret Bakanlığı, WTO TTD, WITS, U.S. Census, ITA gibi resmi katmanları toplar.
   - Her veri noktasına kaynak tarihi bağlar.

4. **Market Intelligence Agent**
   - Hacim, büyüme, ülke yoğunluğu, CIF/value trendi ve erişilebilirlik skoru çıkarır.
   - “Bu HS için önce hangi 3 ülkeye bakmalı?” sorusunu cevaplar.

5. **Buyer Map Agent**
   - Public veriden buyer hipotezi, sektör segmentleri, directory/association/LinkedIn arama sorguları üretir.
   - Paid shipment data varsa bunu company listesine çevirir; yoksa discovery query pack verir.

6. **Tariff & Risk Agent**
   - Tarife, non-tariff, compliance ve volatility notu çıkarır.
   - Tariff shock varsa raporun kapağına taşır.

7. **Compliance QA Agent**
   - “Final authority customs office” uyarısını zorunlu tutar.
   - Lisans, ham veri paylaşımı ve confidence sınırını kontrol eder.

8. **Composer / Delivery Agent**
   - Markdown → PDF/CSV/TXT teslim paketini çıkarır.
   - Mevcut ProfitBridge paketlerine göre fiyat etiketini bağlar.

## Gerekli Bileşenler

- **Script/Bot:**
  - HS intake formu
  - resmi veri fetcher katmanı
  - opportunity/tariff scoring scripti
  - rapor composer
  - buyer query pack üretici

- **MCP/Araç:**
  - ArXiv MCP — classifier/compliance literatürü
  - MCPTube — vendor workflow transkriptleri
  - Browser/scraping stack — WITS/WTO/ITA/Türkiye sayfaları
  - mevcut browser-use / crawlee-python / Scrapeless sinyalleri

- **API:**
  - U.S. Census HS imports API — ücretsiz başlangıç
  - WITS / WTO TTD — resmi veri katmanı
  - opsiyonel ImportGenius / UN Comtrade premium — yalnız doğrulanmış ödeme sonrası

- **İnsan Müdahalesi:**
  - şüpheli HS/GTIP vakalarında son kontrol
  - ilk müşteri teslimatlarında QA
  - dışarı giden outreach'in onayı
  - ticari ve vergisel çerçevenin onayı

## Workflow Haritası

`intake` → `HS adayları` → `resmi veri çek` → `pazar/tarife skoru üret` → `buyer/supplier hipotezi çıkar` → `QA/disclaimer` → `PDF/CSV teslim` → `upsell: aylık GTIP watch / white-label danışmanlık`

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

### Hemen uygulanabilir ürün
**GTIP Opportunity Snapshot**
- 1 HS / 1 ülke / 24 saat teslim PDF
- İçerik:
  - HS/GTIP adayları + confidence
  - son resmi hacim verisi
  - ülke önceliği / tarife notu
  - buyer bulma stratejisi
  - 3 outreach mesajı
  - zorunlu compliance disclaimer

### En düşük çaba / en yüksek çıktı adımı
- Önce 4 örnek lane hazırla:
  1. **HS 570242 — Türkiye halı → ABD**
  2. **HS 870899 — otomotiv parçası → ABD**
  3. **HS 080222 — fındık → ABD**
  4. **HS 610910 — tekstil / tariff-sensitive lane**
- Bunlar hem resmi API ile beslenebiliyor hem de satış konuşmasına dönüşüyor.

### Hangi mevcut araç/script bu işi kısmen yapar?
- Resmi kaynak toplama için mevcut browser/scraping kası yeterli.
- ArXiv + MCPTube + Jina araştırma katmanı zaten hazır.
- ProfitBridge tarafındaki mevcut fiyat mantığı birebir uyuyor:
  - **A1 $19** → mini snapshot
  - **A2 $39** → standart rapor
  - **A3 $79** → buyer map + outreach pack
  - **A4 $499** → çoklu HS / agency white-label paket

### Proof-of-concept minimum gereksinimler
- tek rapor template'i
- 4 örnek rapor
- 20 hedef prospect (ihracat danışmanı / freight forwarder / küçük ihracatçı)
- Türkçe + İngilizce 2 outreach taslağı
- manuel teslim + geri bildirim formu

### Tahmini kurulum süresi ve ilk gelir beklentisi
- Kurulum: **3-5 gün**
- İlk satış testi: **7 gün içinde**
- İlk gelir beklentisi: **$39-$237** arası gerçekçi; iyi senaryoda ilk agency paketinden **$499**
- Break-even: ücretsiz veriyle **tek satışta**

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

### 1. ay sonunda hedef görünüm
- 20+ hazır HS lane cache'i
- 1 haftalık GTIP watch üretimi
- 100+ prospect listesi
- 5+ örnek teslimat veya 3 ciddi discovery görüşmesi
- rapor üretim süresi **90 dakikanın altına** düşmüş olmalı

### Başarı metric'leri
- `report_time_minutes < 90`
- `first_response_rate > %5`
- `paid_conversion > %2-3`
- `hs_confidence_flag_rate` takip edilmeli
- aylık gelir hedefi: **$500-$2,500** productized service bandı

### Paralel çalışabilecek adımlar
- bir ajan yeni HS lane çıkarır
- biri prospect / buyer query pack hazırlar
- biri tarife/risk katmanını günceller
- biri QA/disclaimer standardını korur

### Ölçeklendirme için ne gerekiyor?
- **İnsan:** gerektiğinde customs broker veya trade danışmanı review slotu
- **Araç:** ödeme doğrulanınca ImportGenius veya eşdeğer dataset denemesi
- **Bütçe:** pilotta **$0-$80/ay**, validated sonrası **$229-$449/ay** veri aracı düşünülebilir
- **Süreç:** rapor şablonu + scoring rubric + QA checklist

### Checkpoint'ler
- **2. hafta:** 4 demo rapor + 20 outreach hedefi
- **4. hafta:** ilk ödeme veya güçlü LOI sinyali
- **8. hafta:** hangi lane daha çok cevap veriyor belli olmalı
- **12. hafta:** recurring watchlist mi, white-label ajans mı karar verilmiş olmalı

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

### En iyi senaryo
- Sistem seçili HS kümeleri için haftalık olarak:
  - hacim kayması
  - tarife değişimi
  - buyer/supplier sinyali
  - outreach önerisi
  üretir.
- İnsan yalnız high-risk classification ve satış kapanışında devreye girer.

### Yeni gelir kolları
- **GTIP Watch Subscription:** $49-$199/ay
- **Tariff Shock Alert:** spesifik HS/ülke alarm servisi
- **Buyer Discovery Pack:** sektör/ülke bazlı arama sorguları + listeler
- **White-label trade desk:** danışmanlar ve freight forwarder'lar için markasız rapor motoru
- **SEO long-tail library:** HS bazlı içerik ve lead capture sayfaları

### Rakiplerin yapamadığı, swarm'ın yapabileceği şey
- Rakip platformlar veriyi gösteriyor; swarm **karar + aksiyon** üretiyor.
- “Bu HS büyüyor mu?” değil; **“hangi ülkeye git, kimi hedefle, nasıl yaz, nerede risk var?”** cevabını paketliyor.
- Her lane agentik olarak test edilip reply/satış verisine göre önceliklendirilebilir.

### White-label veya SaaS olarak satılabilir mi?
- **Evet, ama hemen değil.**
- İlk 3 ay productized service
- 3-6 ay white-label report engine
- 6-12 ay self-serve GTIP intelligence portal
- Ham veri lisansı çözülmeden full self-serve shipment SaaS'a atlamak gereksiz risk

## Öncelik & Çaba Tahmini

- **Öncelik:** Yüksek
- **Kurulum Süresi:** 3-7 gün POC, 2-4 hafta yarı-otomatik sistem
- **Aylık İşletme Maliyeti:**
  - pilot: **$0-$80**
  - validated: **$229-$449** + opsiyonel enrichment
- **Potansiyel Gelir:**
  - ilk ay: **$200-$1,500**
  - 3-6 ay: **$1,000-$5,000/ay**
  - iyi vertical fit ile 6-12 ay: **$3,000-$12,000/ay**
- **ROI Beklentisi:** ücretsiz veri ile hemen; paid data'ya geçildiyse **1 A4** veya **3-6 A3** satışta break-even

## Mevcut Sistemle Entegrasyon

- Bu iş mevcut swarm'ın araştırma kasına tam oturuyor: araştırma, scoring, compose, QA zinciri zaten var.
- 113 ürünlük mevcut tool portföyüne yeni deploy olarak değil, **bilgi ürünü / servis lane'i** olarak eklenmeli.
- Vercel veya yeni product build gerekmiyor; ilk aşamada teslimat dosya tabanlı olabilir.
- ProfitBridge fiyat yapısı hazır; ödeme sağlayıcı tarafı oturunca bu raporlar doğal ilk monetization lane olur.

## Riskler & Dikkat Edilecekler

- Yanlış HS/GTIP önerisi hukuki sorun yaratabilir.
- “Legal advice” tonu yasak; ürün ticari zekâ + classification assist olmalı.
- Ham veri redistribüsyonu lisans riski taşır; dönüştürülmüş insight daha güvenli.
- Tarife ve ülke-özel alt kodlar değişken; veri tarihi zorunlu gösterilmeli.
- Çok erken stage'de paid dataset almak aptallık olur; önce satış sinyali.
- ProductHunt / shiny-tool avı bu konuda ana sinyal değil; resmi veri + satış konuşması daha önemli.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Dört demo rapor çıkar:** 570242, 870899, 080222, 610910 lane'leri için aynı formatta örnek oluştur.
2. **GTIP report template'i kilitle:** A1/A2/A3/A4 paketleriyle eşleşen tek bir teslimat şablonu hazırla.
3. **20 hedefe satış testi yap:** ihracat danışmanları, freight forwarder'lar ve küçük üreticiler için Türkçe/İngilizce teklif mesajlarını hazırla; gönderim insan onayına bağlı kalsın.
