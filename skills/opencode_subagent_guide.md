# OpenCode Subagent Rehberi — GLM Micro-Coder İçin

> Bu dosyayı GLM her cycle'da okur. Subagent spawn kararlarını buna göre verir.
> **MAX 2 paralel subagent** kuralı — aynı cycle'da daha fazlası yasak.

---

## Kategori: DEVELOPMENT — Kod Yazma & Refactor

| Durum | Kullanılacak Agent |
|---|---|
| React/UI component yazılacak | `@frontend-developer` |
| API / backend logic yazılacak | `@backend-architect` |
| Script / automation yazılacak | `@senior-developer` |
| AI/LLM entegrasyonu yapılacak | `@ai-engineer` |
| Mobile app geliştirilecek | `@mobile-app-builder` |
| Oyun scripti yazılacak | `@roblox-systems-scripter` / `@godot-gameplay-scripter` |
| Basit CRUD / utility kod | `@senior-developer` |

---

## Kategori: REVIEW — Kod İnceleme & Kalite

| Durum | Kullanılacak Agent |
|---|---|
| Syntax / logic review (commit öncesi) | `@code-reviewer` |
| Güvenlik açığı taraması | `@security-auditor` |
| OWASP Top 10 kontrolü | `@security-auditor` |
| Kanıt toplama / doğrulama | `@evidence-collector` |
| Gerçeklik kontrolü (reality check) | `@reality-checker` |
| Performans / load test review | `@performance-benchmarker` |
| API endpoint testi | `@api-tester` |
| Ergonomics / UX incelemesi | `@ux-researcher` |

---

## Kategori: RESEARCH — Araştırma & Keşif

| Durum | Kullanılacak Agent |
|---|---|
| Pazar / rakip araştırması | `@trend-researcher` |
| Derin teknik araştırma | `@ai-engineer` |
| Rakip analizi | `@trend-researcher` |
| Akademik / teorik araştırma | `@historian` (data research) |
| LinkedIn / sosyal medya trend | `@linkedin-content-creator` |
| Bilibili / video platform trend | `@bilibili-content-strategist` |
| TikTok / kısa video trend | `@tiktok-strategist` |
| E-ticaret pazar araştırması | `@china-e-commerce-operator` |

---

## Kategori: ARCHITECTURE — Sistem Tasarımı & Planlama

| Durum | Kullanılacak Agent |
|---|---|
| Yeni sistem mikro-mimarisi | `@software-architect` |
| İş akışı / workflow tasarımı | `@workflow-architect` |
| API tasarımı | `@backend-architect` |
| Veritabanı şeması / optimizasyon | `@database-optimizer` |
| Frontend mimarisi | `@frontend-developer` |
| Deployment pipeline tasarımı | `@devops-automator` |
| Büyük görev breakdown | `@planner` (Claude teammate — buraya yazılabilir) |
| Sprint / proje planlaması | `@sprint-prioritizer` |

---

## Kategori: DEVOPS — Altyapı & Operasyon

| Durum | Kullanılacak Agent |
|---|---|
| CI/CD pipeline kurulumu | `@devops-automator` |
| Kubernetes / container yönetimi | `@infrastructure-maintainer` |
| Site reliability / health monitoring | `@sre-site-reliability-engineer` |
| Log analizi / debugging | `@devops-troubleshooter` |
| Performans izleme | `@performance-benchmarker` |
| Güvenlik hardening | `@security-engineer` |

---

## Kategori: PRODUCT — Ürün & İş Geliştirme

| Durum | Kullanılacak Agent |
|---|---|
| Ürün stratejisi | `@product-manager` |
| UX araştırması | `@ux-researcher` |
| UI tasarımı | `@ui-designer` |
| A/B test planlaması | `@experiment-tracker` |
| KPI belirleme | `@analytics-reporter` |
| Satış pipeline analizi | `@pipeline-analyst` |
| Müşteri kazanım stratejisi | `@outbound-strategist` |

---

## Kategori: TESTING — Kalite & Doğrulama

| Durum | Kullanılacak Agent |
|---|---|
| API fonksiyonel testi | `@api-tester` |
| Load / stress test | `@performance-benchmarker` |
| Test sonuçları analizi | `@test-results-analyzer` |
| QA süreç tasarımı | `@test-automator` |
| Regresyon test planı | `@test-results-analyzer` |
| Accessibility test | `@accessibility-auditor` |

---

## Kategori: CONTENT — İçerik & Yazım

| Durum | Kullanılacak Agent |
|---|---|
| Teknik dokümantasyon | `@technical-writer` |
| Landing page içeriği | `@content-creator` |
| Pazarlama metni | `@ad-creative-strategist` |
| Sosyal medya içeriği | `@social-media-strategist` |
| Görsel anlatım | `@visual-storyteller` |
| Akademik yazım | `@academic-writer` |
| LinkedIn içeriği | `@linkedin-content-creator` |

---

## Karar Protokolü — GLM Nasıl Seçim Yapar?

```
1. SORUN TİPİNİ BELİRLE
   ├── Kod yazma / refactor → DEVELOPMENT
   ├── Syntax / mantık hatası → REVIEW → @code-reviewer
   ├── Güvenlik şüphesi → REVIEW → @security-auditor
   ├── Araştırma / keşif → RESEARCH
   ├── Sistem tasarımı → ARCHITECTURE
   ├── Altyapı / deploy → DEVOPS
   ├── Ürün kararı → PRODUCT
   ├── Test / kalite → TESTING
   └── İçerik / metin → CONTENT

2. ÖNCELİK SIRALAMASI YAP (MAX 2)
   En kritik 2 agent seç. Daha fazla gerekiyorsa cycle'a bırak.

3. SPAWN ETMEDEN ÖNCE DOĞRULA
   "@<agent> [görev]" formatında yaz.
   Örnek: @code-reviewer review commit 2008229 for syntax errors
   Örnek: @sre-site-reliability-engineer diagnose jwt-generator HTTP 500

4. SONUCU KAYDET
   Agent çıktısını analysis/ altına yaz veya direkt kullan.
```

---

## Hızlı Referans Tablosu (En Sık Kullanılan)

| Kısa tanım | Agent |
|---|---|
| Kod/syntax hatası | `@code-reviewer` |
| Unhealthy ürün teşhisi | `@sre-site-reliability-engineer` |
| Veri tutarlılığı (149 ürün) | `@database-optimizer` |
| SEO / deploy gap | `@search-query-analyst` |
| Trend / pazar araştırması | `@trend-researcher` |
| Sistem verimliliği | `@workflow-optimizer` |
| Güvenlik açığı şüphesi | `@security-auditor` |
| Run ledger analizi | `@analytics-reporter` |
| Yeni API tasarımı | `@backend-architect` |
| Landing page içeriği | `@content-creator` |

---

## Evolve Kuralları

- **MAX 2 paralel subagent** — 3+ gerekiyorsa öncelik sırala, cycle'a bırak
- **Cheap first, expensive later** — `@trend-researcher` yerine önce `@search-query-analyst` dene
- **Spawn etmeden önce sor**: "Bu agent'ı Spawn etmek yerine kendim yapabilir miyim?"
- **Sonuç kullanılmalı** — agent çıktısı boşta kalmamalı, ya dosyaya yazılır ya da direkt uygulanır
- **Fail durumunda**: agent başarısız olursa kendin devam et, ikinci agent spawn etme

---

## Örnek GLM Kullanımı

```
# Cycle başı — kritik sorun tespiti
@sre-site-reliability-engineer diagnose why diffmaster returns HTTP 401

# Aynı cycle — veri kontrolü
@database-optimizer audit product.json vs spec.json consistency across 149 products

# Commit öncesi (bir sonraki cycle)
@code-reviewer review changes in commit 2008229

# Pazar araştırması gerektiğinde
@trend-researcher research competitors for timestamp-converter
```

---

**Son güncelleme:** 2026-04-24 — İlk versiyon, 100+ agent kategorize edildi
