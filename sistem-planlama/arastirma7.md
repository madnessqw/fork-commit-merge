# Araştırma #7 — Voice AI + Sales Funnel
**Tarih:** 2026-04-21 06:18 +03
**Konu:** Voice AI ajanlarıyla missed-call recovery, lead qualification, appointment booking ve düşük-touch satış funnel'ı kurmak; özellikle inbound/after-hours kullanımından başlayıp gerekirse outbound'a genişlemek.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma0-6.md` / `planlama0-6.md`
- Local state: `/home/gokhan/UniverseCreator/STATE_SUMMARY.json`, `/home/gokhan/UniverseCreator/durumraporu.md`
- Sierra Ventures Voice AI Market Map: https://www.sierraventures.com/content/voice-ai-market-map
- Fortune Business Insights Conversational AI public summary: https://www.fortunebusinessinsights.com/conversational-ai-market-109850
- Vapi pricing overview: https://vapi.mintlify.app/pricing
- Vapi billing examples: https://vapi.mintlify.app/billing/examples
- Vapi estimating costs: https://vapi.mintlify.app/billing/estimating-costs
- Vapi sales outreach agent page: https://vapi.ai/custom-agents/sales-outreach-agent
- Retell pricing: https://www.retellai.com/pricing
- Retell AI appointment setter: https://www.retellai.com/ai-appointment-setter
- Retell TripleTen case study: https://www.retellai.com/case-studies-new/tripleten-ai-call-automation-admissions-case-study
- Bland pricing: https://www.bland.ai/pricing
- Twilio US voice pricing: https://www.twilio.com/en-us/voice/pricing/us
- GitHub: https://github.com/pipecat-ai/pipecat , https://github.com/livekit/agents , https://github.com/openai/openai-realtime-twilio-demo , https://github.com/VapiAI/examples
- Reddit: https://reddit.com/r/automation/comments/1m5nbmx/ , https://reddit.com/r/Entrepreneur/comments/1lzsj7o/ , https://reddit.com/r/VoiceAutomationAI/comments/1s368zs/
- ArXiv: https://arxiv.org/abs/2508.04721 , https://arxiv.org/abs/2509.04871 , https://arxiv.org/abs/2602.18448
- YouTube/MCPTube: https://www.youtube.com/watch?v=yKn0qKakUOk , https://www.youtube.com/watch?v=-iLRyOghSYI , https://www.youtube.com/watch?v=BO-jFbN4p8Y , https://www.youtube.com/watch?v=X8XYBzQeko4

## Özet Bulgular
- Bu alanda ilk para eden wedge “tam otomatik soğuk satış closer'ı” değil; **after-hours receptionist + missed-call recovery + appointment booking + lead qualification**. Resmî Retell sayfaları, Reddit deneyimleri ve telesales paper'ı aynı yere işaret ediyor: rutin çağrılar tamam, karmaşık ikna ve objection handling hâlâ zayıf.
- **2026 birim ekonomisi netleşmiş durumda.** Vapi resmî örneğinde outbound real-estate lead-gen senaryosu **1,000 çağrı x 4 dk = 4,000 dk/ay** için **$520/ay** toplam maliyet veriyor; yani yaklaşık **$0.13/dk**. Retell'in kamuya açık breakdown'ında örnek speech-to-speech yapı **$0.11/dk** görünüyor; buna ABD Twilio telephony **$0.015/dk** eklenince yaklaşık **$0.125/dk** bandı oluşuyor. Bu, düşük hacimli SMB use-case'lerinde sağlıklı marj bırakıyor.
- **Bland fiyatlaması değişmiş.** Arama cache'lerinde hâlâ “free / $0.14” kırıntıları dolaşıyor ama 2026-04-21 canlı Jina okumasında kamuya açık planlar **Build = $299/ay + $0.12/dk**, **Scale = $499/ay + $0.11/dk**. Yani Bland artık “çok ucuz giriş” değil; daha çok bundle/compliance/sadelik ürünü.
- Gerçek işaretler var. TripleTen, Retell case study'de **pickup + conversion rate'i %20 artırmış**, **ayda 200+ saat** kazanmış ve **17,000+ çağrıyı** AI ile işlemiş. Community tarafında bir örnek diş kliniği ajanını **$24K/yıl** diye paketliyor; başka bir side-hustle post'u ise **$2K-$4K/ay recurring** gördüğünü söylüyor. Bunlar denetlenmiş finansal tablo değil, ama talep tarafı boş değil.
- Asıl moat “sesli bot” değil. **Latency, turn-taking, voicemail/retry logic, CRM+calendar entegrasyonu, QA/compliance, human fallback ve dikey prompt/knowledge-base paketi**. Sierra Ventures'ın 2025 haritası 150+ şirket gösteriyor; yani çıplak voice layer commodity'leşiyor.

## Gerçek Başarı Hikayeleri
- **TripleTen × Retell (resmî vaka):** Retell'in customer story sayfası, admissions çağrı otomasyonunda **pickup ve conversion rate'de %20 artış**, **aylık 200+ saat tasarruf** ve **17,000+ AI tarafından işlenen çağrı** raporluyor. Ayrıca branded caller ID kaldırıldığında pick-up rate'in düştüğünü söylüyor; bu da telephony/presentation detayının boş laf olmadığını gösteriyor.
- **Dentist after-hours agent — Reddit self-report:** r/automation'daki örnekte creator, bir diş kliniği için after-hours booking agent'ının **$24K/yıl** değerle satıldığını ve ayda yaklaşık **20 lead** kurtardığını, lead başına değeri **$300** kabul ettiklerini yazıyor. Denetlenmiş değil; ama “kaçırılan çağrıyı gelir geri kazanımına çevir” tezi çok somut.
- **Voice agent side income — Reddit self-report:** r/VoiceAutomationAI'de bir satıcı, Retell partner programı üstünden 2026 başından beri **$2K-$4K/ay** recurring side-income gördüğünü yazıyor. Aynı post'un daha değerli kısmı şu: satış kolay, delivery zor. Teknik olmayan kurucu her ajan için **20-30 saat** gömüp latency ve Make hatalarıyla boğuşmuş.
- **Local SMB offer math — creator claim:** Travis Wardrop videosunda AI receptionist kurulumu için **$300-$500/ay** retainer dilini kullanıyor; aynı videoda pitch cümlesi “önümüzdeki 7 günde 3-5 appointment” vaadine dayanıyor. Bu creator marketing, muhasebe defteri değil; ama local-business pricing anchor'ı veriyor.
- **Outbound qualification workflow — creator + gerçek teknik akış:** Nate Herk videosunda n8n + Vapi ile form submission sonrası anında arama, structured outputs, voicemail ayrımı ve CRM/Sheets logging akışı gösteriliyor. Bu, “sadece demo bot” değil, satış sürecine bağlanan çalışan bir playbook olduğunu kanıtlıyor.

## Pazar Büyüklüğü & Fırsat
- **Geniş pazar büyüyor:** Fortune Business Insights'in kamuya açık özetine göre global conversational AI pazarı **2025'te $14.79B**, **2026'da $17.97B** ve **2034'te $82.46B** seviyesine gidiyor; CAGR **%21**. Voice-only değil, ama voice funnel bu pastanın büyüyen alt yüzeyi.
- **Kategori kalabalık ama canlı:** Sierra Ventures'ın 27 Ağustos 2025 tarihli haritası **150+ voice AI şirketi** listeliyor. Bu kötü haber değil; “pazar var” kanıtı. Kötü haber şu: generic agent satmak artık zor.
- **Dikey fırsat daha net:** Retell'in own-site positioning'i healthcare, insurance, logistics, home services ve finance tarafını öne çıkarıyor. Appointment setter sayfası özellikle “yüksek scheduling hacmi olan sektörler” diyor. Community yorumlarında da aynı pattern çıkıyor: **medspa / HVAC / cleaning / dental / home services** gibi dar intent set'li dikeylerde iş daha kolay.
- **Birim ekonomi SMB için mantıklı:** Retell/Vapi usage-based stack ile **300-800 dk/ay** arası tipik küçük hesapta kaba altyapı maliyeti çoğunlukla **$40-$110/ay** bandında kalabilir; telefon numarası ve no-code otomasyon eklenince de hâlâ agency-style **$300-$500/ay** teklifin altında kalır. Bu tahmin; resmî tarife sayfaları + provider örneklerinden türetilmiştir.
- **UniverseCreator leverage var:** `STATE_SUMMARY.json` şu an **113 aktif**, **90 live**, **45 healthy** ürün gösteriyor. Yani bu fikir için yeni dağıtım makinesi kurmuyoruz; mevcut Vercel portföyünden niş landing page, ROI calculator, “kaç missed call = kaç randevu kaybı” aracı ve demo funnel çıkarabiliriz.

## Rakipler & Boşluklar
- **Retell:** En temiz kamuya açık üretim positioning'lerinden biri. Güçlü yanı: açık component pricing, scheduling/CRM/telephony entegrasyonları, enterprise güvenlik ve somut case study. Zayıf yanı: outbound ve compliance katmanında hâlâ entegrasyon/ops işi istiyor.
- **Vapi:** Giriş bariyeri düşük, geliştirici dostu, template ve sample'lar var. Ama **5¢/dk** tek başına masal; gerçek maliyet provider'larla beraber geliyor. Resmî billing example bu farkı zaten kabul ediyor.
- **Bland:** “Tek fiyat, her şey dahil” basitliği çekici. Ama 2026 kamuya açık pricing'de platform fee geldiği için küçük hacimde pahalı kaçıyor. Compliance ve daha az moving part isteyen daha olgun hesaplar için mantıklı olabilir.
- **Twilio DIY + OpenAI Realtime:** En esnek yol ama “telephony + infra + model” parçaları sende. `openai/openai-realtime-twilio-demo` bunun üretime giden çıplak iskeletini veriyor. Güzel, ama ilk para için gereksiz kahramanlık olabilir.
- **Pipecat / LiveKit:** Star sayıları önemli: `pipecat-ai/pipecat` **11,461★**, `livekit/agents` **10,124★**. Bu repo'lar bize şunu söylüyor: daha derin kontrol isteyenler framework katmanına gidiyor. Yani uzun vadede middleware/QA/verticalization tarafı önem kazanacak.
- **Asıl boşluk:** “AI receptionist” değil, **recovered revenue pack**. Yani missed-call recovery + booking + CRM update + SMS fallback + QA report + weekly ROI. Çoğu oyuncu ya alt katmanda altyapı satıyor ya da üst katmanda parlak demo satıyor. Ortadaki operasyon paketi boş.
- **İkinci boşluk:** **TR/MENA + yerel dil + etik/compliance-ready paket.** İngilizce örnek bol; Türkçe/çok dilli, region-specific consent ve insan fallback kurgusu çok daha boş bir alan.

## Teknik Gereksinimler
- **Temel ses hattı:** ASR → LLM/SLM → TTS → telephony → CRM/calendar/tool calling. Sierra Ventures'a göre bu döngünün **500-600 ms altında**, TTS'nin de **100 ms altında** kalması gerekiyor; yoksa konuşma plastikleşiyor.
- **Önerilen başlangıç stack'i:**
  - Voice orchestration: **Retell veya Vapi**
  - Telephony: **Twilio** (veya vendor'ın native numarası, ama ölçeklemede BYOT daha sağlıklı)
  - Workflow: **n8n** veya **Make**
  - Scheduling: **Cal.com / Calendly / Google Calendar**
  - CRM/logging: **HubSpot / Sheets / Airtable / simple DB**
  - SMS fallback: Twilio / CRM SMS katmanı
- **Mutlaka gereken guardrail'ler:**
  - telefon numarası normalizasyonu
  - `endedReason` / voicemail ayrımı
  - structured outputs (budget, urgency, intent, booking status)
  - AI disclosure ve human transfer
  - canlı kişi istediğinde escalation
  - call replay / QA / transcript review
- **Compliance katmanı:** call recording consent, DNC/telemarketing, PII redaction, veri saklama politikası, sektör bazlı kısıtlar. `INSURE-Dial` paper'ı audit-grade reliability'nin hâlâ zor olduğunu açık söylüyor.
- **Model davranışı gerçeği:** `Cloning a Conversational Voice AI Agent from Call Recording Datasets for Telesales` paper'ı, AI ajanının rutin bölümlerde insana yaklaşabildiğini ama **persuasion ve objection handling** tarafında geride kaldığını söylüyor. Bu yüzden ilk ürün “yakala / sırala / randevuya çevir” olmalı; “kapat / ikna et / fiyat pazarlığı yap” değil.
- **Gerçek-time kalite gereği:** `Toward Low-Latency End-to-End Voice Agents...` paper'ı streaming ASR + quantized LLM + real-time TTS kombinasyonunda real-time factor'ın 1.0 altına inebildiğini gösteriyor. Yani teknik olarak yapılabiliyor; ama doğru pipeline kurulursa.
- **Teknik borç noktaları:** voicemail detection, barge-in / turn-taking, kötü bağlantı gürültüsü, çok dilli accent handling, duplicate tool-call'lar, webhook timeout'ları, calendar conflict handling.

## Ham Notlar
- `ddgr` bu cycle'da üç ayrı sorguda da **HTTP 202 / []** döndürdü. İnat edip boş sonuç yazmak yerine web search + Jina + Reddit JSON + GitHub + ArXiv ile devam ettim. Not düşüyorum çünkü sonraki cycle'da ddgr tarafı ayrıca tamir edilmeli.
- Arama cache'i ile canlı sayfa aynı şey değil. En net örnek **Bland pricing**: bazı snippet'ler hâlâ eski ücretsiz planı gösteriyor, ama 2026-04-21 canlı Jina okuması Build/Scale pricing'e dönmüş durumda.
- `projeler.txt` tarafında doğrudan voice-sales stack az ama leverage var: Twilio/WhatsApp automation referansı, VoiceMCP, local voice assistant ve çeşitli speech repo'ları mevcut. Yani sıfırdan öğrenme zorunluluğu yok.
- MCPTube tarafında pratik takeaway'lar:
  - Alex Leischow videosu: Vapi + Make ile outbound flow; Google Maps lead listesi ve “free demo” pitch kurgusu. İlk wedge için yaratıcı ama outbound compliance yüzünden dikkatli olunmalı.
  - Travis Wardrop videosu: missed-call forwarding ve local SMB pricing anchor'ı net.
  - Nate Herk videosu: polling, voicemail branch, structured output, AI disclosure gibi “demo'da görünmeyen” kritik ops parçaları canlı gösteriliyor.
- UniverseCreator tarafında dağıtım motoru hazır ama sağlık tam değil: **113 aktif / 90 live / 45 healthy**. Voice funnel landing page'leri açmadan önce health discipline şart; yoksa lead'i getirip 401/bozuk sayfaya çarparsın. Aptallık olur.
- Kısa hüküm: **Bugün para edecek ürün “voice AI closer” değil, “randevu ve lead yakalayan, raporlayan, insana paslayan voice ops paketi.”** Geri kalan artistlik.
