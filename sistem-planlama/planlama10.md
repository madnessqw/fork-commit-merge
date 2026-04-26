# Planlama #10 — Micro-SaaS & API-First Data Products Uygulama Haritası
**Tarih:** 2026-04-21 08:52 +03
**Bağlı Araştırma:** arastirma10.md

## Swarm Agent ile Nasıl Uygulanır?
UniverseCreator için doğru tasarım **API Product Foundry Lane**: araştırma cycle’larında bulunan veri/otomasyon kabiliyetleri doğrudan SaaS ekranına dönüşmek zorunda değil; önce küçük, ölçülebilir, agent-ready API/veri ürünlerine paketlenmeli.

Önerilen mimari:
1. **Opportunity Scanner**
   - Giriş: önceki araştırma dosyaları, `projeler.txt`, ürün portföyü, canlı pazar sinyalleri.
   - Çıkış: API adayı listesi: persona, veri kaynağı, risk, fiyat, MVP scope.
2. **API Candidate Scorer**
   - Skor: veri erişilebilirliği, legal risk, recurring use, API-first fit, rakip fiyatları, üretim maliyeti, agent/MCP uyumu.
   - Eleme: LinkedIn/Amazon gibi high-risk scraping kırmızı; public/open data ve kendi ürün verisi yeşil.
3. **Spec Designer**
   - Her aday için OpenAPI taslağı, JSON schema, error model, quota modeli, sample payload.
   - Kod yazmadan önce API sözleşmesi ürünün kendisi gibi tasarlanır.
4. **Data/Execution Worker**
   - API’nin arkasındaki veri toplama/normalization/refresh işini ayrı worker yürütür.
   - Önce CSV/manual batch; sonra otomatik refresh.
5. **Metering & Billing Layer**
   - API key, usage counter, quota, plan mapping.
   - Başlangıçta direct checkout + manuel key olabilir; marketplace ikinci kanal.
6. **Docs/DX Publisher**
   - Landing + docs + Postman collection + n8n/Make examples + MCP wrapper.
   - Developer değil agent da okuyabilsin.
7. **Verifier & Cost Ledger**
   - Her endpoint için latency, success rate, freshness, cost/request, failure reason.
   - “API çalışıyor” demek yetmez; doğru, güncel ve kârlı mı ölçülür.
8. **Report/Alert Productizer**
   - Aynı API verisi business buyer için CSV/PDF/weekly digest/Telegram alert olarak paketlenir.
   - Developer API + business report ikili model olur.

## Gerekli Bileşenler
- **Script/Bot:**
  - API aday skorlayıcı
  - OpenAPI/spec şablonu
  - data refresh worker
  - quota/usage ledger
  - API key registry
  - docs/sample generator
  - weekly report exporter
  - cancellation/feedback logger
- **MCP/Araç:**
  - Jina/curl: doküman ve public source okuma
  - chrome-devtools-axi / Playwright MCP: browser-required veri doğrulama, ama API-first kuralıyla
  - ArXiv/MCPTube: pazar ve teknik kaynak izleme
  - Postman/OpenAPI export: agent-readable docs
  - opsiyonel MCP wrapper: API’yi agent tool olarak sunmak
- **API:**
  - Direct billing: Stripe/LemonSqueezy/Paddle veya mevcut payment setup neye izin veriyorsa
  - Marketplace test: RapidAPI/APILayer; RapidAPI fee güncel dokümana göre %25 + payout fee olabileceği için marj hesabına yazılmalı
  - Data providers: Firecrawl/SerpApi/ScrapingBee gibi kaynaklar sadece ürün ekonomisi kaldırıyorsa
- **İnsan Müdahalesi:**
  - ilk 3 API adayı seçimi
  - legal/TOS risk kararı
  - pricing ve refund policy onayı
  - ilk müşteri demo/support
  - high-risk veri kaynaklarında devam/iptal kararı

## Workflow Haritası
Research cycle output
→ API adayı çıkarılır
→ scorecard: problem/persona/source/risk/pricing
→ OpenAPI + sample response yazılır
→ veri kaynağı manuel batch ile doğrulanır
→ landing/docs/waitlist veya marketplace draft hazırlanır
→ 5-10 potansiyel kullanıcıya demo gönderilir
→ ödeme/interest sinyali alınır
→ MVP endpoint + metering kurulur
→ usage/freshness/cost ölçülür
→ weekly report/alert formatı eklenir
→ başarılı aday API catalog’a alınır

Örnek aday #1 — LLM Cost & Pricing Intelligence API:
model/provider listesi
→ fiyat ve context limit kaynakları izlenir
→ normalized JSON: provider/model/input/output/context/date
→ endpoint: `/v1/llm-prices`, `/v1/compare`, `/v1/estimate`
→ n8n/agent örneği
→ weekly pricing change alert
→ $19 starter / $49 pro / $149 agency

Örnek aday #2 — HS/GTIP Trade Snapshot API:
HS code + target country
→ public trade/tariff/source data normalize
→ buyer/supplier/risk/market trend fields
→ endpoint + PDF report
→ exporter/outreach teams için $49-$199/ay veya report başı $39-$79

Örnek aday #3 — Website Health / Checkout Evidence API:
URL listesi
→ HTTP status + screenshot/evidence + console/network summary
→ JSON + weekly digest
→ mevcut UniverseCreator ürün QA hattına da hizmet eder
→ micro-SaaS/devtool buyer için $19-$99/ay

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen yapılacak en mantıklı şey:** Kod yazmadan **3 API ürün adayının spec-first paketini** çıkarmak. Endpoint adı, input/output JSON, fiyat, veri kaynağı, sample response, landing copy, risk sınıfı.
- **En düşük çaba / en yüksek çıktı adımı:** mevcut ürün/araştırma varlıklarından API’ye en yakın olanları seç:
  1. LLM Cost/Pricing API — mevcut AI Cost Dashboard / LLM Token Lens çizgisine yakın.
  2. Website Health/Checkout Evidence API — mevcut ürün sağlık kontrol hafızasına yakın.
  3. HS/GTIP Trade Snapshot API — önceki ticari istihbarat araştırmasına bağlı, daha yüksek B2B değerli.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - `projeler.txt` kaynak kataloğu
  - Jina/curl ve browser tools
  - önceki `arastirma*.md` verileri
  - mevcut product health check deneyimi
  - OpenAPI/Postman/MCP yaklaşımları
- **Proof-of-concept için minimum gereksinimler:**
  - her aday için 1 sayfalık spec
  - 3 örnek JSON response
  - 1 pricing hypothesis
  - 1 demo report/CSV
  - 10 kişilik hedef müşteri listesi
  - manuel ödeme/key delivery planı
- **Tahmini kurulum süresi ve ilk gelir beklentisi:**
  - Spec + demo: **2-3 gün**.
  - Landing/docs/waitlist: **2-4 gün**.
  - İlk manuel demo/outreach: **3-5 gün**.
  - İlk gelir beklentisi: 1-2 hafta içinde gerçekçi hedef **$0-$200 MRR** veya 1-3 paid pilot; daha iyi hedef bir defalık **$39-$99** data report satışı.
- **Kısa vade hükmü:** “API platformu inşa edelim” diye şişirmek aptalca. İlk hafta sadece **satılabilir API sözleşmesi + demo çıktı + ödeme niyeti** ölçülür.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: Sistem nasıl olgunlaşır / 1. ay sonunda nasıl görünmeli?**

- **1. ay sonunda:**
  - 1 API adayı canlı POC: API key, usage log, docs, sample, basic billing/manual fulfillment.
  - 1 business-facing report versiyonu: aynı verinin PDF/CSV/alert çıktısı.
  - 10-30 hedef kullanıcıya gösterilmiş; 3-5 ciddi conversation alınmış.
- **2-3 ay sonunda:**
  - 3 çalışan micro API/data product:
    1. LLM pricing/cost intelligence
    2. website health/evidence monitoring
    3. HS/GTIP veya competitor price/stock snapshot
  - API Product Catalog: pricing, docs, examples, status, changelog.
  - Metering: per-key quota, overage prevention, plan usage email.
  - Agent-ready layer: OpenAPI + Postman collection + MCP wrapper for top endpoint.
- **Hangi metric'ler başarıyı gösterir?**
  - paid keys / trial keys
  - API calls per active key
  - cost per 1,000 successful calls
  - latency and success rate
  - data freshness
  - docs-to-first-call conversion
  - report open/reply rate
  - churn/cancel reason
  - support minutes per customer
- **Hangi adımlar paralel çalışabilir?**
  - API spec/design
  - data source verification
  - landing/docs copy
  - pricing tests
  - marketplace draft
  - target customer list/outreach
  - report template
- **Ölçeklendirme için ne gerekiyor?**
  - küçük DB/ledger
  - reliable background jobs
  - status/monitoring
  - API key + abuse prevention
  - direct payment provider netleşmesi
  - legal/TOS checklist
  - support SLA yoksa açıkça “best effort” pozisyonlama
- **Checkpoint'ler ve başarı kriterleri:**
  1. Hafta 1: 3 spec + demo JSON + pricing hypothesis
  2. Hafta 2: 1 paid/manual pilot veya 10 ciddi feedback
  3. Hafta 4: 1 endpoint stable, 1 docs page, 1 report sample
  4. Hafta 8: 3-5 paying users veya net pivot kararı
  5. Hafta 12: API catalog + agent-ready wrapper + recurring report product

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator bir **agent-ready data/API product studio** olur. Research swarm fırsatı bulur, spec çıkarır, veri hattını doğrular, API + report olarak paketler, küçük fiyatlarla piyasaya salar, başarısızları öldürür, başarılıları büyütür.
- **Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?**
  - API catalog: $19-$299/ay self-serve plans
  - one-off data reports: $39-$499/report
  - managed data API for agencies: $300-$1,500/ay
  - MCP server marketplace: API’lerin agent-tool versiyonu
  - white-label dashboards
  - workflow templates: n8n/Make/Zapier API examples
  - data freshness/monitoring SLA upsell
- **Rakiplerin yapamadığı, swarm yaklaşımıyla yapılabilecek nedir?**
  - Araştırma → veri kaynağı keşfi → browser/API route → spec → docs → pricing → outreach → feedback → iteration tek döngüde birleşir.
  - Çok ürünlü portföy hafızası sayesinde aynı core data farklı paketlere bölünür: API, PDF report, alert, dashboard, MCP tool.
  - Agent-ready docs standart olur: her API insan + agent + workflow tool için tasarlanır.
  - Cost/risk ledger ile “bu API para kazandırıyor mu yoksa proxy/LLM maliyeti yiyor mu?” erken görülür.
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet, ama self-serve SaaS’tan önce managed API/report daha mantıklı.
  - 3-6 ay: “API + weekly report” white-label agency paketleri.
  - 6-12 ay: API catalog + MCP wrappers + customer portal.
  - 12 ay: en iyi endpoint’ten ayrı micro-SaaS/dashboard.
- **3-12 ay evrim sırası:**
  1. Spec-first API aday havuzu
  2. Tek canlı endpoint + manuel billing
  3. 3 endpoint catalog
  4. Direct + marketplace distribution
  5. MCP wrappers
  6. White-label report/dashboard
  7. En çok usage alan endpoint için dedicated SaaS

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** spec/demo **2-7 gün**, canlı POC **2-4 hafta**, 3 ürünlü catalog **2-3 ay**
- **Aylık İşletme Maliyeti:**
  - manual/static/internal-data API: **$0-$30/ay**
  - hosted DB/queue/monitoring: **$20-$100/ay**
  - Firecrawl/SerpApi/ScrapingBee gibi veri provider kullanılırsa: **$16-$249+/ay** başlangıç, usage’a göre artar
  - marketplace fee: RapidAPI güncel destek dokümanında **%25 + payout fee riski**
- **Potansiyel Gelir:**
  - starter API: **$10-$29/ay**
  - pro API: **$49-$99/ay**
  - agency/data API: **$149-$299/ay**
  - managed report/API: **$300-$1,500/ay**
  - one-off data report: **$39-$499**
- **ROI Beklentisi:**
  - Direct low-cost API’de 1-3 müşteri maliyeti kapatır.
  - Provider/API maliyeti kullanan ürünlerde break-even için en az **5-10 paying customer** veya yüksek fiyatlı managed customer gerekir.
  - Marketplace ile satışta fiyatı **%25 fee** sonrası net marja göre koymak şart.

## Mevcut Sistemle Entegrasyon
- Mevcut araştırma/planlama döngüsü API ürün seçimi için zaten veri üretiyor. Her araştırma sonunda “API’ye dönüşür mü?” alanı eklenebilir.
- Product factory tarafında mevcut araçlar API adayıdır:
  - AI Cost Dashboard / LLM Token Lens → LLM pricing/cost API
  - HTTP Pulse / StatusBeacon → website health/evidence API
  - Meta Fetch / OG Forge / URL Forge → URL intelligence API
  - HS/GTIP araştırması → trade snapshot API/report
  - Browser Agent araştırması → checkout proof / competitor price monitor API
- `projeler.txt` içinde API/MCP/wrapper sinyalleri var; yeni fikirler dışarıdan gelmek zorunda değil.
- Mevcut swarm rollerine eşleme:
  - Research agent: pazar + rakip + pricing
  - Codex: spec + docs + risk ledger planı
  - Browser lane: veri kaynağı doğrulama
  - QA/tester: endpoint health/status
  - Analyst: usage/cost/revenue yorumlama

## Riskler & Dikkat Edilecekler
- **Marketplace yanılgısı:** RapidAPI’de popülerlik ya da listing tek başına müşteri getirmez. Buyer persona ayrı bulunmalı.
- **Komisyon/marj:** %25 marketplace fee + payout fee küçük fiyatlı API’lerde marjı yer. Direct channel şart.
- **Scraping legal/TOS riski:** LinkedIn scraper örneği gelir getirse de dava riski taşıyor. High-risk source kırmızı listeye alınmalı.
- **Free tier abuse:** API ürünleri botlar tarafından tüketilir; API key, rate limit, captcha değil ama abuse detection ve quota şart.
- **Support yükü:** API müşteri “çalışmadı” dediğinde debug pahalıdır. Logs, request id, status page, typed errors olmadan destek cehennem.
- **Data freshness:** Veri ürünü eskiyse ürün ölür. Her response freshness timestamp taşımalı.
- **Overbuilding:** API gateway/platform inşa etmeye dalmak erken ölüm. İlk ürün manuel key + usage CSV ile bile doğrulanabilir.
- **Commodity API tuzağı:** QR/screenshot/email verification gibi alanlarda generic olmak zayıf. Niş/persona/use-case olmadan fiyat kırma savaşına girilir.
- **Secret exposure:** API logs ve docs örneklerinde gerçek token asla görünmemeli. Test key ayrı, redaction zorunlu.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **3 API adayı için spec sheet yaz:** LLM cost API, website evidence API, HS/GTIP trade snapshot API. Her biri: persona, endpoint, sample JSON, pricing, data source, risk.
2. **1 aday için demo data pack üret:** Kod değil, mock/sample JSON + CSV/PDF report + landing copy. Hedef: satılabilirliği ölçmek.
3. **10 hedef müşteri/prospect listesi çıkar:** developer API için dev communities; report için exporter/agency/local business. Marketplace’e koymadan önce buyer konuşması başlasın.
