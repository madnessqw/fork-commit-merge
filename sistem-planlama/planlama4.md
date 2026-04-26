# Planlama #4 — Local Business Automation Uygulama Haritası
**Tarih:** 2026-04-21 04:45 +03
**Bağlı Araştırma:** arastirma4.md

## Swarm Agent ile Nasıl Uygulanır?
Bu iş “yerel işletmelere AI ajan satıyoruz” diye paketlenmeyecek. O cümle 2026'nın en hızlı güven kaybettiren cümlelerinden biri. Paket adı problem üzerinden olmalı: **Missed Call Recovery + Booking + Reviews**.

1. **Vertical Scout Agent**
   - Google Maps/GBP, website, review count, rating, booking link, response channel, hours, service value gibi sinyallerle işletmeleri tarar.
   - İlk hedef vertical: HVAC/plumbing/roofing/remodeling veya med spa/dental. Yüksek LTV yoksa ROI anlatmak zorlaşır.
2. **Audit Agent**
   - Her prospect için mini audit çıkarır: GBP eksikleri, booking link yok, reviews az/cevapsız, website form yavaş, phone-only friction, after-hours risk.
   - Çıktı: 1 sayfalık “şu 3 lead sızıntısı para kaçırıyor” raporu.
3. **Demo Builder Agent**
   - Prospect'in public web bilgisinden demo FAQ/KB oluşturur.
   - Demo: missed-call SMS script, website chat response, appointment qualification form, review request message.
   - Gerçek müşteri sistemine dokunmaz; demo sandbox.
4. **Offer Agent**
   - İşletme türüne göre 3 paket yazar:
     - Starter: text-back + booking + review
     - Pro: Starter + website chat + quote follow-up + weekly ROI
     - Premium: Pro + AI voice/front desk + ads/lead gen entegrasyonu
5. **Onboarding Agent**
   - İşletmeden servisler, fiyat aralıkları, çalışma saatleri, hizmet bölgesi, emergency rules, handoff numarası, tone, opt-out metni toplar.
6. **Workflow QA Agent**
   - Calendar conflict, duplicate contact, opt-out, wrong service area, hallucinated pricing, angry customer escalation testlerini çalıştırır.
7. **ROI Reporter Agent**
   - Haftalık rapor üretir: kaç missed call yakalandı, kaç conversation başladı, kaç booking oluştu, kaç review istendi/yayınlandı, tahmini recovered gross profit.
8. **Human Gate**
   - Outreach, fiyat teklifi, gerçek mesaj gönderimi ve müşteri hesabı bağlantısı insan onayıyla olur. Araştırma modunda dış iletişim yok.

## Gerekli Bileşenler
- **Script/Bot:**
  - GBP/website audit generator
  - Prospect scoring sheet
  - Demo KB builder
  - SMS/WhatsApp/chat script generator
  - Booking workflow test runner
  - Weekly ROI report generator
  - Review request scheduler
  - Quote follow-up tracker
- **MCP/Araç:**
  - Playwright/Chrome DevTools: prospect site/booking/GBP inspection, screenshot, form test
  - MCPTube: local automation/agency workflow transkriptlerinden sales + implementation playbook çıkarma
  - ArXiv MCP: workflow automation ve AI adoption araştırma takibi
  - Browser automation stack: Google Maps/website audit için gözlem; mutasyon yok
  - Optional: Google Places API / Maps scraping alternatifi; scraping tarafı ToS ve KVKK/GDPR dikkat ister
- **API:**
  - HighLevel: $297/mo Unlimited veya $497/mo Pro; ölçek ve white-label için
  - Make: $9/$16/$29 mo; düşük maliyetli POC
  - Zapier: $19.99 Pro, $69 Team; hızlı entegrasyon
  - Cal.com: Free/Teams $12 user/mo; booking
  - Twilio: US local number $1.15/mo, outbound $0.014/min, inbound local $0.0085/min; SMS fiyatı ayrıca kontrol edilmeli
  - Retell AI: $0.07-$0.31/min voice agent; premium add-on
  - Google Business Profile / Calendar / Sheets / Gmail: POC omurgası
- **İnsan Müdahalesi:**
  - İlk vertical seçimi
  - 20-30 prospect audit kontrolü
  - Sales call / demo sunumu
  - KVKK/TCPA/call recording/onay metinleri
  - İşletme bilgi formu ve escalation kuralları
  - İlk 2 hafta günlük kalite izlemesi

## Workflow Haritası
Tetikleyici: haftalık local business prospect batch
→ Prospect listesi çıkar
→ GBP/website/contact/booking/review audit
→ Score: high LTV + no booking + weak reviews + phone-heavy + owner-operated
→ Demo KB + SMS/chat/booking script oluştur
→ İnsan onaylı outreach/demo
→ İşletme bilgi formu
→ Sandbox workflow kurulumu
→ QA: 20 test senaryosu
→ Pilot launch
→ Missed call / form / chat lead yakala
→ Qualify: service, urgency, location, preferred time
→ Calendar booking veya human handoff
→ Reminder gönder
→ Service sonrası review request
→ Quote follow-up / reactivation
→ Weekly ROI report
→ Retention check + upsell

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen hayata geçirilecek bulgu:** “AI agency” değil, **Missed Call + Review + Booking Recovery Pack**. İlk POC tek vertical için hazırlanmalı: örn. İstanbul/ABD şehirlerinden plumbing/HVAC/remodeling veya Türkiye'de diş kliniği/estetik/salon.
- **En düşük çaba / en yüksek çıktı:** 30 işletmelik audit batch:
  - Google Business Profile var/yok/tamamlık
  - review sayısı ve son review tarihi
  - booking link var/yok
  - website form/chat var/yok
  - çalışma saatleri dışı lead yakalama var/yok
  - phone-only işletme mi?
- **Hangi mevcut araç/script kısmen yapar:** Browser automation + Playwright/Chrome DevTools gözlem, `projeler.txt` içindeki browser/scraping/automation stack sinyalleri, mevcut research/planning cycle dosya üretimi. Kod yazmadan da audit dosyası ve demo scriptleri hazırlanabilir.
- **Minimum POC gereksinimleri:**
  - 1 vertical
  - 30 prospect audit
  - 5 özel demo
  - 3 paket fiyatı
  - 1 onboarding form taslağı
  - 10 workflow test senaryosu
  - Weekly ROI report template
- **Tahmini kurulum süresi:** 3-5 gün research/audit/demo; 2-4 gün human outreach ve pilot görüşme hazırlığı. Gerçek müşteri entegrasyonu ayrı execution cycle ister.
- **İlk gelir beklentisi:** Gerçekçi kısa vade: 1 pilotten $299-$999 setup veya $199-$499 MRR. Reddit/IH örneklerinde $1K setup + $300-$800 MRR mümkün görünüyor ama bunu baseline almak hayalperestlik olur; başlangıç hedefi ilk ödeyen pilot.
- **İlk paket fiyat önerisi:**
  - Starter: $299 setup + $199/mo — missed-call text-back, booking link, review request, weekly report
  - Pro: $699 setup + $499/mo — Starter + website chat + quote follow-up + reactivation
  - Premium: $1,500 setup + $999/mo — Pro + AI voice/front desk + ad/form lead follow-up

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **Ay 1 hedef görüntü:**
  - 100-150 prospect audit edilmiş
  - 15-25 kişiselleştirilmiş demo hazırlanmış
  - 3-5 pilot müşteriyle gerçek workflow test edilmiş
  - 1 vertical için template snapshot oluşmuş
  - Haftalık ROI raporu standartlaşmış
- **Başarı metrikleri:**
  - Audit → demo kabul oranı: %10-20
  - Demo → pilot oranı: %10+
  - First response time: <60 saniye
  - Missed-call → conversation oranı: başlangıç %15-30 hedef
  - Conversation → booking oranı: vertical'a göre %10-25 hedef
  - Review request → posted review: BrightLocal benchmark'ına göre yüksek potansiyel; ilk hedef %10-25 gerçek posted review
  - Gross margin: %70+; voice eklenirse dakika maliyeti takip edilmeli
  - Churn: ilk 60 gün pilotte 0; retention için weekly ROI şart
- **Paralel çalışabilecek adımlar:**
  - Prospect Scout audit yapar
  - Demo Builder KB/script üretir
  - Offer Agent vertical landing/teklif metni hazırlar
  - QA Agent test senaryolarını çalıştırır
  - Reporter Agent pilot çıktılarını özetler
- **Ölçeklendirme gereksinimi:**
  - 1 ops kişi veya human gate: haftada 5-8 saat
  - HighLevel Unlimited/Pro veya n8n+Make omurgası
  - Twilio/WhatsApp/Cal.com entegrasyonları
  - KVKK/TCPA/opt-out/call recording metinleri
  - 1 müşteri başına onboarding checklist <60 dakika olmalı
- **Checkpoint'ler:**
  - Hafta 2: 30 audit + 5 demo + ilk teklif
  - Hafta 4: 100 audit + 10 demo + 1-2 pilot
  - Hafta 8: 3-5 müşteri + dashboard + churn/ROI öğrenimi
  - Hafta 12: aynı vertical'da templateleşmiş satış ve onboarding; ikinci vertical kararı

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** Swarm her hafta yeni vertical/prospect batch çıkarır, demo üretir, insan satış görüşmesine hazır materyal verir; pilot müşterilerden gelen gerçek workflow sonuçları template library'ye geri beslenir. Sistem “ajans”tan “vertical automation operating system”e dönüşür.
- **Yan ürünler / gelir kolları:**
  - Local Business Leak Audit: tek seferlik $49-$199 rapor
  - Review Recovery Pack: $99-$299/mo
  - Missed Call Recovery Pack: $199-$499/mo
  - Voice Front Desk add-on: $500-$1,500/mo
  - White-label agency snapshot: $299-$999 setup + $99-$299/mo
  - Vertical SaaS: salon/clinic/HVAC için self-serve dashboard
  - Türkiye paketi: WhatsApp/KVKK/Google Business Profile odaklı “Randevu ve Yorum Otomasyonu”
- **Rakiplerin yapamadığı, swarm yaklaşımıyla yapılabilecek şey:** Her işletmeye özel audit + demo + ROI modelini hızlı üretmek. Klasik ajans bunu elle yapınca maliyetli; generic SaaS bunu kişiselleştirmeden yapınca satış zor. Swarm ortadaki “kişiselleştirilmiş ama ölçeklenebilir” alanı alır.
- **White-label/SaaS olarak satılabilir mi?** Evet, ama erken SaaS yapmak dumb olur. Önce 5-10 müşteriyle en çok tekrar eden workflow'u bul. Sonra white-label dashboard/snapshot çıkar. En iyi SaaS feature'ları masada değil, kızgın işletme sahibinin “şu kısmı yine bozdu” dediği yerde doğar.
- **3-12 ay hedefi:**
  - 20-50 müşterilik managed service veya 5-10 ajansa white-label snapshot
  - $5K-$25K MRR bandı potansiyeli
  - 3 vertical template: home services, beauty/wellness, clinic/professional services
  - Onboarding süresi müşteri başına <45 dakika
  - Haftalık rapor otomatik, human sadece exception/upsell ile ilgilenir

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek. Bu konu önceki AI calling + lead gen + SEO araştırmalarını gerçek B2B pakete bağlar.
- **Kurulum Süresi:** Plan/demolar 1 hafta; ilk pilot entegrasyon 1-2 hafta; templateleşmiş managed service 1-3 ay.
- **Aylık İşletme Maliyeti:**
  - POC: $20-$100/mo + iletişim kullanım maliyeti
  - Ajans ölçek: HighLevel $297-$497/mo + Twilio/Retell/LLM usage
  - Voice-heavy: dakika hacmine göre $0.07-$0.31/dk Retell + telefon taşıma maliyeti
- **Potansiyel Gelir:**
  - 1-2 hafta: $0-$1,000 setup / ilk pilot
  - 1-3 ay: $1K-$5K MRR, 3-10 müşteriyle gerçekçi
  - 3-12 ay: $5K-$25K MRR; white-label veya voice add-on ile daha yüksek
- **ROI Beklentisi:**
  - Make/Zapier tabanlı POC tek $299 setup ile break-even olur.
  - HighLevel $297/mo kullanılırsa 2 Starter müşteri veya 1 Pro müşteri maliyeti kapatır.
  - Premium voice pakette gross margin dakika kullanımına bağlı; 1,000 dakika/ay Retell yüksek uçta $310 yapabilir, fiyatlandırmada usage cap/rebilling şart.

## Mevcut Sistemle Entegrasyon
- UniverseCreator'ın 113 ürün/Vercel portföyü burada doğrudan satış ürünü değil; swarm'ın araştırma, audit, browser automation, içerik ve reporting kası üründür.
- `universe_loop.sh` mantığına “localbiz-research cycle” eklenebilir: prospect batch → audit → demo → plan → human gate. Bu araştırma modunda sadece dosya/plan üretilecek.
- Önceki çıktılarla bağlantı:
  - #0 AI Calling Agents: premium voice add-on
  - #1 Lead Generation Automation: prospect list/audit pipeline
  - #3 Content Factory + SEO: local vertical landing pages + case study içerikleri
- Browser automation araçları prospect site/GBP gözlemi için kullanılmalı; gerçek formlara mesaj gönderme, arama yapma veya dış outreach insan onayı olmadan yok.
- Payment tarafı henüz hassas olduğu için ilk satışta “manuel invoice/iyzico link/Lemon unblock sonrası checkout” planlanmalı; araştırma modunda ödeme altyapısına dokunma yok.
- Weekly ROI report, mevcut memory/log disiplinine benzer dosya tabanlı üretilirse hem müşteri raporu hem swarm öğrenimi olur.

## Riskler & Dikkat Edilecekler
- **AI hype satışı:** Yerel işletme AI istemiyor; telefon açılsın, randevu gelsin, yorum artsın istiyor. AI kelimesini fazla öne koymak satışı zayıflatır.
- **Compliance:** ABD için TCPA/SMS opt-in, call recording consent; Türkiye için KVKK, ETK/İYS, ticari ileti onayı. Otomatik mesaj işinde “sonra bakarız” demek pahalı hata.
- **Fake review/gating riski:** Sadece memnun müşteriye yorum linki gönderip mutsuzu saklamak platform policy riski doğurur. Review request nötr ve düzgün olmalı.
- **Yanlış cevap/availability:** AI yanlış fiyat, yanlış saat, yanlış hizmet bölgesi söylerse müşteri güveni gider. KB + human handoff şart.
- **Phone reputation:** Yeni numara, spam algısı, SMS deliverability, carrier filtering takip edilmeli.
- **Localizasyon:** Türkiye'de WhatsApp daha doğal olabilir; ABD'de SMS/phone daha kritik. Tek script global çalışmaz.
- **GHL bağımlılığı:** HighLevel hızlı ama platform lock-in ve affiliate noise var. İlk POC mümkünse portable mantıkla tasarlanmalı: CRM abstraction + workflow templates.
- **Satış emeği:** Bu pasif gelir değil. İlk 10 müşteri ciddi human sales/onboarding ister. “Kurduk, para yağacak” masalı çöpe.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek vertical seç ve audit checklist yaz:** Öneri: remodeling/HVAC/plumbing gibi yüksek ticket home services. 30 işletme için GBP/website/booking/review/missed-call risk skorlaması hazırla.
2. **5 demo paket üret:** Her demo için missed-call SMS, website chat lead qualifier, booking flow, review request, weekly ROI report mockup hazırla. Gerçek outreach yok; sadece sunuma hazır dosya.
3. **Pilot teklifini netleştir:** Starter $299 setup + $199/mo, Pro $699 + $499/mo, Premium $1,500 + $999/mo. Her pakette usage cap, opt-out, human handoff, weekly ROI raporu açık yazılsın.
