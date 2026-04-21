# Sorun Analizi — Cycle 1063 | 2026-04-21 21:06 UTC

## Ana Darboğaz
- **checkout_field_inconsistency** — Canlı checkout gap sıfır olsa da metadata hâlâ üç farklı alan adıyla taşınıyor; bu state drift'i ve gelecekte yanlış rapor üretir.

## Summary'den Gelen Gerçekler
- Healthy live: 113/113
- Checkout gap: 0
- Deploy/url gap: 18
- Spec-ready backlog: 27

## URL/Deploy Eksikleri
- ssl-cert-checker, security-headers-checker, subdomain-finder, htaccess-generator, nginx-config-tester, ssl-cipher-analyzer, diff-checker-pro, yaml-validator-pro, case-converter-pro, htpasswd-generator, docker-run-generator, sql-to-nosql, ...

## Açık Issue Kayıtları
- **state_drift** [high/in_progress] — STATE.json cycle 759, loop log cycle 28, capture files only cycle 9 - critical state sync drift
- **agent_missing** [high/in_progress] — Toolsmith agent not spawned despite capability gap identified
- **checkout_field_inconsistency** [medium/open] — Multiple checkout_url field names (checkout_url, lemon_checkout_url, lemonsqueezy_checkout_url)

## Not
- Bu dosya live `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.
- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.
