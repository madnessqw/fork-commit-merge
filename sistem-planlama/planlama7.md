# Planlama #7 — Voice AI + Sales Funnel Uygulama Haritası
**Tarih:** 2026-04-21 06:18 +03
**Bağlı Araştırma:** arastirma7.md

## Swarm Agent ile Nasıl Uygulanır?
Bu işi “herkese AI receptionist” diye satmak zayıf. Doğru oyun: **tek bir dikey + tek bir gelir metriği + tek bir operational pain**. En mantıklı başlangıç paketi şu:

**After-Hours Appointment Recovery OS**
- Hedef: dental, medspa, cleaning, HVAC, home services, legal intake
- Pain: kaçan çağrı = kaçan randevu = kaçan gelir
- Çözüm: AI çağrıyı alır, lead'i niteler, takvime slot koyar veya insana paslar, her şeyi CRM'e işler

Swarm dağılımı şöyle olmalı:
1. **Vertical Selector Agent**
   - Hangi nişin intent ontology'si basit? (booking / quote / follow-up)
   - Önce tek niş seçer. Bence dental veya home services.
2. **Offer/ROI Agent**
   - “Kaç missed call = kaç randevu = tahmini kaç $ kayıp” hesabını çıkarır.
   - Tek sayfalık ROI sheet üretir.
3. **Voice Flow Builder Agent**
   - Retell/Vapi prompt, knowledge base, action config ve fallback logic'i kurar.
4. **Telephony Agent**
   - Twilio numara yönetimi, forwarding, branded caller ID, voicemail ve retry mantığını kurar.
5. **Calendar + CRM Sync Agent**
   - Cal.com/Google Calendar/HubSpot/Sheets bağlantısını yapar.
6. **Call QA Agent**
   - Transcript kalite puanı, hallucination kontrolü, escalation gerektiren çağrıları etiketler.
7. **Compliance Agent**
   - disclosure, recording consent, data retention ve DNC/sector rule checklist'i uygular.
8. **Human Handoff Agent**
   - düşük güven / sinirli müşteri / karmaşık talep / high-ticket durumda insana aktarır.
9. **Reporter Agent**
   - haftalık booked appointments, answer rate, transfer rate, voicemail rate, cost per appointment, kurtarılan gelir raporu üretir.

## Gerekli Bileşenler
- **Script/Bot:**
  - niche ROI calculator
  - missed-call log parser
  - prompt/FAQ/knowledge-base builder
  - appointment booking connector
  - voicemail retry scheduler
  - transcript QA scorer
  - weekly KPI report generator
- **MCP/Araç:**
  - web/Jina/Reddit/GitHub araştırma stack'i
  - browser automation (prospect site, local business flow, call-forwarding docs)
  - MCPTube (call flow örnekleri)
  - ArXiv MCP (latency/compliance/pipeline pattern'leri)
- **API:**
  - Retell veya Vapi
  - Twilio
  - Cal.com / Calendly / Google Calendar
  - HubSpot / Sheets / Airtable
  - gerektiğinde SMS provider
  - opsiyonel: custom QA/eval katmanı
- **İnsan Müdahalesi:**
  - script onayı
  - live handoff
  - compliance review
  - edge-case booking ve high-ticket satış çağrıları
  - ilk müşteri onboarding'i

## Workflow Haritası
Tetikleyici:
- web form submission
- missed call
- after-hours inbound
- eski lead reactivation listesi

Akış:
lead geldi
→ telefon normalize edilir
→ dikeye özel prompt + knowledge base yüklenir
→ AI çağrıyı alır veya arar
→ intent sınıflandırır (book / quote / support / human)
→ uygun ise takvim slotu önerir
→ uygun değilse SMS/email follow-up veya human handoff
→ transcript + structured output CRM'e işlenir
→ QA agent kalite kontrolü yapar
→ Reporter haftalık metrikleri çıkarır

Branch'ler:
- **Voicemail:** etiketle, SMS bırak, callback queue'ya al
- **Sinirli / düşük güven:** direkt insana aktar
- **Eksik bilgi:** follow-up SMS/email
- **Qualified:** appointment booked + CRM status update
- **Not qualified:** nurture bucket / stop list

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **En düşük çaba / en yüksek çıktı adımı:** **Inbound missed-call recovery + appointment booking POC**. Soğuk outbound closer'a girmek şu aşamada gereksiz artistlik. İlk kazanım, kaçan çağrıyı yakalamak.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - voice side: Retell veya Vapi
  - telephony: Twilio
  - orchestration: n8n / Make
  - scheduling: Google Calendar / Cal.com
  - logging: Sheets / HubSpot
  - mevcut UniverseCreator gücü: Vercel landing page + ROI calculator + niche landing page üretimi
- **Proof-of-concept için minimum gereksinimler neler?**
  - 1 dikey seç (dental veya cleaning öneririm)
  - 1 ana use case seç: “mesai dışı randevu alma”
  - 1 prompt paketi + 1 knowledge base
  - 1 calendar entegrasyonu
  - 1 Sheets/CRM log akışı
  - 1 voicemail/SMS fallback
  - 20-30 sentetik test çağrısı + QA rubric
- **Tahmini kurulum süresi:** 5-7 gün sağlam POC, 2-3 gün demo/landing/offer paketleme.
- **İlk gelir beklentisi:** community/creator benchmark'ı baz alırsak **$300-$500/ay müşteri başı** makul başlangıç anchor'ı. Usage-based stack ile **300-800 dk/ay** kullanımda kaba altyapı çoğu durumda **$40-$110/ay** bandında kalabilir; dolayısıyla 1 müşteri bile gross-margin bırakır. Bunlar tahmindir; canlı çağrı hacmi ve provider seçimine bağlıdır.
- **Kısa vade tezi:** önce “kaçan çağrı → kurtarılan randevu” paketini sat. Kapanış robotu satma.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay görünümü:**
  - 1 dikey için üretim-ready prompt paketi
  - 1 canlı pilot müşteri veya iç test ortamı
  - booking / transfer / voicemail / transcript / weekly report akışlarının tamamı çalışıyor
  - 1 Vercel landing page + ROI calculator + book-demo funnel canlı
- **3. ay görünümü:**
  - 3 dikey paket (örn. dental, cleaning, HVAC)
  - 5-10 pilot hesap
  - 1-2 somut case study
  - QA dashboard ve failure taxonomy
- **Hangi metric'ler başarıyı gösterir?**
  - answer rate
  - booked appointment rate
  - show-up rate
  - transfer-to-human rate
  - voicemail recovery rate
  - cost per booked appointment
  - latency p95
  - hallucination / failed-tool-call oranı
  - booked revenue estimate
- **Hangi adımlar paralel çalışabilir?**
  - bir agent dikey araştırır
  - biri landing page/offer üretir
  - biri voice prompt + KB yazar
  - biri Twilio/CRM entegrasyonunu kurar
  - biri QA ve reporting'i çıkarır
- **Ölçeklendirme için ne gerekiyor (insan, araç, bütçe)?**
  - teknik delivery disiplini
  - daha iyi QA/eval katmanı
  - call replay / error dashboard
  - compliance checklist per vertical
  - daha güçlü CRM entegrasyonları
  - mümkünse teknik ortak veya delivery owner
- **Checkpoint'ler ve başarı kriterleri?**
  1. Hafta: tek dikey, tek prompt, tek booking flow
  2. Hafta: live simulation + human fallback + transcript QA
  4. Hafta: ilk pilot
  8-12. Hafta: 3 dikey playbook + case study + white-label package

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** sistem sadece randevu almaz; missed-call recovery, lead qualification, reactivation, reminder, no-show reduction ve post-call follow-up katmanlarını tek revenue ops layer'ında toplar.
- **Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?**
  - transcript intelligence dashboard
  - objection library / sales script miner
  - “why leads didn't book” raporu
  - voice QA-as-a-service
  - niche prompt packs / template marketplace
  - SMS + WhatsApp follow-up hybrid product
- **Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek nedir?**
  - aynı anda niche research + landing page + ROI calculator + prompt pack + QA rubric + reporting pipeline üretmek
  - Vercel üstünde her dikey için çok hızlı mikro funnel açmak
  - çağrı verisini yeni landing/test/offer döngüsüne geri beslemek
  - research/plan/build/QA döngüsünü tek akışta işletmek
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet. İlk form agency-style managed service.
  - Orta vadede white-label “AI Reception Recovery OS”.
  - Uzun vadede dikey SaaS + metered usage + premium QA/compliance katmanı.
- **Doğal evrim sırası:**
  1. managed service
  2. repeatable vertical package
  3. white-label dashboard
  4. self-serve SaaS
  5. voice + messaging + analytics operating system

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** POC için 1-2 hafta, ilk repeatable paket için 4-8 hafta
- **Aylık İşletme Maliyeti:**
  - usage-based POC: yaklaşık **$50-$150** / müşteri
  - higher-compliance / Bland tipi paket: **$300+** / müşteri sabit maliyet başlayabilir
  - ek no-code / SMS / CRM maliyetleri hariç değildir
- **Potansiyel Gelir:**
  - giriş seviyesi managed service: **$300-$500/ay** / müşteri
  - daha hacimli/regüle hesaplar: **$1,000-$2,500/ay** / müşteri bandı mümkün
  - one-time kurulum bedeli ayrıca alınabilir
- **ROI Beklentisi:**
  - usage-based stack ile **1 müşteri** dahi hızlı break-even getirebilir
  - daha yüksek fixed-cost stack'te **2-3 müşteri** gerekir
  - gerçek ROI, kaçırılan çağrıdan dönen randevu oranına bağlıdır

## Mevcut Sistemle Entegrasyon
- `durumraporu.md`'ye göre `universe_loop.sh` ana döngü zaten çalışıyor. Bu döngü, hangi dikeyin önce denenmesi gerektiğine dair araştırma/backlog üretmeye devam edebilir.
- `STATE_SUMMARY.json` şu an **113 aktif / 90 live / 45 healthy** gösteriyor. Bu Vercel yüzeyi, dikey landing page, ROI calculator, call demo page ve niche lead magnet üretmek için hazır altyapı demek.
- Mevcut ürün fabrikası şu şekilde leverage edilir:
  - Vercel landing page'leri → niche-specific voice funnel sayfaları
  - mevcut research stack → sektör acı noktası çıkarmak
  - browser/search stack → local business prospecting ve rakip tarama
  - içerik/SEO kabiliyeti → “kaç missed call kaç para yakıyor?” içerikleri
- Kritik not: healthy_count düşük olduğu için, yeni voice offer'ı portföye katarken **health gate** koymak şart. Trafiği bozuk ürüne sürmek saçmalık.

## Riskler & Dikkat Edilecekler
- **Yanlış wedge riski:** tam otomatik outbound closer'a erken girmek. Bugün için gereksiz risk.
- **Compliance riski:** telemarketing, recording consent, PII saklama, sektör regülasyonları.
- **Latency riski:** 500-600 ms üstüne çıkarsan çağrı plastikleşir ve insanlar kapatır.
- **Delivery riski:** community sinyali çok net — satış kolay, delivery boğucu. Teknik disiplin yoksa müşteri kızar.
- **Vendor lock-in:** Vapi/Retell/Bland/Twilio fiyat ve limitleri değişebilir.
- **Operational blind spot:** voicemail, duplicate bookings, calendar conflicts, tool failure, no-show takibi.
- **Portfolio distraction:** UniverseCreator zaten geniş. Bu fikri tek dikeyden başlatmadan 7 farklı voice offer açmak odak kaybı yaratır.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek dikey seç ve ROI sheet çıkar:** dental veya cleaning. “Ayda X missed call → Y randevu → Z gelir kaybı” hesabını netleştir.
2. **Usage-based POC kur:** Retell veya Vapi + Twilio + calendar + Sheets/HubSpot. 20-30 test çağrısı yap, QA rubric ile puanla.
3. **Tek bir Vercel funnel aç:** niche landing page + demo audio + ROI calculator + book-demo CTA. Önce tek offer'ı keskinleştir, sonra ölçekle.
