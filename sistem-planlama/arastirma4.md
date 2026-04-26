# Araştırma #4 — Local Business Automation
**Tarih:** 2026-04-21 04:45 +03
**Konu:** Türkiye + global küçük işletmeler için randevu, çağrı, yorum, takip ve müşteri iletişimi otomasyonları
**Kaynaklar:**
- Yerel: `skills/ARASTIRMA_MODU.md`, `sistem-planlama/counter.txt`, `projeler.txt`, önceki `arastirma0-3.md` / `planlama0-3.md`
- SBA 2025 Small Business Profile: https://advocacy.sba.gov/wp-content/uploads/2025/06/United_States_2025-State-Profile.pdf
- KOSGEB/TÜİK KOBİ göstergeleri 2024 PDF: https://webdosya.kosgeb.gov.tr/Content/Upload/Dosya/Tablo%20ve%20Raporlar/2024/T%C3%BCrkiye%27deki_KOB%C4%B0%27lere_%C4%B0li%C5%9Fkin_Baz%C4%B1_%C4%B0statistiki_G%C3%B6stergeler.pdf
- U.S. Chamber 2025 small business AI report: https://www.uschamber.com/technology/artificial-intelligence/u-s-chambers-latest-empowering-small-business-report-shows-majority-of-businesses-in-all-50-states-are-embracing-ai
- Goldman Sachs 10,000 Small Businesses AI survey, 2026: https://www.goldmansachs.com/pressroom/press-releases/2026/small-businesses-embrace-ai-but-need-training-and-support-to-fully-harness-it
- Thryv / BusinessWire 2025 SMB AI survey: https://www.businesswire.com/news/home/20250717239434/en/AI-Adoption-Among-Small-Businesses-Surges-41-in-2025-According-to-New-Survey-from-Thryv
- U.S. Census BTOS AI use among small businesses: https://www.census.gov/newsroom/blogs/research-matters/2024/12/ai-use-small-businesses.html
- SBA Office of Advocacy AI adoption gap note: https://advocacy.sba.gov/2025/09/24/new-advocacy-article-highlights-small-businesses-closing-the-ai-adoption-gap/
- Grand View Research — Marketing Automation market: https://www.grandviewresearch.com/industry-analysis/marketing-automation-software-market
- Grand View Research — Field Service Management market: https://www.grandviewresearch.com/industry-analysis/field-service-management-market
- Grand View Research — Scheduling Apps market: https://www.grandviewresearch.com/industry-analysis/scheduling-apps-market-report
- BrightLocal Local Consumer Review Survey 2026: https://www.brightlocal.com/research/local-consumer-review-survey/
- CallRail business communications report PDF: https://assets.ctfassets.net/7742r3inrzuj/5ZkRJYcIauyKSb7ZxpKp5v/b53a8c0da7d5ef37a4cefa263fc0f9b0/-Report-_Why_business_communications_software_is_the_key_to_unlocking_growth.pdf
- HighLevel pricing: https://www.gohighlevel.com/CcYQhGEz2h
- HighLevel rebilling docs: https://help.gohighlevel.com/support/solutions/articles/155000001156-highlevel-pricing-guide
- Make pricing: https://www.make.com/en/pricing
- Zapier pricing explainer: https://zapier.com/blog/zapier-pricing/
- Retell AI pricing: https://www.retellai.com/pricing
- Twilio Voice pricing US: https://www.twilio.com/en-us/voice/pricing/us
- Jobber pricing: https://www.getjobber.com/pricing
- Housecall Pro pricing: https://www.housecallpro.com/pricing/
- Cal.com pricing: https://cal.com/pricing
- IndieHackers AI Voice SaaS/Agency post: https://www.indiehackers.com/post/building-a-profitable-ai-voice-saas-agency-300-800-mrr-per-client-frAbgO1yQMfHOFFtY3gE
- Reddit r/gohighlevel paid-ads agency thread: https://www.reddit.com/r/gohighlevel/comments/1qul2jv/anyone_here_grow_an_agency_purely_on_paid_ads/
- Reddit r/gohighlevel $1k/mo services thread: https://www.reddit.com/r/gohighlevel/comments/1riynzm/what_services_justify_1000month_on_gohighlevel/
- Reddit r/Entrepreneur GoHighLevel agency model thread: https://www.reddit.com/r/Entrepreneur/comments/183eyhf/is_gohighlevel_agency_model_a_scam/
- ArXiv MCP: `2505.14721`, `2504.17295`, `2505.11646`, `2307.09923`
- MCPTube: `JinTKY1TJZY`, `7Y8eXeweCzc`, `IpS95mi1PPI`

## Özet Bulgular
- Küçük işletme pazarı devasa ve dağınık: ABD'de 36.2 milyon küçük işletme, 62.3 milyon çalışan ve tüm işletmelerin %99.9'u var. Türkiye'de KOSGEB/TÜİK verisinde 3,773,252 KOBİ ve toplam girişimlerin %99.7'si KOBİ. Bu pazar “tek SaaS landing page” ile değil, vertical template + elle satılan ilk paketlerle açılır.
- AI benimsemesi iki farklı gerçek gösteriyor: resmi BTOS/Census çizgisinde AI'ı üretim/hizmet içinde kullanan küçük işletme oranı düşük-orta seviyede; U.S. Chamber/Goldman/Thryv gibi geniş anketlerde ise niyet ve deneme çok yüksek. En kritik veri: Goldman 2026'da %76 AI kullanıyor diyor ama yalnızca %14 “core operations” içine tam gömmüş. Aradaki boşluk otomasyon ajansının ekmek kapısı.
- En hızlı satılabilir problem “AI” değil: kaçan çağrı, geç dönüş, randevu kaçırma, yorum istememe, teklif takibi yapmama. Yerel işletmeye “agentic workflow orchestration” diye gidersen kapı kapanır. “Kaçan aramayı 30 saniyede SMS'e çevirip randevuya bağlayalım” dersen dinlerler.
- Pazar büyümesi bu işleri destekliyor: global marketing automation 2024'te $6.65B → 2030'da $15.58B; field service management 2022'de $4.43B → 2030'da $11.78B; scheduling apps 2025'te $663.1M → 2033'te $1.813B.
- Reddit/IndieHackers örnekleri “tool reselling” değil “sonuç paketi” satanların para kazandığını gösteriyor. En sağlam paket: missed-call text-back + website chat/lead qualifier + calendar booking + review request + weekly ROI report.

## Gerçek Başarı Hikayeleri
- **IndieHackers AI Voice SaaS/Agency:** Ocak 2026 postunda stack `Callin.io + n8n + Cal.com`, hedef “$500K-$5M gelirli local service businesses”, unit economics `$1K-$2K setup + $300-$800 MRR/client`, yaklaşık %80 margin ve 2-3 haftada ilk gelir iddia ediliyor. Bu doğrulanmış finansal rapor değil, ama ürünleştirilebilir paket tasarımını net veriyor.
- **Reddit r/gohighlevel — $10k MRR anekdotu:** Bir kullanıcı `website in 72h + CRM + 5-star review automation + referral text blast + auto call text-back` paketini $297/ay sattığını, başka kullanıcı aynı offer ile 30 günde yaklaşık $10k MRR ve 3.5 ROAS gördüğünü yazıyor. Aynı thread'de bir başkası lead gen + web design + reputation + automation paketini $1,500/ay + ad spend ile sattığını söylüyor. Bunlar self-report; kanıt seviyesi “sinyal”, “bilanço” değil.
- **Reddit r/gohighlevel — $1,000+/ay paket:** Bir kullanıcı AI calls, website, social posts, community, payments ve pipeline içeren sistemi $1,000/ay'a sattığını yazıyor. Ders: $1,000/ay tek bir chatbot için değil, işletmenin satış/iletişim sistemini komple toparlayan paket için mümkün.
- **Reddit r/Entrepreneur — GHL hype uyarısı:** Web developer bir kullanıcı $10K+/ay ajans geliri ve $6.5K recurring revenue iddia ediyor; 60+ müşteriye $0 down / $150 ay website abonelikleri sattığını söylüyor. Aynı thread GHL “guru/affiliate” hype'ına güçlü uyarı veriyor: bedava site + tool resale zayıf; gerçek değer tasarım, takip, SEO, sistem ve güvenilir servis.
- **MCPTube `7Y8eXeweCzc` — Pavlo:** Videoda $20K MRR, 800+ testimonial/case study ve ilk $1K müşteri örnekleri iddia ediliyor; satılan ana workflow missed-call text-back, website chat, AI appointment booking, form submission follow-up ve reporting. Affiliate/course içeriği olduğu için iddialar temkinli kullanılmalı, ama demo akışı pratik.
- **MCPTube `IpS95mi1PPI` — brick-and-mortar AI:** Missed-call text-back + review automation için 30 günlük rollout, POS/CRM/Zapier-Make bağlantısı, QR/kiosk/in-store destek, rebooking nudges ve ROI dashboard öneriliyor. Örnek ROI formülü: 20 geri kazanılmış booking × $80 gross margin = $1,600; yazılım+telefon maliyeti $250 ise payback bir aydan kısa.
- **MCPTube `JinTKY1TJZY` — voice agent kurulumu:** Retell AI + n8n ile form submit → saniyeler içinde outbound call → lead qualify/follow-up → website form integration akışı gösteriliyor. Kısa vadede “AI voice” ana ürün değil, premium add-on olmalı; önce text-back ve booking çalışmalı.

## Pazar Büyüklüğü & Fırsat
- **ABD küçük işletme tabanı:** SBA 2025 profili 36.2M küçük işletme, 62.3M küçük işletme çalışanı ve %45.9 istihdam payı gösteriyor.
- **Türkiye tabanı:** KOSGEB/TÜİK 2024 raporunda 2022 bazlı KOBİ sayısı 3,773,252; toplam girişimlerin %99.7'si. Sektör kırılımında ticaret/onarım 1.36M, konaklama/yiyecek 314K, ulaştırma/depolama 573K, diğer hizmetler 188K civarı görünüyor. Bunlar local automation için doğrudan aday sektörler.
- **Adoption gap:** U.S. Chamber 2025, küçük işletmelerin %58'inin generative AI kullandığını, %96'sının emerging tech benimsemeyi planladığını söylüyor. Goldman Sachs 2026, %76 AI kullanımı, %93 pozitif etki, %84 verimlilik artışı; ama sadece %14 core operations'a tam entegre diyor. Yani satın alma ilgisi var, uygulama kası yok.
- **Operasyonel tasarruf sinyali:** Thryv 2025 anketinde AI kullanan SMB'lerin %58'i ayda 20+ saat tasarruf ettiğini, %66'sı ayda $500-$2,000 tasarruf gördüğünü raporluyor. Bu, $199-$499/ay “done-for-you automation” paketinin fiyat savunmasını güçlendirir.
- **Kaçan iletişim problemi:** CallRail raporu, 411 Local 2016 verisine dayanarak business calls'un %62'sinin unattended olduğunu; bunun %24.3'ünün cevapsız, %37.8'inin voicemail olduğunu aktarıyor. Veri eski ama problem hâlâ Reddit/SMB thread'lerinde aynı: işletme çalışırken telefonu açamıyor, lead rakibe gidiyor.
- **Review fırsatı:** BrightLocal 2026 survey: Google hâlâ review kaynağında açık ara önde; sadece %35 SMB'nin Google Business Profile'ı olduğu belirtiliyor. Ayrıca 2026'da yorum bırakması istenen tüketicilerin %83'ü yorum bırakmış, %28'i istenirse “always” yorum yazar demiş. Review automation düşük riskli, yüksek algılanan değerli bir ilk ürün.
- **Komşu yazılım pazarları:** Marketing automation $15.58B 2030 projeksiyonu, scheduling apps %13.46 CAGR, field service management %13.3 CAGR. Bu, local business automation'ın ayrı bir “toy market” değil, CRM + scheduling + field-service + reputation + comms kesişimi olduğunu gösteriyor.

## Rakipler & Boşluklar
- **GoHighLevel / HighLevel:** $97 Starter, $297 Unlimited, $497 Pro. Ajanslar için white-label, sub-account, phone/email/text/AI rebilling markup imkânı var. Güçlü ama GHL kurs/affiliate gürültüsü pazarı kirletiyor. Boşluk: GHL satmak değil, “GHL içinde çalışan gelir sistemi” satmak.
- **Zapier / Make / n8n:** Make Core $9/mo, Pro $16/mo, Teams $29/mo; Zapier Pro $19.99/mo, Team $69/mo. Bunlar POC için yeterli. n8n self-host daha ucuz ama bakım yükü var.
- **Vertical SaaS:** Jobber, Housecall Pro, Square Appointments, Booksy, Fresha, Thryv gibi araçlar randevu/field-service/POS tarafını çözüyor. Boşluk: küçük işletmeler “hangi tool” değil, “benim workflow'um kurulsun ve ölçülsün” istiyor.
- **Voice AI platformları:** Retell AI $0.07-$0.31/dk AI voice agent; Twilio US outbound $0.014/dk, inbound local $0.0085/dk + $1.15/ay number. Voice güçlü ama yanlış ilk ürün olabilir: maliyet, kalite, güven ve compliance daha zor. Text/SMS/WhatsApp ile kanıtla, sonra voice ekle.
- **Review/GBP ajansları:** Çok sayıda local SEO ajansı var ama çoğu rapor üretip bırakıyor. Boşluk: GBP + missed call + booking + review + weekly revenue estimate tek loop'ta bağlanırsa daha somut olur.
- **Türkiye boşluğu:** İYS/KVKK nedeniyle toplu ticari mesaj hassas; ama WhatsApp, Google Business Profile, randevu hatırlatma, yorum isteme, form follow-up ve telefon kaçırma Türkiye'de de bariz problem. Paket yerelleştirilirse yabancı GHL ajans kopyalarından ayrışır.

## Teknik Gereksinimler
- **Minimum ürün paketi:**
  1. Missed-call text-back veya WhatsApp follow-up
  2. Website chat / contact form instant reply
  3. Calendar booking + reminder
  4. Google review request + response draft
  5. Quote / estimate follow-up
  6. Weekly ROI report: missed calls, conversations, bookings, reviews, estimated recovered revenue
- **Stack seçenekleri:**
  - POC düşük maliyet: Google Sheets + Google Calendar + Cal.com + Make/Zapier + Twilio/WhatsApp + Gmail
  - Ajans ölçek: HighLevel $297 veya $497 + custom snapshots + rebilling
  - Voice add-on: Retell/Vapi/Twilio + n8n/Make webhook + human handoff
  - Türkiye varyantı: WhatsApp Business, Google Calendar, Google Sheets, lokal SMS/arama sağlayıcısı, KVKK/İYS onay kontrolü
- **Data modeli:** Contact, source, consent, channel, business vertical, service type, urgency, zip/area, preferred time, appointment status, quote amount, follow-up state, review status, revenue estimate.
- **Agent rolleri:** Prospect auditor, demo builder, onboarding interviewer, knowledge-base builder, workflow tester, ROI reporter, compliance checker.
- **Metrikler:** first-response time, missed-call recovery %, conversation-to-booking %, appointment show rate, review request → posted review %, quote follow-up conversion, owner time saved, monthly recovered gross profit.
- **İnsan müdahalesi:** İlk satış görüşmesi, işletme bilgi formu, tone/policy onayı, fiyat/availability doğrulama, şikayet/iptal/refund/medical/legal konularda human handoff.
- **Kalite kapısı:** AI hiçbir zaman garanti fiyat, kesin müsaitlik veya tıbbi/hukuki tavsiye vermemeli. “Bunu kontrol edip size döneceğiz” demeyi bilmeli; aksi yerel işletmeye yapay zeka değil yapay bela satmış olursun.

## Ham Notlar
- `projeler.txt` taramasında local business'a doğrudan paketlenmiş proje az çıktı; sinyal daha çok local agent, browser automation, Google Maps/scraping ve genel automation tarafında. Bu iyi: UniverseCreator mevcut ürün kataloğundan değil, swarm operasyon kabiliyetinden ürün çıkarmalı.
- En iyi ilk vertical'lar: HVAC/plumbing/roofing/remodeling, dental/clinic/med spa, salon/barber/beauty, restaurant/cafe, auto repair, local legal/accounting. Ortak payda: inbound call + appointment + high LTV + geç dönüşte kayıp.
- Düşük ticket restoran/kafe için voice agent değil; queue, reservation, review, menu FAQ, Google profile, rebooking/loyalty. Yüksek ticket remodeling/HVAC için missed-call + quote follow-up çok daha mantıklı.
- “AI kullanıyor musunuz?” sorusu kötü satış sorusu. “Geçen hafta kaç çağrı/randevu/yorum kaçtı?” iyi satış sorusu.
- ArXiv MCP ilk denemede 429 verdi; daha sonra `get_abstract` çalıştı. Akademik ders: LLM'ler business process modelleme ve bilgi yoğun görev otomasyonunda işe yarıyor ama süreç varyantlarını ölçmek şart. Local business'ta da workflow'u kurup dashboard olmadan “değer yarattık” demek boş.
- Census/SBA resmi verileri, vendor survey'lerden daha düşük AI adoption gösteriyor. Bu çelişki kötü değil: vendor survey'ler “AI tool deniyorum”, resmi anketler “üretim/hizmet sürecimde kullanıyorum” farkını yakalıyor. Bizim fırsat tam bu implementasyon boşluğu.
