# Araştırma #6 — E-commerce Automation
**Tarih:** 2026-04-21 05:51 +03
**Konu:** Shopify / Amazon / Etsy ekseninde e-commerce operasyonlarını otomatize etmek: inventory, repricing, listing üretimi, review intelligence ve düşük-touch seller ops.
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma0-5.md` / `planlama0-5.md`
- Shopify Flow app: https://apps.shopify.com/flow
- Shopify Flow help: https://help.shopify.com/en/manual/shopify-flow
- Shopify workflow automation examples: https://www.shopify.com/enterprise/workflow-automation-examples
- Shopify pricing: https://www.shopify.com/pricing
- Shopify Q1 2025 results: https://www.shopify.com/investors/press-releases/merchant-success-drives-shopifys-excellent-q1---delivering-strong-revenue-growth-and-profitability
- Amazon seller pricing: https://sell.amazon.com/pricing
- Amazon Automate Pricing: https://sell.amazon.com/tools/automate-pricing
- Amazon seller ecosystem / 25 years: https://sellingpartners.aboutamazon.com/25-years-of-amazons-partnership-with-independent-sellers
- Etsy Q4/FY2025 results: https://investors.etsy.com/news-events/press-releases/detail/218/etsy-inc-reports-fourth-quarter-and-full-year-2025-results
- Etsy Listings tutorial / Open API: https://developer.etsy.com/documentation/tutorials/listings
- Make pricing: https://www.make.com/en/pricing
- Grand View Research — e-commerce software market: https://www.grandviewresearch.com/industry-analysis/e-commerce-software-market
- Reddit: https://reddit.com/r/shopify/comments/1pdulmb/anyone_else_tired_of_paying_for_6_different_apps/ , https://reddit.com/r/FulfillmentByAmazon/comments/1r9zm9b/i_built_a_simple_google_sheets_inventory/ , https://reddit.com/r/FulfillmentByAmazon/comments/1rssrcu/software_stacks_for_678figure_sellers/ , https://reddit.com/r/EtsySellers/comments/1psevsc/my_yearly_reminder_have_those_automated_responses_ready
- GitHub: https://github.com/Shopify/shopify-app-template-node , https://github.com/ScaleLeap/awesome-amazon-seller , https://github.com/oxylabs/etsy-scraper , https://github.com/anitabyte/etsyv3 , https://github.com/Cloud-Dev77/Amazon_Seller_Data_Extract , https://github.com/SerendipityOneInc/APIClaw-Skills , https://github.com/nusquama/n8nworkflows.xyz
- ArXiv: https://arxiv.org/abs/2602.07695 , https://arxiv.org/abs/1912.02572 , https://arxiv.org/abs/2112.08414 , https://arxiv.org/abs/2505.03828
- YouTube/MCPTube: https://www.youtube.com/watch?v=DAoxfhgaFOU , https://www.youtube.com/watch?v=LkBI0VotnEA , https://www.youtube.com/watch?v=muX-M-r0c6Y

## Özet Bulgular
- En hızlı para eden e-commerce automation teklifi “tam mağaza kuruyorum” değil; **Shopify app-sprawl cleanup + Amazon repricing/inventory guardrails + Etsy draft listing factory** üçlüsü. Üçü de seller'ın aynı sinirine basıyor: fazla tab, fazla tool, fazla tekrar işi.
- Pazar canlı ve büyük. Grand View'e göre global e-commerce software pazarı **2025'te $9.42B**, **2033'te $34.18B**; CAGR **%18.5**. Shopify Q1 2025 GMV'si **$74.75B**. Amazon'da bağımsız satıcılar satışların **%60+**'ını oluşturuyor ve 25 yılda **$2.5T+** satış yaptı. Etsy 2025 sonunda **86.5M aktif buyer** ve **5.6M aktif seller** raporluyor.
- Teknik olarak giriş bariyeri düşük ama operasyonel bariyer gerçek. Shopify Flow **Basic/Grow/Advanced/Plus** planlarında ücretsiz. Amazon Automate Pricing resmi olarak **ücretsiz**, ama Seller Central Professional planı **$39.99/ay** gerektiriyor. Etsy Open API ile draft listing açılabiliyor, fakat OAuth scope, image upload, taxonomy/shipping/readiness alanları düzgün kurulmazsa süreç patlıyor.
- Community sinyali çok net: seller'lar “AI” diye değil, **zaman tasarrufu + tool maliyeti düşüşü + stockout/pricing hatası azalması** diye satın alıyor. Reddit'te tek kişilik Shopify mağaza sahibi 6 app'e **$167/ay** ödediğini, bunu n8n + Pipedream ile düşürdüğünü söylüyor. FBA tarafında hâlâ Sheets/Excel ile forecast yapan satıcılar var; çünkü birçok araç ya pahalı ya da gereksiz şişkin.
- Moat başlık yazdırmak değil. Asıl değer; **güvenilir veri akışı, policy-safe otomasyon, insan onaylı draft aşaması, fiyat tabanı/üst sınırı guardrail'leri ve seller'a görünür ROI raporu**.

## Gerçek Başarı Hikayeleri
- **Resmi Amazon ekosistem ölçeği:** Amazon Selling Partners sayfasına göre bağımsız satıcılar artık Amazon mağazasındaki satışların **%60+**'ını oluşturuyor; 25 yılda **$2.5 trilyon+** satış ürettiler. Aynı sayfa, 2024'te bu satıcıların ABD'de **2 milyondan fazla kişiyi** istihdam ettiğini söylüyor. Bu doğrudan “automation product” hikâyesi değil ama pazardaki para ve hacmin gerçek olduğunu kanıtlıyor.
- **Hawaiian Shaved Ice — operasyon ölçeklenmesi:** Amazon'un aynı makalesinde Hawaiian Shaved Ice kurucusu, FBA sonrası operasyonlarının **4,000 sq ft** depodan toplam **200,000+ sq ft** alana çıktığını anlatıyor. Yani seller ops otomasyonu ve lojistik katmanı gerçekten kapasite çarpanı oluyor.
- **Shopify Flow — gerçek operasyon problemi çözümü:** Shopify'nin resmi örneğinde Kate McLeod, sıcak bölgelerdeki müşterileri Flow ile işaretleyip eriyen ürün riskini azaltıyor; Magnolia Bakery ise hediye mesajlarından “birthday purchasers” segmenti çıkarıp doğum günü SMS'leri atıyor. Bu örnekler revenue rakamı vermiyor ama doğrudan “manuel veri ayıklama yerine workflow” değerini gösteriyor.
- **Reddit self-report — app-sprawl tasarrufu:** r/shopify'da tek kişilik mağaza sahibi; post-purchase email, inventory ping, Slack notifier, UTM tagger, review requester ve CSV exporter için **6 app / $167 aylık** ödediğini; aynı işleri n8n senaryosu + kısa bir Pipedream script ile taşıdığını yazıyor. Bu denetlenmiş finansal tablo değil; ama seller'ın acısını ve offer dilini çok net gösteriyor.
- **Etsy listing factory — creator claim ama işe yarayan matematik:** MCPTube'da MakeBoxAI videosu “**20 Etsy listing in 40 minutes**”, yani listing başına yaklaşık **2 dakika** iddia ediyor. Aynı videoda 50 listing ile **$250-$750**, 200 listing ile **$2,000-$3,000** gelir senaryosu sunuluyor. Bu creator math; finansal doğrulama değil. Ama “listing throughput” gerçekten para değişkeni olduğu için ciddiye alınmalı.
- **Amazon repricer workflow — creator claim ama somut akış:** Aura videosu, yaşlanan stok için 0-30 / 31-60 / 61+ gün kovalı üç strateji (profit, buy-box, liquidation) kurup bunu saatlik çalışan otomasyona bağlamayı gösteriyor. Ayrıca erken aşama plan için **$27/ay** creator claim'i veriyor. Fikir doğru: repricing'i çalışan gibi kullan, ama guardrail'siz bırakma.

## Pazar Büyüklüğü & Fırsat
- **Global yazılım pazarı büyüyor:** Grand View Research, global e-commerce software market size'ı **2025'te $9.42B**, **2026'da $10.43B**, **2033'te $34.18B** olarak veriyor; **%18.5 CAGR**. Buradaki ders basit: seller ops tooling pazarı “niş oyuncak” değil.
- **Shopify hacmi dev:** Shopify Q1 2025 sonuçlarına göre GMV **$74.75B**. Bu sadece bir çeyrek. Ayrıca Shopify pricing sayfası “millions of merchants” dilini kullanıyor; yani bir Flow cleanup / ops pack satmak için müşteri havuzu geniş.
- **Amazon seller side çok daha büyük ama daha sert:** Amazon'a göre bağımsız seller'lar satışların **%60+**'ını alıyor ve ilk 10 ay 2025 performansı, ilk 10 yılın toplamını aşmış durumda. Bu tarafın fırsatı büyük; ama pricing hatası, policy hatası ve inventory lock-up daha pahalıya patlıyor.
- **Etsy hacmi küçümsenmemeli:** Etsy Q4/FY2025 açıklamasında marketplace tarafında **86.5M aktif buyer**, **5.6M aktif seller**, çeyrekte **17.2M gross buyer addition** raporlanıyor. Bu kitlenin önemli kısmı tek kişilik ya da küçük ekipler; yani automation için klasik “time-poor, tool-confused” profil.
- **Somut fırsat yüzeyleri üç başlıkta toplanıyor:**
  1. **App consolidation:** Shopify gibi kanallarda 4-6 utility app yerine 1 otomasyon paketi.
  2. **Inventory & repricing guardrails:** Amazon'da price war ve stock aging kontrolü.
  3. **Listing throughput & review intelligence:** Etsy/Amazon/Shopify katalog tarafında daha hızlı draft üretimi ve yorumlardan insight çıkarma.

## Rakipler & Boşluklar
- **Shopify Flow:** Güçlü yanı; ücretsiz, native, güvenli, trigger-condition-action mantığı temiz. Zayıf yanı; gerçek dış servis entegrasyonlarında **Send HTTP Request** aksiyonu sadece **Grow/Advanced/Plus** tarafında. Basic'te “full orchestration” için duvara toslayabiliyorsun.
- **Amazon Automate Pricing:** Resmi araç “free” ve 24/7 çalışıyor. Güzel. Ama bu sadece pricing. Review mining, seller analytics, multi-marketplace sync, policy explanation, edge-case handling yok. Yani tam ops suite değil, tek silah.
- **Etsy Open API:** Draft listing, image upload, inventory, digital file akışını destekliyor. Güzel. Ama category/taxonomy/shipping/readiness ve listing policy tarafı hâlâ insan kontrolü istiyor. “Tam otomatik publish” hevesi burada saçma risk üretir.
- **Make / n8n / script stack:** Güçlü yanı hızlı kurulum. Zayıf yanı maliyetin ve hata yüzeyinin hızla görünmezleşmesi. Make tarafında krediler, image-heavy listing factory senaryolarında sessizce şişebilir.
- **Seller tool stack karmaşası:** Reddit/FBA topluluğu hâlâ Flieber, Finaloop, Profasee, JungleScout, Excel/Sheets karışımı kullanıyor. Boşluk şu: **tek iş için 6 tool kullanmak istemeyen seller**. Buraya “ops cockpit” satılabilir.
- **GitHub tarafı hazır parçalarla dolu:** `Shopify/shopify-app-template-node`, `ScaleLeap/awesome-amazon-seller`, `Cloud-Dev77/Amazon_Seller_Data_Extract`, `oxylabs/etsy-scraper`, `anitabyte/etsyv3`, `nusquama/n8nworkflows.xyz` gibi parçalar var. Ama **Shopify + Amazon + Etsy için tek opinionated seller-ops starter kit** yok. Boşluk burada.

## Teknik Gereksinimler
- **Veri katmanı:** SKU, inventory age, min/max price, order events, customer tags, review text, listing draft state, marketplace channel, publish status, ROI metrics.
- **Shopify lane:**
  - Trigger / condition / action workflow kurgusu
  - düşük stokta vendor e-postası veya Slack mesajı
  - VIP customer tagging
  - abandoned checkout follow-up
  - Sheets / Klaviyo / Slack bağlantıları
- **Amazon lane:**
  - Seller Central Professional hesabı (**$39.99/ay + selling fees**)
  - Automate Pricing rules veya SP-API data pull
  - price floor / ceiling guardrail
  - inventory age bucket'ları (örn. 0-30, 31-60, 61+ gün)
  - exception queue: liquidation da satmayan ürünler için insan kararı
- **Etsy lane:**
  - Open API OAuth token (`listings_r`, `listings_w`, opsiyonel `listings_d`)
  - `x-api-key`
  - `createDraftListing` → `uploadListingImage` → gerekirse `uploadListingFile` → `updateListing(state=active)`
  - zorunlu alanlar: quantity, title, description, price, who_made, when_made, taxonomy_id, shipping_profile_id, readiness_state_id
  - draft-first, publish-later akışı
- **Orkestrasyon / maliyet:**
  - Shopify Flow: ücretsiz app, Basic/Grow/Advanced/Plus planlarında çalışıyor
  - Shopify planları (ABD pricing snippet'i): Basic **$29/ay**, Grow **$79/ay**, Advanced **$299/ay** billed yearly; fiyat lokasyona göre değişebiliyor
  - Make pricing snippet'i: Free **1,000 credit/ay**, Core **$9 / 10k credits**, Pro **$16 / 10k**, Teams **$29 / 10k**
  - OpenAI / uygun LLM sağlayıcısı
  - gerektiğinde Google Sheets / Drive / Slack / Telegram / email relay
- **İnsan müdahalesi gereken noktalar:**
  - kategori / shipping / taxonomy doğrulaması
  - repricing floor ve liquidation kararı
  - review/request policy kontrolü
  - first-publish QA
  - marketplace hesabı yetkilendirmesi

## Ham Notlar
- `projeler.txt` içinde doğrudan Shopify/Amazon/Etsy yoğun değil; ama iç leverage güçlü: `browser-use`, `browser-use/agent-sdk`, `crawlee-python`, `CyberScraper-2077`, Scrapeless ve benzeri scraping/browser araçları seller ops research için zaten elimizde.
- Shopify Flow App Store sayfasında 4.7 rating ve **9,515 review** var; merchant summary kısmında **haftalık 15-20 saat tasarruf** ifadesi geçiyor. Bu App Store AI summary olduğu için ikinci el sinyal; ama güçlü.
- Amazon resmi Automate Pricing sayfası “free tool” diyor, ama aynı sayfa “Featured Offer oranını ve satışları artırmak için 30 günlük history ile etkisini izle” diye uyarıyor. Yani kur ve unut değil; kur, izle, gerektiğinde düzelt.
- r/FulfillmentByAmazon'daki inventory forecasting post'u önemli: insanlar hâlâ “expensive tools” yerine Google Sheets şablonu istiyor. Basit ama görünür otomasyon, şişkin enterprise tool'dan daha kolay satılabilir.
- r/EtsySellers tarafında holiday rush ve automated responses teması tekrar ediyor. Burada listing factory kadar message macro / SLA expectation yönetimi de satılabilir.
- ArXiv tarafı şunu söylüyor:
  - **EventCast (2602.07695)**: e-commerce demand forecasting'de event-aware yaklaşım event dönemlerinde ciddi hata düşüşü sağlıyor; yani inventory otomasyonu kör kalmamalı.
  - **Dynamic Pricing with DRL (1912.02572)**: gerçek Tmall field experiment'i var; pricing otomasyonu akademik oyuncak değil.
  - **DSGPT (2112.08414)** ve **Sentiment-Aware Recommendation Review (2505.03828)**: title/review summarization commodityleşiyor. Tek başına “AI title writer” edge değil.
- ProductHunt/Jina tarafında Cloudflare koruması nedeniyle bazı sayfalar erişilemedi. Bu turda esas yük resmi doküman + Reddit + GitHub + ArXiv + MCPTube ile taşındı.
