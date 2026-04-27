# Innovation Brief — Cycle 1233

## Durum Analizi
- **Canlı ürün:** 181 (tümü Polar checkout ile)
- **Checkout gap:** 0 (tümü synched)
- **Bakiye:** $0
- **Sorun:** Altyapı hazır, trafik/yükleme yok

## Temel Gerçek
181 ürün deploy edilmiş ve çalışıyor. $0 satış = trafik sorunu, NOT ürün/executing sorunu.
Checkout URL'leri Polar'a redirect ediyor (doğru davranış).

## MEVCUT ÜRÜN ENVENTERİ (181 ürün)
```
API Tools: api-compare, api-doc-generator, api-mock-generator, api-mock-server,
           api-request-builder, api-security-scanner, api-spec-validator, api-to-mcp
Code Tools: code-complexity-analyzer, code-formatter-universal, code-minifier-pro,
            code-screenshot-beautifier, code-snippet-manager
Converter: base64-encoder-pro, base64-pro, binary-inspector, case-converter-pro,
           html-entity-encoder, html-to-markdown, json-formatter, yaml-converter-pro,
           cron-expression-parser, cron-master, csv-to-json-pro, xml-to-json
Visual: ascii-art-generator, carbonlite, chart-studio, codesnap, colormine,
        color-palette-extractor, css-gradient-studio, css-grid-gen, css-shadow-studio
OG/Media: og-forge (OG image generator), image-compressor-pro
Auth/Security: jwt-generator, jwtinspector, secretguard, api-key-manager
Terminal: terminal-os, terraink (map poster $19)
Infrastructure: diffmaster, diffforge, nginx-config, mcphub, keyforge
```

## BULUNAN ARAŞTIRMA NOTLARI (projeler.txt [***]):
- `xtermjs / xterm.js` — web terminal emulator
- `Terminal UI OS (Terminal Multiplexer)` — [***] highest priority
- `yousifamanuel // terraink` — GitHub owner
- `Dimos`, `EverMind-AI`, `we put Openclaw on a drone`

## EKSİK ÜRÜN FIRSATLARI (ürün var ama kalite artırılabilir):
1. **OG Image Generator** (og-forge $29) — mevcut ama canonical drift olabilir, SEO güncellenebilir
2. **Terminal OS** — [***] konsept, mevcut ürün çalışıyor ama canonical 500 hatası
3. **Terraink** — $19 map poster, canonical 404, preview alias çalışıyor

## TAVSİYE EDILEN Sİradaki ÜRÜN: "xterm-web"
**Neden:** Terminal emulator web arayüzü — xterm.js kullanarak web tarayıcısında çalışan terminal. [***] ile işaretli.

**Spec:**
- slug: `xterm-web`
- Fiyat: $15 (dev tool, hızlı kazanım)
- Konsept: Her developer bir terminal ister — xterm.js + WebSocket backend
- Tech: Single HTML + xterm.js CDN, WebSocket proxy (Vercel serverless)
- Value prop: "Works anywhere, no install" —browser'da çalışan profesyonel terminal
- Competitive: crosh (Chrome), Azure Cloud Shell — ama daha basit, tek URL

**Alternatif (daha hızlı build):**
- `screenash` — screen/tmux session viewer
- `port-checker` — port scanner for devs
- `webhook-debugger` — webhook inspector

## CANONICAL DRIFT (12 ürün — Vercel domain yapılandırması gerekiyor):
Yapılandırma için Vercel Dashboard'da domain doğrulaması gerekiyor:
- chmod-calculator, commit-message-generator, croncraft, email-validator-pro,
- html-entity-encoder, jwt-generator, nginx-config, pdf-forge, terminal-os,
- terraink, timestamp-converter, webhook-tester

**NOT:** Manuel müdahale gerekli — DNS TXT record doğrulaması

## HAREKET:
1. [ ] Builder agent'a `xterm-web` spec ver ve build ettir
2. [ ] Canonical drift için Vercel domain doğrulaması (manuel — Gokhan'a bildir)
3. [ ] Alternatif: mevcut og-forge'i canonical'a bağla (SEO için)

---
*Cycle 1233 — INNOVATE mode — Ana sorun: $0 satış = trafik eksikliği*
