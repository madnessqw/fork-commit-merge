# Planlama #21 — Voice AI + Sales Funnel Uygulama Haritası
**Tarih:** 2026-04-21 16:51 +03
**Bağlı Araştırma:** arastirma21.md

## Swarm Agent ile Nasıl Uygulanır?
Bu iş “AI phone bot” diye satılmaz. Doğru ürün adı şudur:

**Revenue Recovery Voice OS**
- Hedef dikeyler: home services, dental/clinic, medspa, legal intake, service booking yoğun SMB’ler
- İlk problem: mesai dışı veya yoğun saatlerde kaçan çağrılar
- İlk çıktı: soft booking + qualified handoff + CRM log + reminder + haftalık ROI

Swarm dağılımı şöyle kurulmalı:
1. **Vertical Selector Agent**
   - Tek dikey seçer: home services veya dental.
   - Script, jargon, booking logic ve compliance farklarını çıkarır.
2. **Offer / ROI Agent**
   - “Kaç missed call = kaç randevu = kaç $ kayıp” hesabını çıkarır.
   - Niş landing page ve audit sheet üretir.
3. **Voice Flow Builder Agent**
   - Retell/Vapi prompt, first message, tools, KB, objection guardrail, escalation logic kurar.
4. **Telephony Router Agent**
   - After-hours / overflow / emergency routing ve branded caller ID mantığını kurar.
5. **Calendar + CRM Sync Agent**
   - Booking, reschedule, cancellation, duplicate-check ve field mapping’i bağlar.
6. **QA + Compliance Agent**
   - Transcript review, latency, hallucination, emergency transfer, consent, retention ve failure tagging yapar.
7. **Human Handoff Agent**
   - Acil durum, sinirli müşteri, yüksek değerli fırsat veya düşük güven durumunda çağrıyı insana aktarır.
8. **Reporter Agent**
   - Haftalık answered calls, recovered bookings, transfer rate, no-answer leakage, cost per handled call ve booked revenue raporu çıkarır.

## Gerekli Bileşenler
- **Script/Bot:**
  - missed-call ROI calculator
  - synthetic call test harness
  - transcript scorer / QA rubric runner
  - calendar availability + duplicate booking checker
  - CRM logger / enrichment mapper
  - weekly recovered-revenue report generator
- **MCP/Araç:**
  - web/Jina/Reddit/GitHub/ArXiv araştırma stack’i
  - MCPTube (workflow çıkarımı)
  - browser araçları (prospect funnel, docs, integration debug)
- **API:**
  - **Retell** veya **Vapi**
  - **Twilio** numara + gerektiğinde branded calling
  - **n8n** / Make
  - **Google Calendar / Cal.com / Calendly**
  - **HubSpot / ServiceTitan / Housecall Pro / Jobber / Sheets**
  - SMS/email provider
- **İnsan Müdahalesi:**
  - emergency / escalation
  - hassas sorular ve fiyat pazarlığı
  - compliance onayı
  - ilk onboarding ve vertical script revizyonu
  - booked lead’lerin final teyidi (özellikle ilk pilotta)

## Workflow Haritası
Tetikleyiciler:
- mesai dışı inbound çağrı
- yoğun saat / lunch-hour overflow
- web form submission sonrası otomatik çağrı
- mevcut müşteri listesi üzerinden reactivation

Akış:
çağrı geldi veya trigger oluştu
→ saat / availability router çalışır
→ AI agent açılır
→ intent ve urgency sınıflandırılır
→ eğer emergency / human request ise warm transfer
→ değilse CRM + calendar lookup yapılır
→ soft booking veya qualified handoff yapılır
→ SMS/email summary ve reminder tetiklenir
→ transcript + structured output CRM’e işlenir
→ QA skoru çıkarılır
→ weekly ROI report güncellenir

Branch’ler:
- **Emergency:** direkt teknisyen / insan / on-call kişi
- **Not qualified:** nurture bucket veya callback queue
- **Voicemail / no answer:** retry → SMS → email sırası
- **Qualified:** booking + CRM status + follow-up
- **Needs human:** warm transfer veya next-available callback

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **En düşük çaba / en yüksek çıktı adımı:** tek dikey için **after-hours missed-call recovery + soft booking POC**.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - Retell veya Vapi voice runtime
  - Twilio telephony
  - n8n orchestration
  - Google Calendar / Cal.com booking
  - Sheets / HubSpot CRM log
  - UniverseCreator tarafında mevcut Vercel gücüyle ROI landing page + demo page + intake form
- **Proof-of-concept için minimum gereksinimler neler?**
  - 1 dikey (home services veya dental)
  - 1 use case (after-hours appointment capture)
  - 1 telefon numarası
  - 1 prompt + knowledge base
  - 1 calendar entegrasyonu
  - 1 CRM/Sheets log akışı
  - 20-30 sentetik test çağrısı
  - emergency/human transfer branch’i
- **Tahmini kurulum süresi ve ilk gelir beklentisi?**
  - Teknik POC: **4-7 gün**
  - Offer/landing/demo paketleme: **2-3 gün**
  - İlk gelir: iyi paketlenmiş pilotta **$500-$1,200/ay** veya setup + ilk ay kombinasyonu makul. Altyapı maliyeti düşük olduğu için ilk müşteriyle break-even mümkündür.
- **Net kısa vade kararı:** outbound SDR kovalamak yerine **kaçan çağrı → kurtarılan randevu** ürününü çıkar.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonunda ideal görünüm:**
  - 1 dikey için çalışan prompt/KB seti
  - 1 canlı pilot veya çok gerçekçi iç test hattı
  - after-hours + overflow + human transfer akışı stabil
  - landing page + ROI calculator + demo transcript seti hazır
- **Başarı metric’leri neler?**
  - routed çağrılarda answer/capture rate: **>%95**
  - booking / qualified human handoff success: **>%60**
  - booking veri doğruluğu: **>%90**
  - hissedilen latency: **~1.2s ve altı**
  - kritik failure (yanlış booking / yanlış transfer / emergency miss): **0 tolerans**
- **Hangi adımlar paralel çalışabilir?**
  - vertical prompt geliştirme
  - landing + ROI sayfası
  - test harness / QA rubric
  - prospect listesi ve outreach
  - CRM/calendar integration templates
- **Ölçeklendirme için ne gerekiyor?**
  - 1 operasyon sahibi (onboarding + QA)
  - 1 builder (voice flow + n8n)
  - aylık araç bütçesi: **$75-$250** pilot başı; Bland seçilirse daha yüksek
  - vaka çalışması ve haftalık rapor üretimi
- **Checkpoint’ler ve başarı kriterleri?**
  - Hafta 1: script + number + routing hazır
  - Hafta 2: sentetik çağrı testi ve QA raporu
  - Hafta 4: pilot canlı veya shadow mode
  - Ay 2: lead reactivation modülü eklenir
  - Ay 3: ikinci vertical veya white-label onboarding paketi çıkar

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** sistem sadece çağrı cevaplamaz; voice + SMS + email + CRM + dispatch üzerinden çok kanallı bir gelir geri kazanım makinesine döner.
- **Yan ürünler / yeni gelir kolları:**
  - transcript QA / observability aboneliği
  - missed-call audit raporu
  - vertical prompt/KB paketleri
  - branded caller ID / trust optimization danışmanlığı
  - reactivation campaign yönetimi
- **Rakiplerin yapamadığı, swarm yaklaşımıyla yapılabilecek nedir?**
  - aynı anda birden fazla niche için hızlı landing + ROI + script + QA paketi çıkarmak
  - weekly transcript review ve prompt düzeltmesini sistematik hale getirmek
  - public landing pages + internal call ops + reporting katmanını tek operatör ekranında toplamak
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet. İlk safhada **done-for-you / done-with-you** paket daha mantıklı.
  - Daha sonra **white-label onboarding kit + dashboard + QA layer** şeklinde agency enablement ürünü çıkar.
  - En uzun vadede “Voice Revenue Recovery OS” diye çok dikeyli SaaS mümkündür; ama ilk önce vaka ve operasyonal disiplin gerekir.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** 1-2 hafta sağlam pilot
- **Aylık İşletme Maliyeti:** yaklaşık **$75-$250** / müşteri (Retell/Vapi + Twilio + orchestration); Bland seçilirse taban daha yüksek
- **Potansiyel Gelir:** yaklaşık **$500-$2,000/ay** / müşteri + setup/onboarding
- **ROI Beklentisi:** ilk müşteriyle **ilk ay içinde** break-even mümkün; iyi vertical’de çok daha hızlı

## Mevcut Sistemle Entegrasyon
- Vercel üzerindeki mevcut üretim/distribution gücü kullanılarak:
  - niche landing pages
  - ROI calculators
  - call audit mini-tools
  - lead capture forms
  - case-study / demo transcript sayfaları
  hızlıca çıkarılabilir.
- Voice runtime’ı Vercel’e zorla gömmek saçma; runtime dış servislerde, pazarlama ve lead-gen yüzeyi mevcut stack’te kalmalı.
- UniverseCreator swarm mevcut ürün kataloğunu “voice-adjacent funnel assets” üretmek için kullanabilir: HVAC missed-call calculator, dental after-hours audit, medspa booking-loss estimator gibi.

## Riskler & Dikkat Edilecekler
- TCPA / robocall / consent riski; özellikle cold consumer outbound tarafı
- emergency call’ı yanlış sınıflandırma
- hallucinated booking / yanlış takvim slotu
- telephony verification ve number reputation
- düşük latency tutturamama → yapay his
- müşteri beklentisinin “AI closer” fantezisine kayması
- CRM/dispatch mapping hataları
- call recording / retention / privacy yükü

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek wedge seç:** home services veya dental için “after-hours missed-call recovery” offer’ını sabitle.
2. **Pilot hattı kur:** Retell/Vapi + Twilio + n8n + calendar + CRM/Sheets ile sentetik testlerden geçen demo oluştur.
3. **Satış yüzeyini hazırla:** ROI calculator + demo transcript + “kaçan çağrı maliyeti” landing page çıkar; sonra sadece bu probleme sahip 10-20 adaya git.
