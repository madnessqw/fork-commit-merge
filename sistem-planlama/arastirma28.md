# Araştırma #28 — AI Calling Agents 3. Tur: Missed-Call / Speed-to-Lead Gelir Hattı
**Tarih:** 2026-04-21 21:54 +03  
**Konu:** AI Calling Agents — Vapi / Retell / Bland / Twilio ile consent-first telefon otomasyonu, gerçek gelir metrikleri ve 2026 teknik riskleri

**Kaynaklar:**
- Yerel katalog: `/home/gokhan/UniverseCreator/projeler.txt` — `vapi|retell|twilio|calling|voice|bland|phone` taraması.
- Vapi pricing: https://vapi.ai/pricing
- Vapi automotive case study: https://vapi.ai/blog/case-study-automotive
- Retell pricing: https://www.retellai.com/pricing
- Retell homepage / MDS case link: https://www.retellai.com/
- Retell MDS case: https://www.retellai.com/case-study/how-medical-data-systems-scales-280-000-in-monthly-collections-with-ai-voice-agents-on-retell
- Retell ISpeedToLead search snapshot: https://www.retellai.com/case-studies-new/ispeedtolead-retell-ai-lead-response-case-study
- Retell TripleTen search snapshot: https://www.retellai.com/case-studies-new/tripleten-ai-call-automation-admissions-case-study
- Retell Boatzon case: https://www.retellai.com/case-study/how-retell-ai-became-boatzons-top-performing-employee
- Bland pricing: https://www.bland.ai/pricing
- Twilio US Programmable Voice pricing: https://www.twilio.com/en-us/voice/pricing/us
- Grand View Research AI Voice Agents Market: https://www.grandviewresearch.com/industry-analysis/ai-voice-agents-market-report
- FCC AI-generated voice robocalls ruling: https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal
- Federal Register AI robocalls NPRM: https://www.federalregister.gov/documents/2024/09/10/2024-19028/implications-of-artificial-intelligence-technologies-on-protecting-consumers-from-unwanted-robocalls
- Türkiye Ticaret Bakanlığı — ticari elektronik iletiler genel bilgiler: https://ticaret.gov.tr/ic-ticaret/ticari-elektronik-iletiler/genel-bilgiler
- KVKK — açık rıza alırken dikkat edilecek hususlar: https://www.kvkk.gov.tr/Icerik/2037/Acik-Riza-Alirken-Dikkat-Edilecek-Hususlar
- Indie Hackers / Rosie: https://www.indiehackers.com/post/tech/from-failure-to-1m-arr-in-8-months-oA0AqL4jY25lxrQ4uGBl
- D13Digital HVAC case: https://www.d13digital.com/case-studies/hvac-voice-agent/
- Reddit JSON: r/sales `1ooeqfx`, r/Entrepreneur `1skhn6y`, r/automation `1nmzmek`, r/automation `1lp6haf`, r/AI_Agents market-risk posts.
- GitHub search: `VapiAI/examples`, `sshh12/llm_convo`, `amanp8l/ai-call`, `bobbylkchao/ai-phone-agent`, `homgorn/real-voice-agent-free`, `TEN-framework/ten-vad`, `bentoml/BentoVoiceAgent`, `Anil-matcha/AI-Voice-Agent`.
- ArXiv: `2503.04721` Full-Duplex-Bench, `2603.13686` τ-Voice, `2603.26515` JAL-Turn, `2509.14515` full-duplex survey.
- MCPTube: Kyle Friel — “Build an AI Voice Agent that Never Misses a Call (Vapi + n8n, Free Template)” https://www.youtube.com/watch?v=uvh5pynPEz4 plus prior Vapi+n8n videos.
- ProductHunt Jina denendi ama Cloudflare/anti-bot “Just a moment...” verdi; fallback olarak ddgr ProductHunt arama snippetleri kullanıldı.

## Özet Bulgular
- **En iyi giriş hâlâ cold-call değil, missed-call recovery + speed-to-lead.** Vapi ve Retell case’lerinde para sıcak lead, inbound, after-hours, callback, CRM lead reactivation ve randevu booking akışında görünüyor. Cold outbound ise hem hukuki hem marka riski.
- **Kategori artık “demo” değil, operasyon işi.** Maliyet, latency, caller ID, DNC/opt-out, consent kayıtları, voicemail, transcript QA, human handoff ve dashboard olmadan bu iş hızla ucuz AI receptionist çöplüğüne döner.
- **Fiyatlar POC için düşük ama production maliyeti dakika başına şişer.** Vapi $0.05/dk platform + provider maliyeti; Retell $0.07-$0.31/dk; Bland Start $0.14/dk all-in; Twilio telephony $0.0140/dk outbound + $0.0085/dk inbound local call. Dakika maliyeti değil, kaç randevu/revenue kurtardığın satılmalı.
- **Pazar güçlü:** Grand View Research AI voice agents pazarını 2025’te **$2.54B**, 2033’te **$35.24B**, CAGR **%39.0** veriyor; inbound voice agents 2025 revenue share **%52.1**, customer support automation **%44.2**.
- **Akademik sinyal net: voice agent güvenilirliği metinden çok geride.** τ-Voice benchmark’ında text GPT-5 reasoning pass@1 **%85** iken voice agents temiz koşulda **%31-%51**, gerçekçi gürültü/aksan koşulunda **%26-%38**. Bu, satışta “AI insan gibi konuşur” masalını değil, eval/handoff gereğini ispatlıyor.

## Gerçek Başarı Hikayeleri

### 1) Vapi — büyük otomotiv marketplace
- Resmî Vapi case study tarihi: **7 Ocak 2026**.
- Önceki durum: çok şehirli call center operasyonu, günde **10,000-15,000** çağrı.
- Sonuç: call center footprint **%50+ azaldı**, revenue **%200 arttı**, CAC **%50 düştü**.
- Ölçek: **450+ concurrent calls**, **5 ülke**, **1000+ localized agents**.
- Teknik ders: MCP/internal services + LangGraph workflow + observability bağlanmış; yani “sesli chatbot” değil, production voice orchestration.

### 2) Retell — Medical Data Systems collections
- Resmî Retell case: **30,000 calls/month**, **70 containment rate**, **$280,000 monthly collections**.
- Sistem **100% inbound calls** alıyor, sadece **%30 transfer rate** ile insanlara aktarıyor.
- Bu B2B collections gibi regülasyonlu bir alanda bile iyi tasarlanmış voice agent’ın yüksek hacimli inbound işte kullanılabildiğini gösteriyor. İlk ürün için collections ağır olabilir; ama metrikler voice ops’un sadece randevu botu olmadığını kanıtlıyor.

### 3) Retell — ISpeedToLead speed-to-lead
- Web arama snapshot’ı Retell sayfasından: response time **100 dakikadan 5 dakikanın altına** indi.
- Sonuç: **20x** hızlı lead response, **+40% call-to-meeting booking rate**, AI outbound ile haftada **20-30 demo**.
- Entegrasyonlar: Zoho, GoHighLevel, Calendly, Make.com.
- Ders: “form submit oldu → 2 dakika içinde ara → qualify et → SMS/booking link gönder” en temiz satış wedge’i.

### 4) Retell — TripleTen admissions
- Retell snapshot’ı: **+17,000 calls handled by AI agents**, **+200 hours saved/month**, **%20 pickup + conversion increase**.
- Branded Caller ID yokken pickup rate’in **%20 düştüğü** belirtiliyor.
- Ders: caller trust, ses kalitesi kadar para getiriyor. Unknown number’dan gelen bot, iyi bot olsa da kaybeder.

### 5) Retell — Boatzon
- Boatzon marketplace: yaklaşık **2,400 dealer** ve **90,000 boat listing**.
- Problem: 7-8 insan temsilci outbound/inbound hacmini verimli çeviremiyordu; busy professionals unknown number’ı iş saatinde açmıyordu.
- Çözüm: lead financing akışında 24/7 follow-up, inbound underwriting support, CRM disposition, sürekli call QA.
- Ders: AI agent insanı tamamen silmekten çok, insanı yüksek değerli approval/sales işine geri iterse çalışıyor.

### 6) Rosie — Indie Hackers self-serve voice SaaS
- Indie Hackers hikâyesi: Rosie pivot sonrası **8 ayda $1M ARR**.
- Stack kısmında Bland.ai kullanımı anlatılıyor; GTM önce cold email, sonra Meta/Google ads, sonra SEO.
- Ders: agency modeli dışında self-serve SMB voice ürünleri de çalışıyor; ama onboarding ve fiyatlama burada ana ürün.

### 7) HVAC missed-call recovery — vendor case, orta/düşük güven
- D13Digital case: local HVAC şirketi peak saatlerde inbound çağrıların **%30**’unu, mesai sonrası/hafta sonu **%100**’ünü kaçırıyordu.
- İddia: **$15k/mo** recovered missed-call revenue; her missed call potansiyel **$5,000 install** olarak çerçevelenmiş.
- Önce/sonra: response **2-5 dakika/voicemail → <1 saniye**, kapasite **1 call → unlimited concurrent**, booking manual → calendar sync.
- Not: Vendor case; yön gösterir ama bağımsız kanıt değil. Yine de “kaçan çağrı = ölçülebilir kayıp” pitch’i iyi.

### 8) Reddit / community intelligence — sert gerçekler
- r/sales’te AI voice platform demo post’u **~400 score / 310 comments** civarı ilgi aldı. Ana duygu ikiye bölünmüş: basit appointment booking için evet; B2B relationship satışında bir kötü çağrı markayı yakar.
- r/Entrepreneur’da AI receptionist kuran bir founder, CRM/phone-system built-in özellikleri ve ucuz klonlar yüzünden işinin race-to-bottom’a döndüğünü yazdı. Ders: tool-layer satmak zayıf.
- r/automation mortgage örneği: 6 ayda Google Sheet+n8n hack’inden web app’e evrilmiş; **20 dials/day**, **%60 connection**, son hafta **1 booked call/day**. Dashboard, callbacks ve DNC handling’in “dead CRM”i canlı satış motoruna çevirdiğini söylüyor. Düşük güven ama pratik saha detayı yüksek.
- r/automation real estate Vapi+GHL+n8n post’u: lead gelince anında inbound/outbound qualify + post-call summary/email. Yorumlarda “speed-to-lead is everything” ve compliance vurgusu tekrar ediyor.

## Pazar Büyüklüğü & Fırsat
- **Grand View Research:** 2025 market size **$2.54B**, 2026 **$3.51B**, 2033 **$35.24B**, CAGR **%39.0**.
- 2025 segmentleri: North America revenue share **%38.1**, inbound voice agents **%52.1**, customer support automation **%44.2**.
- Healthcare 2026-2033 için en hızlı büyüyen end-use olarak **%42.0 CAGR** gösteriliyor.
- Outbound voice agents hızlı büyüyor; ama outbound için güvenli kullanım appointment reminder, payment follow-up, consented lead qualification ve proactive support. Cold robo-call değil.
- **Bottom-up fırsat tahmini:** local service business için $500-$2,000 setup + $300-$1,500 MRR bandı mantıklı. İlk 5 müşteri: $1.5K-$7.5K MRR + kurulum gelirleri. Bu tahmindir; vendor/community fiyat sinyallerinden türetildi.

## Rakipler & Boşluklar

| Katman | Oyuncular | Gerçek durum | Boşluk |
|---|---|---|---|
| Voice platform | Vapi, Retell, Bland | Platformlar hızlı yakınsıyor; ses kalitesi tek başına fark değil | Dikey workflow + ROI dashboard + compliance kayıtları |
| Telephony | Twilio, Telnyx, SIP/BYOC | Güvenilir taşıyıcı katmanı; agent ürünü değil | KOBİ’ye altyapıyı görünmez yapmak |
| Self-serve SMB | Rosie, Slang, Phonely, Smith.ai hybrid, local AI receptionist tools | Kalabalık ve hızla ucuzluyor | “Missed revenue recovered” gibi outcome satmak |
| Agency / white-label | AI automation agencies | Çok kişi aynı template’i satıyor | Operasyonel QA ve aylık raporlama ile retainer savunması |
| QA/eval | Vapi testing, simulation tools, open-source eval | Yeni ama kritik | Voice agent CI/eval + transcript risk flagging |

### En büyük boşluk
“AI receptionist kurarım” artık zayıf cümle. Güçlü cümle şu:  
**“Kaçırdığın veya geç döndüğün yüksek niyetli çağrıları 60 saniye içinde yakalar, qualify eder, randevuya çevirir, CRM’e işler ve haftalık recovered revenue raporu verir.”**

## Maliyet & Platform Karşılaştırması

### Vapi
- Pay-as-you-go: **$0.05/dk Vapi hosting**.
- SMS/chat: **$0.005/msg**.
- **10 call concurrency included**, üstü **$10/line/month**.
- STT/LLM/TTS provider maliyetleri “at cost”; yani gerçek all-in maliyet tek satır değil.
- Call history: 14 gün; HIPAA Zero Data Retention add-on **$1000/mo**.
- Güçlü: developer control, outbound/batch, custom tools, MCP/internal services entegrasyonu.
- Zayıf: non-technical agency için maliyet/latency/provider karmaşası.

### Retell
- Pay-as-you-go: **$10 free credits**, **$0.07-$0.31/dk AI Voice Agents**, chat **$0.002+/msg**.
- **20 free concurrent calls**, full platform access, templates, analytics/transcripts, simulation testing, webhooks/API.
- Pricing page örnek breakdown: **$0.11/dk** toplam; LLM **$0.04**, Retell infra **$0.055**, TTS **$0.015**, telephony **$0.00**.
- Güçlü: case study havuzu, post-call analysis, batch call, branded/verified phone number, hızlı POC.
- Zayıf: dakika maliyeti stack’e göre artar; client billing/reporting ops’u şart.

### Bland
- Start: free + **$0.14/dk**, **10 concurrent**, **100 calls/day**, 1 voice clone.
- Build: **$0.12/dk + $299/month**, **50 concurrent**, **2,000 calls/day**.
- Scale: **$0.11/dk + $499/month**, **100 concurrent**, **5,000 calls/day**.
- All-in iddiası: LLM + STT + TTS + telephony dahil.
- Güçlü: billing sade; yüksek hacimde tahmin edilebilir.
- Zayıf: erken aşamada platform fee moral bozar; esneklik Vapi kadar developer-first değil.

### Twilio
- US local outbound: **$0.0140/dk**, inbound: **$0.0085/dk**.
- Clean local number: **$1.15/mo**.
- Answering Machine Detection: **$0.0075/call**.
- Branded Calls: **$0.12/call**.
- ConversationRelay voice AI bridge: **$0.07/dk**.
- Güçlü: carrier katmanı ve enterprise güven.
- Zayıf: tek başına voice agent ürünü değil; orchestration ve eval bizde kalır.

## Teknik Gereksinimler

### Minimum POC
- Voice platform: Retell veya Vapi.
- Trigger: missed call webhook, website form, CRM lead status, after-hours inbound, abandoned quote.
- Orchestrator: n8n / Make / küçük webhook servisi.
- Calendar/CRM: Google Calendar + Google Sheets/Airtable/HubSpot/GHL.
- Post-call: transcript, summary, structured output, booking status, call cost, human handoff flag.
- Notification: Telegram/Slack/email to business owner.
- QA: haftalık 10 call review + failure taxonomy.

### Production olmazsa olmazları
- Consent source: form checkbox, timestamp, IP/source URL, lead source, privacy notice version.
- DNC/opt-out list: “beni arama” dediği anda global block.
- Branded/verified caller ID veya en azından stable local number.
- Voicemail handling: detection, beep wait, retry schedule, voicemail script.
- Call retries: no answer → retry window; busy → backoff; wrong number → suppress.
- Human handoff: acil, ödeme, medikal/legal hassasiyet, kullanıcı ısrarı, düşük confidence.
- Cost ledger: provider dakika, telephony, recording/transcription, per-client margin.
- Eval: prompt/script version, scenario tests, synthetic caller tests, real transcript scoring.
- Compliance audit trail: consent, disclosure, opt-out, recording notice, data retention.

## Hukuk & Uyum — cold-call bot yapıp yangın çıkarmayalım
- **ABD:** FCC, 8 Şubat 2024’te AI-generated voices’un TCPA kapsamındaki “artificial/prerecorded voice” olduğunu teyit etti. Sonuç: izin/consent olmadan AI robocall yapmak mayın tarlası.
- **ABD 2024 NPRM:** Federal Register metni AI-generated call tanımı ve disclosure/consumer protection tarafını sıkılaştıran öneriler içeriyor. Regülasyon hâlâ hareketli.
- **Türkiye:** Ticaret Bakanlığı ticari elektronik iletileri SMS/e-posta/telefon araması olarak ele alıyor. Onay ticari elektronik ileti gönderilmeden önce alınmalı; alıcı reddetme hakkını kullanana kadar geçerli. Tacir/esnaf için önceden onay istisnası var ama ret hakkı kullanıldıysa ileti gönderilemez; ayrıca onay talebi ticari elektronik iletiyle yapılamaz.
- **KVKK:** açık rıza belirli konuya ilişkin, bilgilendirmeye dayalı ve özgür iradeyle olmalı. Çağrı merkezi/elektronik ortamla alınabilir ama ispat yükü veri sorumlusunda. “Her şeye rıza” battaniye rıza geçersiz; rıza geri alınabilir.
- **Pratik karar:** İlk ürün cold outbound değil. First-party lead, missed call, callback request, existing customer, appointment reminder veya açık opt-in olmalı.

## Derin Araştırma — Akademik ve Video Bulguları

### ArXiv
- `2603.13686` τ-Voice: 278 gerçek dünya görevi; text GPT-5 reasoning **%85 pass@1**, voice agents temiz koşulda **%31-%51**, gerçekçi noise/accent koşulunda **%26-%38**. Failures’ın **%79-%90**’ı agent behavior kaynaklı. Bu, voice agent satışında eval olmadan production iddiasının boş olduğunu gösteriyor.
- `2503.04721` Full-Duplex-Bench: pause handling, backchanneling, turn-taking ve interruption management ölçen benchmark. Voice agent kalitesi sadece WER veya “ses güzel mi?” değil.
- `2603.26515` JAL-Turn: industrial-grade voice AI deployment’larda turn-taking hâlâ ciddi problem; acoustic+linguistic low-latency model öneriyor.
- `2509.14515` full-duplex survey: synchronous data scarcity, architecture divergence ve evaluation gaps ana darboğazlar.

### MCPTube / Kyle Friel Vapi+n8n missed-call tutorial
- Claim: inbound call’ların yaklaşık **%27**’si cevapsız kalıyor; restoranlarda **%43**’e çıkabiliyor; voicemail’a düşenlerin **%85**’i geri aramıyor; bazı venue’lerde kayıp yıllık **$300k** seviyesine çıkabiliyor. Bu rakamlar video kaynağı; resmi pazar verisi değil ama pitch için iyi problem çerçevesi.
- Sistem tasarımı: Vapi agent + n8n + Google Calendar.
- İki tool: `check availability` webhook’u ve `create appointment` webhook’u.
- Kritik uygulama detayı: agent prompt’una **current date/time** verilmezse “tomorrow/next Tuesday” gibi tarihleri yanlış yorumlayabiliyor.
- Tool response formatı Vapi’nin beklediği JSON yapısına dönmezse appointment calendar’a yazılsa bile agent kullanıcıya “hata oldu” diyebiliyor. Bu küçük bug production’da güven öldürür.

## GitHub Implementasyon Sinyali
- `VapiAI/examples` — resmî örnek repo, 2025 sonunda açılmış, 2026 Nisan’da güncel; star düşük ama doğru başlangıç noktası.
- `sshh12/llm_convo` — ChatGPT + Twilio ile inbound/outbound AI phone agent, **117 star**.
- `amanp8l/ai-call` — appointment/customer call use-case, **53 star**.
- `bobbylkchao/ai-phone-agent` — OpenAI Realtime + Twilio + Amazon Connect starter, 2026 Nisan’da güncel.
- `TEN-framework/ten-vad` — voice activity detector, **2,084 star**; altyapı komponentlerinin uygulama repolarından çok daha olgun olduğunu gösteriyor.
- `bentoml/BentoVoiceAgent`, `Anil-matcha/AI-Voice-Agent`, `pheonix-delta/axiom-voice-agent` — self-hosted/open-source voice agent yolu var ama ilk ticari pilot için gereksiz kahramanlık.

## projeler.txt İlgili Notlar
Yerel katalogda doğrudan Vapi/Retell/Bland yoğunluğu düşük. Çıkan ilişkili sinyaller:
- Twilio + WhatsApp + TailScale ile mesaj geldiğinde makinede action tetikleme fikri.
- VoiceMCP: agent’a “mouth and ears” ekleme.
- AutoGLM-Phone-9B: smartphone üzerinde ekran okuma/aksiyon alma; phone-native agent yönü.
- Voicebox, VibeVoice, OmniVoice gibi TTS/voice cloning/open-source ses teknolojileri; ticari POC için değil, uzun vadede maliyet düşürme için izlenebilir.

## Ham Notlar
- ProductHunt sayfaları Jina üzerinden Cloudflare “Just a moment...” verdi; ddgr fallback Vapi ProductHunt review/customer/alternatives sayfalarını buldu ama metrik güveni düşük.
- Retell eski ISpeedToLead/TripleTen URL’leri Jina’da 404 verdi; web search snapshot’ları hâlâ ilgili metrikleri gösteriyor. Dosyada bu yüzden “search snapshot” olarak etiketlendi.
- Chrome DevTools AXI ile Vapi automotive case canlı sayfadan doğrulandı: 10k-15k çağrı/gün, 450+ concurrent, 5 ülke, 1000+ localized agents, -50% call center, -50% CAC, +200% revenue.
- Reddit’te en önemli negatif sinyal: ucuz AI receptionist pazarı commodity oluyor. En güçlü savunma “voice bot” değil, **ölçülen recovered revenue + compliance + QA**.
