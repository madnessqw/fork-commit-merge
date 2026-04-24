# Portfolio Snapshot
**Cycle:** 1109 | **Mode:** OPTIMIZE
**Generated:** 2026-04-24T08:28:43.204597+00:00
**Grade:** A (96.7%)

## Overview
| Metric | Value |
|--------|-------|
| Active | 149 |
| Live | 90 |
| Healthy | 87 |
| Canonical healthy | 83 (92.2%) |
| Fallback healthy | 4 |
| Unhealthy | 3 |
| Checkout gap | 0 |
| Deploy gap | 6 |
| Spec ready | 12 |
| Deploy readiness | 16 |
| Codex handoff | YES |

## Unhealthy Live Products
| Slug | HTTP | Status |
|------|------|--------|
| jwt-generator | 500 | error_500 |
| diffmaster | 401 | unauthorized |
| timestamp-converter | 451 | error_451 |

## Canonical URL Drift
| Slug | Canonical Status | Ideal URL |
|------|-----------------|-----------|
| pdf-forge | error_500 | https://pdf-forge.vercel.app |
| webhook-tester | not_found | https://webhook-tester.vercel.app |
| email-validator-pro | not_found | https://email-validator-pro.vercel.app |
| html-entity-encoder | deployment_disabled | https://html-entity-encoder.vercel.app |

## Deploy Readiness Gap
**16 products** with missing fields:
- **htpasswd-generator** — missing: vercel_url, deployment_url, github_url
- **case-converter-pro** — missing: vercel_url, deployment_url, github_url
- **diff-checker-pro** — missing: vercel_url, deployment_url, github_url
- **mcp-inspector-pro** — missing: vercel_url, deployment_url, webhook_url
- **yaml-validator-pro** — missing: vercel_url, deployment_url, github_url
- **api-mock-generator** — missing: vercel_url, deployment_url, github_url
- **browser-mock-studio** — missing: vercel_url, deployment_url, github_url
- **json-schema-to-ts** — missing: vercel_url, deployment_url, webhook_url
- **docker-run-generator** — missing: vercel_url, deployment_url, github_url
- **subdomain-finder** — missing: vercel_url, deployment_url, github_url
- **favicon-generator-pro** — missing: vercel_url, deployment_url, webhook_url
- **htaccess-generator** — missing: vercel_url, deployment_url, github_url
- **html2markdown** — missing: vercel_url, deployment_url, webhook_url
- **nginx-config-tester** — missing: vercel_url, deployment_url, github_url
- **ssl-cipher-analyzer** — missing: vercel_url, deployment_url, github_url
- **toml-parser** — missing: vercel_url, deployment_url, webhook_url

## Next Actions
1. Fix 3 unhealthy live products
2. Deploy 6 ready products
3. Resolve 4 canonical URL drifts
4. Normalize 4 fallback alias products
