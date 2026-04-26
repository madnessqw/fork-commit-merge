# Agent payments / AI commerce araştırması — 2026-04-19

## Kısa hüküm
AgentCard, Visa/Mastercard Agent Pay, Google AP2, Stripe Projects ve OpenAI/Stripe ACP aynı başlık altında dönüyor ama aynı şey değiller. ProfitBridge için bugün para almak istiyorsak gerçek yol hâlâ merchant/payment provider onayıdır: iyzico Link veya LemonSqueezy. AgentCard ve Stripe Projects müşteri ödemesini Enpara'ya çekme kestirmesi değil.

## ProfitBridge bağlamı
- ProfitBridge fiziksel ürün, navlun, gümrük veya üçüncü taraf tahsilatı satmıyor.
- Satılan şey HS-code/GTİP bazlı dijital trade intelligence raporu.
- LemonSqueezy: store/test ürünleri var ama identity verification rejected; support cevabı bekleniyor.
- iyzico: bireysel Link yolu deneniyor; IBAN sorunu aşılmış; iş modeli açıklama maili gerekli.

## İncelenen sistemler

### 1) AgentCard — agent'a sanal kart verme
Kaynaklar:
- https://www.agentcard.sh/
- https://docs.agentcard.sh/introduction
- https://www.agentcard.sh/terms
- https://www.agentcard.sh/about

Bulgular:
- AI agent'ların web üzerinde alışveriş yapabilmesi için tek kullanımlık/prepaid sanal kartlar veriyor.
- CLI, MCP ve Chrome extension akışı var.
- Kartlar cardholder/payment method üzerinden fonlanıyor; Stripe Checkout ile payment method bağlanıyor.
- Human-in-the-loop onay ve limit mantığı var.
- Site bazı yerlerde Visa, bazı yerlerde Mastercard diyor; erken ürün ve messaging tutarsızlığı var.

ProfitBridge açısından sonuç:
- Bu ürün satıcı hesabı değil. Sen müşteri ödemesi almak için AgentCard'dan Enpara'ya payout alamazsın.
- AgentCard ancak senin/müşterinin agent'ının online harcama yapması için kullanılır. Müşteri bu kartla ödeme yaparsa senin hâlâ iyzico/Lemon/başka checkout'a ihtiyacın var.

### 2) X linki — RoundtableSpace / AgentCard duyurusu
Kaynak:
- https://x.com/RoundtableSpace/status/2030678680431628601
- Orijinal medya/tweet bağlamı: https://x.com/keyserfaty/status/2030451548841758910

Bulgular:
- Duyuru AgentCard çevresindeki “Claude agent tek kullanımlık Visa kart oluşturabiliyor” iddiasına dayanıyor.
- Bu alıcı/agent harcama ürünü; satıcı payout ürünü değil.

### 3) Stripe Projects — agent/developer servis provisioning
Kaynaklar:
- https://projects.dev/
- https://docs.stripe.com/projects

Bulgular:
- Stripe Projects, agent veya developer'ın Vercel/Supabase/Clerk/PostHog/OpenRouter gibi servisleri CLI ile provision etmesi, credentials yönetmesi ve usage/billing akışını yönetmesi için.
- Developer Preview.
- Provider upgrade ödeme handoff'u Stripe Shared Payment Token ile yapılıyor; docs'a göre developer preview payment handoff sadece US/EU/UK/Canada tarafında.

ProfitBridge açısından sonuç:
- Stripe Projects müşteri checkout'u ya da merchant payout ürünü değil.
- Enpara'ya satış geliri çekme yolu sağlamaz.

### 4) OpenAI + Stripe ACP / ChatGPT Instant Checkout
Kaynaklar:
- https://openai.com/index/buy-it-in-chatgpt/
- https://stripe.com/newsroom/news/stripe-openai-instant-checkout
- https://docs.stripe.com/agentic-commerce
- https://docs.stripe.com/agentic-commerce/protocol
- https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens

Bulgular:
- ChatGPT içinde Instant Checkout, Agentic Commerce Protocol ile başladı.
- İlk kapsam US ChatGPT kullanıcıları + US Etsy; Shopify merchant genişlemesi duyuruldu.
- Merchant ödeme/fulfillment/customer relationship kontrolünü koruyor.
- Stripe kullanan seller için kolay; başka provider kullananlar SPT veya delegated payments spec ile teorik olarak katılabilir.

ProfitBridge açısından sonuç:
- Gelecek için önemli ama bugünkü Enpara çözümü değil.
- Türkiye'den bireysel ProfitBridge için önce merchant/payment provider onayı gerekir.

### 5) Google AP2
Kaynak:
- https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
- https://github.com/google-agentic-commerce/AP2

Bulgular:
- AP2 ödeme yönteminden bağımsız agent-payment protokolü: kart, stablecoin, gerçek zamanlı banka transferi gibi yöntemleri desteklemeyi hedefliyor.
- Mandates + verifiable credentials ile user intent/authorization/audit trail kuruyor.
- 60+ partner: Adyen, AmEx, Ant, Coinbase, Mastercard, PayPal, Revolut, Salesforce, Worldpay vb.

ProfitBridge açısından sonuç:
- Protokol/standart, ödeme hesabı değil.
- Tek başına Enpara payout sağlamaz.

### 6) Mastercard Agent Pay
Kaynaklar:
- https://www.mastercard.com/news/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai
- https://investor.mastercard.com/investor-news/investor-news-details/2025/Mastercard-Unveils-New-Tools-and-Collaborations-to-Power-Smarter-Safer-Agentic-Commerce/default.aspx

Bulgular:
- Mastercard Agent Pay, agentic tokens ve mevcut tokenization altyapısı üzerine kurulu.
- Trusted/registered agents, consumer controls, issuer/merchant visibility, fraud/dispute desteği hedefleniyor.
- Microsoft, IBM, Braintree, Checkout.com gibi partnerler var.
- Mastercard Agent Toolkit / MCP developer erişimi duyurulmuş.

ProfitBridge açısından sonuç:
- Ağ/standart katmanı. Direkt “hesap aç, satış al, Enpara'ya çek” ürünü değil.

### 7) Visa Intelligent Commerce / Trusted Agent Protocol
Kaynaklar:
- https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html
- https://corporate.visa.com/en/products/intelligent-commerce.html
- https://corporate.visa.com/en/sites/visa-perspectives/innovation/visa-mcp-server-agent-acceptance-toolkit.html
- https://developer.visa.com/use-cases/visa-intelligent-commerce-for-agents

Bulgular:
- Visa Trusted Agent Protocol, Cloudflare ile geliştirilen agent identity/commerce intent framework'ü.
- Visa Intelligent Commerce tokenized credentials, passkeys, controls ve commerce signals etrafında.
- Visa MCP Server ve Acceptance Agent Toolkit pilot durumda.
- Visa developer sayfası ürünün geliştirme/deployment sürecinde olduğunu ve her pazarda olmayabileceğini söylüyor.

ProfitBridge açısından sonuç:
- Partner/developer/pilot seviyesinde network altyapısı. Direkt bireysel satış-payout ürünü değil.

## Enpara'ya çekim cevabı

### Evet, şu şartla
- iyzico bireysel Link onaylanırsa ve Enpara IBAN senin adına doğrulanırsa, ödeme banka hesabına aktarılabilir.
- iyzico resmi sayfası bireysel şirket sahibi olmayan kişilerin kendi adına ödeme alabileceğini ve kullanılabilecek ürünün Link Yöntemi olduğunu söylüyor.
- iyzico payout tarafında ödemelerin muhasebeleşme + blokaj sonrası banka hesabına aktarılacağını söylüyor.

Kaynaklar:
- https://www.iyzico.com/isim-icin/hesap-olustur
- https://www.iyzico.com/destek/yardim-merkezi/urunler-ve-ozellikler/link-ile-odeme-al

### LemonSqueezy için teorik evet, pratik şu an hayır
- LemonSqueezy bank/PayPal payout destekliyor, $50 minimum payout ve ayda iki payout döngüsü var.
- Ama mevcut durumda identity rejected olduğu için canlı satış ve payout mümkün değil.

Kaynaklar:
- https://docs.lemonsqueezy.com/help/getting-started/getting-paid
- https://docs.lemonsqueezy.com/help/getting-started/activate-your-store
- https://docs.lemonsqueezy.com/help/getting-started/verify-your-identity

### Stripe direct için hayır
- Stripe global availability listesinde Türkiye yok.
- Stripe Atlas ile US şirket + US bank hesabı kurulabilir ama bu Enpara'ya direkt payout değil; ayrı şirket, vergi, muhasebe ve transfer meselesi.

Kaynak:
- https://stripe.com/global

## Tavsiye edilen rota
1. iyzico iş modeli açıklama mailini hemen gönder.
2. ProfitBridge checkout'u önce iyzico Link / ödeme linki ile çalıştır.
3. AgentCard/Stripe Projects'e ödeme alma çözümü diye zaman harcama.
4. LemonSqueezy destek dönerse identity akışını tekrar açtır; ürün açıklamasını “digital report / downloadable/generated report” ekseninde keskinleştir.
5. ACP/AP2/Visa/Mastercard tarafını izleme listesine al; bugünkü production ödeme omurgası değil.
6. AI model üstünden satış istiyorsan ilk sürüm: agent kullanıcıdan HS code + paket + email alır, iyzico ödeme linkini verir, ödeme sonrası rapor teslim edilir. Teknik olarak sıkıcı ama para alır. Fancy protokol beklemek şu an dumb bekleyiş olur.
