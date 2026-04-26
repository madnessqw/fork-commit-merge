# Durum Raporu — ProfitBridge / profitbridgeintel.com

**Son güncelleme:** 2026-04-18  
**Amaç:** Yeni konuşmada bu dosya tek başına bağlam versin. Payment provider denemeleri, domain/hosting, iyzico durumu, canlı site uyumu ve sonraki adımlar burada.

---

## 1) ProfitBridge tam olarak ne satıyor?

ProfitBridge, **HS code / GTİP bazlı dijital trade intelligence raporları** satar.

Bu iş modeli:
- fiziksel ürün satmaz
- navlun / lojistik satmaz
- gümrük bedeli tahsil etmez
- üçüncü taraf adına para toplamaz
- pazaryeri / escrow / komisyonculuk yapmaz
- asıl olarak **tek seferlik dijital rapor / analiz hizmeti** satar

### Hedef kullanıcılar
- ihracatçılar
- ithalatçılar
- sourcing ekipleri
- trade analyst / BI / strategy ekipleri

### Sitedeki paket yapısı
- **A1 Scout** — 25 şirket — **$19**
- **A2 Intel** — 100 şirket — **$39**
- **A3 Commander** — 200 şirket — **$79**
- **A4 Enterprise** — 800 şirket — **$499**

### Rapor içeriği
Seçilen HS code’a göre şunlar bulunabilir:
- importer / exporter şirket isimleri
- ülke bilgileri
- quantity / weight verileri
- yıllara göre ticaret geçmişi
- paid-price / price context
- competitor intelligence
- rota / liman verileri
- uygun olduğu yerde iletişim bilgileri

### En kritik cümle
İyzico’ya ve herhangi bir payment provider’a anlatılması gereken net cümle şu:

> ProfitBridge üzerinden alınan ödeme, ProfitBridge’in kendi dijital trade intelligence raporu için alınan hizmet bedelidir; mal bedeli, navlun, gümrük veya üçüncü taraf tahsilatı değildir.

---

## 2) LemonSqueezy tarafında ne oldu?

### Başlangıç durumu
LemonSqueezy store açıldı, ürünler yayınlandı ama sistem **Test Mode**’da kilitli kaldı.

### Ana blocker
- **Identity verification = Rejected**
- Bu yüzden store live moda geçmedi
- Test mode toggle açılmadı

### Net ayrım
- W-8 / W-9 tarafı ayrı konu
- payout readiness ayrı konu
- ana blokaj **identity verification rejection**

### Lemon için yapılan aksiyon
- kayıtlı hesap e-postasından destek maili atıldı
- kullanılan destek adresi: **hello@lemonsqueezy.com**
- amaç:
  - identity verification akışını yeniden açtırmak
  - red nedenini net öğrenmek
  - store’u test moddan çıkarmak

### Lemon mevcut durum
- **destek cevabı bekleniyor**
- çalışırsa tekrar checkout alternatifi olabilir
- ama şu an güvenilir canlı çözüm olarak bekleme modunda

---

## 3) Neden iyzico’ya geçildi?

Lemon bloke olunca Türkiye tarafından hızlı fallback arandı.

Kritik gerçek:
- kullanıcıda **tüzel kimlik / vergi no yok**
- bu yüzden klasik merchant / sanal POS yerine **bireysel Link** ihtimali üzerinden ilerleniyor

Resmi iyzico kaynaklarında doğrulanan mantık:
- **tüzel kimliği olmayanlar, iş modeline bağlı olarak yalnızca Link ürünü için bireysel başvuru yapabilir**

Yani hedef baştan beri şuydu:
- tam merchant POS değil
- **iyzico Link ile bireysel başvuru / link üzerinden ödeme alma**

---

## 4) iyzico tarafında yaşananlar

### İlk onboarding sırasında
- IBAN doğrulama sorunu çıktı
- ilk IBAN hata verdi
- sonra farklı TR ile başlayan kullanıcıya ait hesap IBAN’ı girildi
- sorun aşıldı

### Sonra istenenler
- kimlik bilgileri
- ürün / hizmet açıklaması
- platform / site adresi
- iş modelinin anlaşılır biçimde açıklanması

### Merchant panel tarafındaki kafa karıştıran durum
Kullanıcı panelde giriş yaptı ama klasik bir “merchant dashboard” deneyimi yerine onboarding akışına düştü.

Bulunan gerçekler:
- doğru giriş adresi: **https://merchant.iyzipay.com/login**
- yardım merkezindeki “Panele Giriş Yap” bağlantısı buna gidiyor
- hesap tamamlanmamışken **Profil** menüsü tekrar `/application` akışına dönebiliyor
- bu yüzden kullanıcıya panel yokmuş gibi döngü yaşatıyor

### Görülen uyarı
Başvuru ekranında şu uyarı çıktı:

- **Gerekli Kriterler Sağlanmadı**
- “İş modeliniz hakkında detaylı bilgiye ihtiyacımız var. iyzico posları üzerinden geçecek olan ödeme nedir? Konuyla ilgili geri dönüşü basvuru@iyzico.com adresine mail yoluyla yapabilirsiniz.”

Bu şu anlama geliyor:
- sorun tek bir input alanı hatası değil
- iyzico, iş modelini yeterince net anlamadı
- “Başvuruyu Güncelle” butonu gerekli açıklama alanını açmadan kullanıcıyı onboarding’e geri atıyor
- yani burada çözüm **panelde alan bulmak değil**, **maille iş modelini açıklamak**

### İyzico için artık doğru aksiyon
**Mail gönderilecek ana adres:** `basvuru@iyzico.com`  
**CC / bilgi kopyası:** `destek@iyzico.com`  
**Gönderen adres:** iyzico hesabına kayıtlı e-posta

Not:
- sitedeki `profitbridgeintel@gmail.com` destek mailidir
- iyzico dönüşlerini büyük ihtimalle **hesaba kayıtlı e-posta adresine** yapar
- bu yüzden iyzico maili kayıtlı hesap mailinden atılmalı

### iyzico mailinin amacı
Açıkça anlatılmalı:
- satılan şey fiziksel ürün değil
- hizmet, HS-code bazlı dijital trade intelligence raporu
- ödeme, yalnızca bu dijital rapor hizmeti için alınıyor
- mal bedeli / freight / customs / third-party collection değil

### iyzico mevcut durum
Bu dosyanın hazırlandığı an itibarıyla:
- başvuru tamamen çökmedi
- ama **“review bekleniyor” demek tek başına doğru değil**
- mevcut doğru durum:
  - başvuru alınmış
  - sistem ek açıklama istiyor
  - **iş modeli açıklama maili gönderilip yeniden değerlendirme beklenmeli**

Yani kısa doğru özet:
> iyzico tarafı şu an “otomatik review bekleniyor” aşamasında değil; iş modelini açıklayan mail atılması gereken aşamada.

---

## 5) iyzico için site tarafında yapılan uyum düzeltmeleri

Local projede ve sonra production’da şu işler yapıldı:

### Temizlik
- fake telefon kaldırıldı
- fake adres / çoklu şehir ifadesi kaldırıldı
- fake `hello@profitbridge.ai` kaldırıldı

### Gerçek iletişim
- aktif iletişim maili: **profitbridgeintel@gmail.com**
- contact bölümünde destek e-posta üzerinden konumlandı

### Legal / güven sayfaları
- **Privacy Policy**
- **Distance Sales**
- **Refund & Delivery**
- **Contact**

### Ödeme / güven sinyalleri
- pricing tarafında **Pay with iyzico**
- **Visa**
- **Mastercard**
- **SSL-secured checkout**

### Metin düzeltmeleri
Site metinlerine özellikle şu vurgu eklendi:
- ödeme yalnızca dijital rapor hizmeti içindir
- freight / customs / marketplace / third-party collection değildir

---

## 6) Domain kararı ve sonucu

### Değerlendirilen domainler
- profitbridgehq.com
- profitbridge.tech
- profitbridge.agency
- profitbridgeintel.com

### Nihai karar
**profitbridgeintel.com** seçildi.

### Gerekçe
- `.com`
- markayı bozmuyor
- işin “trade intelligence” doğasını net anlatıyor
- `hq` kadar boş bir ek değil
- `.tech` kadar developer-tool havası vermiyor

### Registrar
- domain **Cloudflare Registrar** üzerinden alındı

### Domain mevcut durum
- domain aktif: **profitbridgeintel.com**
- auto-renew açık
- DNS Cloudflare üzerinden yönetiliyor

---

## 7) Hosting ve canlı kurulum

### Altyapı kararı
Vercel yerine ana omurga için **DigitalOcean droplet + Caddy** tercih edildi.

### Kullanılan sunucu
- provider: **DigitalOcean**
- droplet adı: **openagents-server**
- public IP: **64.227.116.216**

### DNS
Cloudflare DNS kayıtları:
- `A @ -> 64.227.116.216`
- `CNAME www -> profitbridgeintel.com`

### Sunucudaki yayın klasörü
- `/var/www/profitbridge/current`

### Sunucuda yapılan kurulum
- Caddy kuruldu
- domain bağlandı
- SSL aktif hale geldi
- bundle sunucuya açıldı
- site `profitbridgeintel.com` ve `www.profitbridgeintel.com` için servis ediliyor

### Deploy modeli
Lokal bundle üretim komutu:
```bash
cd /home/gokhan/projects/websitesi432552
./scripts/package-static-bundle.sh
```

Sonrasında bundle sunucuya açılıyor ve Caddy aynı root’tan servis ediyor.

### Canlı doğrulanan durum
- `https://profitbridgeintel.com` çalışıyor
- `https://www.profitbridgeintel.com` çalışıyor
- HTTPS aktif
- server Caddy

---

## 8) Production’da düzeltilen kritik şeyler

Başta canlı bundle’da eski placeholder/fake veriler kalmıştı:
- `hello@profitbridge.ai`
- fake ABD telefon numarası
- `London, Istanbul, New York`

Bunlar daha sonra production’a gerçekten deploy edilerek temizlendi.

### Production’da doğrulanan yeni durum
- aktif destek maili: **profitbridgeintel@gmail.com**
- fake iletişim bilgileri kaldırıldı
- `Pay with iyzico`, `Visa`, `Mastercard` production bundle’da var
- dijital rapor / freight-customs-third-party ayrımı production bundle’da var
- legal sayfalar ve contact yapısı sitede mevcut

---

## 9) Resmi kaynaklardan doğrulanan önemli iyzico gerçekleri

### Başvuru / hesap tipi
- tüzel kimliği olmayanlar iş modeline bağlı olarak **yalnızca Link** için bireysel başvuru yapabilir
- bu, mevcut ProfitBridge denemesiyle uyumlu yoldu

### Site beklentileri
iyzico’nun public başvuru kriterlerinde beklenen şeyler:
- ürün / hizmetin anlaşılır gösterimi
- fiyatlandırma
- gizlilik politikası
- mesafeli satış / satış sözleşmesi
- teslimat / iade bilgileri
- iletişim bilgileri
- SSL / güvenli site
- iyzico / Visa / Mastercard logoları

### İletişim bilgileri
- destek maili: **destek@iyzico.com**
- genel hat: **+90 216 599 01 00**
- iş modeli açıklama için yönlendirilen adres: **basvuru@iyzico.com**

---

## 10) Şu anki net durum

### LemonSqueezy
- store var
- ürünler var
- **identity rejected** nedeniyle live değil
- destek maili atıldı
- cevap bekleniyor

### iyzico
- onboarding ilerledi
- IBAN sorunu aşıldı
- site referansı verildi
- canlı site iyzico açısından daha temiz hale getirildi
- sistem “gerekli kriterler sağlanmadı / iş modeli açıklayın” noktasına geldi
- **bir sonraki doğru adım:** `basvuru@iyzico.com` adresine iş modeli açıklama maili atmak
- sonra yeniden değerlendirme beklemek

### Domain + hosting
- **profitbridgeintel.com alındı**
- Cloudflare DNS aktif
- DigitalOcean droplet üzerinde canlı host edildi
- production bundle güncel

### Marka / positioning sonucu
- display brand: **ProfitBridge**
- live domain: **profitbridgeintel.com**
- positioning: **HS-code trade intelligence / digital trade reports**

---

## 11) Sonraki doğru adımlar

### 1. iyzico mailini gönder
- **To:** `basvuru@iyzico.com`
- **Cc:** `destek@iyzico.com`
- **From:** iyzico hesabına kayıtlı mail
- mailde net anlat:
  - fiziksel ürün yok
  - dijital rapor satılıyor
  - freight/customs/third-party collection yok
  - teslimat dijital

### 2. Gerekirse gerçek telefon bilgisi ekle
Şu an fake bilgiler kaldırıldı; bu doğruydu.  
Ama iyzico daha sonra gerçek telefon isteyebilir. O zaman gerçek numara eklenmeli.

### 3. Tüzel kimlik konusu netleşsin
Kullanıcıda şirket / vergi no olmadığı için beklenti **Link** düzeyinde tutulmalı.  
Klasik merchant POS beklentisiyle ilerlemek yanlış olur.

### 4. Sunucu güvenliği
Root erişim bilgileri sohbetlerde dolaştığı için **root şifre rotate edilmeli**.

---

## 12) Tek paragraf ultra kısa özet

ProfitBridge, HS-code bazlı dijital trade intelligence raporları satan bir yapıdır. LemonSqueezy tarafı identity rejection yüzünden canlıya alınamadı. Bu yüzden bireysel kullanımda Link ihtimali nedeniyle iyzico fallback olarak seçildi. Domain olarak profitbridgeintel.com alındı, Cloudflare DNS ile DigitalOcean droplet üzerinde Caddy üzerinden canlıya alındı. Site production’da iyzico uyumuna göre temizlendi: fake iletişim bilgileri kaldırıldı, profitbridgeintel@gmail.com eklendi, privacy / distance sales / refund / contact sayfaları ve iyzico-Visa-Mastercard güven işaretleri kondu. İyzico başvurusu tamamen düşmedi ama “iş modelinizi açıklayın” aşamasına geldi; şu an doğru sonraki adım basvuru@iyzico.com adresine, kayıtlı iyzico e-postasından, “satılan şeyin yalnızca dijital rapor hizmeti olduğu; mal/freight/customs/third-party collection olmadığı” şeklinde net açıklama maili gönderip yeniden değerlendirme beklemektir.
