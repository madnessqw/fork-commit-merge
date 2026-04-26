# Planlama #2 — Ticari İstihbarat & HS Codes Uygulama Haritası
**Tarih:** 2026-04-21 03:47
**Bağlı Araştırma:** arastirma2.md

## Swarm Agent ile Nasıl Uygulanır?

Bu sistemin ilk versiyonu bir **rapor fabrikası** olmalı; full SaaS'a atlamak erken ve maliyetli. Dashboard fetişi burada para yakar. Para, tek HS/GTIP için hızlı, kaynaklı, satın alınabilir PDF/CSV raporda.

### Agent rolleri

1. **Researcher Agent**
   - HS/GTIP, hedef ülke, ürün açıklaması için resmi veri kaynaklarını bulur.
   - Trade Map/WITS/Census/UN Comtrade/ITA/Türkiye kaynaklarından tarihli veri notu çıkarır.

2. **Classifier Agent**
   - Ürün açıklamasından HS-2/4/6 adayları üretir.
   - Türkiye GTIP yapısını açıklar; kesin sınıflandırma iddiası kurmaz.
   - Confidence + alternatif HS adayları verir.

3. **Market Intelligence Agent**
   - Pazar hacmi, trend, ithalatçı ülkeler, rakip supplier ülkeleri, duty yükü, sezon/yıllık oynaklık hesaplar.
   - Opportunity score üretir: hacim, büyüme, duty, data confidence, buyer accessibility.

4. **Lead Strategy Agent**
   - Şirket-level data yoksa bile importer directory, trade association, LinkedIn/Apollo/Clay search query, fuar listesi, freight forwarder hedefleri üretir.
   - Paid shipment data varsa company/consignee/shipper export listesi oluşturur.

5. **Outreach Agent**
   - 3 mesaj üretir: ihracatçıya rapor satışı, importer'a supplier pitch, logistics/freight-forwarder'a route pitch.
   - Otomatik göndermez. İnsan onayı olmadan dışarı çıkmak yok.

6. **QA/Compliance Agent**
   - Kaynak tarihlerini, lisans riskini, “legal/tariff advice değil” disclaimer'ını, anti-spam/KVKK/GDPR uyarısını kontrol eder.
   - Şüpheli HS kodunda “customs broker / BTI required” etiketi koyar.

7. **Composer Agent**
   - Markdown → PDF/CSV rapor paketi üretir.
   - Rapor sonunda “ilk 3 aksiyon” ve satışa dönük next-step ekler.

## Gerekli Bileşenler

- **Script/Bot:**
  - Şimdilik plan: rapor template'i + manuel kaynak toplama checklist'i.
  - Sonraki aşama: HS query runner, Census/WITS fetcher, opportunity scorer, PDF exporter, lead CSV formatter.

- **MCP/Araç:**
  - ArXiv MCP: HS classification / customs AI literatür kontrolü.
  - MCPTube: trade data ve export tutorial transkriptleri.
  - Browser/web fetch: Trade Map, WITS, Census, ITA, Bakanlık, ImportGenius/Volza sayfaları.
  - Browser automation/scraping stack: public directory ve tariff pages için.
  - Spreadsheet/CSV: rapor çıktısı ve lead listeleri için.

- **API:**
  - U.S. Census HS Import API: ücretsiz başlangıç; aylık/YTD value, duty, quantity.
  - WITS/World Bank + Trade Map: ücretsiz/hesaplı analiz; bulk kısıtları var.
  - UN Comtrade Premium: **$2,000/yıl individual**, **$12,000/yıl private-sector institutional**; scale olana kadar alma.
  - ImportGenius: **$199–$399/mo** U.S. trade data başlangıcı, enterprise **$1,999/mo**; sadece müşteri ödemesi doğrulanınca.
  - Volza: 203 ülke coverage / full shipment view; fiyat için sales/plan seçimi gerekebilir.
  - Apollo/Clay/Proxycurl/Instantly: lead enrichment/outreach için orta vade.

- **İnsan Müdahalesi:**
  - HS/GTIP kesinliği ve customs riskinde insan kontrolü.
  - İlk satışlarda raporu manuel QA.
  - Outreach gönderim onayı.
  - Ödeme/vergisel süreçler.
  - Ticaret verisi lisans kontrolü.

## Workflow Haritası

`Rapor isteği / hedef HS` → `ürün & ülke intake` → `HS/GTIP adayları + confidence` → `resmi veri kaynakları tarama` → `pazar hacmi/trend/duty çıkarımı` → `buyer/supplier route strategy` → `opportunity score` → `outreach mesajları` → `QA + disclaimer` → `PDF/CSV teslim` → `upsell: lead list / monthly alert / white-label dashboard`

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

### Hemen yapılacak ürün: GTIP Opportunity Snapshot
- Tek ürün/HS için 6-8 sayfalık PDF:
  - Ürün açıklaması + HS/GTIP adayları.
  - Hedef pazar hacmi ve son veri trendi.
  - Duty/tariff snapshot.
  - Rakip supplier countries.
  - Buyer finding strategy.
  - 3 outreach mesajı.
  - “Customs authority final” disclaimer.
- İlk vertical'lar:
  1. **HS 570242 — Türkiye halı → ABD**: 2026-02 tek ay Census değeri $56.5M; güçlü örnek.
  2. **HS 080222 — fındık → ABD**: daha dar ama Türkiye markası kuvvetli.
  3. **HS 610910 — pamuklu T-shirt → ABD**: duty yüksek; compliance/tariff açısı var.

### En düşük çaba / en yüksek çıktı adımı
- 3 örnek raporu manuel üretmek ve bunları satış materyali yapmak.
- Ürün başlığı: **“GTIP Pazar Fırsatı Raporu — 24 saatte teslim”**.
- Fiyat testi:
  - Mini: **$19** — 1 HS / 1 ülke, kısa snapshot.
  - Standard: **$39** — 1 HS / 3 ülke, trend + duty.
  - Pro: **$79** — 1 HS / 5 ülke + outreach pack.
  - Enterprise/Agency: **$499** — 10 HS + CSV + lead strategy.

### Hangi mevcut araç/script bu işi kısmen yapar?
- Mevcut browser/scraping/API notları ve agent döngüsü kaynak toplamaya uygun.
- ArXiv/MCPTube/web fetch araştırma katmanı hazır.
- Üretim kodu yazmadan, markdown/PDF template ile ilk POC yapılabilir.

### Proof-of-concept minimum gereksinimler
- 1 rapor template'i.
- 3 örnek HS raporu.
- 30-50 hedef prospect:
  - ihracat danışmanları,
  - dış ticaret ajansları,
  - lojistik/freight forwarder firmaları,
  - küçük üretici/ihracatçı LinkedIn profilleri,
  - ticaret odası/exporter association listeleri.
- 2 outreach mesajı: biri Türkçe, biri İngilizce.
- Manuel teslimat ve geri bildirim formu.

### Tahmini kurulum süresi ve ilk gelir beklentisi
- Kurulum: **2-4 gün** manuel rapor template + 3 örnek.
- İlk satış denemesi: **1 hafta** içinde 50 hedefe founder-led outbound.
- İlk gelir beklentisi: gerçekçi **$39-$158** (1-4 rapor). İyi senaryoda 1 agency paketi **$499**.
- Break-even: ücretsiz veriyle **1 satış**; paid tool yoksa maliyet token/zaman.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

### 1. ay hedef görüntüsü
- 20-30 HS için hazır opportunity cache.
- Haftalık “GTIP Watchlist” üretimi.
- 100-200 prospect'lik segmentli liste.
- 10+ rapor satışı veya en az 3 ciddi discovery call.
- Her raporda aynı kalite standardı: kaynak tarihi, data confidence, duty/tariff warning, next action.

### Başarı metric'leri
- Rapor üretim süresi: manuel 3-4 saatten **45 dakikaya** düşmeli.
- Report-to-call conversion: **%5-10** hedef.
- Cold outreach reply rate: **%3-8** hedef; trade vertical niş olduğu için kişiselleştirme şart.
- Paid report conversion: ilk 100 hedefte **1-3 satış** bile sinyal sayılır.
- Accuracy metric: HS confidence + insan QA flag oranı.
- Revenue metric: ilk 90 günde **$500-$3,000** arası servis geliri hedeflenebilir.

### Paralel çalışabilecek adımlar
- Researcher: yeni HS/ülke raporları.
- Lead Agent: prospect listeleri.
- Outreach Agent: mesaj varyantları.
- QA Agent: kaynak/disclaimer kontrolü.
- Analyst: hangi vertical cevap veriyor analiz eder.

### Ölçeklendirme için gerekenler
- **İnsan:** 1 customs/trade danışmanı ile part-time doğrulama ilişkisi.
- **Araç:** müşteri geliri doğrulanırsa ImportGenius/Volza aylık planı; yoksa alma.
- **Bütçe:** başlangıç $0-$50/mo; validated sonrası $199-$399/mo data platform; UN Comtrade premium ancak redistrib/legal ihtiyaç netleşirse.
- **Süreç:** rapor template standardı + QA checklist + CRM takip.

### Checkpoint'ler
- 2. hafta: 3 sample report + 50 prospect + 10 yanıt.
- 4. hafta: 5 paid/LOI veya net ret sebepleri.
- 8. hafta: vertical focus seçimi: halı/textile/food/logistics.
- 12. hafta: recurring alert veya agency paketi kararı.

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

### En iyi senaryo
- Sistem her hafta seçili HS/GTIP kümelerinde pazar değişimi, duty değişimi, yeni buyer/supplier sinyali ve outreach fırsatı çıkarır.
- İnsan sadece QA ve satış stratejisine bakar.
- Ürün 3 kola ayrılır:
  1. **Self-serve report checkout:** $19-$79.
  2. **Monthly GTIP alert subscription:** $49-$199/mo.
  3. **White-label export intelligence agency:** $499-$2,000/mo.

### Yan ürünler / yeni gelir kolları
- **GTIP classifier assist**: ürün açıklaması → HS/GTIP adayları + kaynaklı rationale.
- **Tariff shock alert**: belirli HS/country için duty değişimi uyarısı.
- **Importer lead pack**: “bu HS ürününü alan firma segmentleri + outreach metinleri”.
- **Exporter SEO content factory**: “HS 570242 ABD halı ithalatı 2026” gibi long-tail SEO raporları.
- **Trade consultant toolkit**: danışmanlara white-label rapor jeneratörü.
- **Chamber/exporter association paketleri**: üyeleri için aylık fırsat bülteni.

### Swarm yaklaşımıyla rakiplerin yapamadığı şey
- ImportGenius/Volza data platform; bizim swarm **operator + analyst + copywriter + QA** gibi çalışır.
- Rakip dashboard'unda kullanıcı yine düşünür. Biz “hangi fırsat, neden, kime yaz, ne söyle” paketini veririz.
- Çoklu ajanlar sürekli vertical test eder: bir hafta halı, bir hafta fındık, bir hafta textile; reply/sales signal'a göre odak kaydırır.

### White-label veya SaaS olarak satılabilir mi?
- Evet, ama erken SaaS yanlış. Önce productized service.
- 3-6 ayda white-label rapor motoru daha mantıklı:
  - Export consultants,
  - freight forwarders,
  - chambers of commerce,
  - B2B trade agencies.
- 6-12 ayda self-serve SaaS:
  - HS/GTIP lookup + opportunity score + report generator + alert.
- Veri lisansı çözülmeden shipment-level SaaS satmak riskli; aggregate insight/report satışı daha güvenli.

## Öncelik & Çaba Tahmini

- **Öncelik:** Yüksek. ProfitBridge'in mevcut dijital rapor fiyatlandırmasına çok uyuyor; ürün inşa etmeden gelir denenebilir.
- **Kurulum Süresi:**
  - Manuel POC: **2-4 gün**.
  - Productized report workflow: **1-2 hafta**.
  - Paid-data/enrichment entegrasyonu: **1-3 ay**.
- **Aylık İşletme Maliyeti:**
  - Başlangıç: **$0-$50**.
  - Validated: **$199-$399/mo** ImportGenius/benzeri + email/enrichment.
  - Scale: **$2,000/yıl** UN Comtrade Individual veya **$12,000/yıl** private institutional; ancak data redistribution kuralları netleşmeden alma.
- **Potansiyel Gelir:**
  - İlk ay: **$100-$1,000** manuel rapor.
  - 3 ay: **$500-$3,000/mo** productized service.
  - 6-12 ay: **$3,000-$15,000/mo** white-label + recurring alert, iyi outbound ile mümkün.
- **ROI Beklentisi:**
  - Ücretsiz veriyle break-even: 1 rapor.
  - $199/mo paid data ile break-even: 3 adet $79 rapor veya 1 adet $499 paket.

## Mevcut Sistemle Entegrasyon

- **UniverseCreator swarm:** Researcher rapor verisi toplar, Analyst fırsat skorlar, Writer/Composer PDF üretir, QA kaynak/disclaimer kontrol eder.
- **Mevcut ürün portföyü:** Dev tool ürünleriyle aynı checkout/micro-product mantığı; fark, çıktı statik tool değil “bilgi ürünü”.
- **Ödeme:** LemonSqueezy/iyzico blokajı çözülene kadar otomatik satış kanalı kırılgan. Bu yüzden ilk aşama “satış niyeti + manuel teslim” olarak planlanmalı.
- **SEO:** Mevcut SEO content factory ileride HS bazlı long-tail sayfalara genişleyebilir.
- **universe_loop:** Yeni ürün build/deploy tetiklenmeyecek; araştırma modunda sadece rapor template ve plan. Uygulama seçilirse ayrı cycle'da kodlanır.

## Riskler & Dikkat Edilecekler

- **Yanlış HS/GTIP riski:** AI kesin hüküm vermemeli. Customs broker/BTI önerisi eklenmeli.
- **Legal advice riski:** Rapor “commercial intelligence” olmalı, gümrük müşavirliği veya hukuki görüş gibi satılmamalı.
- **Data licensing:** UN Comtrade ve paid shipment data re-distribution kuralları var. Raw data dump satmak tehlikeli; transform edilmiş analiz + sınırlı kayıt daha güvenli.
- **Company-level data sınırlaması:** ABD bill of lading public; her ülkede importer/exporter adı yok. Resmi aggregate data ile buyer listesi karıştırılmamalı.
- **Spam/KVKK/GDPR:** Outreach otomatik gönderilmemeli; insan onaylı ve compliant olmalı.
- **Payment blocker:** Ödeme sağlayıcı doğrulaması çözülmeden ölçekli satış funnel'ı zayıf kalır.
- **Turkish tax/accounting:** Düzenli ticari gelir doğarsa vergi setup'ı gerekebilir.
- **Veri tazeliği:** Bazı kaynaklar 3-6 ay geriden gelir; raporda source date açık yazılmalı.
- **Dashboard tuzağı:** İlk aşamada dashboard yapma. Bu fikirde para “rapor + satış”ta; dashboard sonra.

## Önce Yapılacak 3 Adım (Bu Hafta)

1. **3 örnek rapor üret:** HS 570242 halı, HS 080222 fındık, HS 610910 T-shirt için aynı template ile GTIP Opportunity Snapshot hazırla.
2. **50 prospect listesi çıkar:** Türkiye'deki ihracat danışmanları, halı/textile/food ihracatçıları, freight forwarders, trade consultants; her biri için kişiselleştirilmiş ilk mesaj yaz.
3. **Satış testi yap:** “$39 sample report / 24h delivery” teklifini 50 hedefe gönderilecek hale getir; gönderim insan onayına bağlı kalsın. İlk 10 yanıttan ret sebeplerini topla ve paket/fiyatı düzelt.
