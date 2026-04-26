# Landing Page Template — WOW Etkisi İçin Şablon
**Version:** 1.2 | **Son Güncelleme:** Cycle 637 | **Güven skoru:** Yüksek

> skill-writer, her 10 üründe bir bu şablonu başarılı örneklerden güncelleyecek.

---

## Prensip
**Kullanıcı siteye geldiğinde ilk 3 saniyede karar verir. WOW dedirtmezsen satış yok.**

---

## HTML Şablon Yapısı (Bölüm Sırası)

```
1. <meta/og tags>
2. <style> → dark tema CSS
3. NAV → logo + CTA butonu (sticky, blur)
4. HERO → büyük gradient başlık + tagline + CTA glow buton + trust badges
5. DEMO → canlı interaktif preview (mock data)
6. FEATURES → 3-4 glassmorphism kart
7. HOW IT WORKS → 3 adım, numara daireler
8. PRICING → tek kart, büyük fiyat, pulse CTA
9. FAQ → accordion (details/summary)
10. FOOTER
<script> → scroll animations
```

---

## Renk Sistemi

| Kullanım | Değer |
|---------|-------|
| Ana arka plan | `#0a0a0a` veya `#0f172a` |
| Başlık gradient başlangıç | `#8b5cf6` (mor) |
| Başlık gradient bitiş | `#3b82f6` (mavi) |
| Alternatif gradient | `#f97316 → #ec4899` (turuncu→pembe) |
| Alt metin | `#94a3b8` |
| CTA yeşil | `#22c55e` |
| Fiyat sarı | `#eab308` |
| Kart border | `rgba(255,255,255,0.1)` |
| Kart arka plan | `rgba(255,255,255,0.05)` |

---

## Gradient Başlık CSS
```css
.gradient-text {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

## CTA Glow Butonu CSS
```css
.cta-button {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  padding: 1rem 2.5rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 700;
  animation: pulse 2s infinite;
  box-shadow: 0 0 30px rgba(139, 92, 246, 0.4);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 50px rgba(139, 92, 246, 0.7);
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 30px rgba(139, 92, 246, 0.4); }
  50% { box-shadow: 0 0 60px rgba(139, 92, 246, 0.8); }
}
```

## Glassmorphism Kart CSS
```css
.feature-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  transition: all 0.3s ease;
}
.feature-card:hover {
  border-color: rgba(139, 92, 246, 0.5);
  box-shadow: 0 25px 50px -12px rgba(139, 92, 246, 0.2);
  transform: translateY(-4px);
}
```

## fadeInUp Animasyonu
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
.hero-title { animation: fadeInUp 0.8s ease-out; }
.hero-subtitle { animation: fadeInUp 0.8s ease-out 0.2s both; }
.hero-cta { animation: fadeInUp 0.8s ease-out 0.4s both; }
```

## Demo Bölümü Yapısı
```html
<section class="demo-section">
  <div class="demo-container">
    <div class="demo-input">
      <input type="text" id="demoInput" placeholder="Test input...">
      <button onclick="runDemo()">Try it →</button>
    </div>
    <div class="demo-output" id="demoOutput">
      <!-- Sonuç burada görünür -->
    </div>
  </div>
</section>
<script>
function runDemo() {
  const input = document.getElementById('demoInput').value;
  // Mock data ile çalışan demo
  document.getElementById('demoOutput').innerHTML = `<pre>${JSON.stringify({result: "...", input}, null, 2)}</pre>`;
}
</script>
```

## Trust Badges
```html
<div class="trust-badges">
  <span>✓ No signup required</span>
  <span>✓ Instant results</span>
  <span>✓ API ready</span>
  <span>✓ One-time payment</span>
</div>
```

---

## ZORUNLU Meta Tags
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Product Name] — [Tagline] | $[Price] one-time</title>
<meta name="description" content="[155 karakter açıklama]">
<meta property="og:title" content="[Product Name]">
<meta property="og:description" content="[Kısa açıklama]">
<meta property="og:image" content="[URL]/og-image.png">
<meta property="og:url" content="[URL]">
<meta name="twitter:card" content="summary_large_image">
```

---

## Başarılı Örnekler
*(skill-writer tarafından doldurulur)*

## Dikkat: Bu Hatalardan Kaçın
- Beyaz arka plan kullanma
- Demo bölümü atlama
- 200 satırdan az HTML yazma
- Gradient text sız başlık

---

## Cycle 637 Guncellemeleri

### En Iyi Landing Page Ornekleri
| Urun | One Cikan Ozellik |
|------|-------------------|
| dataflip | Scroll reveal animasyonlari, interaktif demo |
| rateguard | Rate limit gosterimi, canli ornek |
| regex-tester-pro | Testimonial bolumu, gercek zamanli regex test |
| json-formatter-pro | JSON input/output demo, syntax highlighting |
| curl2code | Canli curl to code conversion demo |

### Kanitlanmis Pattern'ler
1. Scroll reveal her sayfada olmali - IntersectionObserver ile
2. Interactive demo bolumu sart - mock data ile calisan
3. Trust badges en az 4 adet
4. FAQ accordion minimum 4 soru
5. og:image her urunde olmali - social sharing icin kritik
6. Mobile responsive test edilmis olmali

### Kacinilacak Hatalar (Cycle 637)
- og:image tag'ini atlama
- Mobile responsive kontrolu yapmama
- Demo bolumunu atlamak
- 200 satirdan az HTML yazmak
