# Planlama #28 — AI Calling Agents Uygulama Haritası
**Tarih:** 2026-04-21 21:54 +03  
**Bağlı Araştırma:** arastirma28.md

## Sert Karar
UniverseCreator için AI Calling Agents tarafında doğru hamle **cold-call bot ajansı** değil. O fikir hem gürültülü hem riskli hem de ucuz klonlarla dolu. Doğru hamle: **Missed-Call / Speed-to-Lead Recovery Agent** — first-party lead’i 60 saniye içinde arayan, randevuya çeviren, CRM’e işleyen ve haftalık recovered revenue raporu çıkaran dikey paket.

## Swarm Agent ile Nasıl Uygulanır?
1. **Vertical Researcher:** HVAC, dental/medspa, real estate, clinic, education/admissions gibi dikeylerde missed-call economics, ticket size, compliance ve CRM stack çıkarır.
2. **Compliance Verifier:** ABD/Türkiye ayrımı, TCPA/FCC, İYS, KVKK, opt-in/opt-out ve call recording disclosure checklist’i oluşturur.
3. **Script Designer:** 3-5 dakikalık konuşma akışları, objection branches, human handoff, voicemail ve SMS follow-up metinlerini üretir.
4. **Workflow Architect:** Vapi/Retell + n8n + Google Calendar/Sheets/CRM tool şemasını tasarlar.
5. **QA/Eval Agent:** sentetik caller senaryoları, transcript rubric’i, hallucination/latency/failure taxonomy ve haftalık kalite raporu çıkarır.
6. **ROI Analyst:** missed calls, booked appointments, estimated ticket value, close rate ve cost-per-booked-call hesabını raporlar.

## Gerekli Bileşenler
- **Script/Bot:** missed-call callback agent, after-hours receptionist, speed-to-lead form callback, lead reactivation bot, post-call summarizer.
- **MCP/Araç:** n8n/Make, Google Sheets, Calendar, CRM/GHL/HubSpot connector, Telegram/Slack notification, optional browser automation for CRM update.
- **API:** Retell veya Vapi; Twilio/Telnyx number; optional ElevenLabs voice; SMS provider; analytics sheet/API.
- **Maliyet:** demo aşaması $20-$100/ay + dakika; production Retell $0.07-$0.31/dk veya Vapi $0.05/dk + provider + telephony; Bland all-in $0.14/dk Start.
- **İnsan Müdahalesi:** ilk script onayı, compliance onayı, client onboarding, düşük confidence call review, hassas çağrılarda human handoff.

## Workflow Haritası
**Trigger → Lead prep → Call → Tool calls → Post-call → Follow-up → ROI report**

1. Website form / missed call / CRM new lead / after-hours call geldi.
2. Lead normalize edilir: phone E.164, timezone, consent flag, duplicate check, DNC/opt-out check.
3. Voice agent 0-2 dakika içinde arar veya inbound çağrıyı anında karşılar.
4. Agent konuşma sırasında:
   - niyet ve aciliyeti anlar,
   - servis alanı/uygunluk sorar,
   - Google Calendar/CRM availability tool’unu çağırır,
   - randevu oluşturur veya human callback queue’ya atar.
5. Post-call webhook transcript + summary + structured output üretir.
6. Follow-up SMS/email gönderilir; business owner’a Telegram/Slack bildirimi düşer.
7. Haftalık dashboard: calls answered, missed-call saved, booked appointments, human transfers, opt-outs, cost, estimated recovered revenue.

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen yapılacak en düşük çaba / yüksek çıktı:** tek dikey için demo + ROI audit paketi. Öneri: **HVAC veya dental/medspa missed-call recovery**.
- **Mevcut araç/script:** n8n + Vapi/Retell + Google Calendar + Google Sheets yeterli. Kyle Friel/Nate Herk tarzı Vapi+n8n akışı model alınabilir; kod yazmadan template POC çıkar.
- **Minimum POC gereksinimleri:**
  - 1 demo phone number,
  - 1 fake veya gönüllü işletme calendar’ı,
  - 10 sentetik caller senaryosu,
  - consent/disclosure metni,
  - transcript + call outcome sheet,
  - 1 sayfalık ROI calculator.
- **Tahmini kurulum süresi:** 2-4 gün demo, 5-10 gün pilot-ready checklist.
- **İlk gelir beklentisi:** İlk paid pilot için $500-$1,500 setup + $300-$800 MRR makul. İlk müşteri kapanmadan önce tool cost düşük kalmalı; dakika maliyeti değil recovered appointment satılmalı.
- **Bu bulgudan hemen hayata geçirilecek şey:** “Missed Call Revenue Audit” rapor ürünü. Müşteriden call log ister, kaç missed call olduğunu, estimated lost revenue’yu ve AI callback ROI’sini hesaplar. Voice agent satmadan önce rapor satar; bu daha az riskli.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay hedefi:** 1 çalışan vertical template + 1 gerçek pilot + haftalık ROI dashboard.
- **Metric’ler:**
  - answer rate / connect rate,
  - booked appointment count,
  - cost per booked appointment,
  - human transfer rate,
  - opt-out rate,
  - transcript QA score,
  - estimated recovered revenue,
  - client-reported closed revenue.
- **Paralel çalışabilecek adımlar:**
  - Compliance Verifier TR/US checklist’i çıkarır.
  - Script Designer 3 dikey için konuşma akışını yazar.
  - Workflow Architect Retell ve Vapi için iki alternatif blueprint hazırlar.
  - ROI Analyst dashboard formatını oluşturur.
  - Researcher 50 lokal işletme için missed-call pain sinyali toplar.
- **Ölçeklendirme ihtiyacı:**
  - 3-5 pilot müşteri için manuel QA şart.
  - Aylık $200-$500 tool bütçesi yeterli olabilir; çağrı hacmine göre artar.
  - Branded Caller ID / verified number ve call recording policy 2. ayda netleşmeli.
- **Checkpoint’ler:**
  - Hafta 2: demo 20 test call’dan 16’sını doğru bitiriyor mu?
  - Hafta 4: ilk pilotta en az 20 gerçek çağrı işlenmiş mi?
  - Ay 2: 3 dikey template var mı?
  - Ay 3: 3+ paid clients veya net “bu dikey çalışmıyor” kararı.

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator içinde voice ops pipeline yarı otomatik çalışır: lead source bağlanır, compliance check yapılır, script üretilir, test senaryoları koşar, agent yayına alınır, haftalık ROI raporu otomatik çıkar.
- **Yan ürünler / gelir kolları:**
  - Missed Call Revenue Audit ($49-$199 tek seferlik)
  - Voice Agent Setup ($500-$2,000)
  - Managed Voice Ops Retainer ($300-$1,500 MRR)
  - Transcript QA / Compliance Monitoring ($99-$499 MRR)
  - White-label n8n/Retell/Vapi templates ($49-$299)
  - Vertical playbooks: HVAC, dental, medspa, real estate, admissions.
- **Swarm yaklaşımıyla rakiplerden fark:** çoğu rakip “agent kurduk” diyor. Bizim fark: research + compliance + eval + ROI raporu + weekly ops loop. Yani voice bot değil, ölçülen revenue recovery sistemi.
- **White-label / SaaS olabilir mi?** Evet ama 3-6 ay müşteri operasyonu görmeden SaaS’a atlamak aptallık olur. Önce managed service, sonra dashboard, sonra white-label portal.
- **Teknik evrim:** ilk 3 ay Vapi/Retell; 6-12 ayda open-source VAD/TEN, self-hosted voice components, cheaper routing, model/provider arbitrage denenebilir. Ama erken DIY voice infra kahramanlığı zaman yakar.

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek — önceki sentezde #2 fırsat; hızlı gelir potansiyeli var ama compliance yüzünden GTIP kadar temiz değil.
- **Kurulum Süresi:** demo 2-4 gün; pilot 1-2 hafta; retainer operasyonu 1-3 ay.
- **Aylık İşletme Maliyeti:** ilk pilot $20-$100; 3-5 client $200-$800; yüksek hacimde dakika + telephony cost ayrı izlenmeli.
- **Potansiyel Gelir:** 5 client ile $1.5K-$7.5K MRR + $2.5K-$10K setup; 20 client ile $6K-$30K MRR.
- **ROI Beklentisi:** 1 paid client setup fee ile ilk ay tool maliyeti kapanır. Break-even satış süresine bağlı; teknik maliyet değil, müşteri edinme darboğaz.

## Mevcut Sistemle Entegrasyon
- UniverseCreator’ın mevcut swarm’ı bu işi “ürün geliştirme” gibi değil, **operasyonel revenue recovery workflow** gibi ele almalı.
- `projeler.txt` içindeki Twilio/VoiceMCP/phone-native notları uzun vadeli altyapı fikirleri olarak tutulur; ilk pilotta Retell/Vapi ile hız alınır.
- 113 ürün portföyüyle birleşme yolu:
  - Ürün sayfalarında “talk to support / book setup call” voice widget fikri sonra değerlendirilebilir.
  - Asıl kısa vade fırsat, mevcut portföyden bağımsız local business retainer.
  - Ancak swarm’ın audit/report üretme kabiliyeti burada direkt avantaj: haftalık client ROI raporu otomatikleşir.

## Riskler & Dikkat Edilecekler
- **Compliance:** TCPA/FCC, İYS, KVKK, recording disclosure, opt-out. Cold outbound spam yapılırsa sistem para değil bela üretir.
- **Commodity riski:** AI receptionist çok kalabalık. Outcome + dashboard + dikeyleşme yoksa ezilir.
- **Teknik güven:** turn-taking, barge-in, ASR, latency, hallucination, tool response JSON hataları.
- **Phone trust:** unknown number pickup düşük; branded caller ID veya stable local number gerekebilir.
- **Client support borcu:** her müşteri farklı calendar/CRM/iş kuralı ister; paket sınırları net olmazsa boğar.
- **Yanlış metrik:** dakika/çağrı sayısı vanity metric. Booked appointment ve recovered revenue ölçülmeli.
- **Hukuki iddia:** “garanti gelir” deme. “Estimated recovered revenue” ve “tracked booked opportunity” diye raporla.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Dikey seç ve audit şablonu yaz:** HVAC veya dental/medspa için missed-call revenue audit formatı; input: call log, average ticket, close rate, missed call rate, hours coverage.
2. **Demo akışı tasarla:** Retell/Vapi + n8n + Google Calendar için iki tool’lu demo — availability check + appointment create. 10 synthetic caller senaryosu ve failure rubric’i ekle.
3. **Compliance-first pitch hazırla:** “No cold calls. Only first-party leads / missed calls / callback requests. Consent + opt-out + human handoff included.” Bu cümle satış deck’inin merkezinde olmalı.
