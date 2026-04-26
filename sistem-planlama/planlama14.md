# Planlama #14 — AI Calling Agents Uygulama Haritası
**Tarih:** 2026-04-21 11:19 +03
**Bağlı Araştırma:** arastirma14.md

## Swarm Agent ile Nasıl Uygulanır?

Bu turdaki net karar şu:

**Genel-purpose “AI cold caller” kurma.**

Bu fikir hem hukuken çamurlu hem de artık commodity. Doğru ürün:

**Consent-based Missed-Call Recovery + Speed-to-Lead Operating System**

Yani kullanıcıya satılan şey “AI ses” değil, şu çıktı:
- kaç çağrı kaçtı?
- kaçı geri kazanıldı?
- kaçı randevuya döndü?
- kaçı gelir pipeline’ına girdi?
- maliyet / booked appointment ne oldu?

### Swarm rol dağılımı
- **Research Agent:** hedef dikeyleri seçer, rakip/review mining yapar, call pain map çıkarır.
- **Offer Agent:** her dikey için teklif, ROI hesabı, fiyatlandırma ve paket çıkarır.
- **Flow Architect:** trigger → call → booking → CRM → reporting akışını standartlaştırır.
- **QA/Eval Agent:** voice test suite, transcript rubriği, failure taxonomy ve weekly review üretir.
- **Analytics Agent:** booked call, missed-call recovery, pickup, voicemail, opt-out, cost/minute dashboard üretir.
- **Human:** compliance kararı, müşteri görüşmesi, pricing onayı, outbound izni.

## Gerekli Bileşenler
- **Script/Bot:**
  - lead intake/trigger router
  - consent + dedupe + phone normalize katmanı
  - call orchestration worker
  - voicemail / retry policy
  - post-call parser
  - CRM updater
  - QA sampler
  - weekly ROI reporter
- **MCP/Araç:**
  - araştırma için web + arxiv + mcptube
  - CRM/log için Sheets/Airtable/HubSpot/GHL
  - browser araçları landing/demo/audit için
  - eval için Vapi Voice Testing veya `voicetest`
- **API:**
  - **Phase 1 öneri:** Retell (pilot hız, net paygo, güçlü case study seti)
  - **Phase 2 opsiyon:** Vapi (daha derin kontrol, eval/observability, provider abstraction)
  - telephony için gerekirse Twilio/Telnyx/BYOC
  - Cal.com / Calendly
  - SMS/WhatsApp kanalı
- **İnsan Müdahalesi:**
  - ilk 30-50 çağrı QA review
  - compliance/disclosure metni
  - ilk teklif görüşmeleri
  - düşük güvenli call’larda manual handoff

## Workflow Haritası
**Tetikleyici →** form submit / missed call / callback request / CRM event

1. Lead gelir.
2. Consent kontrolü yapılır.
3. Numara normalize edilir; invalid ise insan kuyruğuna düşer.
4. Dikeye göre uygun agent persona + script seçilir.
5. Çağrı oluşturulur.
6. Voicemail detection devreye girer.
7. İnsan açarsa kısa qualification akışı çalışır.
8. Uygunsa booking link SMS/WhatsApp/email ile gönderilir veya canlı transfer yapılır.
9. No-answer/voicemail ise retry policy veya voicemail bırakma branch’i çalışır.
10. Call bitince transcript + summary + structured outputs alınır.
11. CRM/Sheets güncellenir.
12. QA agent düşük güven, complaint, hallucination, opt-out ve cost anomaly call’larını işaretler.
13. Analytics agent haftalık rapor çıkarır.

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

### Hemen uygulanabilir hamle
**Tek dikeyde “Missed-call + form follow-up recovery” demo paketi.**

En mantıklı ilk dikeyler:
- HVAC / plumbing
- dental / medspa
- financing / insurance lead follow-up

### En düşük çaba / en yüksek çıktı adımı
- “Cevapsız çağrı ve form lead’lerini 2 dakika içinde arayan, kısa qualify eden, booking link yollayan agent” demosu.
- Bunu **genel AI receptionist** diye değil, **revenue recovery system** diye konumla.

### Hangi mevcut araç/script bu işi kısmen yapar?
- MCPTube’da zaten görülen Vapi+n8n pattern’leri
- GitHub’daki Airtable/Sheets tabanlı Vapi örnekleri
- Retell’in resmî batch/booking/call analysis feature seti
- Vapi voice testing + `voicetest` ile test katmanı

### POC için minimum gereksinimler
- 1 vertical prompt pack
- 1 booking link / calendar
- 1 CRM log tablosu
- 10-15 test senaryosu
- consent/disclosure metni
- manual override kuralı

### Tahmini kurulum süresi ve ilk gelir beklentisi
- **Kurulum süresi:** 4-7 gün (plan + prompt + flow + QA spec)
- **İlk gelir beklentisi (tahmin):** 1 pilot müşteri için **$500-$1,500 setup**, ardından **$300-$800 MRR**
- **Pilot operating cost (tahmin):** düşük hacimde **$50-$200/ay/client**

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

1. ay sonunda hedef çalışan demo değil, **tekrarlanabilir vertical template**.

### Hedef görünüm
- 2 dikeyde tekrar kullanılabilir prompt pack
- ortak call-state modeli
- ortak QA rubric
- ortak metrics dashboard
- ortak consent/disclosure blokları

### Başarı metric’leri
- first-call latency
- pickup rate
- voicemail rate
- call-to-booking rate
- booked appointment başına maliyet
- opt-out / complaint rate
- transcript failure rate
- human handoff rate
- MRR / gross margin

### Paralel çalışabilecek adımlar
- Research: yeni dikey ve offer keşfi
- Flow: ortak trigger/call/post-call şablonu
- QA: voice tests + judge rubric
- Analytics: ROI dashboard
- Sales: demo video + case narrative

### Ölçeklendirme için gerekenler
- branded caller ID / verified number
- merkezi suppression / opt-out listesi
- client bazlı workspace izolasyonu
- transcript retention policy
- weekly optimization loop
- platform abstraction (tek vendor’a kilitlenmemek için)

### Checkpoint’ler ve başarı kriterleri
- **Hafta 2:** 10+ senaryolu QA planı ve tek vertical offer net
- **Hafta 4:** demo-ready pilot flow + 1 canlı pilot aday
- **Ay 2:** 2-3 ücretli müşteri ya da eşdeğer güçlü pipeline
- **Ay 3:** vertical template + weekly report + QA cycle oturmuş

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

### En iyi senaryo
- Çok kiracılı voice ops platformu
- dikey bazlı prompt + eval + reporting paketleri
- intake formundan otomatik agent config üretimi
- call transcript’lerinden otomatik script optimizasyonu
- çok dilli paketler (TR / EN / AR) ile MENA açılımı

### Yeni gelir kolları
- voice agent QA-as-a-service
- “missed-call revenue audit” ürünü
- vertical template marketplace
- ROI dashboard / analytics micro-SaaS
- white-label local business automation paketi
- enterprise için compliance review + transcript risk scanning

### Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek şey
- platform değil **operating system** satmak
- her müşteriye haftalık “ne bozuldu / ne iyileşti / hangi script işe yaradı” raporu vermek
- araştırma + planlama + QA + reporting’i aynı loop’ta tutmak
- yeni vertical’e geçişi sıfırdan kurmak yerine şablonlaştırmak

### White-label veya SaaS olarak satılabilir mi?
- **White-label:** evet, kısa-orta vadede daha gerçekçi
- **SaaS:** evet, ama önce service layer ile hangi feature’ların gerçekten para ettiğini görmek lazım
- Kestirme yok: önce 5-10 canlı müşteri, sonra self-serve

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** POC 1 hafta, tekrar kullanılabilir sistem 4-8 hafta
- **Aylık İşletme Maliyeti:** tahmini **$100-$500/client** (hacme ve vendor seçimine göre)
- **Potansiyel Gelir:** tahmini **$300-$800 MRR/client** + **$500-$1,500 setup**
- **ROI Beklentisi:** ilk 1-2 ücretli müşteri ile break-even; 5 müşteri civarında sistem anlamlı hâle gelir

## Mevcut Sistemle Entegrasyon
- UniverseCreator’ın araştırma döngüsü, yeni vertical araştırması ve case-study biriktirme işini zaten yapıyor; bu lane doğrudan mevcut `sistem-planlama` arşivine oturuyor.
- `arastirma*.md` dosyaları vertical knowledge base gibi kullanılabilir.
- Gelecek execution modunda swarm şu şekilde ayrılmalı:
  - biri call script / prompt ve eval rubric
  - biri CRM/reporting şeması
  - biri offer/case-study/sales materyali
- 113 ürün ve mevcut Vercel evreni bu ürün için landing / audit / demo sayfası altyapısı olabilir. Ama burada deploy yok; sadece plan.

## Riskler & Dikkat Edilecekler
- **Compliance riski:** FCC/TCPA tarafında AI voice zaten riskli alan; disclosure ve consent’i hafife almak aptallık.
- **Spam algısı:** cold outbound lane’i kısa vadede marka çürütür.
- **ASR/latency kırılganlığı:** saha gürültüsü, aksan, overlap, arka plan sesi performansı bozar.
- **Audio prompt injection:** tool erişimi olan sesli ajanı ikinci doğrulamasız bırakma.
- **Vendor lock-in:** Vapi/Retell/Bland fiyat veya policy oynarsa margin bozulur.
- **Fixed-price paket riski:** dakika maliyetini bilmeden sınırsız kullanım satmak zarar ettirir.
- **Support yükü:** her müşteri için custom flow yapmak agency’i öldürür; vertical template şart.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek wedge seç:** “Missed-call recovery + speed-to-lead” için ilk vertical’i kilitle ve value proposition’ı tek cümlede netleştir.
2. **KPI + QA iskeleti çıkar:** pickup, booking, cost, opt-out, voicemail, transcript failure metriklerini ve test senaryolarını yaz.
3. **Teklif paketi oluştur:** setup + retainer + usage mantığını ve hangi sonucu sattığını açıklaştır; “AI receptionist” değil “recovered revenue system” diye paketle.
