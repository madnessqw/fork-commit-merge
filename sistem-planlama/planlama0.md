# Planlama #0 — AI Calling Agents Uygulama Haritası
**Tarih:** 2026-04-21 02:45
**Bağlı Araştırma:** arastirma0.md

## Swarm Agent ile Nasıl Uygulanır?

UniverseCreator için doğru uygulama “herkesi rastgele arayan AI cold caller” değil. O yol gürültülü, hukuki riskli ve spam kokuyor. Doğru wedge:

**Consent-based Speed-to-Lead / Missed-Call Recovery Agent**

Yani: bir kişi form doldurur, callback ister, randevu talep eder veya cevapsız arama bırakır → AI agent 1-2 dakika içinde arar → 3-5 kritik soru sorar → randevu/transfer/SMS link → CRM/Sheets’e yapılandırılmış veri → dashboard/rapor.

### Swarm rolleri
- **Researcher:** dikey ve müşteri acısı bulur; review mining yapar (“phone not answered”, “can’t get through”, “missed calls”).
- **Planner/Analyst:** unit economics, teklif paketi, risk ve fiyatlama çıkarır.
- **Builder/Codex:** seçilen voice platform + n8n/webhook entegrasyonunu uygular. Bu dosyada kod yok; bu rol sonraki execution modunda devreye girer.
- **QA Tester:** call script test matrisi, edge-case konuşmalar, latency/voicemail/transfer doğrulaması yapar.
- **Sales/Outreach Agent:** sadece izinli veya manuel onaylı hedeflere demo/pitch hazırlar; spam yapmaz.
- **Human/Gokhan:** ilk müşteri görüşmesi, ödeme hesabı, hukuki onay, cold outreach onayı.

## Gerekli Bileşenler
- **Script/Bot:**
  - Lead intake webhook botu
  - Phone normalizer + consent checker
  - Voice call trigger
  - Call status webhook/poll processor
  - Structured output parser
  - CRM/Sheets logger
  - Follow-up SMS/email notifier
  - QA sampler
- **MCP/Araç:**
  - n8n veya Make: workflow orchestration
  - browser/agent-reach: lead/review research
  - mcptube/arxiv/web fetch: sürekli araştırma
  - Google Sheets/Airtable/Notion: erken dönem CRM
  - Playwright/Chrome tools: landing/demo akışlarını test etmek için
- **API:**
  - Retell AI: $0.07-$0.31/dk, 20 free concurrent, webhooks/post-call analysis
  - Vapi: $0.05/dk platform + STT/LLM/TTS/telephony provider cost, $2/ay number
  - Bland: Start $0.14/dk, Build $0.12/dk + $299/ay, Scale $0.11/dk + $499/ay all-in
  - Twilio: ABD local outbound ~$0.0140/dk, inbound ~$0.0085/dk
  - Cal.com/Calendly: booking
  - CRM: HubSpot/GoHighLevel/Zoho veya Sheets başlangıç
- **İnsan Müdahalesi:**
  - İlk 20-50 call transcript review
  - Hukuki/compliance metni
  - İlk müşteri demo görüşmeleri
  - Pricing/contract onayı
  - Caller ID/phone number doğrulama

## Workflow Haritası

**Tetikleyici → Lead intake**
1. Website form / missed call / callback request / CRM new lead gelir.
2. Consent ve iletişim izni kontrol edilir.
3. Phone E.164 formatına normalize edilir; invalid ise human review.
4. Lead segmentlenir: vertical, urgency, source, timezone.

**Call orchestration**
5. Voice platform call create endpoint’i çağrılır.
6. Agent değişkenleri enjekte edilir: isim, şirket, talep, kaynak, uygun slotlar.
7. Agent kendini AI olarak açıklar, kısa soru seti uygular.
8. Kullanıcı randevu isterse Cal.com/Calendly slotu gönderilir veya canlı transfer yapılır.
9. No-answer/voicemail ise retry policy uygulanır; opt-out yakalanır.

**Post-call**
10. Webhook/poll ile transcript + summary + structured outputs alınır.
11. Sheets/CRM güncellenir: status, intent, budget, urgency, appointment, follow-up needed.
12. Telegram/Slack/email ile özet gönderilir.
13. QA sampler düşük confidence/complaint/handoff call’ları işaretler.
14. Haftalık dashboard: calls, pickup, booked meetings, revenue pipeline, cost/minute, failed calls.

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

En hızlı ve en az aptalca hamle: **tek dikey için consent-based speed-to-lead demo sistemi**.

- **Dikey seçimi:** dental, medspa, HVAC/plumbing, real estate seller lead, car dealership. İlk tercih: **HVAC/plumbing veya dental**; acı net: missed call = kayıp randevu/iş.
- **Minimum POC:**
  - Google Form/Tally/Web form → n8n webhook
  - Retell veya Vapi test agent
  - Google Sheets log
  - Cal.com booking link
  - 5-10 senaryo test: valid phone, invalid phone, voicemail, angry caller, human request, booking success, no-show follow-up.
- **Mevcut araç/script desteği:** projeler.txt’deki Twilio/voice notları, mevcut browser/research stack, n8n video template’leri ve MCPTube akışları yeterli. İlk POC için yeni ürün yazmak şart değil.
- **İlk gelir beklentisi:**
  - Demo iyi çıkarsa 1 pilot müşteri: $500-$1,500 setup + $300-$800/ay bakım.
  - Kullanım maliyeti: ilk pilotta $10 free credit + düşük call volume; production’da yaklaşık $50-$150/ay/client erken seviye.
- **Kurulum süresi:** 2-4 gün teknik POC, 3-5 gün demo/offer/lead list, toplam 1-2 hafta.
- **Yasak çizgi:** soğuk AI robocall kampanyası başlatma. Önce form/callback/onaylı lead.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

1. ay sonunda sistem “tek demo” değil, **tekrarlanabilir dikey şablon** olmalı.

- **Başarı metrikleri:**
  - Call connection rate
  - Form submit → first call latency (<2 dk hedef)
  - Call-to-booking rate
  - Human transfer rate
  - No-answer/voicemail rate
  - Cost per booked appointment
  - Agent failure rate / hallucination / compliance flag
  - MRR + setup revenue
- **Paralel adımlar:**
  - Researcher: 3 dikeyde review mining + lead list
  - Builder: voice workflow template’i standardize eder
  - QA: call scenario suite ve transcript scoring rubric hazırlar
  - Analyst: pricing + ROI dashboard çıkarır
  - Sales agent: demo video + teklif metni + objection handling hazırlar
- **Ölçeklendirme gereksinimi:**
  - 3 dikey script pack: dental, HVAC, real estate
  - White-label dashboard: client call logs + booked meetings + savings
  - Consent/opt-out registry
  - Branded caller ID / verified number süreci
  - Per-client workspace izolasyonu
- **Checkpoint’ler:**
  - Hafta 2: çalışan demo + 20 test call
  - Hafta 4: 1 pilot müşteri veya en az 10 ciddi demo görüşmesi
  - Ay 2: 3 paying client hedefi
  - Ay 3: 5-10 client, $1.5K-$8K MRR bandı

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

En iyi senaryo: UniverseCreator voice automation agency → multi-tenant voice AI SaaS/white-label platforma evrilir.

- **Tam otomatik sistem:**
  - Review mining ile müşteri acısı bulur.
  - Landing page/demo script üretir.
  - İzinli lead akışlarında demo/POC hazırlar.
  - Client onboarding formundan otomatik agent prompt + calendar + CRM setup çıkarır.
  - Haftalık call QA ve optimization önerisi üretir.
- **Yan ürünler / gelir kolları:**
  - Vertical voice agent templates marketplace
  - “Missed Call Revenue Calculator” lead magnet
  - White-label dashboard for agencies
  - Call QA / compliance audit service
  - Multilingual Turkish-English receptionist package
  - Voice agent analytics micro-SaaS: Retell/Vapi/Bland call logs → ROI dashboard
- **Swarm avantajı:** rakipler tek tek müşteri kurulumunda boğuluyor. Swarm; research, prompt/script generation, QA, analytics, sales collateral ve support’u paralel çalıştırabilir.
- **White-label/SaaS satışı:** Evet. Ama direkt SaaS’a atlamak erken. Önce 5-10 service client ile tekrarlayan pattern çıkar, sonra self-serve/white-label dashboard.
- **12 ay hedefi:** 30-50 client veya 5-10 agency reseller; $15K-$40K MRR gerçekçi üst bant. Enterprise outbound call center hedefi için compliance + telephony + support çok daha ağır.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek.
- **Kurulum Süresi:** POC 3-7 gün; ilk pilot 10-14 gün; tekrarlanabilir sistem 1-3 ay.
- **Aylık İşletme Maliyeti:**
  - POC: $0-$50
  - İlk client: $50-$200/client/ay, call volume’a göre
  - 10 client: $500-$2,000/ay platform/telephony/automation toplam bandı
- **Potansiyel Gelir:**
  - Setup: $800-$2,000/client
  - Retainer: $300-$800/client/ay
  - Usage overage: $0.25-$0.50/dk veya paket dakika aşımı
  - High-ticket/custom: $2K-$5K+/ay
- **ROI Beklentisi:** İlk paid setup ile break-even. 1 client bile $800 setup getirirse erken maliyetleri kapatır. 5 client x $500 MRR = $2,500 MRR; usage maliyeti doğru yönetilirse %60-%80 gross margin mümkün.

## Mevcut Sistemle Entegrasyon
- UniverseCreator’ın mevcut ürün portföyü ve Vercel altyapısı demo/landing/lead magnet için kullanılabilir; ancak bu araştırma turunda deploy yok.
- `universe_loop.sh` / swarm döngüsüne yeni “voice-agent-research → demo-plan → QA-plan” iş tipi eklenebilir.
- Mevcut araştırma hafızası `sistem-planlama/arastirma*.md` üzerinden dikey bilgi bankasına dönüşür.
- Analist agent haftalık olarak call metrics dosyalarını okuyup “client ROI report” üretir.
- QA agent transcript sampling yapar; kötü call’ları “prompt düzeltme kuyruğu”na atar.
- Builder agent sadece insan onayı sonrası integration work yapar; araştırma modunda kod yok.

## Riskler & Dikkat Edilecekler
- **Compliance:** Cold AI outbound arama tehlikeli. First-party consent, opt-out, DNC/İYS/KVKK kayıtları şart.
- **Spam labeling / pickup:** Branded caller ID ve verified number performansı etkiler; TripleTen örneğinde caller ID yokluğu pickup’ı %20 düşürmüş.
- **Latency:** >2 sn gecikme demo güvenini öldürür; platform/model/telephony hop sayısı azaltılmalı.
- **Hallucination:** Agent fiyat, garanti, tıbbi/hukuki tavsiye gibi alanlarda sınırlandırılmalı.
- **Fixed-price tuzağı:** Dakika maliyetini bilmeden sınırsız kullanım satmak zarar ettirir. Paket + overage şart.
- **Client onboarding yükü:** Her müşteri için custom flow yazmak agency bottleneck olur. Dikey template zorunlu.
- **Data privacy:** Call recording/transcript saklama, PII redaction ve retention policy baştan tasarlanmalı.
- **Vendor lock-in:** Vapi/Retell/Bland fiyat değişikliği margin’i vurabilir; orta vadede provider abstraction düşünülmeli.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek dikey seç ve offer netleştir:** “Missed-call + speed-to-lead AI receptionist for [HVAC/dental] — 2 dakika içinde arar, qualify eder, booking’e bağlar.”
2. **No-code POC blueprint hazırla:** form → n8n → Retell/Vapi call → post-call analysis → Sheets → Cal.com. 10 test senaryolu QA checklist yaz.
3. **Demo ve satış paketi çıkar:** 90 saniyelik demo script, ROI calculator, fiyat paketi ($1K setup + $500/ay + dakika aşımı), compliance/consent açıklaması.
