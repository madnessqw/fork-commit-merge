# Araştırma #14 — AI Calling Agents (2. Tur / 2026 doğrulama)
**Tarih:** 2026-04-21 11:19 +03
**Konu:** AI Calling Agents — Vapi / Retell / Bland / Twilio ekosisteminde gelir, maliyet, risk ve uygulama boşlukları

**Kaynaklar:**
- Vapi pricing: https://vapi.ai/pricing
- Vapi enterprise/customer metrics: https://vapi.ai/enterprise
- Vapi automotive case study: https://vapi.ai/blog/case-study-automotive
- Vapi voice testing docs: https://docs.vapi.ai/test/voice-testing
- Vapi voicemail detection docs: https://docs.vapi.ai/calls/voicemail-detection
- Retell pricing: https://www.retellai.com/pricing
- Retell iSpeedToLead case study: https://www.retellai.com/case-studies-new/ispeedtolead-retell-ai-lead-response-case-study
- Retell TripleTen case study: https://www.retellai.com/case-studies-new/tripleten-ai-call-automation-admissions-case-study
- Retell Boatzon case study: https://www.retellai.com/case-study/how-retell-ai-became-boatzons-top-performing-employee
- Retell Anker case study: https://www.retellai.com/case-study/how-anker-transformed-global-customer-support-with-human-quality-al-voice
- Bland pricing: https://www.bland.ai/pricing
- Twilio US Voice pricing: https://www.twilio.com/en-us/voice/pricing/us
- Grand View Research AI Voice Agents Market: https://www.grandviewresearch.com/industry-analysis/ai-voice-agents-market-report
- FCC July 17, 2024 AI robocall fact sheet: https://docs.fcc.gov/public/attachments/DOC-404036A1.pdf
- FCC enforcement / Feb 8, 2024 AI voice confirmation reference: https://docs.fcc.gov/public/attachments/FCC-24-59A1.pdf
- Product Hunt — Vapi: https://www.producthunt.com/products/vapi
- Product Hunt — Retell AI: https://www.producthunt.com/products/retell-ai
- Product Hunt — Relyable: https://www.producthunt.com/products/relyable
- Indie Hackers — Rosie: https://www.indiehackers.com/post/tech/from-failure-to-1m-arr-in-8-months-oA0AqL4jY25lxrQ4uGBl
- GitHub — realtime-phone-agents-course: https://github.com/neural-maze/realtime-phone-agents-course
- GitHub — voicetest: https://github.com/voicetestdev/voicetest
- GitHub — Outbound Real State Voice AI Agent: https://github.com/Awaisali36/Outbound-Real-State-Voice-AI-Agent-
- Reddit signals: https://reddit.com/r/sales/comments/1ooeqfx/demod_an_ai_voice_platform_and_yes_it_will_take/ , https://reddit.com/r/Entrepreneur/comments/1skhn6y/my_business_failed_not_sure_how_to_pivot_help/
- MCPTube / workflow videos: https://www.youtube.com/watch?v=BO-jFbN4p8Y , https://www.youtube.com/watch?v=UJg8DDojyMk , https://www.youtube.com/watch?v=X8XYBzQeko4
- ArXiv: https://arxiv.org/abs/2604.04847 , https://arxiv.org/abs/2603.25727 , https://arxiv.org/abs/2604.15037 , https://arxiv.org/abs/2604.01897 , https://arxiv.org/abs/2604.14604

## Özet Bulgular
- **Doğru wedge hâlâ aynı ama artık daha net:** en iyi ticari giriş noktası cold-call spam değil, **missed-call recovery + speed-to-lead**. Resmî case study’lerde gelir ve dönüşüm artışı burada görünüyor; Reddit tarafındaki anti-spam hissiyatı da bunu destekliyor.
- **Kategori büyüyor ama platform savaşı tek başına yetmiyor.** Grand View Research verisine göre AI voice agents pazarı 2025’te **$2.54B**, 2033’te **$35.24B**, CAGR **%39.0**. Ama pazarı kazanan sadece “daha doğal ses” değil; eval, observability, compliance ve dikey workflow sahibi olanlar.
- **Maliyet yapısı platforma göre ciddi değişiyor:** Vapi geliştirici esnekliği veriyor ama provider maliyetlerini ayrıca taşıyorsun; Retell daha net pay-as-you-go; Bland fiyatı sadeleştiriyor ama ücretli katmanlarda sabit platform fee devreye giriyor. Twilio hâlâ telephony katmanı, ürün değil.
- **Gerçek kullanım örnekleri artık hacimli:** Vapi otomotiv örneği 10k-15k çağrı/gün ve revenue +%200; Retell örnekleri 2 dakika içinde form sonrası arama, +%20 pickup/conversion, 7-8 rep işini 1 agent ile karşılama gibi somut metrikler veriyor.
- **Teknik frontier hâlâ kırılgan.** Yeni akademik çalışmalar turn-taking, ASR dayanıklılığı, proactive behavior ve audio prompt injection tarafında önemli açıklar gösteriyor. Yani “insandan ayırt edilemez bot” pazarlaması çok gürültülü; üretimde asıl mesele güvenli fallback ve ölçüm.

## Gerçek Başarı Hikayeleri

### 1) Vapi — Latin Amerika otomotiv marketplace
- Resmî Vapi case study’sine göre (7 Ocak 2026): **10,000-15,000 çağrı/gün**, **450+ eşzamanlı çağrı**, **5 ülke**, **1000+ localized agent**.
- Sonuçlar: **çağrı merkezi footprint -%50**, **CAC -%50**, **revenue +%200**.
- En kritik ders: başarı “tek bir ses modeli” değil; MCP/internal services + telephony + observability + ölçeklenebilir altyapı.

### 2) Retell — ISpeedToLead
- Resmî case study’de AI agent’ın **form submit’ten 2 dakika içinde** arama başlattığı belirtiliyor.
- Akış: tek core qualification sorusu, yüksek değerli lead’e **SMS ile booking link**, Zoho + GoHighLevel + Make + Calendly entegrasyonu.
- Çıkarım: local-business ya da high-intent lead akışında “ilk arayan kazanır” mantığı gerçek.

### 3) Retell — TripleTen
- Resmî case study metrikleri: **+17,000 AI-handled calls**, **+200 saat/ay tasarruf**, **pickup + conversion rate +%20**.
- Branded Caller ID kritik: case study’de bu özelliğin performansı kaldırdığı açık yazıyor; geçici yokluğunda pickup rate’in düştüğü belirtiliyor.
- Ders: arayan numara güveni, ses kalitesi kadar önemli.

### 4) Retell — Boatzon
- Resmî case study “At a glance” kısmı: **1 AI agent, 7-8 insan temsilcinin operasyonunu geçti**; **same-day launch**; **weeks içinde tam entegrasyon**; **%80 call quality benchmark** korunmuş.
- Lead’lere **uygulamadan dakikalar içinde** dönülüyor.
- Ders: AI caller en iyi, insanın peşinden koştuğu sıcak lead’de çalışıyor.

### 5) Retell — Anker
- Resmî case study: **80.4% case resolution**, **NPS 63**, **95%+ speech recognition accuracy**, **<2 saniye latency**.
- Kullanım alanı: global consumer support, post-sales support, out-of-office inquiries.
- Ders: enterprise tarafı duygu sömürüsü değil KPI satın alıyor.

### 6) Rosie — Indie Hackers / self-serve voice SaaS
- 14 Ağustos 2025 tarihli Indie Hackers hikâyesine göre Rosie, bir pivot sonrası **8 ayda $1M ARR**’a ulaştı.
- Stack tercihi olarak kurucu açıkça **Bland.ai** kullandığını söylüyor.
- GTM: ilk traction cold email ile, sonra Meta/Google ads, sonra SEO. Base fiyatı **$49/ay** ile düşük tutulmuş.
- Ders: sadece agency değil, self-serve SMB voice ürünü de çalışıyor; ama bu lane’de onboarding ve fiyatlama oyunu farklı.

### 7) SavvyAgents dental case — yüksek sinyal, düşük güven
- Vendor-published case’e göre bir dental clinic 30 günde **417 çağrı**, **32 appointment**, **$38,400 recovered revenue**, **25 saniye ortalama response time** ve **%98 call capture** görmüş.
- 90 günde 2 lokasyonda **1,700+ call**, **180+ appointment**, **$247,500 production revenue** iddia ediliyor.
- Not: Bu rakamlar vendor case study; yön gösterir ama bağımsız doğrulama değil.

## Pazar Büyüklüğü & Fırsat
- Grand View Research: **2025 market size $2.54B**, **2026 $3.51B**, **2033 $35.24B**, **CAGR %39.0**.
- Aynı rapor North America’yı 2025’te en büyük pazar, Asia Pacific’i en hızlı büyüyen bölge olarak işaretliyor.
- Product Hunt sinyali de kategori momentumunu doğruluyor:
  - **Vapi** ürün sayfasında 4.9/5 puan, 23 review, 1.3K follower; 2 Nisan 2025 launch’ı günün **#5** ürünü olmuş.
  - **Retell AI** ürün sayfasında 621 follower ve 299 puan civarı topluluk görünürlüğü var.
  - **Relyable** gibi “simulation + monitoring for voice agents” oyuncuları ortaya çıkmış durumda; bu önemli çünkü piyasa artık sadece arama motoru değil, QA katmanı da satın alıyor.
- Bottom-up fırsat (tahmin): local business voice automation için **$500-$1,500 kurulum + $300-$800 MRR** bandı hâlâ mantıklı. 10 müşteri = **$3K-$8K MRR + kurulum gelirleri**. Bu rakam tahmindir; resmî platform case’leri ve topluluk fiyat örneklerinden türetildi.

## Maliyet Karşılaştırması — Şu Anki Gerçekler

### Vapi
- Resmî pricing sayfası: **$0.05/dk Vapi hosting**, provider maliyetleri **at cost**.
- **10 concurrency included**, üstü **$10/line/month**.
- Call history varsayılan **14 gün**.
- **HIPAA Zero Data Retention add-on: $1000/ay**.
- Güçlü taraf: geliştirici kontrolü, observability, MCP, testing, 4,200+ config point.
- Zayıf taraf: toplam gerçek maliyet tek rakam değil; STT/TTS/LLM/transport katmanlarını ayrıca düşünmek gerekiyor.

### Retell
- Resmî pricing sayfası: **$10 free credits**, **$0.07-$0.31/dk** AI voice agents, **20 free concurrent calls**.
- Aynı sayfada detay kırılımı da var: **Retell Voice Infra $0.055/dk**, birçok platform voice için **$0.015/dk**, GPT 5.4 standard **$0.080/dk**, Claude 4.6 Sonnet **$0.08/dk**.
- Güçlü taraf: ilk pilot için net paygo, güçlü case study havuzu, batch call / branded call ID / verified numbers / post-call analysis.
- Zayıf taraf: ses-model kombinasyonuna göre dakika maliyeti hızla şişebilir.

### Bland
- Resmî pricing sayfası:
  - Start: **free + $0.14/dk**, **10 concurrent**, **100 calls/day**
  - Build: **$0.12/dk + $299/ay**, **50 concurrent**, **2,000 calls/day**
  - Scale: **$0.11/dk + $499/ay**, **100 concurrent**, **5,000 calls/day**
- Artı: “LLM + STT + TTS + telephony dahil” diye sade fiyatlama sunuyor.
- Eksi: volume düşükse platform fee moral bozabilir.

### Twilio
- Resmî US voice pricing: **local outbound $0.0140/dk**, **local inbound $0.0085/dk**, local numara **+$1.15/ay**.
- Twilio agent değil, taşıyıcı/infrastructure katmanı. Kendi stack’ini kuruyorsan gerekli; ürünleşme için tek başına yetmez.

## Rakipler & Boşluklar

| Katman | Oyuncular | Gerçek durum | Boşluk |
|---|---|---|---|
| Voice platform | Vapi, Retell, Bland | Platformlar hızla yakınsıyor | Outcome dashboard + compliance-first vertical paket |
| DIY infra | Twilio + FastRTC + open-source STT/TTS | Kontrol yüksek, bakım derdi yüksek | Küçük ekip için erken aşamada gereksiz kahramanlık |
| SMB/self-serve product | Rosie, Pernell, heyLibby, Sandra AI | Dikey/self-serve lane kalabalıklaşıyor | TR/MENA çok dilli, consent-first, raporlanabilir ürün |
| QA / eval | Vapi Voice Testing, voicetest, Relyable | Yeni ama kritik katman | “voice ops QA + ROI analytics” birleşik ürün çok boş |

### Reddit / community intelligence ne diyor?
- r/sales tarafında iki net duygu var: **“demo çok etkileyici”** ve **“tek kötü arama ilişkiyi yakar”**. Yani satış için hype var ama güven eşiği acımasız.
- r/Entrepreneur’daki AI receptionist pivot post’u “race to the bottom” riskini net söylüyor: sadece tool-layer satarsan ezilirsin.
- En faydalı çıkarım: “AI receptionist kurarım” cümlesi commodity oldu. “Missed calls → booked revenue → dashboard” cümlesi hâlâ satılabilir.

## Teknik Gereksinimler

### Minimum ticari sistem
- Trigger kaynakları: form submit, missed call, callback request, inbound overflow, CRM status change
- Lead prep: dedupe, consent flag, timezone, E.164 normalize, invalid-number branch
- Call engine: Vapi veya Retell
- Post-call: transcript, summary, structured outputs, booking status, retry status
- CRM/logging: Google Sheets / Airtable / HubSpot / GHL
- Follow-up: SMS / WhatsApp / email booking link
- Human handoff: canlı transfer veya callback kuyruğu

### Üretimde şart olan ama çoğu demo’nun salladığı parçalar
- **Voice testing / eval:** Vapi docs artık simüle telefon çağrılarıyla rubric tabanlı test sunuyor. `voicetest` de Retell/Vapi/Bland/LiveKit import + LLM judge + CI/CD veriyor.
- **Voicemail strategy:** Vapi docs bunu ayrı ürün seviyesi konu yapmış; detection method, backoff, beep wait, false positive tuning var. Bu, gerçek dünyada voicemail’ın demo detayı değil maliyet kalemi olduğunu gösteriyor.
- **Branded Caller ID / verified numbers:** TripleTen örneği bunu doğrudan conversion faktörü yapıyor.
- **Observability:** call reason, transfer reason, voicemail, cost, transcript quality, ASR confidence, opt-out flag loglanmalı.
- **Permissioning:** hassas aksiyonlarda (ör. ödeme almak, üyelik iptali, kritik veri değiştirmek) sesli onay tek başına yetmez; ikinci doğrulama gerekir.

### Akademik bulguların pratik etkisi
- **Full-Duplex-Bench-v3 (2026):** GPT-Realtime Pass@1’da **0.600**; Gemini Live 3.1 latency’de **4.25s** ile hızlı ama turn-take oranı **%78.0**; cascaded yaklaşım **10.12s** ile çok yavaş. Çıkarım: düşük gecikme hâlâ zor.
- **WildASR (2026):** gerçek konuşma koşullarında ASR performansı ciddi ve dengesiz düşüyor; modeller konuşulmayan içeriği halüsinasyon olarak üretebiliyor. Çıkarım: gürültülü saha ortamı, lüks problem değil, ürün problemi.
- **ProVoice-Bench (2026):** 1,182 örnekle proactive voice agent’larda over-triggering ve reasoning açığı gösteriyor. Çıkarım: botun ne zaman konuşmayacağını bilmesi de konuşması kadar kritik.
- **FastTurn (2026):** gerçek diyalog verisiyle düşük latency turn detection iyileşiyor. Çıkarım: full-duplex kalite, önümüzdeki 12 ayın rekabet alanlarından biri.
- **AudioHijack (2026):** 13 modelde **%79-%96** arası saldırı başarısı raporlanıyor. Çıkarım: sesli prompt injection gerçek; tool erişimi olan voice agent’a kör güven aptallık.

## Hukuk & Uyum — Burada artistlik yok
- **8 Şubat 2024:** FCC, TCPA’daki “artificial or prerecorded voice” kısıtlarının **AI-generated human voices** için de geçerli olduğunu teyit etti.
- **17 Temmuz 2024:** FCC, AI-generated call disclosure’ını ve consent açıklamalarını güçlendiren kuralları **önerdi**; özellikle çağrının başında AI kullanıldığının açıkça belirtilmesi önerisi var.
- **5 Mart 2026 tarihli FCC materyalleri hâlâ proposal dilinde** görünüyor. **İnference:** disclosure tarafı “tamamen oturdu, rahatız” diyeceğin bir alan değil; hâlâ değişen bir regülasyon zemini var.
- Sonuç: ilk ürün cold outbound değil, **first-party, consent-based, intent-high** akış olmalı.

## Ham Notlar
- MCPTube’daki Vapi+n8n videolarında ortak workflow aynı: **form/lead list → number normalize → call create → wait/poll/webhook → transcript/summary/recording/cost → Sheets/Airtable/CRM update → SMS/booking link**.
- GitHub’daki en güncel repo’lar artık sadece “nasıl ararım” değil, **nasıl test ederim, nasıl trace ederim, nasıl CI’ya sokarım** sorusuna odaklanıyor. Bu iyi haber: QA artık ürünün merkezine geldi.
- Product Hunt Jina fetch’i doğrudan 403 verdi; web search fallback’i ile ürün sayfaları okundu.
- En önemli iş dersi: platform satmak kolayca commodity’ye dönüyor; **dikey şablon + sonuç paneli + compliance** daha savunulabilir.
