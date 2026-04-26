# Planlama #5 — White-label Otomasyon Ajansı Uygulama Haritası
**Tarih:** 2026-04-21 05:15 +03
**Bağlı Araştırma:** arastirma5.md

## Swarm Agent ile Nasıl Uygulanır?
Bu işin ilk sürümü “AI agency” diye değil, **vertical automation operating system** diye kurulmalı. Yani müşteri workflow'un mutfağını değil, sonucu ve kontrol panelini görmeli.

1. **Vertical Strategy Agent**
   - Hangi niche'in seçileceğine karar verir.
   - Kriterler: yüksek LTV, tekrarlayan lead akışı, hızlı satış döngüsü, compliance yönetilebilirliği, tekrar eden workflow.
   - İlk adaylar: roofing/HVAC/home services, med spa/beauty, dental/clinic, B2B lead-gen yapan küçük ajanslar.
2. **Audit Agent**
   - Prospect için 1 sayfalık leak audit üretir: lead capture eksikleri, missed-call riski, booking friction, slow follow-up, reporting körlüğü.
   - Çıktı satış kapısını açar; koddan daha çok para getirir.
3. **Demo Builder Agent**
   - Vertical'a özel template'i markalar, örnek verilerle doldurur, portal ekran görüntüsü veya demo URL üretir.
   - Müşteriye ham workflow değil, kendi logosuyla görünen mini ürün gösterir.
4. **Offer & Pricing Agent**
   - Setup fee, retainer, usage cap, overage, SLA ve upgrade yollarını hesaplar.
   - HighLevel Pro veya n8n+portal stack'ine göre brüt marjı izler.
5. **Onboarding Agent**
   - Knowledge base, SOP, credentials, escalation rules, allowed automations, business hours, tone ve compliance checklist toplar.
6. **QA & Compliance Agent**
   - Test senaryoları: duplicate lead, yanlış appointment, opt-out, review gating, hallucinated answer, billing overage, portal permission leak.
7. **ROI Reporter Agent**
   - Haftalık olarak müşteriye “kaç lead, kaç booking, kaç touchpoint, tahmini gelir etkisi, kullanım maliyeti, marj” raporu üretir.
8. **Human Sales Gate**
   - Satış görüşmesi, fiyat pazarlığı, outreach ve production aktivasyonu insan onayıyla gider.

## Gerekli Bileşenler
- **Script/Bot:**
  - Vertical scoring sheet
  - Prospect audit generator
  - Demo template cloner
  - Portal branding pack generator
  - Usage/margin calculator
  - Weekly ROI report generator
  - Compliance checklist runner
  - Churn risk detector
- **MCP/Araç:**
  - Browser automation / Chrome DevTools / Playwright: prospect site ve booking akışı gözlemi
  - ArXiv MCP: workflow automation / SME deployment kalıpları
  - MCPTube: playbook ve sales demo extraction
  - GitHub araştırması: FlowEngine / n8n template / portal mimarileri
- **API:**
  - HighLevel $497 Pro: markup + SaaS configurator + rebilling için en temiz ticari yol
  - n8n $50 Pro veya self-host: esnek backend otomasyon motoru
  - Stripe: seat + subscription + usage overage
  - Twilio / WhatsApp / SMTP / Google Calendar / Airtable / Sheets
  - İhtiyaca göre Make/Zapier glue layer
- **İnsan Müdahalesi:**
  - Vertical seçimi
  - İlk 10 satış görüşmesi
  - Pricing ve sözleşme
  - Compliance onayı
  - İlk müşteri onboarding'i

## Workflow Haritası
Tetikleyici: yeni araştırma sonucu veya yeni hedef vertical
→ niche seçimi
→ 30-50 prospect audit
→ common pain map çıkar
→ 1 demo template + 1 ROI modeli hazırla
→ insan onaylı outreach
→ discovery call
→ özel demo / mini pilot
→ onboarding form + credentials
→ branded portal + workflow aktivasyonu
→ QA testleri
→ pilot launch
→ haftalık ROI/margin raporu
→ upsell / referral / ikinci template

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen uygulanabilir çekirdek karar:** Aynı anda hem GHL hem n8n hem Make kovalamak saçma. İlk 2 haftada **tek yol seçilmeli**:
  - **Ticari hız yolu:** HighLevel Pro ($497) + SaaS/rebilling
  - **Esnek kontrol yolu:** n8n Pro ($50) + manuel billing + portal taslağı
- **En düşük çaba / en yüksek çıktı adımı:** 1 vertical seçip 20-30 prospect için **leak audit + ROI calculator + branded demo** üçlüsünü hazırlamak.
- **Hangi mevcut araç/script kısmen yapar:** mevcut araştırma döngüsü, browser gözlem araçları, GitHub template örnekleri, flowengine tarzı portal pattern'leri, n8n/GHL pricing ve rebilling bilgileri.
- **Minimum POC gereksinimleri:**
  - 1 niche
  - 1 paket seti (Starter / Growth / Premium)
  - 1 ROI calculator
  - 1 branded demo portal veya en azından demo ekran akışı
  - 1 onboarding checklist
  - 10 QA senaryosu
- **Tahmini kurulum süresi:** 4-7 gün net araştırma+paketleme, 2-4 gün demo materyali.
- **İlk gelir beklentisi:** gerçekçi hedef, ilk pilotta **$500-$2,000 setup** veya **$300-$1,000 MRR**. İlk iki haftada $10K MRR beklemek YouTube'da güzel görünür, gerçek hayatta genelde saçmalıktır.
- **İlk offer önerisi:**
  - Starter: $500 setup + $300/mo — 1 workflow + haftalık rapor
  - Growth: $1,500 setup + $750/mo — multi-step workflow + portal + usage tracking
  - Premium: $3,000+ setup + $1,500-$3,000/mo — dashboard + support + multi-channel automation + ROI reporting

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **Ay 1 hedef görüntü:**
  - 1 vertical için net offer
  - 50-100 prospect audit
  - 5-10 kişiselleştirilmiş demo
  - 2-3 pilot müşteri veya çok net reddedilme nedeni listesi
  - onboarding ve QA checklist'i stabilize olmuş
- **Başarı metrikleri:**
  - audit → discovery call: %5-15
  - discovery → pilot: %15-30
  - onboarding süresi: <90 dk
  - aylık brüt marj: %60+
  - ilk 30 günde müşteri başına support ticket: yönetilebilir seviyede (<10 kritik)
  - haftalık rapor açılma / okunma oranı yüksek olmalı; görünmez rapor retention yaratmaz
- **Paralel çalışabilecek adımlar:**
  - bir agent prospect audit yapar
  - biri demo template üretir
  - biri pricing/margin modeli çıkarır
  - biri compliance ve QA checklist yazar
  - biri case-study / landing page kopyası hazırlar
- **Ölçeklendirme için gerekenler:**
  - portal/permissions katmanı
  - subscription + usage billing otomasyonu
  - template update mekanizması
  - credential yönetimi
  - log/observability
- **Checkpoint'ler:**
  - Hafta 2: niche + offer + demo hazır
  - Hafta 4: ilk discovery/pilotlar
  - Hafta 8: 2-3 case-study adayı
  - Hafta 12: tek vertical'da tekrar eden template + net pricing

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** Ajans, her müşteriye sıfırdan workflow kuran bir servis olmaktan çıkar; vertical-specific bir operating system'e dönüşür. Portal, template library, credential manager, usage billing ve ROI reporting birleşir.
- **Yan ürünler / yeni gelir kolları:**
  - template marketplace
  - paid audit report
  - onboarding sprint
  - usage overage / AI margin
  - support retainer
  - white-label portal lisansı
  - vertical SaaS spinout
- **Rakiplerin yapamadığı, swarm yaklaşımımızla yapılabilecek nedir?**
  - Her prospect için hızlı audit
  - hızlı demo kopyalama
  - müşteriye özel ROI raporu
  - template update'lerini çoklu müşteriye kontrollü itme
  - her vertical için living playbook üretme
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet. Ama erkenden salt SaaS'a kaçmak aptallık olur. Önce managed service ile pattern'i kanıtla, sonra self-serve / agency-facing ürünleştir.
- **3-12 ay hedefleri:**
  - 5-10 aktif müşteri veya 2-3 agency partner
  - 2 vertical template
  - müşteri başına onboarding <45 dk
  - support yükünü knowledge base + portal ile düşürme
  - MRR hedefi: **$5K-$25K** bandı gerçekçi; ama sadece offer-market fit bulunduysa

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek. Çünkü bu konu önceki AI calling, lead gen ve local automation araştırmalarını tek gelir modelinde birleştiriyor.
- **Kurulum Süresi:** 1 hafta paketleme, 2-6 hafta ilk müşteri/pilot, 1-3 ay templateleşme.
- **Aylık İşletme Maliyeti:**
  - Lean yol: $50-$250/mo (n8n + hosting + temel araçlar)
  - GHL ticari yol: $497/mo + usage
  - Multi-tool kurgu: $500-$1,500/mo aralığına rahat çıkar
- **Potansiyel Gelir:**
  - İlk pilot: $500-$2,000 setup + $300-$1,000 MRR
  - 1-3 ay: $2K-$10K MRR
  - 3-12 ay: $5K-$25K MRR
- **ROI Beklentisi:**
  - Lean path 1 müşteriyle breakeven olabilir
  - GHL Pro path için genelde 1 Growth müşteri veya 2 küçük müşteri yeter
  - En kötü hata: tool maliyetinden değil, kötü niche seçip çok support yemek

## Mevcut Sistemle Entegrasyon
- UniverseCreator'ın mevcut gücü kod kataloğu değil; **araştırma, otomasyon, browser gözlemi, içerik üretimi ve raporlama** kası. Bu iş tam ona oturuyor.
- Mevcut swarm rollerine doğal dağılım:
  - researcher → niche/competitive research
  - analyst → ROI/margin model
  - builder → demo template ve portal prototipi
  - qa-tester → workflow test senaryoları
  - skill-writer → onboarding/compliance playbook
- Vercel portföyü doğrudan ürün değil ama branded mini dashboard, calculator, landing page ve client portal demoları için kullanılabilir.
- Günlük log/memory disiplini haftalık müşteri raporlamasına çevrilebilir. Başka bir deyişle kendi iç çalışma düzenimiz, satılacak operasyon düzeninin çekirdeği olabilir.
- Araştırma modunda dış outreach yok; bu plan sadece hazır sistemin iskeletini çıkarır.

## Riskler & Dikkat Edilecekler
- **Tool-first saçmalığı:** Müşteriye n8n/Make/GHL anlatırsan kaybedersin. Sonuç anlatırsan kazanma şansın olur.
- **Compliance:** SMS/voice consent, call recording, KVKK/GDPR/TCPA, review gating.
- **Vendor lock-in:** GHL hızlı ama içine gömülürsen çıkış maliyeti yüksek. n8n esnek ama ops yükü getirir.
- **Support cehennemi:** Ucuz müşteri + çok custom iş = kötü marj.
- **Black-label beklentisi:** Agency → agencies → SMB zinciri teoride seksi, pratikte karmaşık. Önce doğrudan SMB veya küçük agency partner modeli daha temiz.
- **Usage-based sürpriz maliyet:** özellikle AI/voice/chat tarafında marj kaybolabilir. Her pakette cap ve overage kuralı şart.
- **Sahte kanıt / creator hype:** YouTube'daki $10K in 7 days içeriklerini baseline almak aptallık olur. Onları idea generator olarak kullan, finansal forecast olarak değil.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek lane seç:** GHL Pro reseller modeli mi, n8n+portal esnek modeli mi? İkisini aynı anda kurmaya çalışma.
2. **Tek vertical seç ve audit paketini yaz:** Öneri: roofing/HVAC veya med spa. 20 prospect için leak audit + ROI hesaplama tablosu hazırla.
3. **1 demo ve 1 fiyat kartı çıkar:** Starter/Growth/Premium paketlerini, usage cap ve haftalık raporla birlikte netleştir. Satış görüşmesine girilecekse elde görünür bir şey olsun.
