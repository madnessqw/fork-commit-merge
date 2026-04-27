# Codex Analiz Özeti — 2026-04-27 12:00 UTC

## Canlı State
- Cycle: **237**
- Mode: **OPTIMIZE**
- Live sağlık: **184/184** (%100.0)
- Canonical healthy: **170/184** (%92.4)
- Health pending: **0**
- Fallback healthy: **14**
- Checkout gap: **0**
- Deploy readiness gap: **0**
- Deploy/url gap: **0**
- Canonical drift: **14**
- Spec-ready: **0**
- Next action: `14 canonical URL drift'ini düzelt; fallback alias'ı ezme`

## Ana Darboğaz
- **Ready-for-payment health açığı:** 1 ready_for_payment ürün health-check'te sorunlu; ilk örnek `git-workflow-auto` (HTTP 404, not_found).

## Kod için Öneri
1. **Ready-for-payment health düzeltmesi**
   - Live sağlık metriğini şişirmeden ready_for_payment ürünlerin health sorunlarını da görünür tut. Bu ürünleri ayrı takip et; live outage diye sayma ama 404/401 gibi sonuçları context'e kaybetme.
2. Production'da manuel Vercel/ödeme-provider adımlarını script ile 'çözüldü' gibi göstermeden bırak.
3. Kod değişikliği sonrası summary/context jenerasyonunu tekrar çalıştır; stale rapor bırakma.

## Canonical Drift Ürünleri
- `croncraft` — current=https://quickcron.vercel.app ideal=https://croncraft.vercel.app health=alternate_healthy code=200 probe=https://croncraft.vercel.app canonical_code=200 canonical_status=redirected_preview_alias
- `diffmaster` — current=https://diffmaster-coral.vercel.app ideal=https://diffmaster.vercel.app health=alternate_healthy code=200 canonical_code=401 canonical_status=unauthorized
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app health=alternate_healthy code=200 canonical_code=402 canonical_status=deployment_disabled
- `jwt-generator` — current=https://jwt-generator-rho.vercel.app ideal=https://jwt-generator.vercel.app health=alternate_healthy code=200 canonical_code=500 canonical_status=error_500
- `nginx-config` — current=https://nginx-config-egj3ho5tp-madnessqws-projects.vercel.app ideal=https://nginx-config.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app health=alternate_healthy code=200 canonical_code=500 canonical_status=error_500
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `chmod-calculator` — current=https://chmod-calculator-5atogp6t7-madnessqws-projects.vercel.app ideal=https://chmod-calculator.vercel.app health=alternate_healthy code=200 canonical_code=307 canonical_status=error_307
- `timestamp-converter` — current=https://timestamp-converter-pro.vercel.app ideal=https://timestamp-converter.vercel.app health=alternate_healthy code=200 canonical_code=451 canonical_status=error_451
- `commit-message-generator` — current=https://commit-message-generator-gamma.vercel.app ideal=https://commit-message-generator.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found

## Fallback Alias Ürünleri
- `croncraft` — current=https://quickcron.vercel.app ideal=https://croncraft.vercel.app health=alternate_healthy code=200 probe=https://croncraft.vercel.app canonical_code=200 canonical_status=redirected_preview_alias
- `diffmaster` — current=https://diffmaster-coral.vercel.app ideal=https://diffmaster.vercel.app health=alternate_healthy code=200 canonical_code=401 canonical_status=unauthorized
- `html-entity-encoder` — current=https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app ideal=https://html-entity-encoder.vercel.app health=alternate_healthy code=200 canonical_code=402 canonical_status=deployment_disabled
- `jwt-generator` — current=https://jwt-generator-rho.vercel.app ideal=https://jwt-generator.vercel.app health=alternate_healthy code=200 canonical_code=500 canonical_status=error_500
- `nginx-config` — current=https://nginx-config-egj3ho5tp-madnessqws-projects.vercel.app ideal=https://nginx-config.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `pdf-forge` — current=https://pdf-forge-five.vercel.app ideal=https://pdf-forge.vercel.app health=alternate_healthy code=200 canonical_code=500 canonical_status=error_500
- `webhook-tester` — current=https://webhook-tester-beryl.vercel.app ideal=https://webhook-tester.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- `chmod-calculator` — current=https://chmod-calculator-5atogp6t7-madnessqws-projects.vercel.app ideal=https://chmod-calculator.vercel.app health=alternate_healthy code=200 canonical_code=307 canonical_status=error_307
- `timestamp-converter` — current=https://timestamp-converter-pro.vercel.app ideal=https://timestamp-converter.vercel.app health=alternate_healthy code=200 canonical_code=451 canonical_status=error_451
- `commit-message-generator` — current=https://commit-message-generator-gamma.vercel.app ideal=https://commit-message-generator.vercel.app health=alternate_healthy code=200 canonical_code=404 canonical_status=not_found
- ...

## Ready-for-Payment Health Issues
- `git-workflow-auto` — code=404 status=not_found url=https://git-workflow-auto.vercel.app canonical_url=https://git-workflow-auto.vercel.app canonical_code=404 canonical_status=not_found
