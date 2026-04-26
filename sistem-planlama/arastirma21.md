# Araştırma #21 — Voice AI + Sales Funnel
**Tarih:** 2026-04-21 16:51 +03
**Konu:** Voice AI ile missed-call recovery, appointment booking, lead qualification ve human handoff sistemi kurmak. 2. tur / 2026 doğrulama. Bu tur odak: **inbound / after-hours / overflow backup / reactivation**; genel “AI closer” masalı değil.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma7.md` / `planlama7.md`, `STATE_SUMMARY.json`
- ddgr sorguları: `voice ai sales funnel appointment booking case study 2026`, `missed call recovery ai appointment booking smb 2026`, `site:indiehackers.com voice ai agency mrr 2025`, `retell vapi bland twilio pricing 2026 voice ai` (**bu turda yine boş döndü; fallback kullanıldı**)
- Resmî / pazar kaynakları:
  - https://www.grandviewresearch.com/industry-analysis/ai-voice-agents-market-report
  - https://www.sierraventures.com/content/voice-ai-market-map
  - https://vapi.mintlify.app/billing/examples
  - https://vapi.mintlify.app/billing/estimating-costs
  - https://vapi.ai/custom-agents/sales-outreach-agent
  - https://www.retellai.com/pricing
  - https://www.retellai.com/ai-appointment-setter
  - https://www.retellai.com/case-studies-new/tripleten-ai-call-automation-admissions-case-study
  - https://www.bland.ai/pricing
  - https://www.twilio.com/en-us/voice/pricing/us
  - https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal
- Reddit JSON API:
  - https://reddit.com/r/automation/comments/1m5nbmx/i_recreated_a_dentist_voice_agent_making_24kyr/
  - https://reddit.com/r/VoiceAutomationAI/comments/1s368zs/im_making_2k4k_usd_a_month_selling_ai_voice/
  - https://reddit.com/r/smallbusiness/comments/1md74gu/ai_receptionist_that_handles_booking_appointments/
  - https://reddit.com/r/sales/comments/1ooeqfx/demod_an_ai_voice_platform_and_yes_it_will_take/
- GitHub:
  - https://github.com/pipecat-ai/pipecat
  - https://github.com/livekit/agents
  - https://github.com/openai/openai-realtime-twilio-demo
  - https://github.com/VapiAI/examples
- ArXiv:
  - https://arxiv.org/abs/2603.05413
  - https://arxiv.org/abs/2602.23266
  - https://arxiv.org/abs/2509.04871
  - https://arxiv.org/abs/2411.13577
- MCPTube / YouTube:
  - https://www.youtube.com/watch?v=HGBMr1RQliY
  - https://www.youtube.com/watch?v=JinTKY1TJZY
  - https://www.youtube.com/watch?v=CNNSoKLL414

## Özet Bulgular
- **İlk wedge hâlâ outbound closer değil.** 2026 verisi de aynı yere çıkıyor: önce **after-hours missed-call recovery + overflow backup + appointment booking + human handoff**. Grand View’da inbound voice agents 2025 gelirinin **%52.1**’ini almış; outbound büyüyor ama ilk para inbound/ops tarafında.
- **Birim ekonomi daha netleşti.** Vapi’nin resmî outbound örneği **1,000 çağrı x 4 dk = 4,000 dk/ay** için toplam **$520/ay** veriyor; yani yaklaşık **$0.13/dk**. Retell kamuya açık pricing’de **$0.07-$0.31/dk** diyor; appointment-setter sayfasında **$0.07-$0.12/dk**, pricing calculator örneğinde ise **$0.11/dk** breakdown görünüyor. Twilio US local outbound **$0.014/dk**, inbound local **$0.0085/dk**. Yani küçük pilot için gerçek taban çoğunlukla **$0.11-$0.15/dk** bandı.
- **Bland küçük pilotta artık pahalı.** Kamuya açık pricing: **Build = $299/ay + $0.12/dk**, **Scale = $499/ay + $0.11/dk**. 50-100 concurrent call ve yüksek günlük limit sunuyor ama SMB pilot için gereksiz ağırlık.
- **Gerçek üretim kanıtı var.** TripleTen × Retell vaka sayfası **%20 pickup + conversion artışı**, **aylık 200+ saat tasarruf**, **17,000+ AI çağrısı** ve Ağustos 2024’ten beri **3,000+ saat talk time** raporluyor. Ayrıca branded caller ID geçici kapanınca pick-up rate’in **%20 düştüğünü** söylüyor. Yani sadece “sesli bot” yetmiyor; presentation layer önemli.
- **Teknik gerçek değişmedi:** tam self-hosted end-to-end voice-to-voice hâlâ olgun değil. 2026 tutorial paper’ı pratik yapının hâlâ **STT → LLM → TTS** olduğunu söylüyor; ölçtükleri **time-to-first-audio 755ms** (best case **729ms**). DDTSR paper’ı da latency’yi **%19-%51** düşürebildiğini gösteriyor. Yani mimari disiplini hâlâ oyun kurucu.

## Gerçek Başarı Hikayeleri
- **TripleTen × Retell (resmî vaka):** Retell’in canlı vaka sayfasına göre TripleTen, Retell ile admissions çağrılarında **%20 pickup + conversion artışı**, **aylık 200+ saat tasarruf**, **17,000+ aylık çağrı hacmi** ve toplamda **3,000+ saat** AI talk time gördü. Uygulama yaklaşık **1 ayda** kuruldu ve HubSpot trigger’larıyla bağlandı. Ayrıca branded caller ID gidince pick-up’ın **%20 düştüğü** özellikle not edilmiş.
- **Dentist after-hours agent — Reddit self-report:** r/automation’daki detaylı post, diş kliniği için after-hours booking ajanını **$24K/yıl** değerle çerçeveliyor; yaklaşık **20 lead/ay** ve lead başına yaklaşık **$300** değer varsayımıyla ROI anlatıyor. Denetlenmiş finansal tablo değil; ama “kaçan çağrıyı gelir geri kazanımına çevir” tezi çok somut.
- **Voice agent agency — Reddit self-report:** r/VoiceAutomationAI’de bir satıcı, AI voice ajanlarından **$2K-$4K/ay** recurring gelir gördüğünü yazıyor. Aynı postun daha değerli kısmı şu: teknoloji çalışıyor ama **delivery bottleneck** can yakıyor. Yani satışı değil operasyonu ürünleştiren kazanıyor.
- **Corporate pilot → agency fırsatı:** Aynı Reddit postunda kurucu, Haziran 2025’te iş yerinde kurdukları Retell sisteminin üç ay sonra inbound çağrıların neredeyse **%50**’sini handle ettiğini yazıyor. Bu da “SMB’ler hazır değil” demek yerine “hazır ama kurulum ve bakım bilmiyor” demek.
- **HVAC blueprint — creator claim ama işe yarayan açıdan değerli:** HVAC odaklı video, üç stratejiyle müşteriler için **$100K+/yıl** geri kazanım iddia ediyor: after-hours coverage, lead reactivation, overflow backup. Aynı videoda **haftada 3 kaçan çağrı** ve iş başına **$300-$800** ticket varsayımıyla aylık **$5K-$10K** kayıp hesabı yapılıyor. Bu creator claim; yine de satış cümlesi net.

## Pazar Büyüklüğü & Fırsat
- **Pazar artık oyuncak değil.** Grand View Research, global AI voice agents pazarını **2025’te $2.54B**, **2026’da $3.51B**, **2033’te $35.24B** ve **%39.0 CAGR** olarak veriyor.
- **İlk wedge’i veri söylüyor:** aynı raporda 2025’te **inbound voice agents %52.1 pay**, customer support automation **%44.2 pay** alıyor. Appointment scheduling büyüyen uygulama; outbound ise 2026-2033 döneminde en hızlı büyüyecek segment diye işaretlenmiş. Yani doğru sıra: **önce inbound recovery**, sonra outbound reactivation.
- **Healthcare / home services / service booking tarafı daha sıcak.** Grand View healthcare için **%42.0 CAGR** bekliyor. Retell’in appointment-setter sayfası healthcare, home services, finance, insurance, logistics gibi dikeyleri öne çıkarıyor.
- **Kategori kalabalık.** Sierra Ventures 2025 market map’i **150+ voice AI şirketi** gösteriyor. Bu kötü haber değil; şu an commodity olan şey alt katman voice infra. Para kalacak yer, dikey workflow + CRM + compliance + reporting katmanı.
- **UniverseCreator için fırsat net:** mevcut Vercel/landing-page üretim gücüyle niş ROI hesaplayıcılar, “kaç missed call = kaç $ kayıp” audit sayfaları, demo transcript’ler ve lead forms hızlı çıkabilir. Asıl runtime ise Retell/Vapi/Twilio tarafında kalır; Vercel’i ses runtime’a çevirmeye çalışmak gereksiz artistlik.

## Rakipler & Boşluklar
- **Retell:** En net vertical productization yüzeyi burada. Açık pricing, booking/call transfer/knowledge base, Make/n8n/HubSpot entegrasyonları, 20 concurrent calls, under-a-week go-live söylemi ve güçlü vaka anlatısı var. Zayıf yanı: PSTN maliyeti, vertical QA ve compliance hâlâ senin omzunda.
- **Vapi:** Geliştirici dostu ve maliyet şeffaflığı yüksek. Billing examples + cost estimator gerçekten iş görüyor; sales outreach page’i CRM, calendar, guardrails ve “deployment within days” anlatıyor. Zayıf yanı: maliyet parçalı, orchestration sorumluluğu yüksek.
- **Bland:** Daha sade commercial packaging ve concurrency kapasitesi veriyor ama **$299/ay** taban fee küçük pilotu anlamsızlaştırıyor. SMB’de değil, daha yüksek hacim / daha az moving-part isteyen hesapta anlamlı olabilir.
- **Twilio + OpenAI Realtime DIY:** Esneklik ve kontrol maksimum; ama telephony, realtime, state, eval, compliance, voicemail ve fallback katmanını sen kuruyorsun. İlk gelir için fazla kahramanlık.
- **OSS framework’ler (Pipecat / LiveKit):** `pipecat-ai/pipecat` **11,470★**, `livekit/agents` **10,130★**. Açık kaynak infra olgunlaşıyor ama gerçek “iş çözümü” hâlâ ayrı ürünleştirme istiyor. `openai/openai-realtime-twilio-demo` **517★** ve güncel; `VapiAI/examples` yalnızca **6★**. Yani infra var, dikey paket eksik.
- **Asıl boşluk:** “AI SDR” değil, **Revenue Recovery Voice OS**. İçeriği: missed-call pickup + soft booking + branded caller ID + CRM log + SMS/email follow-up + human confirm + weekly ROI report + compliance checklist.

## Teknik Gereksinimler
- **Temel mimari:** telephony → STT → LLM/dialog manager → TTS → function calling → CRM/calendar/SMS → transcript/QA/reporting.
- **Latency hedefi:** Sierra Ventures’a göre loop idealde **500-600 ms altı**, TTS **100 ms altı** olmalı. 2026 enterprise tutorial paper’ı pratik self-hosted zincirde **755 ms** TTFA gösteriyor. Bu yüzden ilk ürün “flashy voice-to-voice research demo” değil, **streaming cascaded pipeline** olmalı.
- **Mutlaka gereken işlevler:** voicemail / answering-machine detection, call transfer, human handoff, calendar conflict check, duplicate booking guard, structured outputs, transcript logging, QA scoring, branded caller ID, retry/SMS fallback.
- **Önerilen başlangıç stack’i:**
  - Voice runtime: **Retell** veya **Vapi**
  - Telephony: **Twilio**
  - Orchestration: **n8n** (veya Make)
  - Booking: **Google Calendar / Cal.com / Calendly**
  - CRM: **HubSpot / ServiceTitan / Housecall Pro / Jobber / Sheets**
  - Reminders: SMS / email follow-up
- **Compliance katmanı:** FCC’nin **8 Şubat 2024** açıklaması AI-generated voice robocall’ları TCPA altında “artificial” sayıyor. Dolayısıyla ilk paket için **consent-based inbound / after-hours / reminder / reactivation** daha güvenli; cold consumer outbound tarafı mayın tarlası.
- **Model davranışı gerçeği:** telesales paper’ı (2509.04871) AI’nin rutin call parçalarında iyiye yaklaştığını ama **ikna ve objection handling** tarafında hâlâ zayıf kaldığını söylüyor. Bu yüzden ürün “randevu al / sırala / insana aktar” olmalı; “kapatışı yap / pazarlık et / kırık müşteriyi ikna et” değil.

## Ham Notlar
- `ddgr` bu turda dört sorguda da yine **NO_RESULTS** verdi. Web/Jina/Reddit/GitHub/ArXiv/MCPTube fallback’iyle devam ettim. ddgr’ye güvenip araştırmayı kitlemek aptallık olurdu.
- `projeler.txt` tarafında doğrudan vertical voice-sales asset az. Çıkan yerel leverage daha çok **Twilio WhatsApp**, **VoiceMCP**, **AutoGLM-Phone**, **VibeVoice**, **voicebox** gibi çevresel sinyaller. Yani ürün değil, altyapı farkındalığı var.
- MCPTube tarafında tekrar eden pattern çok net:
  - form submit → otomatik çağrı
  - AI qualify / schedule / transfer
  - calendar + CRM sync
  - transcript + post-call analysis
  - gerekiyorsa insan devralma
- Home-services / dental / clinic tarafı “pain is obvious, ROI is explainable” olduğu için daha iyi. Generic sales funnel lafı çok geniş; **after-hours revenue recovery** çok daha kolay satılır.
- Satış tarafında iki zıt sinyal var: bir yanda “AI will take over” heyecanı, öte yanda “AI screener another AI screener’ı filtreleyecek” dalgası. Sonuç: outbound demo gaza getiriyor ama kalıcı ürün, **ops disiplini + trust layer + compliance** isteyen paket.
- Kısa hüküm: **2026’da hâlâ en mantıklı voice ürünü, kaçan çağrıyı yakalayan ve insana değerli kısmı bırakan paket.** “Tam otonom closer” diye koşmak hâlâ gereksiz masal.
