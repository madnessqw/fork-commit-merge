# Araştırma #20 — E-commerce Automation
**Tarih:** 2026-04-21 16:15 +03
**Konu:** Shopify / Amazon / Etsy seller operasyonlarını otomatize etmek; bu tur odak: **cross-channel inventory sync + repricing guardrails + review intelligence + policy-safe listing draft**. 2. tur / 2026 doğrulama.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma6.md` / `planlama6.md`, `STATE_SUMMARY.json`.
- ddgr: `e-commerce automation software market size 2025`, `shopify amazon etsy automation case study revenue 2025`, `site:indiehackers.com shopify app mrr inventory`, `amazon repricer software case study 2025`, pricing query'leri.
- Reddit JSON API: r/shopify, r/FulfillmentByAmazon, r/EtsySellers, r/ecommerce.
- GitHub: https://github.com/amzn/selling-partner-api-samples , https://github.com/saleweaver/python-amazon-sp-api , https://github.com/Shopify/shopify-app-template-node , https://github.com/malikad778/nexus-inventory , https://github.com/oxylabs/etsy-scraper
- Resmi / pazar kaynakları: https://www.grandviewresearch.com/industry-analysis/e-commerce-software-market , https://s27.q4cdn.com/572064924/files/doc_financials/2025/q4/SHOP-Q4-2025-10K.pdf , https://help.shopify.com/en/manual/shopify-flow , https://apps.shopify.com/flow , https://www.repricerexpress.com/pricing/ , https://sellersnap.io/pricing/ , https://www.veeqo.com/pricing , https://storeinspect.com/blog/how-many-shopify-stores-are-there
- ArXiv: https://arxiv.org/abs/2602.07695 , https://arxiv.org/abs/1912.02572 , https://arxiv.org/abs/2505.23421 , https://arxiv.org/abs/2307.14305 , https://arxiv.org/abs/2404.05243
- MCPTube / YouTube: https://www.youtube.com/watch?v=pgIgKEHC73Y , https://www.youtube.com/watch?v=yaIgY4tQ6Iw , https://www.youtube.com/watch?v=LkBI0VotnEA
- ProductHunt/Jina araması: https://www.producthunt.com/search?q=ecommerce%20automation , https://www.producthunt.com/search?q=shopify%20inventory , https://www.producthunt.com/search?q=amazon%20repricer (bu turda sinyal zayıf / gürültülü).

## Özet Bulgular
- **“Bir tane daha automation app” yapmak aptallık.** Native/free baseline yukarı çıkmış durumda: Shopify Flow ücretsiz; Veeqo shipping tarafını bedava veriyor; Amazon'un resmi Automate Pricing alternatifi zaten var. Asıl boşluk, tek kanal içi otomasyon değil; **kanallar arası margin, stock, policy ve approval katmanı**.
- **Pazar büyük, ama merchant iştahı “az app, yüksek ROI” yönünde.** Grand View Research, global e-commerce software pazarını **2025'te $9.42B** ve **2033'te $34.18B** gösteriyor. Shopify 10-K'ya göre **31 Aralık 2025 itibarıyla 21,000+ app** var. Buna rağmen StoreInspect veri setinde mağazaların **%55'i 0 veya 1 aktif app** kullanıyor; ortalama **1.7 app**. Yani merchant'lar yeni oyuncak değil, **sprawl azaltan kontrol düzeyi** istiyor.
- **Community acısı çok net:** r/shopify'da solo mağaza sahibi 6 utility app için **$167/ay** ödediğini ve bunu n8n + kısa script ile düşürdüğünü söylüyor. r/FulfillmentByAmazon'da bir seller, Amazon'un yanlış AI/price matching davranışı yüzünden **6 haneli revenue loss** yaşadığını yazıyor. r/EtsySellers'ta AI title suggestion yüzünden **3 policy violation** yiyen satıcı var. Ortak ders: seller'lar “AI” istemiyor; **güvenli otomasyon** istiyor.
- **Açık kaynak tarafında altyapı var, ürün katmanı yok.** `python-amazon-sp-api` **640★**, `Shopify/shopify-app-template-node` **1002★**, resmi Amazon SP-API samples **148★**; ama gerçek multi-channel sync paketi `nexus-inventory` sadece **29★**. Yani connector/SDK katmanı hazır; **opinionated seller-ops control plane** hâlâ açık alan.
- **Akademik ve video tarafı aynı şeyi söylüyor:** Demand forecasting, repricing, opinion summarization ve multichannel stock sync artık yapılabilir şeyler. Zor olan algoritma değil; **guardrail, insan onayı, rate-limit, webhook disiplini ve görünür ROI raporu**.

## Gerçek Başarı Hikayeleri
- **DropCommerce — 78K CAD MRR:** Indie Hackers post'unda kurucu, Shopify App Store'da 3 ay sonra launch ettiklerini, başlangıçta günde **18 install** aldıklarını, **Aralık 2018**'de ilk subscription revenue'yu gördüklerini, **Ağustos 2019**'da **~3K MRR**'a gelip full-time olduklarını, **Şubat 2020'de 12K/ay** iken **Mayıs 2020'de 46K MRR**'a çıktıklarını ve ardından **10 kişilik ekip** kurduklarını anlatıyor. Ders: marketplace-distribution + iyi support + review rating, seller ops ürünlerinde hâlâ çalışıyor.
- **WideBundle — $25K MRR:** Başka bir Indie Hackers post'unda WideBundle'ın **Mayıs 2020'de** sıfırdan başlayıp bir yıldan kısa sürede **2,000 kullanıcı** ve **~$25K MRR** seviyesine çıktığı yazıyor. Kurucunun en net dersi: “customer support first feature.” Seller ürününde support kalitesi direkt büyüme motoru.
- **RepricerExpress vendor-claim sonuçları:** RepricerExpress pricing sayfasında müşteri istatistiği olarak **2 haftada %63 Buy Box artışı**, **%30 revenue artışı** ve **ilk ay %50+ profit artışı** iddia ediyor. Bu bağımsız audit değil; vendor claim. Ama seller'ların repricing için para ödemesinin sebebi net: doğru kurulduğunda marj ve volume fark yaratıyor.
- **Shopify solo merchant — app-sprawl tasarrufu:** r/shopify'daki örnekte tek kişilik merchant, post-purchase email, inventory ping, Slack notifier, UTM tagger, review requester ve CSV exporter için **6 ayrı subscription / $167 aylık** ödediğini; bunu n8n + Pipedream ile sadeleştirdiğini yazıyor. Bu bir finansal tablo değil ama gerçek satın alma cümlesini veriyor: “daha çok AI” değil, **daha az araç, daha az tekrar işi**.
- **Amazon repricing workflow — operasyonel kaldıraç:** Aura videosu, yeni listing geldiğinde repricing'i otomatik açan workflow'u ve age-of-inventory'ye göre **0-30 / 31-60 / 61+ gün** strateji geçişini gösteriyor. Repricer'i çalışan gibi kullanıp eski stoku likide etmek mümkün; ama min/max guardrail ve insan override şart.

## Pazar Büyüklüğü & Fırsat
- **Toplam yazılım pazarı:** Grand View Research'e göre e-commerce software market **2025'te $9.42B**, **2033'te $34.18B**. Bu kategori oyuncak değil; ciddi yazılım bütçesi var.
- **Shopify ekosistemi kalabalık ama hâlâ para dönüyor:** Shopify 10-K'ya göre **21,000+ app** mevcut ve merchant solutions revenue **2025'te $8.8B**'a çıkmış (**2024'e göre +%35**). Ekosistem doymuş gibi görünse de para burada.
- **Merchant davranışı fırsatı daraltıyor ve netleştiriyor:** StoreInspect veri setinde mağazaların **%21.2**'si hiç app görünürlüğüne sahip değil; **%33.8**'i sadece 1 app kullanıyor; ortalama **1.7 app**. Bu şu demek: “5. app'i satmak” zor; ama **3 tool'u kaldıran ya da mevcut tool'ların üstüne risk katmanı koyan** teklif satılabilir.
- **Fiyat benchmark'ı sağlam:** RepricerExpress giriş seviyesi **$99/ay** ve **1,000 SKU** içeriyor. Seller Snap **$100 / $250 / $500** bandında. Veeqo shipping'i ücretsiz veriyor, ama inventory/listing/high-volume katmanlarını order volume bazlı fiyatlıyor; high-volume plan **$350/ay**'dan başlıyor. Yani merchant'lar inventory/price korumasına zaten para ödüyor.
- **En güçlü fırsat yüzeyi:**
  1. **Amazon margin guardrails** — supplier cost / shipping / referral fee / aged inventory değişince price floor'u koru.
  2. **Cross-channel stock sync** — Amazon/Walmart/eBay/Shopify/Etsy arasında oversell ve stockout'u azalt.
  3. **Policy-safe draft ops** — Etsy/Shopify tarafında AI'yı publish butonuna değil, draft + review aşamasına koy.
  4. **Review intelligence** — Amazon/Etsy/Shopify yorumlarından complaint cluster, feature request ve pricing objection çıkar.

## Rakipler & Boşluklar
- **Shopify Flow:** Güçlü, ücretsiz, native ve App Store tarafında **4.7 rating / 9,524 review** seviyesinde. Basit internal workflow işlerini zaten çözüyor. Burayla kafa kafaya girmek gereksiz; onu **alt katman** olarak kullanmak daha akıllı.
- **RepricerExpress:** Güçlü yanı hızlı Amazon repricing, 1,000 SKU giriş paketi, EPM mantığı ve custom planda multichannel/API. Zayıf yanı review intelligence, listing safety, cross-channel approval ve seller-specific insight katmanının olmaması.
- **Seller Snap:** Amazon repricer + business intelligence tarafında ciddi. Pricing bandı **$100 / $250 / $500**. Güçlü olduğu yer Amazon marj savaşı; zayıf olduğu yer Amazon dışı orkestrasyon ve insan onaylı karar akışı.
- **Veeqo:** Amazon-owned, shipping ücretsiz, inventory/listings kullanım bazlı. Multichannel order/inventory backbone için iyi. Ama asıl değer önerisi fulfillment operasyonu; **AI review mining + policy-risk + seller-facing insight** burada merkez değil.
- **Etsy tarafı:** API ve scraper parçaları var; ama community AI suggestion'lardan dayak yemiş durumda. “Autopublish listing AI” tarafı riskli. Boşluk: **draft-first, policy-safe, human-approved listing assistant**.
- **GitHub parçalı ekosistem:** resmi Amazon samples, Shopify template, Etsy scraper, multi-channel sync package ayrı ayrı var. Ama **Shopify + Amazon + Etsy + approval queue + margin guardrail + weekly report** setini opinionated sunan baskın OSS ürün görünmüyor.

## Teknik Gereksinimler
- **Ortak veri modeli:** channel, SKU, supplier cost, shipping cost, referral fee, min/max price, competitor price, inventory age, warehouse qty, draft status, publish approval, review clusters, exception reason.
- **Connector katmanı:**
  - Shopify: OAuth, GraphQL Admin API, REST/GraphQL mutasyonlar, webhooks, Flow entegrasyonu.
  - Amazon: SP-API / seller reports / pricing feeds / inventory reports.
  - Etsy: Open API veya kontrollü scraper; listing draft ve review/top-of-funnel veri çekme.
- **Orkestrasyon disiplini:** rate limiting, job queues, retry politikası, webhook imza doğrulama, audit log, per-channel failure queue. `nexus-inventory` örneğindeki unified driver + Redis-backed rate limit yaklaşımı mantıklı.
- **AI katmanı:**
  - Review summarization / complaint clustering
  - price anomaly detection
  - event-aware restock forecasting
  - draft listing assist (publish değil)
- **İnsan onayı gereken yerler:** liquidation threshold, price floor reset, Etsy/Shopify listing publish, IP/trademark riskli title/tag, supplier cost değişikliği, high-risk exception'lar.
- **Raporlama:** haftalık “hours saved / tool spend avoided / stockout prevented / aged inventory reduced / review themes / manual interventions” raporu.

## Ham Notlar
- Yerel `projeler.txt` içinde Shopify/Amazon/Etsy yoğunluğu neredeyse yok. Bu kötü haber değil; aksine mevcut portföyün seller-ops tarafında **boşta kaldığını** gösteriyor. Yani bu lane, mevcut 113 ürün ailesinden doğal olarak çıkmıyor; bilinçli yeni wedge istiyor.
- MCPTube transkriptleri çok somut: `Inventorify` videolarında Shopify ürünlerini otomatik track edip price + inventory update yaptığı; `Reprice Solution` videosunda supplier cost, shipping fee, referral fee değişikliklerini tek yerden child SKU'lara yaydığı; multichannel stock sync, low-stock alert ve eBay min-push stock yaptığı görülüyor. Yani feature set zaten net.
- ArXiv `EventCast` makalesi bunu ciddi şekilde doğruluyor: event-driven dönemlerde forecasting hatasını sert düşürüyor ve sistemin **Mart 2025'ten beri gerçek endüstriyel pipeline'da** kullanıldığı yazıyor. Prime Day / holiday / campaign dönemlerinde forecast katmanı kör olmamalı.
- `Automatically Evaluating Opinion Prevalence in Opinion Summarization` ve `MEDOS` çizgisi review mining işini destekliyor: ürün review özetleme hâlâ çözülebilir ve merchant-facing hale getirilebilir.
- ProductHunt tarafı bu turda boş konuştu; gerçek sinyal resmi pricing/docs + community posts + GitHub implementation layer'dan geldi. Bazen parlak launch sayfası yerine sıkıcı pricing sayfası daha değerli.
- `STATE_SUMMARY.json` şu an **113 active / 99 live / 107 healthy** diyor. Bu, ileride audit/report viewer veya demo landing için dağıtım yüzeyi olduğunu gösteriyor; ama seller-ops ürününü mevcut tool portföyüne yamamak yerine önce offer doğrulamak daha akıllı.
