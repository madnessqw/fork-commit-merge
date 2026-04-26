# Araştırma #0 — AI Calling Agents
**Tarih:** 2026-04-21 02:45
**Konu:** AI Calling Agents — Vapi/Retell/Bland/Twilio ile gelir odaklı B2B telefon otomasyonu

**Kaynaklar:**
- Vapi Pricing: https://vapi.mintlify.app/pricing
- Vapi outbound docs: https://docs.vapi.ai/phone-calling/outbound-calls
- Vapi automotive case study: https://vapi.ai/blog/case-study-automotive
- Retell Pricing: https://www.retellai.com/pricing
- Retell webhook/post-call analysis docs: https://docs.retellai.com/features/webhook , https://docs.retellai.com/features/post-call-analysis-consumption
- Retell case studies: Anker, ISpeedToLead, TripleTen, Boatzon
  - https://www.retellai.com/case-study/how-anker-transformed-global-customer-support-with-human-quality-al-voice
  - https://www.retellai.com/case-studies-new/ispeedtolead-retell-ai-lead-response-case-study
  - https://www.retellai.com/case-studies-new/tripleten-ai-call-automation-admissions-case-study
  - https://www.retellai.com/case-study/how-retell-ai-became-boatzons-top-performing-employee
- Bland Pricing: https://www.bland.ai/pricing
- Twilio US Voice Pricing: https://www.twilio.com/en-us/voice/pricing/us
- Grand View Research AI Voice Agents Market: https://www.grandviewresearch.com/industry-analysis/ai-voice-agents-market-report
- Grand View Research Conversational AI Market: https://www.grandviewresearch.com/industry-analysis/conversational-ai-market-report
- Market.us Voice AI Agents Market: https://market.us/report/voice-ai-agents-market/
- IndieHackers community playbook: https://www.indiehackers.com/post/building-a-profitable-ai-voice-saas-agency-300-800-mrr-per-client-frAbgO1yQMfHOFFtY3gE
- Reddit/HN search snippets tarandı; Reddit doğrudan fetch 403 verdi, bu yüzden Reddit rakamları **anekdot / düşük güven** olarak işaretlendi.
- MCPTube videoları:
  - Nate Herk — “I Built a Voice Agent That Calls Every New Lead (n8n + Vapi)” — https://www.youtube.com/watch?v=BO-jFbN4p8Y
  - Azim K — “The ONLY Outbound Calling Tutorial You'll Ever Need (Vapi + n8n)” — https://www.youtube.com/watch?v=UJg8DDojyMk
  - Mohamed Elgazzar — “Complete Voice AI Outbound System for Business Owners Guide” — https://www.youtube.com/watch?v=X8XYBzQeko4
- ArXiv:
  - 2012.14653 — “Can You be More Social? Injecting Politeness and Positivity into Task-Oriented Conversational Agents”
  - 2005.10438 — “Conversational End-to-End TTS for Voice Agent”
  - 1812.07339 — “Motivations, Classification and Model Trial of Conversational Agents for Insurance Companies”
  - 2602.02270 — “dziribot: rag based intelligent conversational agent for algerian arabic dialect”

## Özet Bulgular
- **En güçlü wedge cold-call spam değil, consent-based speed-to-lead.** Form dolduran, fiyat isteyen, randevu isteyen veya cevapsız arama bırakan lead’i 1-2 dakika içinde AI ile aramak; hem hukuki risk daha düşük hem ROI daha görünür.
- **Maliyetler artık POC için düşük:** Vapi platform ücreti $0.05/dk + provider maliyetleri; Retell $0.07-$0.31/dk pay-as-you-go; Bland Start $0.14/dk all-in, Build $0.12/dk + $299/ay, Scale $0.11/dk + $499/ay. Twilio taşıyıcı katmanı ABD yerel aramada yaklaşık $0.0140/dk outbound, $0.0085/dk inbound.
- **Gerçek case study’lerde rakam var:** Vapi otomotiv marketplace örneği 10k-15k çağrı/gün, 450+ concurrent call, 5 ülke, çağrı merkezi -%50, CAC -%50, revenue +%200. Retell örneklerinde ISpeedToLead 100 dk response time → <5 dk, 20-30 demo/hafta; TripleTen 17k+ AI call, 200 saat/ay tasarruf; Boatzon 1 agent ile 7-8 rep coverage.
- **Teknik başarı “prompt”tan çok operasyon:** latency, barge-in, phone validation, voicemail detection, webhooks, structured outputs, CRM/calendar entegrasyonu, QA ve human handoff. Sadece güzel ses yetmiyor; üretim sistemi gerekiyor.
- **Pazar hızlı büyüyor ama kalabalıklaşıyor:** Grand View Research AI voice agents pazarını 2025’te $2.54B, 2033’te $35.24B, CAGR %39 olarak veriyor. Market.us 2024 $2.4B → 2034 $47.5B, CAGR %34.8 diyor. Farklı raporlar oynuyor ama trend net: voice agent segmenti ciddi büyüyor.

## Gerçek Başarı Hikayeleri

### 1) Vapi — Latin Amerika otomotiv marketplace
- Müşteri: $1.68B funding’e sahip büyük otomotiv marketplace.
- Hacim: 10,000-15,000 voice AI call/gün.
- Ölçek: 450+ concurrent calls, 5 ülke, 1000+ localized agents.
- Sonuç: çağrı merkezi footprint -%50+, CAC -%50, revenue +%200.
- Kritik ders: “voice AI” bir chatbot entegrasyonu değil; telephony + MCP/internal services + LangGraph + observability altyapısı.

### 2) Retell — ISpeedToLead speed-to-lead
- Problem: 24/7 gelen real estate seller lead’leri insan SDR’lar yüzünden gecikiyordu.
- Sonuç: average lead response time 100 dakikadan <5 dakikaya; outbound call form submit’ten 2 dakika içinde; 20-30 sales demo/hafta; call-to-meeting booking +%40.
- Entegrasyon: Zoho, GoHighLevel, Calendly, Make.com.
- Ders: Soru sayısını azalt, tek core qualification sorusu sor, uygun lead’e SMS ile booking link gönder.

### 3) Retell — TripleTen admissions
- Sonuç: +17,000 AI-handled calls, +200 saat/ay tasarruf, +%20 pickup/conversion, 3,000+ talk hour since Aug 2024.
- Branded Caller ID geçici yokken pickup rate %20 düşmüş. Caller trust işi süs değil, performans kaldıracı.

### 4) Retell — Boatzon
- 1 AI voice agent, 7-8 human rep coverage’ı karşıladı.
- Lead’e financing application sonrası 1 dakika içinde ulaşıyor.
- 80% high-quality call benchmark otomatik follow-up ile korunuyor.
- Same-day initial launch, HubSpot + Twilio gibi entegrasyonlar birkaç haftada olgunlaştı.

### 5) Retell — Anker global support
- 80.4% case resolution rate, NPS 63, 95%+ speech recognition accuracy.
- Kullanım: U.S./U.K. post-sales support ve out-of-office inquiries.
- Ders: Büyük marka tarafında AI voice agent kabulü için “humanlike” değil, ölçülebilir resolution + NPS gerekiyor.

### 6) IndieHackers — AI voice agency playbook
- Stack önerisi: white-label voice platform + n8n + Cal.com.
- Hedef: $500K-$5M revenue local service businesses.
- Fiyatlama: $1K-$2K setup + $300-$800 MRR/client, yaklaşık %80 margin iddiası.
- Time-to-first-revenue: 2-3 hafta, eğer hızlı uygulanırsa.
- Hedef segmentler: dental, plumbing/HVAC, salon, küçük hukuk büroları, medikal klinikler, home services.
- Bu kaynak community post; doğruluğu resmi case kadar güçlü değil ama agency GTM için pratik.

### 7) Reddit anekdotları — düşük güven ama sinyal var
- r/AIReceptionists arama snippet’i: car dealership voice receptionist, ilk müşteri $22k + $500/ay maintenance.
- r/automation arama snippet’i: “0 to $7K/month in 2 months” AI voice agency iddiası.
- r/aiagents snippet’i: Vapi+n8n ile ilk $1,000 AI voice agent satışı; müşteri Reddit/Fiverr’dan.
- r/VoiceAutomationAI snippet’i: $2K-$4K/ay voice agent satışı ama 20-30 saat/agent debug, latency/hallucination/Make.com hataları.
- Karar: Reddit hikâyeleri umut veriyor ama “kanıt” değil. Planlama için resmi case + kendi pilot metriği esas alınmalı.

## Pazar Büyüklüğü & Fırsat
- Grand View Research: AI voice agents pazarı 2025’te **$2.54B**, 2026’da **$3.51B**, 2033’te **$35.24B**, CAGR **%39.0**.
- Aynı rapor: North America 2025 revenue share **%38.1**; inbound voice agents revenue share **%52.1**; customer support automation share **%44.2**; healthcare CAGR **%42.0**.
- Outbound voice agents en hızlı büyüyen segment olarak belirtiliyor: appointment reminders, payment follow-ups, lead qualification, promotional campaigns.
- Conversational AI daha geniş pazar: Grand View Research 2024 **$11.58B** → 2030 **$41.39B**, CAGR **%23.7**.
- Market.us: Voice AI agents 2024 **$2.4B** → 2034 **$47.5B**, CAGR **%34.8**.

### En kârlı görünen nişler
1. **Speed-to-lead / form follow-up:** real estate, solar, insurance, home services.
2. **AI receptionist / missed-call recovery:** dental, medspa, hair salon, HVAC/plumbing, clinics.
3. **Appointment reminder / no-show reduction:** clinics, dental, education/admissions, service appointments.
4. **Lead reactivation:** eski CRM lead’leri, quote request’ler, abandoned cart/high-ticket ecommerce.
5. **Payment reminder / collections:** yüksek compliance ihtiyacı var; ilk wedge için ağır olabilir.

## Rakipler & Boşluklar

| Oyuncu | Güçlü taraf | Zayıf/boşluk | POC kararı |
|---|---|---|---|
| Vapi | Developer-flex, outbound/batch API, assistant overrides, BYO providers | $0.05/dk sadece platform; provider maliyetleri ve latency hop’ları ayrı yönetilir | Eğer Codex/n8n ile esnek demo lazımsa iyi |
| Retell | Pay-as-you-go, post-call analysis, webhooks, 20 free concurrent calls, case studies güçlü | Dakika maliyeti stack’e göre $0.07-$0.31; add-on’lar maliyeti artırır | İlk ticari POC için en dengeli aday |
| Bland | All-in fiyat; LLM/STT/TTS/telephony dahil; Norm builder; appointment node | Build/Scale platform fee erken aşamada pahalı; Start 100 calls/day | Volüm ve predictable billing varsa iyi |
| Twilio | Güvenilir telephony katmanı; ABD local outbound $0.0140/dk | Voice agent değil; AI pipeline’ı biz kurarız | Taşıyıcı/BYOC katmanı olarak kullan |
| DIY stack | Maliyet kontrolü, vendor lock-in azalır | Latency, barge-in, monitoring, compliance derdi büyür | İlk 1-3 ay gereksiz kahramanlık |

### Boşluk
- “AI voice agent kurarım” kalabalıklaştı. Boşluk **ölçülebilir outcome + dikey şablon + dashboard + compliance kayıtları**.
- Küçük işletme sahibinin istediği şey “Vapi agent” değil: kaç arama cevaplandı, kaç randevu geldi, kaç missed call kurtarıldı, kaç $ pipeline oluştu.
- En satılabilir paket: **Missed Call / Speed-to-Lead Recovery Agent**. İddia basit: “Formu dolduran veya aramayı kaçırdığın kişiyi 2 dakika içinde arar, qualify eder, randevuya bağlar, CRM’e işler.”

## Teknik Gereksinimler

### Minimum POC stack
- Voice platform: Retell veya Vapi.
- Orchestrator: n8n / Make / küçük Python webhook.
- Telephony: platform number, Twilio/Telnyx BYOC veya Retell telephony.
- CRM/log: Google Sheets, Airtable veya mevcut CRM.
- Calendar: Cal.com / Calendly / Google Calendar.
- Notification: Telegram/Slack/email.
- QA: transcript + call summary + structured outputs + manual review checklist.

### Üretim için gerekenler
- Consent/opt-in kayıtları: form checkbox, timestamp, IP, source URL, lead source.
- Phone normalization: ülke kodu, E.164 formatı, invalid number branch.
- Do-not-call / opt-out registry: “beni arama” dediğinde global block list.
- Call state: created → ringing → in_progress → ended → voicemail/no-answer/human → analyzed.
- Structured outputs: intent, urgency, budget, service_interest, appointment_time, human_transfer_needed, compliance_flag.
- Handoff: kullanıcı insan isterse transfer; agent emin değilse human review.
- Latency hedefi: mümkünse sub-second; >2 sn demo güvenini öldürür.
- Branded/verified caller ID: TripleTen örneğinde yokluğu pickup’ı %20 düşürmüş.
- QA loop: düşük puanlı konuşmaları haftalık incele; prompt + flow + FAQ düzelt.

### Compliance notu — kritik
- ABD’de AI-generated outbound robocalls TCPA/FTC hattında ciddi risk. FCC 2024’te AI-generated voice’u “artificial/prerecorded voice” kapsamına aldı. FTC TSR/DNC de özellikle telemarketing ve robocall alanında sıkı.
- Türkiye’de ticari elektronik ileti arama/SMS/email için İYS/onay ve KVKK aydınlatma/rıza süreçleri dikkate alınmalı.
- Bu yüzden ilk ürün **cold call bot** olmamalı. İlk ürün: kullanıcının form doldurduğu, callback istediği, müşteri olduğu veya açık onay verdiği first-party lead akışı.

## projeler.txt İlgili Notlar
`projeler.txt` içinde doğrudan Vapi/Retell/Bland yoğunluğu düşük; ama ilişkili voice/phone altyapısı notları çıktı:
- Twilio + WhatsApp + TailScale ile mesaj geldiğinde makinede action tetikleme fikri.
- VoiceMCP: agent’a “mouth and ears” ekleme yaklaşımı.
- AutoGLM-Phone-9B: smartphone üstünde ekran okuma/aksiyon alma; telefon tabanlı agent geleceği için sinyal.
- Voicebox / VibeVoice / OmniVoice: düşük maliyetli TTS/voice cloning/open-source ses teknolojileri; ilk ticari POC için değil ama uzun vadede maliyet düşürme için izlenebilir.

## Ham Notlar
- MCPTube / Nate Herk videosu: form submit → phone normalization → Vapi create call → 60 sn wait/poll → get call details → voicemail check → structured outputs → Google Sheets. Agent kendini AI olarak tanıtıyor; user insan isterse fallback transfer öneriliyor.
- MCPTube / Azim K videosu: outbound calling 4 seviye: manual call, scheduled call, webhook-triggered call, batch calling. Level 4 Google Sheets’ten lead alıp tek tek çağırıyor, status “calling/completed” güncelliyor, transcript/summary/recording/cost logluyor.
- Vapi docs: outbound API single/batch calls, schedulePlan ile ileri tarihli call, customers array ile batch; customer-specific assistant overrides gerekiyorsa endpoint ayrı çağrılmalı.
- Retell docs: webhook eventleri call_started, call_ended, call_analyzed, transcript_updated; webhook signature verify var; post-call analysis dashboard/webhook/API ile alınabiliyor.
- ArXiv 2012.14653: task-oriented conversational agent’larda sosyal/polite dil kullanıcı responsiveness ve task completion ile ilişkili. Satış/appointment scriptlerinde kuru bot dili yerine kısa, empatik, direkt ton kullanılmalı.
- ArXiv 2005.10438: conversational TTS’te context-aware prosody daha doğal; kullanıcı güveni için ses modeli + turn-taking kritik.
- ArXiv 1812.07339: insurance gibi dikeylerde conversational agent için domain use-case/requirement/prototype yaklaşımı gerekli; genel bot değil, dikey akış.
- ArXiv 2602.02270: dialect/code-switching için RAG + NLU katmanı gerekiyor; Türkiye/TR-EN konuşmalarda bilgi tabanı ve Türkçe akış ayrı tasarlanmalı.
