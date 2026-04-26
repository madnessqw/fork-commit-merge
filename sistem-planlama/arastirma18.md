# Araştırma #18 — Türkiye + MENA Dijital Pazar
**Tarih:** 2026-04-21 14:15 +03
**Konu:** Trendyol / Hepsiburada / Sahibinden ekseninde Türkiye pazaryeri otomasyonu; MENA e-ticaret lokalizasyonu; TR/MENA için satılabilir agentic ops fırsatları
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `projeler.txt`, `STATE.json`, `STATE_SUMMARY.json`, önceki `sistem-planlama/sentez14.md`, `arastirma4.md`, `arastirma7.md`, `arastirma10.md`, `arastirma16.md`
- T.C. Ticaret Bakanlığı — Türkiye'de E-Ticaretin Görünümü Raporu, 06.05.2025: https://ticaret.gov.tr/duyurular/turkiyede-e-ticaretin-gorunumu-raporu-yayinlandi-06-05-2025
- ETBİS ana sayfa / rapor ve kayıtlı site işletme sayaçları: https://etbis.ticaret.gov.tr
- Trendyol Developers — Marketplace API dokümantasyonu: https://developers.trendyol.com/
- Hepsiburada Developer Portal — Getting Started: https://developers.hepsiburada.com/hepsiburada/docs/getting-started
- Hepsiburada Developer Portal — Sipariş entegrasyonu önemli bilgiler: https://developers.hepsiburada.com/hepsiburada/reference/siparis-entegrasyonu-onemli-bilgiler
- sahibinden.com Yardım Merkezi — API Kullanımı ile Veri Transferi: https://yardim.sahibinden.com/hc/tr/articles/19780244786460-API-Kullan%C4%B1m%C4%B1-ile-Veri-Transferi
- EZDubai / Euromonitor — E-commerce Report 2025 light version: https://www.ezdubai.ae/uploads/682b1ad891fe3_E-commerce_Report_2025_%28Light_Version%29.pdf
- Digital Commerce 360 — MENA ecommerce $34.5B 2024 → $57.8B 2029: https://www.digitalcommerce360.com/2025/05/27/mena-ecommerce-market-57-billion-by-2029/
- Pazaryeri Bot — Trendyol/Hepsiburada/ÇiçekSepeti automation vendor page: https://pazaryeribot.com/
- Sopyo fiyatlar / entegrasyonlar: https://www.sopyo.com/fiyatlar
- ikas e-ticaret paketleri: https://ikas.com/tr/fiyatlar
- iyzico Link: https://www.iyzico.com/iyzilink
- Ticaret Bakanlığı — İleti Yönetim Sistemi (İYS): https://ticaret.gov.tr/ic-ticaret/ticari-elektronik-iletiler/ileti-yonetim-sistemi-iys
- KVKK Kurul Kararı 2022/229 — e-ticaret çerez/kişisel veri işleme: https://www.kvkk.gov.tr/Icerik/7275/2022-229
- Reddit JSON API: r/SaaS, r/AskTurkey, r/saudiarabia, r/UAE, r/ecommerce, r/shopify; özellikle sanal POS ve Saudi address behavior postları
- GitHub search: `trendyol api`, `hepsiburada api`, `sahibinden scraper`, `trendyol bot`, `iyzico payment`
- GitHub repo detayları: https://github.com/boolxy/trendyol , https://github.com/altuntasmuhammet/trendyol-api-python-sdk , https://github.com/mustafa-m-ugur/hepsiburada-api-php , https://github.com/0Baris/sahibinden-scraper
- ArXiv MCP: `2412.05964`, `2205.04185`, `2503.03512`, `2602.13870`
- MCPTube: `P8e1i-6jk8U`, `k1eXUkSB1RQ`, `-PAdDtLVjAo`; transkript çıkmadı, video başlığı/metadata sinyali olarak kullanıldı
- ProductHunt: Jina ve `chrome-devtools-axi` ile denendi; Cloudflare “Just a moment / Verify you are human” engeline takıldı.

## Özet Bulgular
- Türkiye e-ticaret pazarı artık “küçük lokal niş” değil. Ticaret Bakanlığı 2024 hacmini **3 trilyon TL+**, işlem sayısını **5.91 milyar**, perakende e-ticaret hacmini **1.619 trilyon TL**, e-ticaretin GSYH payını **%6.5**, genel ticaretteki payını **%19.1** olarak verdi. ABD doları bazında hacim 2019'daki **$23.94B** seviyesinden 2024'te **$89.58B** seviyesine çıktı.
- 2024'te Türkiye'de **600,800 işletme** e-ticaret faaliyeti yürüttü. Bu sayı UniverseCreator için tekil satıcıya “entegrasyon yazılımı” değil, satıcı operasyon açığına “agentic ops copilot” satma fırsatı demek.
- Trendyol ve Hepsiburada API tarafı açıkça ürün aktarımı, stok/fiyat güncelleme, sipariş, fatura, müşteri soruları gibi operasyonları destekliyor. Yani teknik giriş noktası var; asıl problem connector yazmak değil, connector üstünde para kazandıran karar katmanı kurmak.
- Sahibinden tarafında public scraping zayıf fikir. Site Cloudflare ile sıkı korunuyor; resmi API de sadece aktif kurumsal emlak/vasıta mağazaları ve EİDS entegre ilancılık firmaları için veri transferi talebiyle açılıyor. “Sahibinden scraper SaaS” riski yüksek; “yetkili ilan sahibi/kurumsal mağaza için analiz ve veri transferi” daha temiz.
- MENA tarafı da ciddi: EZDubai/Euromonitor 2024 MENA e-ticaret pazarını **$34.5B** ve 2029 projeksiyonunu **$57.8B** olarak veriyor; UAE 2024 **$8.8B** → 2029 **$13.8B**. Penetrasyon hâlâ düşük: rapor MENA e-commerce penetration için 2019 **%2.0**, 2024 **%4.4**, 2029 **%6.6** çiziyor. Düşük penetrasyon kötü değil; iyi lokal ürün için büyüme alanı.
- En güçlü fırsat: **TR/MENA Marketplace Ops Copilot** — satıcıya tek panel daha satmak değil; iade, kargo gecikmesi, müşteri sorusu, stok/fiyat sapması, kâr/zarar kaçağı, e-fatura ve ödeme friction'ını günlük aksiyon listesine çeviren agent sistemi.

## Gerçek Başarı Hikayeleri
- **Pazaryeri Bot vendor sinyali:** Trendyol, Hepsiburada, ÇiçekSepeti ve Pazarama için AI destekli Q&A, iade takip/auto-approval, kargo gecikme alarmı, kâr-zarar analizi ve multi-store management iddia ediyor. Sayfa üzerinde **500+ active sellers**, **2M+ questions answered**, **98% return catch rate**, **40% avg profit increase** ve paket fiyatları **2,499 TL/ay**, **5,999 TL/ay**, **14,999 TL/ay** olarak listelenmiş. Bunlar vendor claim; bağımsız doğrulama değil. Yine de pricing envelope ve feature demand için iyi sinyal.
- **Sopyo kategori doğrulaması:** Sopyo, pazaryeri/e-ticaret/XML/kargo/fulfillment/muhasebe/e-fatura için **50+ entegrasyon**, 7 gün ücretsiz deneme ve satış geliri üzerinden komisyon almama pozisyonu sunuyor. Bu kategori zaten var; demek ki “entegrasyon paneli” commodity. Boşluk, karar/ajan/uyarı/otomasyon katmanı.
- **ikas yerel Shopify alternatifi sinyali:** ikas, Start paketinde Trendyol entegrasyonu; Scale paketinde Trendyol, Hepsiburada, Amazon, ETSY entegrasyonları; Scale Plus'ta 19 yurt içi + 7 yurt dışı pazaryeri entegrasyonu ve WhatsApp sepet hatırlatıcı gibi özellikler anlatıyor. Ayrıca sanal POS kurulumunun paket ücretine dahil olduğunu ve en geç 1 hafta içinde hazır hale geldiğini söylüyor. Türkiye'de “Shopify ama yerel ödeme + yerel pazaryeri” ihtiyacı canlı.
- **GitHub gerçek implementasyonlar:** `boolxy/trendyol` PHP Trendyol API client'ı 36 star ile ürün/order/claim/settlement servislerini kapsıyor. `altuntasmuhammet/trendyol-api-python-sdk` 14 star; README'de product integration tamam, order/common label/return/accounting/Q&A eksik görünüyor. `mustafa-m-ugur/hepsiburada-api-php` 17 star; Hepsiburada listing/product örnekleri var. Bu açık kaynakların star sayısı düşük; lokal pazarda kod var ama güçlü ürünleşmiş open-source ekosistem yok.
- **Sahibinden GitHub sinyali:** `0Baris/sahibinden-scraper` 19 star, 2026-04-12 güncel, Python + nodriver/undetected_chromedriver + SQLite/PostgreSQL ile araç ilanı çekiyor. Bu talep var demek; ama resmi yardım sayfası API'nin yetkili kurumsal akışla sınırlı olduğunu gösterdiği için ticari ürünleştirme scraping üzerinden yapılırsa mayın tarlası.
- **Reddit / AskTurkey ödeme sinyali:** E-ticaret için sanal POS sorusunda kullanıcılar iyzico/PayTR'yi kolay ama pahalı görüyor; yorumlarda iyzico/PayTR için yaklaşık **%3-4**, Shopify ek kart ücretleriyle toplam **%5-6** maliyet konuşuluyor; alternatif olarak daha düşük teklif veren sağlayıcılar anekdot düzeyinde geçiyor. Bu doğrulanmış fiyat listesi değil, community pain: ödeme maliyeti ve entegrasyon sürtünmesi.
- **Reddit / Saudi eCommerce address behavior:** Saudi/UAE'ye satış yapan satıcı, 32 Saudi siparişin 30'unda eksik adres bilgisi aldığını yazdı; yorumlar harita pin / Google Maps location ve yerel kuryenin müşteriyle iletişime geçmesi pattern'ini öneriyor. MENA localization sadece çeviri değil; adres, ödeme, teslimat ve güven sinyali.
- **MCPTube video metadata:** Trendyol entegrasyonu için “Aylık 1000 TL — XML, CSV, Excel, JSON ve API” başlıklı video; pazaryeri XML otomasyonu videosu; Pixa Software'in “Marina Mayo, Sipariş Hazırlama Süresini %120 Hızlandırdı” case başlığı çıktı. Transkript gelmediği için bunlar kanıt değil, kategori/mesajlandırma sinyali.

## Pazar Büyüklüğü & Fırsat
- **Türkiye TAM sinyali:** 2024 **3T+ TL** e-ticaret hacmi, **5.91B** işlem ve **600.8K** aktif e-ticaret işletmesi. En büyük sektör hacimleri: giyim/ayakkabı/aksesuar **301.34B TL**, havayolları **208.9B TL**, seyahat/taşımacılık/depolama **180.23B TL**, elektronik **176.92B TL**.
- **Satıcı sayısı ≠ alıcı sayısı.** 600.8K işletmenin çoğu entegrasyon/SaaS almaz; ama %1 bile 6,008 potansiyel satıcı eder. Ayda 2,000 TL düşük paket varsayımıyla teorik mikro-SAM **12M TL/ay** eder. Bu kaba tahmin; doğrulanmış gelir değil.
- **MENA büyüme sinyali:** EZDubai PDF 2024 MENA pazarını **$34.5B**, 2029'u **$57.8B** gösteriyor; UAE **$8.8B** 2024 ve **$13.8B** 2029. Penetrasyon global ortalamaya göre düşük kaldığı için merchant ops tooling, payment/logistics localization ve Arabic/Turkish customer ops için yer var.
- **Kategori parası nerede:** Trendyol/Hepsiburada satıcısının günlük para sızdırdığı yerler: yanlış stok/fiyat, geç kargo, iade süresi, eksik fatura, müşteri sorularına geç cevap, buybox/fiyat rekabeti, düşük marjlı ürünler, yanlış kampanya, ödeme komisyonu ve kargo/iadeden kayıp.
- **En hızlı wedge:** “Pazaryeri Kâr Kaçağı Raporu” — satıcı CSV/API çıktısını al, 24 saatte kargo gecikme riski, iade riski, cevaplanmamış soru, stok/fiyat anomalisi, düşük marj SKU ve fatura/operasyon darboğazı raporu ver. SaaS yapmadan satılabilir.

## Rakipler & Boşluklar
- **Mevcut rakip sınıfları:** Sopyo/Dopigo/Entegra/PraPazar/ikas/Ticimax gibi entegrasyon veya e-ticaret altyapıları; Pazaryeri Bot gibi AI'lı operasyon katmanı; kargo/muhasebe/e-fatura/ödeme sağlayıcıları; ajanslar; basit XML entegrasyon yazılımları.
- **Boşluk 1 — “connector” değil “decision layer”:** Rakiplerin çoğu mağazaları tek panelde topluyor. Satıcı için asıl değer “Bugün hangi 7 aksiyonu alırsam para kaybetmem?” sorusunun cevabı. Agent burada fark yaratır.
- **Boşluk 2 — Türkçe + Arapça müşteri dili:** ArXiv `2412.05964` Türkçe sentiment tool performansının hedef metnin karakteristiğine çok bağlı olduğunu söylüyor. `2205.04185` Türkçe targeted sentiment için anotasyon verisi ve BERT modelleri öneriyor. `2602.13870` Arabic politeness dataset'i 10,000 örnek, Gulf/Egyptian/Levantine/Maghrebi dialect coverage ve 40 model benchmark içeriyor. TR/MENA müşteri soruları için kültürel/polite cevap gate'i iyi differansiyel.
- **Boşluk 3 — MENA operasyon lokalizasyonu:** KSA adres/harita pin, UAE digital wallet, cashless hedefler, Arapça/İngilizce/Türkçe support, cross-border customs/fatura/kargo akışı. Generic Shopify app bunu lokal çözmüyor.
- **Boşluk 4 — compliance-first outbound:** Türkiye'de ticari elektronik ileti için İYS/onay ve ispat yükümlülüğü var. KVKK kararları çerez/hedefleme/analitik için açık rıza ve aydınlatma sorunlarının cezaya dönebileceğini gösteriyor. “Hadi herkese WhatsApp atalım” aptalca. Opt-in, transactional message, müşteri sorusu cevabı ve satıcı dashboard aksiyonu ayrı tasarlanmalı.
- **Boşluk 5 — Sahibinden veri ürünleri:** Public scraping yerine kurumsal mağaza yetkili veri transferi veya kullanıcıya ait ilan portföyü analizi. Araba/emlak ilan fiyat takip piyasası cazip ama resmi yetki olmadan ticari scraping kırılgan.

## Teknik Gereksinimler
- **Kaynak veri:** Trendyol API, Hepsiburada API, satıcı panel export CSV/XLS, kargo entegrasyonları, e-fatura/e-arşiv çıktıları, ödeme provider raporları, müşteri soru/iade verisi.
- **Connector katmanı:**
  - Trendyol: product transfer, stock/price update, order/shipment, claims/returns, settlement, Q&A.
  - Hepsiburada: product/listing, stock/price/shipping time, order, invoice URL, cargo barcode/status.
  - Sahibinden: sadece yetkili kurumsal/API akış; scraping fallback ticari ürünün omurgası olmamalı.
- **Agent katmanı:**
  1. Inventory Diff Agent — stok/fiyat sapması ve stale listing bulur.
  2. Order Risk Agent — kargoya verme deadline, gecikme ve iptal riski çıkarır.
  3. Return/Claim Agent — iade süresi, auto-approval riski, kayıp sebebi ve ürün bazlı alarm üretir.
  4. Customer Q&A Agent — Türkçe/İngilizce/Arapça taslak cevap üretir; high-risk cevapları human gate'e yollar.
  5. Margin Agent — satış fiyatı, komisyon, kargo, iade, ödeme kesintisi ve kampanya etkisiyle net kâr tahmini yapar.
  6. Compliance Agent — İYS/KVKK, pazaryeri ToS, scraping/authorized API, müşteri verisi ve mesaj türü kontrolü yapar.
  7. Report Agent — günlük aksiyon listesi + haftalık kâr kaçağı raporu üretir.
- **MCP/Araç:** Jina Reader, Reddit JSON, GitHub, ArXiv, MCPTube, chrome-devtools-axi / Playwright for portal QA; browser automation yalnızca izinli panel ve kullanıcı hesabı üzerinde.
- **İnsan müdahalesi:** İlk müşteri kurulumunda API credential / export; ilk 2 hafta Q&A ve iade kararlarında human approve; fiyat değiştirme / iade onayı / mesaj gönderme gibi para-hukuk etkili adımlarda onay.
- **Maliyet:** İlk POC sıfıra yakın: satıcı export + LLM + Google Sheets/CSV yeterli. Entegrasyon sonrası hosting $0-20/ay, LLM $10-50/ay pilot, ödeme komisyonu sağlayıcıya göre değişir. En büyük maliyet müşteri edinme ve destek.

## Ham Notlar
- `projeler.txt` taramasında doğrudan Trendyol/Hepsiburada/Sahibinden sinyali neredeyse yok; tek anlamlı link Framer marketplace template çıktı. Bu konu UniverseCreator mevcut proje kataloğunda boşluk olarak duruyor.
- `ddgr` dört geniş sorguda anlamlı JSON sonuç döndürmedi. Sonuçsuz kalınca web search, Jina, Reddit JSON, GitHub, ArXiv, MCPTube ve chrome-devtools-axi kullanıldı.
- ProductHunt hem Jina hem Chrome tarafında Cloudflare verification'a takıldı; snapshot “Verify you are human” ekranını gösterdi. Bu yüzden ProductHunt bu turda kaynak olarak kullanılamadı.
- `sistem-planlama/sentez14.md` zaten bu konuyu “net ve ayrı tur olarak eksik” diye işaretlemişti. #18 bu açığı kapatıyor.
- `STATE_SUMMARY.json` ve `STATE.json` minimal okuma: cycle 1025, **113 active / 113 healthy / balance 0.0**. Bu konu kısa vadede para harcamadan rapor-first/manuel delivery ile denenmeli; ödeme altyapısı hâlâ hassas.
- Rekabet Kurumu sonuçlarında Trendyol/Hepsiburada otomatik fiyatlandırma ve buybox taahhütleri gibi regülasyon sinyalleri var. Repricing agent kurulacaksa “rakip verisiyle fiyat sabitleme/collusion” tarafına yaklaşmamak şart.
- Turkish/MENA için “AI müşteri cevabı” model kalitesi sadece dil çevirisiyle çözülmez; Türkçe agglutinative yapı, hedef/aspect sentiment, Arapça lehçeler ve nezaket/kültürel ton ayrı QA ister.
