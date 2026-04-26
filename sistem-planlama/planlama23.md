# Planlama #23 — Browser Agent + Otomasyon Uygulama Haritası
**Tarih:** 2026-04-21 17:51 +03
**Bağlı Araştırma:** arastirma23.md

## Swarm Agent ile Nasıl Uygulanır?
Yanlış hamle: “Biz de genel amaçlı browser agent platformu kuralım.” Bu şu aşamada gereksiz ego projesi.

Doğru hamle:

**Browser Ops Layer**
- **Scout:** Bilinmeyen sitede akışı keşfeder.
- **Compile:** Başarılı akışı repeatable workflow'a çevirir.
- **Operate:** Bu workflow'u planlı, izlenebilir ve düşük maliyetli şekilde tekrar koşturur.
- **Verify:** Çıktının doğru olduğunu ve yanlış yere tıklanmadığını doğrular.
- **Human Gate:** Login, CAPTCHA, ödeme, son submit gibi riskli anlarda kontrolü alır.

Önerilen swarm rol dağılımı:
1. **Scout Agent**
   - Browser Use / Skyvern / mevcut MCP browser araçlarıyla siteyi keşfeder.
   - Hangi sayfada ne kırılıyor, login/CAPTCHA nerede, hangi veri lazım çıkarır.
2. **Flow Compiler**
   - Başarılı trajectory'yi Stagehand / Playwright / agent-browser benzeri deterministik akışa çevirir.
   - Input schema + output schema + error branch'leri tanımlar.
3. **Runner Agent**
   - Batch veya schedule ile akışı çalıştırır.
   - Queue, timeout, retry ve session reuse burada.
4. **Verifier Agent**
   - Beklenen veri çıktı mı?
   - Yanlış form submit edildi mi?
   - Sayfa sapması var mı?
   - Screenshot / DOM / response farkı var mı?
5. **Human Operator**
   - İlk login
   - 2FA/CAPTCHA
   - Son onay
   - Riskli sapma kararı

Kritik prensip:
**Exploratory agent keşif için; deterministic workflow operasyon için.**
Aynı pahalı agent'ı sonsuza kadar gecelik batch'e salmak kötü fikir.

## Gerekli Bileşenler
- **Script/Bot:**
  - workflow card şablonu
  - site profile registry
  - secret / credential mapping katmanı
  - run queue + scheduler
  - retry / timeout / checkpoint yöneticisi
  - screenshot + structured output saklama
  - verifier rubric runner
  - günlük browser ops raporu
- **MCP/Araç:**
  - `chrome-devtools-axi` (lokalde hızlı gözlem ve kontrol)
  - Playwright MCP
  - Chrome DevTools MCP
  - `windows-mcp` fallback
  - Browser Use
  - Browserbase + Stagehand
  - Skyvern
  - `agent-browser` CLI
- **API:**
  - LLM sağlayıcısı (OpenAI / Anthropic / Gemini; seçilecek)
  - Browserbase veya Skyvern ya da Browser Use Cloud (tek lane'e göre)
  - Proxy / CAPTCHA çözüm hizmeti (gereken sitelerde)
- **İnsan Müdahalesi:**
  - login / 2FA
  - ödeme / satın alma
  - hassas veri girişi
  - son submit
  - sapmalı run incelemesi

## Workflow Haritası
Tetikleyici
→ iş talebi gelir (`QA smoke`, `price extract`, `portal form fill`, `document download`)
→ workflow card açılır
→ Scout Agent siteyi keşfeder
→ gerekiyorsa insan login/CAPTCHA kapısı açılır
→ başarılı yol kaydedilir
→ Flow Compiler bunu deterministik akışa çevirir
→ Verifier örnek run ile doğrular
→ Runner schedule/batch ile tekrar çalıştırır
→ maliyet/süre/hata metriği kaydedilir
→ sapma varsa retry veya yeniden scout
→ çıktı JSON/CSV/screenshot/report olarak teslim edilir

Önerilen ilk 3 lane:
- **Lane 1 — İç QA:** canlı ürünlerde smoke/check-out/form akışı testleri
- **Lane 2 — Rekabet/istihbarat:** rakip pricing/features/veri çekme
- **Lane 3 — Portal ops:** login gerektiren panel/kurum/CRM/form işlerinin otomasyonu

## ⏱️ Kısa Vade (1-2 hafta içinde yapılabilir)
**Soru: Bu araştırmadan ne 1-2 haftada hayata geçirilebilir?**

- **En düşük çaba / en yüksek çıktı adımı:** iç tarafta **browser smoke test + screenshot doğrulama lane'i** kurmak. Çünkü mevcut browser araçları zaten hazır; eksik olan sadece workflow card + verify standardı.
- **Dış gelir için en mantıklı ilk pilot:** login gerektiren tek bir portal veya panelde **veri çekme / form doldurma / belge indirme** işi. “Boring browser ops” satmak, genel agent satmaktan daha gerçekçi.
- **Hangi mevcut araç/script bu işi kısmen yapar?**
  - `chrome-devtools-axi`
  - Playwright MCP
  - Chrome DevTools MCP
  - `windows-mcp`
  - mevcut file-first log/memory disiplini
- **Proof-of-concept için minimum gereksinimler neler?**
  - 3 workflow card: `smoke test`, `price extract`, `portal form fill`
  - 1 secret handling kuralı
  - 1 verifier checklist'i
  - 1 run report formatı
  - 1 insan kapısı protokolü
- **Tahmini kurulum süresi ve ilk gelir beklentisi?**
  - iç pilot: **3-5 gün**
  - 3 akışlık mini sistem: **7-10 gün**
  - ilk dış pilot gelir beklentisi: **$500-$1,500 setup + $300-$800/ay** managed run (**tahmin**)
- **Kısa vade net karar:** önce iç QA ve tek portal pilotu. Üç vendor'ı birden kurup panayır yapmak gereksiz.

## 📆 Orta Vade (1-3 ay içinde)
**Soru: 1. ay sonunda sistem nasıl görünmeli?**

- **1. ay sonunda hedef görünüm:**
  - 5-10 workflow card hazır
  - en az 2 lane prod-benzeri çalışıyor
  - her run için screenshot/log/structured output tutuluyor
  - login/CAPTCHA kapıları net
  - başarısız run'lar yeniden scout kuyruğuna düşüyor
- **2-3 ay sonunda olgun görünüm:**
  - keşif → derleme → operasyon akışı standart hale gelir
  - belirli siteler için reusable site profile kütüphanesi oluşur
  - iç QA, fiyat izleme ve portal ops aynı çekirdeği paylaşır
  - maliyet dashboard'u çıkar
  - vendor bağımlılığı role göre ayrılır
- **Hangi metric'ler başarıyı gösterir?**
  - successful run rate
  - cost per successful run
  - human handoff rate
  - retry / reroute rate
  - average time per completed workflow
  - extracted/submitted item count
  - false action / false submit count
  - verification pass rate
- **Hangi adımlar paralel çalışabilir?**
  - workflow card standardı
  - site profile registry
  - verifier rubricleri
  - session/secrets katmanı
  - ilk lane'lerin hazırlanması
- **Ölçeklendirme için ne gerekiyor (insan, araç, bütçe)?**
  - 1 operatör sahibi
  - 1 teknik derleyici/otomasyon sahibi
  - pilot bütçe: **$30-$150/ay** (tek vendor + düşük hacim)
  - üretimleşme: **$200-$1,000+/ay** (proxy, captcha, browser hour, LLM, gözlemleme) (**tahmin**)
- **Checkpoint'ler ve başarı kriterleri?**
  1. Hafta: 3 workflow card + verify checklist
  2. Hafta: ilk iç smoke lane canlı
  4. Hafta: ilk dış portal pilotu
  8-12. Hafta: 5-10 template workflow + maliyet raporu + site profile kütüphanesi

## 🚀 Uzun Vade (3-12 ay) ve Evrim
**Soru: Bu sistem nasıl evrilebilir / büyüyebilir?**

- **En iyi senaryo:** UniverseCreator kendi browser ops control plane'ine sahip olur. Bilinmeyen siteye önce scout gider, sonra akış compile edilir, sonra schedule ile çalışır. İnsan yalnızca riskli noktalarda devreye girer.
- **Hangi yan ürünler / yeni gelir kolları ortaya çıkabilir?**
  - managed browser QA service
  - website-to-API / portal-to-CSV service
  - TR/MENA portal automation package
  - workflow template marketplace
  - white-label browser ops dashboard
- **Rakiplerin yapamadığı, bizim swarm yaklaşımımızla yapılabilecek nedir?**
  - keşif ve operasyonu ayrı lane'lere bölmek
  - agent + deterministic workflow hibriti
  - vendor-agnostic çalışma (siteye göre Browser Use / Stagehand / Skyvern / MCP seçmek)
  - file-first hafıza ve raporlamayla her run'dan ders çıkarmak
- **White-label veya SaaS olarak satılabilir mi?**
  - **Evet**, ama ancak template'lenmiş akışlarda başarı oranı istikrarlıysa.
  - İlk faz: hizmet olarak kurulum + managed run
  - İkinci faz: tekrarlayan dikeyler için paket
  - Üçüncü faz: dashboard + template + verifier ürünleşmesi
- **Uzun vade evrim sırası:**
  1. iç akışları stabilize et
  2. tekrarlayan site profillerini çıkar
  3. dış müşteri pilotlarını kapat
  4. aynı işi tekrar tekrar yaptığın yerde template çıkar
  5. sonra ancak ürünleşmeyi düşün

## Öncelik & Çaba Tahmini
- **Öncelik:** Yüksek
- **Kurulum Süresi:** ilk pilot için **1 hafta**, 3 lane'li olgun sürüm için **1-3 ay**
- **Aylık İşletme Maliyeti:** pilotta **$30-$150**, üretim hacminde **$200-$1,000+** (**tahmin**)
- **Potansiyel Gelir:** tek workflow setup için **$500-$1,500**, düzenli managed automation için **$300-$800/ay / müşteri**; daha karmaşık kurumsal işlerde üstü mümkün (**tahmin**)
- **ROI Beklentisi:** iç tarafta zaman tasarrufu **1-3 hafta** içinde görünür; dış gelirde **1-2 pilot müşteri** ile break-even mümkün (**tahmin**)

## Mevcut Sistemle Entegrasyon
- Mevcut browser operasyon talimatları zaten doğru yönde: önce `chrome-devtools-axi`, sonra Playwright MCP, sonra Chrome DevTools MCP, en son `windows-mcp`. Yani entegrasyon için yeni davranış icat etmeye gerek yok.
- Araştırma/planning agent'ları scout lane'de kullanılabilir; QA/test tarafı operate lane'e geçebilir.
- Canlı ürün smoke test'leri, checkout doğrulamaları, support panel işleri ve rakip veri toplama bu katmana doğal oturur.
- File-first hafıza, günlük log ve artifact saklama disiplinin olduğu için run raporlarını sistem hafızasına bağlamak kolay.
- Kritik nokta: browser ops katmanı çekirdek sisteme yapışmalı ama onu ele geçirmemeli. Her işi browser agent'a çevirmek saçma.

## Riskler & Dikkat Edilecekler
- vendor benchmark'larını körü körüne gerçek sanmak
- her işi exploratory agent ile sonsuza kadar koşturmak
- gizli maliyetleri (proxy, captcha, session hour, token) takip etmemek
- login ve hassas veriyi ajana gereksiz yere açmak
- uzun session stabilitesini küçümsemek
- anti-bot savaşını hafife almak
- verifier koymadan submit yapan akış çıkarmak
- dikey paket yerine genel “AI browser platformu” hayaline saplanmak

## Önce Yapılacak 3 Adım (Bu Hafta)
1. **Üç workflow card yaz:** `smoke test`, `price extract`, `portal form fill` için giriş/çıkış/doğrulama şeması çıkar.
2. **Bir iç, bir dış keşif koşusu yap:** mevcut bir canlı ürün ve tek bir dış portal üzerinde scout run al; login/CAPTCHA/sapma noktalarını kaydet.
3. **Bir akışı deterministic'e dondur:** başarılı keşif koşusunu Playwright/Stagehand/agent-browser tarzı tekrar edilebilir workflow'a çevir ve verifier ile test et.
