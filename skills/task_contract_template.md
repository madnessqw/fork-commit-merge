# Task Contract Template

Bir subagent spawn etmeden önce bu şablonu doldur.
Belirsiz, eksik veya açık uçlu contract ile task spawn etme.

---

## Task Contract: {task_id}

### Amaç
{Ne yapılacak — 1-2 cümle, net ve spesifik. "Araştır" veya "Bak" kabul edilmez.}

### Input
{Agent hangi dosyaları, URL'leri veya sinyalleri okuyacak. Tam yollar ver.}

### Done Kriteri
{Tamamlanma ne anlama geliyor — ölçülebilir. "Bitti" veya "çalışıyor" kabul edilmez.}

### Çıktı Dosyaları
{Ne yazılacak, tam olarak nereye. Format: `path/to/file.ext`}

### Allowed Tools
{Bu görev için izin verilen tool'lar. Listelenmeyenler yasak.}

### Timeout
{Max süre — örn: 15dk, 30dk, 1sa}

### Cost Cap
{Max API call sayısı veya tahmini maliyet — örn: 20 LLM call, $0.10}

### Verify Rule
{Sonucun doğrulanma yöntemi — dosya var mı, içerik doğru mu, test geçti mi?}

### Escalation Rule
{Hangi durumda agent durup Claude ana'ya bildirir — örn: dosya bulunamazsa, hata 3 kez tekrarlarsa}

### Out of Scope
{Bu task için kesinlikle yasak eylemler — örn: production'a yazma, email gönderme}

### Assigned Agent
{Hangi subagent — örn: Researcher, Codex, QA-Tester}

### Priority
{HIGH / MED / LOW}

---

## Örnekler

---

### Örnek 1 — Research Task

## Task Contract: research-supabase-rls-2024

### Amaç
Supabase Row Level Security (RLS) policy'lerinin Next.js ile nasıl kullanıldığını araştır ve özet çıkar.

### Input
- Web araması: "supabase RLS nextjs 2024"
- URL: https://supabase.com/docs/guides/auth/row-level-security

### Done Kriteri
- En az 3 kaynak incelendi
- RLS enable/disable, policy sözdizimi ve Next.js entegrasyonu kapsandı
- Özet dosyası yazıldı

### Çıktı Dosyaları
`research/supabase-rls-summary.md`

### Allowed Tools
- web_search
- web_fetch
- create / edit (sadece çıktı dosyası)

### Timeout
20dk

### Cost Cap
15 LLM call

### Verify Rule
`research/supabase-rls-summary.md` var ve en az 200 kelime içeriyor.

### Escalation Rule
Resmi dokümantasyon 404 dönerse veya 3 farklı kaynakta çelişkili bilgi bulunursa Claude ana'ya bildir.

### Out of Scope
- Kod yazmak
- Herhangi bir dosyayı değiştirmek (yalnızca çıktı dosyasına yaz)
- Login veya authentication gerektiren sayfalara erişim

### Assigned Agent
Researcher

### Priority
MED

---

### Örnek 2 — Build Task

## Task Contract: build-auth-middleware-jwt

### Amaç
`src/middleware/auth.ts` dosyasını oluştur — JWT token doğrulama middleware'i, her protected route'ta çalışacak.

### Input
- `src/types/user.ts` — User tipini okuyacak
- `docs/api-spec.md` — Endpoint listesi ve auth gereksinimleri
- `.env.example` — JWT_SECRET key adını kontrol et

### Done Kriteri
- `src/middleware/auth.ts` oluşturuldu
- Token yoksa 401, geçersizse 403 döndürüyor
- `npm run build` hatasız geçiyor
- `npm test -- auth` 3/3 test geçiyor

### Çıktı Dosyaları
`src/middleware/auth.ts`

### Allowed Tools
- view / edit / create
- bash (sadece `npm run build` ve `npm test`)

### Timeout
30dk

### Cost Cap
25 LLM call

### Verify Rule
`npm test -- auth` çalıştır, tüm testler yeşil olmalı.

### Escalation Rule
Build 2 kez başarısız olursa veya tip hatası çözülemezse Claude ana'ya bildir.

### Out of Scope
- `src/middleware/auth.ts` dışında başka dosya değiştirme
- Package yükleme (`npm install`)
- Test dosyası yazmak

### Assigned Agent
Codex

### Priority
HIGH

---

### Örnek 3 — QA Task

## Task Contract: qa-checkout-flow-e2e

### Amaç
Checkout akışını uçtan uca test et: ürün seç → sepete ekle → ödeme → sipariş onayı.

### Input
- `tests/e2e/checkout.spec.ts` — mevcut test dosyası
- `http://localhost:3000` — çalışan lokal uygulama

### Done Kriteri
- 5 test senaryosu çalıştırıldı (happy path + 2 edge case + 2 hata senaryosu)
- Her senaryo için sonuç kayıt altına alındı (PASS / FAIL)
- Bulunan her bug için repro adımları yazıldı

### Çıktı Dosyaları
`reports/qa-checkout-YYYY-MM-DD.md`

### Allowed Tools
- bash (test runner, curl)
- view (log okuma)
- create / edit (yalnızca rapor dosyası)

### Timeout
25dk

### Cost Cap
20 LLM call

### Verify Rule
`reports/qa-checkout-*.md` var, PASS/FAIL tablosu içeriyor, en az 5 satır.

### Escalation Rule
Uygulama ayağa kalkmıyorsa veya 2'den fazla FAIL varsa Claude ana'ya bildir ve dur.

### Out of Scope
- Kaynak kodu değiştirme
- Bug fix yapmak (yalnızca raporla)
- Production ortamına bağlanma

### Assigned Agent
QA-Tester

### Priority
HIGH

---

## Kural Hatırlatıcıları

- **Contract yoksa spawn yok.** Her task bu şablona göre doldurulur.
- **Done Kriteri ölçülebilir olmalı.** "Bitti" veya "tamamlandı" geçmez.
- **Out of Scope açık yaz.** Agent ne yapamayacağını bilmeli.
- **Escalation Rule koy.** Sonsuz döngüyü önler.
- **Timeout ve Cost Cap zorunlu.** Maliyeti bilirsiz bırakma.
