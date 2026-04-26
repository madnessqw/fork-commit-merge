# Planlama #27 — Swarm Agent Başarı Hikayeleri Uygulama Haritası
**Tarih:** 2026-04-21 20:46 +03  
**Bağlı Araştırma:** arastirma27.md

## Swarm Agent ile Nasıl Uygulanır?

Doğru mimari: **serbest ajan kalabalığı değil; deterministic supervisor + dar rol ajanları + verifier + artifact ledger.** UniverseCreator zaten Claude+Codex+GLM, `scripts/codex_loop.sh`, `scripts/glm_loop.sh`, `.team/active_agents.json`, 113 ürünlük portföy ve dosya tabanlı hafızaya sahip. Bunu “gelir odaklı swarm OS”e çevirmek gerekiyor.

### Önerilen v0 sistem: UniverseCreator Swarm Ops OS
1. **Supervisor / Router Agent**
   - Gelen işi sınıflandırır: araştırma, ürün audit, SEO sayfası, lead intelligence, GTIP raporu, browser task, outreach draft.
   - Pattern seçer: sequential, fan-out, hierarchical supervisor-worker, evaluator/reflexive loop.
   - Token/bütçe limiti koyar.

2. **Research Workers**
   - Web/Reddit/GitHub/arXiv/YouTube/Jina katmanlarını ayrı yürütür.
   - Her worker sadece kendi kaynak tipini okur ve kısa artifact üretir.

3. **Product/Portfolio Worker**
   - `STATE_SUMMARY.json`, ürün metadata, live/healthy/checkout durumunu okur.
   - 113 ürün içinde hangi ürünün SEO, lead, checkout, positioning fırsatı taşıdığını çıkarır.

4. **Verifier / Critic Worker**
   - Kaynak linkleri, rakamlar, iddialar, maliyet/gelir varsayımları ve riskleri kontrol eder.
   - “Hype kokusu” olan Reddit/YouTube claim'lerini bağımsız doğrulanmış gibi yazmayı engeller.

5. **Report Writer Worker**
   - Markdown/PDF/CSV/JSON artifact üretir.
   - Müşteri-facing rapor ile iç operasyon notunu ayırır.

6. **Human Gate**
   - Email, public post, call, lead outreach, fiyat/stok değişimi, payment veya external action için Gokhan onayı zorunlu.
   - Araştırma/planlama dosyası yazmak serbest; dış dünyaya çıkan aksiyon serbest değil.

## Gerekli Bileşenler

- **Script/Bot:**
  - Task ledger dosyası: `sistem-planlama/swarm-ledger.md` veya JSONL formatında run kayıtları.
  - Research artifact klasörü: her run için `sistem-planlama/runs/YYYYMMDD-HHMM-topic/`.
  - Cost/latency tracker: her agent run için token, süre, kaynak, çıktı, hata.
  - Verifier checklist: kaynak linki var mı, rakamın tarihi var mı, gelir iddiası verified/vendor/community mi?

- **MCP/Araç:**
  - ArXiv MCP: akademik validation.
  - MCPTube: video transcript ve workflow demo extraction.
  - Jina Reader: resmi docs/blog/PDF okuma.
  - GitHub CLI / `gh-axi`: repo/live implementation taraması.
  - `ddgr`, Reddit JSON API: community intelligence.
  - Browser automation: sadece JS/Cloudflare/visual confirmation gerektiğinde `chrome-devtools-axi` / Playwright.

- **API:**
  - Başlangıçta mümkün olduğunca ücretsiz/var olan araçlar.
  - Ücretli katman gerekiyorsa önce pilot gelir veya Gokhan approval.
  - Dış satış için ileride: LLM provider, PDF renderer, email/CRM, Stripe/iyzico/LemonSqueezy ödeme.

- **İnsan Müdahalesi:**
  - Offer seçimi, müşteri segmenti, dış mesaj gönderimi, ödeme, public posting, hukuki/regülasyon kararları.
  - Compliance-heavy alanlarda (HR, voice, GTIP/tarife, scraping) insan son kontrolü şart.

## Workflow Haritası

**Tetikleyici:** Yeni research/ops/sales fırsatı veya portföy audit ihtiyacı  
→ **Supervisor:** işi sınıflandırır, pattern seçer, worker listesi ve budget çıkarır  
→ **Research Fan-out:** web + Reddit + GitHub + akademik + video + local state paralel artifact üretir  
→ **Synthesis:** ana tez, pazar, rakip, boşluk, teknik gereksinim çıkarılır  
→ **Verifier:** rakam/kaynak/risk/safety kontrolü yapar  
→ **Report Writer:** iç plan + müşteri-facing çıktı + next action hazırlar  
→ **Human Gate:** dış aksiyon gerekiyorsa Gokhan onayı  
→ **Ledger:** outcome, maliyet, süre, açık loop ve reuse edilen pattern kaydedilir.

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **En düşük çaba / en yüksek çıktı adımı:** “manual swarm protocol v0” kurmak. Kod yazmadan bile her araştırma/ops turunda şu artifact seti zorunlu hale getirilebilir: source notes, verifier notes, plan, next action, cost/time estimate.
- **Mevcut araç/script kullanımı:**
  - `skills/ARASTIRMA_MODU.md` zaten araştırma fan-out disiplini veriyor.
  - `scripts/codex_loop.sh` ve `scripts/glm_loop.sh` mevcut agent döngülerinin omurgası.
  - `STATE_SUMMARY.json` 113 ürünlük portföyü verir; product/SEO/ops worker için hazır input.
  - `sistem-planlama/*` araştırma serisi zaten iyi artifact store.
- **Minimum POC:**
  1. Tek vertical seç: **GTIP/HS Opportunity Snapshot** veya **local missed-call audit**.
  2. 3 worker rolü tanımla: Researcher, Verifier, Report Writer.
  3. 1 örnek müşteri-facing PDF/Markdown rapor çıkar.
  4. Token/süre/kaynak ve varsayılan fiyatı ledger'a yaz.
- **Tahmini kurulum süresi:** 2-5 gün dokümantasyon + ilk sample artifact; 7-10 gün tekrar edilebilir SOP.
- **İlk gelir beklentisi:** En gerçekçi kısa vadeli gelir, swarm infra satmak değil; swarm ile üretilmiş **rapor/audit** satmak. Fiyat çıpası: $19-$79 düşük paket veya $300-$800 managed pilot. Payment blokerleri devam ettiği için PayPal/manual ödeme opsiyonu ayrıca düşünülmeli.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay hedef görüntüsü:**
  - 3 tekrar kullanılabilir lane:
    1. GTIP/HS buyer-intel report lane
    2. Local business voice/marketing audit lane
    3. 113 ürün için SEO/API/workflow audit lane
  - Her lane için source checklist, verifier checklist, report template ve fiyatlama hazır.
  - 10+ sample artifact üretilmiş; hangisinin satışa daha uygun olduğu ölçülmüş.

- **Başarı metric'leri:**
  - Research run başına süre: hedef <60 dk.
  - Verified-source oranı: her önemli rakamda link + tarih.
  - Hallucinated/unsupported claim: 0 tolerans.
  - Reusable artifact oranı: her run en az 1 template/checklist iyileştirsin.
  - İlk satış metric'i: 10 outreach / 3 call / 1 paid pilot gibi net funnel.

- **Paralel çalışabilecek adımlar:**
  - Research worker'lar ayrı kaynaklarda çalışır.
  - Product worker 113 ürün portföyünü tarar.
  - Verifier önceki run'lardaki hataları kontrol eder.
  - Report writer sadece verified notes gelince final üretir.

- **Ölçeklendirme için gerekenler:**
  - Basit queue/ledger.
  - Run-level budget cap.
  - Manual approval UI/ritüeli.
  - Belki LangGraph/OpenAI Agents SDK/CrewAI değil, önce file-first orchestration. Framework seçimi eval sonrası.

- **Checkpoint'ler:**
  - Hafta 2: 3 sample rapor + verifier checklist.
  - Hafta 4: 1 gerçek satış denemesi + 1 productized offer page draft.
  - Ay 2: 1 paid pilot veya en az 20 hedefli outbound öğrenimi.
  - Ay 3: retainer-ready ops SOP + monitoring/alert/checklist.

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator, kendi portföyünü ve müşteri işlerini yöneten **self-improving agent operations company** olur. Supervisor task alır, worker'lar araştırır/üretir/test eder, verifier kaliteyi kilitler, human gate dış aksiyonu onaylar.
- **Yan ürünler / gelir kolları:**
  - Swarm-generated GTIP/HS raporları.
  - Local business audit + missed-call/voice setup retainer.
  - Agent-ready API/MCP workflow kits.
  - SEO/content intelligence for 113 product portfolio.
  - White-label automation ops package.
  - “Agent audit / observability setup” danışmanlığı.
- **Rakiplerden fark:** Framework satmak yerine **outcome + evidence + maintenance** satmak. Çoğu rakip ya “ajan platformu” ya “template pazarı”; UniverseCreator dosya-hafızalı, çok kaynaklı araştırma + verifier + ürün portföyü ile gerçek çıktı gösterebilir.
- **White-label/SaaS potansiyeli:** Evet, ama erken SaaS yapmak dumb move olur. Önce 3-5 manuel/yarı otomatik müşteri işi; sonra en tekrar eden lane SaaS/portal haline gelir.
- **3-12 ay teknik evrim:**
  - Durable queue + dashboards.
  - Multi-agent eval harness.
  - Customer-facing report portal.
  - MCP/OpenAPI wrappers for internal data products.
  - Cost-aware model routing.
  - Memory distillation: başarılı run pattern'leri skill'e dönüşür.

## Öncelik & Çaba Tahmini
- **Öncelik:** Çok Yüksek — çünkü bu araştırma tek konu değil, önceki 27 araştırmayı çalıştıracak işletim modeli.
- **Kurulum Süresi:** Manual protocol 2-5 gün; reusable internal OS 3-6 hafta; müşteri-facing managed swarm ops 2-3 ay.
- **Aylık İşletme Maliyeti:** Başlangıçta $0-$100; ciddi müşteri/LLM/API kullanımıyla $100-$500; observability/hosted workers genişlerse $500+.
- **Potansiyel Gelir:**
  - Rapor/audit: $19-$499 / çıktı.
  - Setup/pilot: $500-$2,000.
  - Managed retainer: $300-$2,500/ay / müşteri.
  - Enterprise workflow: $5K+ proje, ama ilk hedef olmamalı.
- **ROI Beklentisi:** İç operasyon ROI'si 1-2 haftada zaman/kalite olarak görünür. Dış gelir için en hızlı break-even tek paid audit/pilot ile mümkün.

## Mevcut Sistemle Entegrasyon
- Mevcut durum: `STATE_SUMMARY.json` cycle **1051**, **113 active product**, **99 live**, **108 healthy**, balance **$0.0**, mode **INNOVATE**.
- Entegrasyon noktaları:
  - `sistem-planlama/` → research/plan/synthesis artifact store.
  - `/home/gokhan/mind` + workspace memory → stable cognition / error prevention.
  - `scripts/codex_loop.sh`, `scripts/glm_loop.sh` → mevcut döngü runner mantığı.
  - `.team/active_agents.json` → agent inventory / role registry.
  - `STATE_SUMMARY.json` → product portfolio worker input.
- Uygulama prensibi: önce dosya-first; sonra gerekirse LangGraph/OpenAI Agents SDK/CrewAI. Vercel case’i yüzünden “framework alalım, halleder” yaklaşımı yasaklanmalı.

## Riskler & Dikkat Edilecekler
- **Swarm theater:** Çok ajan var diye değer var sanmak. Ölçüm yoksa tiyatro.
- **Tool sprawl:** Gereksiz MCP/tool artışı latency, token ve hata yüzeyini büyütür.
- **Coordination tax:** ArXiv MAFBench’e göre yanlış framework/pattern kaliteyi ciddi düşürebilir.
- **Maintenance debt:** Müşteri workflow'u bozulursa retainer kârlı değil, destek borcu olur.
- **Compliance:** HR, voice, outreach, scraping, GTIP/tarife gibi alanlarda human gate ve disclaimer şart.
- **Gelir iddiası:** Reddit/YouTube anekdotları verified değil; marketing copy'de “kanıtlanmış gelir” diye yazılmamalı.
- **Balance $0:** Ücretli API/infra harcaması gelir veya onay olmadan yapılmamalı.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Swarm run template'i yaz:** Researcher / Verifier / Report Writer rollerini ve her rolün artifact formatını tek dosyada tanımla.
2. **Tek satış lane seç:** GTIP/HS Opportunity Snapshot veya local missed-call/marketing audit. 1 örnek müşteri-facing rapor üret.
3. **Verifier checklist'i zorunlu yap:** Her rakam için source+tarih, her gelir iddiası için `official/vendor/community/anecdote` etiketi, her dış aksiyon için human gate.
