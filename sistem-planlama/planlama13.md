# Planlama #13 — Swarm Agent Başarı Hikayeleri Uygulama Haritası
**Tarih:** 2026-04-21 10:49
**Bağlı Araştırma:** arastirma13.md

## Swarm Agent ile Nasıl Uygulanır?
Bu alanda doğru hamle “UniverseCreator için daha büyük bir swarm kuralım” değil. O fikir çoğu zaman oyuncak üretir. Doğru hamle: **router kontrollü, outcome-first, human-gated swarm lane** kurmak.

Önerilen yapı:
1. **Intake / Router Agent**
   - Gelen işi sınıflar: single-agent mı, supervisor mı, gerçek swarm mı?
   - Kriterler: görev uzunluğu, parallelizable mı, tool sayısı, risk seviyesi, teslim formatı.
2. **Planner / Supervisor Agent**
   - Görevi 3-5 net alt işe böler.
   - Her worker’ın scope’unu ve output schema’sını tanımlar.
3. **Specialist Worker'lar**
   - Research Worker: web / arxiv / YouTube / docs.
   - Browser Worker: portal/QA/fiyat/ekran doğrulama.
   - Data Worker: CSV, JSON, karşılaştırma, skorlama.
   - Draft Worker: rapor, teklif, outreach draft.
4. **Verifier / Analyst Agent**
   - Çelişki, kaynak boşluğu, hallucination, maliyet sapması, broken flow yakalar.
5. **Human Gate**
   - Para, public output, müşteri iletişimi, deployment ve hassas kararlar burada durur.

Bu model mevcut Claude+Codex+GLM düzenine oturur:
- Claude / research tarzı akış: keşif ve synthesis
- Codex: sistematik execution / artifact üretimi
- GLM veya ikinci verifier: karşı-kontrol ve failure sniffing

## Gerekli Bileşenler
- **Script/Bot:**
  - task classification matrix
  - shared artifact schema (`brief`, `evidence`, `draft`, `qa`, `final`)
  - run ledger (token, süre, hata, override)
  - budget cap / timeout policy
  - verifier checklist
  - case-study/demo generator
- **MCP/Araç:**
  - ArXiv MCP
  - MCPTube
  - web/Jina okuma
  - browser automation stack (Playwright / Chrome DevTools / gerekirse Windows fallback)
  - GitHub search / repo inspection
- **API:**
  - mevcut model/API erişimleri
  - gerekirse browser veya data API’leri ama sadece müşteri/ürün ekonomisi taşıyorsa
  - opsiyonel notification / CRM / calendar entegrasyonları
- **İnsan Müdahalesi:**
  - task routing kuralları
  - high-risk action approval
  - ilk 10 müşteri/dogfood run değerlendirmesi
  - kalite standardı ve satış dili

## Workflow Haritası
Tetikleyici: yeni iş / lead / research sorusu / müşteri isteği
→ Router işin tipini sınıflar
→ single-agent ise düz akışa gider, swarm gerekiyorsa supervisor devreye girer
→ supervisor 3-5 alt görev tanımlar
→ worker’lar paralel artifact üretir
→ verifier çelişki/maliyet/risk kontrolü yapar
→ gerekiyorsa ikinci tur düzeltme
→ human gate onayı
→ final çıktı (rapor / demo / teklif / dataset / QA sonucu)
→ run ledger ve öğrenim dosyaları güncellenir

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen uygulanabilir en iyi şey:** generic swarm OS değil, **Swarm-Backed Research Sprint**.
- İlk canonical kullanım:
  - GTIP/HS opportunity snapshot
  - local business leak audit
  - browser-based competitor/process audit
- **En düşük çaba / en yüksek çıktı adımı:** task-route matrix + 1 supervisor template + 3 worker rolü + 1 verifier checklist yazmak.
- **Hangi mevcut araç/script bunu kısmen yapıyor?**
  - mevcut `ARASTIRMA_MODU` akışı zaten research swarm’ın manuel omurgası
  - `/mind` + `sistem-planlama` dosya sistemi shared-state görevini görüyor
  - arxiv/mcptube/browser/Jina katmanı specialist toolset olarak hazır
- **POC için minimum gereksinimler:**
  - görev brief şablonu
  - worker output schema
  - kaynak zorunluluğu
  - verifier checklist
  - budget/time cap
  - final deliverable template
- **Tahmini kurulum süresi:** 3-5 gün iç dogfood, 7-10 gün ilk müşteri gösterilebilir demo
- **İlk gelir beklentisi:**
  - research sprint / audit: **$149-$599**
  - DFY setup / custom swarm lane: **$499-$1,500**
  - aylık bakım/raporlama: **$99-$399/mo**

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonunda hedef görünüm:**
  - router karar veriyor: hangi iş single, hangi iş supervisor, hangi iş full swarm
  - 3 net lane çalışıyor:
    1. research/report lane
    2. browser audit/QA lane
    3. setup/onboarding lane
  - her run için artifact trail var
  - verifier olmayan hiçbir run “tamam” sayılmıyor
- **Başarı metric'leri:**
  - successful run rate
  - human correction rate
  - cost per successful deliverable
  - time-to-delivery
  - report/demo → sale conversion
- **Paralel çalışabilecek adımlar:**
  - task matrix yazımı
  - template kütüphanesi
  - verifier checklist kütüphanesi
  - pricing / offer packaging
- **Ölçeklendirme için gerekenler:**
  - run queue
  - cost dashboard
  - better observability
  - reusable offer library
  - müşteri başına workspace/credential izolasyonu
- **Checkpoint'ler:**
  - 10 iç run
  - 3 dış demo
  - 1 ücretli sprint
  - 1 failure postmortem seti

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator, iş tipine göre kendi kendine lane seçen bir operating system olur; her görev otomatik olarak doğru orchestration pattern’ine düşer.
- **Yan ürünler / yeni gelir kolları:**
  - managed swarm deployment
  - vertical workflow kits
  - audit/governance layer
  - agent-ready narrow APIs
  - weekly intelligence subscriptions
- **Rakiplerin yapamadığı şey:** aynı anda dosya-tabanlı hafıza, çoklu model doğrulama, browser/data/research worker karması ve human gate’i bir arada çalıştırmak.
- **White-label / SaaS ihtimali:** evet, ama “general swarm platform” olarak değil; mission-control + vertical kit + verifier layer olarak.

## Öncelik & Çaba Tahmini
- Öncelik: **Yüksek**
- Kurulum Süresi: **5-10 gün** ilk dogfood lane, **4-8 hafta** daha oturmuş ticari paket
- Aylık İşletme Maliyeti: **$50-$300** iç kullanım; yoğun browser/voice/data ile **$300-$1,500** bandına çıkabilir
- Potansiyel Gelir: **$149-$599** sprint, **$499-$2,500** setup, **$99-$499/mo** bakım
- ROI Beklentisi: **1-3 müşteri** veya **5-10 ücretli rapor/audit** ile break-even mümkün

## Mevcut Sistemle Entegrasyon
- `sistem-planlama` araştırma çıktıları future brief bankası olur.
- `/mind` run sonrası öğrenim ve hata kayıtlarını tutar.
- `projeler.txt` opportunity memory olarak kalır.
- browser/arxiv/mcptube/web/GitHub katmanları worker capability catalog’u gibi çalışır.
- `universe_loop.sh` veya benzeri orchestration katmanı gelecekte sadece **route + budget + approval** işi yapmalı; tüm zekâyı tek agent’a gömmemeli.

## Riskler & Dikkat Edilecekler
- gevşek swarm = koordinasyon çorbası
- tool patlaması = token ve latency mezarlığı
- silent failure = broken form / broken API / yanlış veri ile sahte başarı
- güven eksikliği = güzel demo ama sıfır satış
- external action riski = onaysız outreach / deploy / ödeme
- model homogeneity riski = herkes aynı saçmalığı üretir; verifier ve karşı-perspektif şart

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Swarm task matrix yaz:** hangi iş single-agent, hangisi supervisor, hangisi gerçek swarm netleşsin.
2. **Bir lane seç ve dogfood et:** öneri `research/report lane`; ilk aday GTIP snapshot veya local business leak audit.
3. **Verifier + offer paketini çıkar:** kalite checklist’i ve müşteri-facing tek sayfalık “swarm-backed sprint” teklifi hazır olsun.
