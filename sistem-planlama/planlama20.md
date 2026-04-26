# Planlama #20 — E-commerce Automation Uygulama Haritası
**Tarih:** 2026-04-21 16:15 +03
**Bağlı Araştırma:** arastirma20.md

## Swarm Agent ile Nasıl Uygulanır?
Bu konuya “e-commerce automation agency” diye girmek zayıf kalır. Doğru çerçeve: **Seller Margin Guardrail OS**. Native tool'lar basit işi zaten yapıyor; bizim katmanımız cross-channel risk, approval ve görünür ROI.

1. **Seller Scanner Agent**
   - Shopify / Amazon / Etsy seller'ını inceler.
   - App-sprawl, stockout riski, aged inventory, pricing körlüğü, listing riskleri ve review yoğunluğunu puanlar.
2. **App-Sprawl Auditor**
   - Özellikle Shopify tarafında “hangi işleri native Flow çözer, hangi app gereksiz, hangi iş custom connector ister” ayrımını yapar.
3. **Margin Guardrail Agent**
   - Amazon/Walmart/eBay tarafında supplier cost, shipping, referral fee ve aged inventory değişimine göre min/max price guardrail kurar.
   - Price war için otomasyon, liquidation için insan kapısı açar.
4. **Listing Safety Agent**
   - Etsy/Shopify ürün içeriğini draft üretir, title/tag/alt-text önerir.
   - Ama publish etmez; policy/IP riskini insana bırakır.
5. **Review Intelligence Agent**
   - Amazon/Etsy/Shopify yorumlarını cluster'lar.
   - “ürün bozuluyor”, “fiyat yüksek”, “kargo geç”, “paketleme kötü” gibi temaları haftalık çıkarır.
6. **Forecast & Restock Agent**
   - Event-aware yaklaşım ile kampanya/holiday etkisini hesaba katar.
   - Low-stock alert + reorder suggestion üretir.
7. **Weekly Ops Reporter**
   - Saat tasarrufu, tool tasarrufu, stockout önleme, aged inventory recovery, review trendleri ve manuel müdahale sayısını raporlar.
8. **Human Approval Gate**
   - Liquidation, publish, aggressive repricing, IP/trademark riskli title/tag ve kritik kanal kararları burada insan onayından geçer.

## Gerekli Bileşenler
- **Script/Bot:**
  - seller ops audit generator
  - app-sprawl / tool spend analyzer
  - margin floor calculator
  - low-stock / aged inventory alert engine
  - review cluster summarizer
  - draft listing builder
  - human approval queue tracker
  - weekly ROI report generator
- **MCP/Araç:**
  - `chrome-devtools-axi` / Playwright / browser gözlem araçları: mağaza akışı, app-sprawl ve public funnel incelemesi
  - GitHub / `gh`: connector ve starter repo araştırması
  - ArXiv MCP: forecasting / pricing / opinion summarization validasyonu
  - MCPTube: gerçek operasyon videolarından feature ve workflow extraction
  - Jina Reader: pricing/docs/case study okuma
- **API:**
  - Shopify app stack: OAuth, Admin API, webhooks, gerekirse Flow
  - Amazon SP-API / seller reports / pricing feeds
  - Etsy Open API ve gerektiğinde kontrollü scraping
  - Ops backbone için Redis / queue / audit log
  - OpenAI / uygun LLM sağlayıcısı
  - Slack / email / Sheets / webhook sink'leri
- **İnsan Müdahalesi:**
  - pricing floor / liquidation kararı
  - publish öncesi listing QA
  - trademark/IP/policy kontrolü
  - seller credential onayı
  - high-risk marketplace exception'ları

## Workflow Haritası
Tetikleyici: yeni seller / yeni audit talebi
→ mağaza ve kanal taraması
→ problem sınıflandırma (Shopify sprawl / Amazon margin risk / Etsy listing risk / cross-channel stock)
→ ROI ve risk skoru çıkarma
→ ilk use case seçimi
→ connector planı + veri modeli
→ shadow mode / dry run
→ insan onayı
→ rollout
→ haftalık ops raporu
→ ikinci otomasyon / upsell

Alt akışlar:
- **Shopify lane:** app-sprawl → Flow/native çözüm → eksik olan dış connector → tool azaltma raporu
- **Amazon lane:** supplier cost + aged inventory → repricing guardrail → exception queue → manual override
- **Etsy lane:** listing draft → policy/IP check → human approve → publish
- **Cross-channel lane:** order event → stock decrement → multichannel sync → low-stock / reorder signal

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **Hemen yapılabilir en mantıklı iş:** tam ürün değil, **Seller Ops Audit Pack**.
  - 1 Shopify mağaza için app-sprawl + native Flow fırsatı
  - 1 Amazon seller için repricing / aged inventory guardrail audit'i
  - 1 Etsy mağaza için listing draft / policy risk audit'i
- **En düşük çaba / en yüksek çıktı adımı:** 10-15 örnek mağaza/seller üstünde standart audit scorecard üretmek.
  - Skorlar: app-sprawl, price-war riski, stockout riski, listing/policy riski.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - mevcut araştırma stack'i: browser gözlem, GitHub kaynak tarama, Jina okuma, MCPTube, ArXiv
  - mevcut dağıtım yüzeyi: ileride audit/report landing sayfası için 113 ürün portföyünden türetilecek Vercel yüzeyleri
- **Proof-of-concept için minimum gereksinimler:**
  - 1 audit şablonu
  - 1 fiyat benchmark tablosu
  - 1 ROI modeli
  - 1 Amazon repricing playbook
  - 1 Shopify Flow consolidation playbook
  - 1 Etsy draft-review playbook
- **Tahmini kurulum süresi:** 4-7 gün.
- **İlk gelir beklentisi:**
  - paid audit: **$250-$750**
  - ilk managed pilot/setup: **$500-$1,500**
  - aylık izleme/raporlama: **$100-$500/mo**
- **Kısa vade kararı:** önce “build” değil “audit + guardrail planı” sat. Merchant'a önce güven ver, sonra connector aç.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay hedef görüntü:**
  - 20-30 seller audit'i tamamlanmış
  - 3-5 discovery call
  - 1-2 paid pilot
  - tek bir ortak veri modeli netleşmiş
  - haftalık rapor formatı ve approval queue tasarımı bitmiş
- **Başarı metrikleri:**
  - mağaza başına azaltılan tool sayısı
  - düşen aylık tool spend
  - price-floor violation sayısı
  - stockout / oversell uyarı doğruluğu
  - aged inventory recovery oranı
  - review cluster'dan çıkan aksiyon sayısı
  - pilot gross margin ve support yükü
- **Paralel çalışabilecek adımlar:**
  - researcher: seller / rakip / pricing araştırması
  - analyst: ROI ve price benchmark modeli
  - builder: dashboard / approval queue taslağı
  - qa: policy ve edge-case checklist
  - reporter: weekly ops report şablonu
- **Ölçeklendirme için gerekenler:**
  - secrets/credential vault
  - queue + retry sistemi
  - audit log
  - per-channel rate limit koruması
  - human approval UI veya en azından net queue çıktısı
  - usage cost monitor
- **Checkpoint'ler:**
  - Hafta 2: audit paketi ve puan kartı hazır
  - Hafta 4: ilk 3-5 görüşme
  - Hafta 6-8: 1 pilot canlı veya pivot kararı
  - Hafta 12: tekrar eden playbook + haftalık rapor standardı

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** sistem, “workflow kuran biri” olmaktan çıkıp **cross-channel seller control plane** olur. Tek yerde stock, margin risk, listing draft, review insight, aged inventory ve approval queue görünür.
- **Yan ürünler / yeni gelir kolları:**
  - paid seller audit raporları
  - weekly monitoring subscription
  - review intelligence API
  - inventory / aged stock alert SaaS'i
  - agency/aggregator white-label dashboard
  - managed marketplace ops retainers
- **Rakiplerin yapamadığı, swarm yaklaşımımızla yapılabilecek şey:**
  - çok kaynaklı seller insight'ı hızlı sentezlemek
  - her mağaza için risk/ROI raporunu haftalık üretmek
  - channel-specific edge-case'leri hafızada tutup tekrar hata yapmamak
  - research + audit + policy + reporting'i paralel ucuzlatmak
- **White-label veya SaaS olarak satılabilir mi?**
  - Evet. Ama önce managed-service ve audit ürünüyle desen doğrulanmalı. Erken SaaS hevesi yine duvara toslayabilir.
- **12 ay hedefi:**
  - 5-10 aktif seller veya 2 agency/aggregator partner
  - 1 ortak approval/reporting katmanı
  - 2 güçlü lane (ör. Amazon guardrails + Shopify sprawl cleanup)
  - **$5K-$20K MRR** bandı gerçekçi; üstü ancak güçlü dağıtım ve case study ile gelir.

## Öncelik & Çaba Tahmini
- **Öncelik:** Orta-Yüksek. Pazar güçlü, fiyat benchmark'ı net, community acısı gerçek. Ama mevcut UniverseCreator portföyü e-commerce-native değil; bu lane bilinçli odak ister.
- **Kurulum Süresi:**
  - audit paketi: 1 hafta
  - ilk pilot: 2-6 hafta
  - reusable control plane: 1-3 ay
  - white-label / SaaS dönüşümü: 3-12 ay
- **Aylık İşletme Maliyeti:**
  - lean audit/research: **$50-$150/ay**
  - connector + queue + LLM pilotu: **$150-$600/ay**
  - daha ciddi managed operasyon: **$500-$1,500+/ay**
- **Potansiyel Gelir:**
  - paid audit: **$250-$750**
  - pilot/setup: **$500-$1,500**
  - aylık izleme/guardrail: **$100-$500/mo**
  - 5 müşteriyle anlamlı bant: **$2K-$5K MRR**
- **ROI Beklentisi:** 1-2 paid audit ile araştırma maliyeti çıkar; ilk düzgün pilot tüm stack'i öder. Ama yanlış pricing/publish otomasyonu tek hatada kârı siler; ROI'yi guardrail belirler.

## Mevcut Sistemle Entegrasyon
- UniverseCreator şu an **113 active / 99 live / 107 healthy** durumda. Güçlü olduğu yer: araştırma, browser gözlemi, çoklu kaynak sentezi, raporlama ve deployment yüzeyi.
- Zayıf olduğu yer: seller connector'ları ve operasyonel domain bilgisi. Yani bu konu **mevcut tool portföyüne zorla gömülmemeli**; önce audit/offer olarak denenmeli.
- Mevcut Vercel yüzeyi ileride audit viewer, ROI report demo veya prospect landing için kullanılabilir. Ama şu aşamada deploy gerekmez.
- `projeler.txt` tarafında e-commerce odaklı local asset az; bu da ilk sprint'in “mevcut asset reuse” değil, **yeni lane doğrulaması** olması gerektiğini söylüyor.
- Swarm rol eşlemesi net:
  - researcher → seller pain / rakip / fiyat araştırması
  - analyst → ROI / risk / price benchmark
  - builder → ileride dashboard / report yüzeyi
  - qa → policy / edge-case / approval checklist
  - reporter → weekly ops summary

## Riskler & Dikkat Edilecekler
- **Marketplace ToS / policy riski:** scraping, messaging, pricing ve listing automation yanlış yapılırsa seller hesabı yanabilir.
- **Repricing deliliği:** volume kovalamak uğruna marjı gömmek çok kolay.
- **AI content riski:** Etsy örneğinde görüldüğü gibi yanlış title/tag önerisi policy violation doğurabilir.
- **Vendor lock-in:** Shopify/Amazon/Etsy/Veeqo değişiklikleri connector maliyetini artırır.
- **Support cehennemi:** küçük merchant + yüksek custom iş + düşük fiyat = kötü kombinasyon.
- **Credential güvenliği:** seller API token'ları, OAuth yetkileri ve webhook secret'ları ciddi operasyon yüküdür.
- **Yanlış wedge:** “Bir app daha” diye satış yapmak aptalca olur; wedge “sprawl azalt, risk düşür, kontrol ver” olmalı.

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Tek offer'ı kilitle:** `Seller Ops Audit Pack` veya `Seller Margin Guardrail Audit` ismini seç; app-sprawl + pricing + stock + listing risk puan kartını tek formatta topla.
2. **10-15 mağaza/seller üstünde kuru koşu yap:** Shopify, Amazon, Etsy karışık örnekler seç; aynı audit'i uygulayıp hangi lane'in en hızlı ROI verdiğini gör.
3. **İlk paid pilot lane'ini seç:** ya `Amazon Margin Guardrails` ya da `Shopify App-Sprawl Cleanup`. İkisini birden ilk sprintte kovalamak dağınıklık olur.
