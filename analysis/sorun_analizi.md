# Sorun Analizi — Cycle 1094 | 2026-04-22 12:42 UTC

## Ana Darboğaz
- **live_health** — 12 canlı ürün sağlıksız. Ayrıca 2 canlı ürün fallback alias ile ayakta. İlk örnek `webterminal-pro` (HTTP None).

## Summary'den Gelen Gerçekler
- Healthy live: 79/91
- Checkout gap: 0
- Deploy/url gap: 14
- Canonical drift: 2
- Spec-ready backlog: 11

## Canlı Sağlıksız Ürünler
- `webterminal-pro` — code=None status=None url=https://webterminal-pro.vercel.app
- `html-entities` — code=None status=None url=https://html-entities.vercel.app
- `html-minifier-pro` — code=None status=None url=https://html-minifier-pro.vercel.app
- `jwt-generator` — code=0 status=timeout url=https://jwt-generator.vercel.app
- `pdf-forge` — code=0 status=timeout url=https://pdf-forge.vercel.app
- `css-grid-gen` — code=None status=None url=https://css-grid-gen.vercel.app
- `dockerfile-generator` — code=None status=None url=https://dockerfile-generator.vercel.app
- `markdown-previewer-pro` — code=None status=None url=https://markdown-previewer-pro.vercel.app
- `image-compressor-pro` — code=None status=None url=https://image-compressor-pro.vercel.app
- `email-validator-pro` — code=None status=None url=https://email-validator-pro.vercel.app

## URL/Deploy Eksikleri
- browser-use-studio, agent-prompt-engineer

## Canonical Drift Ürünleri
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app
- `timestamp-converter` — current=https://timestamp-converter-oql54ya5f-madnessqws-projects.vercel.app ideal=https://timestamp-converter.vercel.app

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified
- **checkout_field_inconsistency** [medium/open] — Multiple checkout_url field names (checkout_url, lemon_checkout_url, lemonsqueezy_checkout_url)

## Not
- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
