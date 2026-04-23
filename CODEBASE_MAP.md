# CODEBASE_MAP.md — UniverseCreator

**Otonom dijital ürün fabrikası.** Her cycle: araştır → inşa et → Vercel'e deploy et → LemonSqueezy'de sat.
Cycle 1108 itibarıyla: 144 aktif, 88 canlı, 85 sağlıklı (%96.6).
Codex ve subagentler bu dosyadan context alır — tam repo scan yapmadan.

---

## 📁 Klasör Yapısı

| Klasör | Ne İşe Yarar |
|---|---|
| `products/<slug>/` | Her ürün kendi klasöründe. `product.json` + kaynak kod + `spec.json` |
| `scripts/` | Bash/Python otomasyon scriptleri (loop, deploy, SEO) |
| `skills/` | Skill tanımları + subagent rolleri |
| `skills/agents/` | Agent rol kartları (analyst, builder, optimizer, researcher, toolsmith) |
| `analysis/` | Codex task dosyaları, sorun analizleri, Vercel audit JSON'ları |
| `research/` | Cycle bazlı fırsat araştırma dosyaları |
| `logs/` | Loop logları, hata logları, agent notları |
| `.signals/` | Loop PID, status, health.json, universe_loop.lock |
| `memory/` | Günlük hafıza notları (`YYYY-MM-DD.md`) |
| `plans/` / `tasks/` / `issues/` | Planlama ve takip dosyaları |
| `config/` | `capabilities.json` — MCP/skill durumu |
| `prompts/` | `codex_prompt.txt` — codex_loop'un çalıştırdığı prompt |

---

## 🗂 Kritik Dosyalar

| Dosya | Ne İşe Yarar | Okuyan | Yazan |
|---|---|---|---|
| `STATE.json` | Ana durum: cycle no, tüm ürünler, mod, bakiye | Her agent (ilk okuma) | `scripts/update_state.py`, deploy scriptleri |
| `STATE_SUMMARY.json` | Özet istatistikler (live count, spec_ready vb.) | Codex, analyst | `scripts/update_summary.py` |
| `WALLET.json` | Gelir/gider bakiyesi | Ana loop, FACTORY | `update_wallet.py` |
| `SESSION.md` | Önceki cycle durumu, devam noktası | Her session başında | Ana agent, sonunda günceller |
| `SOUL.md` | Kim olduğu, misyon, kurallar | İlk boot'ta okunur | Manuel |
| `MEMORY.md` | Uzun vadeli kurumsal hafıza | Ana session | Ana agent (heartbeat'te) |
| `HEARTBEAT.md` | Heartbeat checklist ve reminders | Heartbeat trigger'da | Ana agent |
| `skills/FACTORY.md` | **Ana çalışma talimatları** — her cycle'ın kutsal kitabı | Her session başı | Manuel |
| `skills/EVOLUTION.md` | Capability engineering, yeni skill ekleme protokolü | toolsmith agent | toolsmith |
| `products/CATALOG.md` | Ürün kataloğu özeti | Analyst, codex | Deploy scriptleri |
| `prompts/codex_prompt.txt` | Codex loop'a gönderilen prompt | `codex_loop.sh` | Manuel / toolsmith |
| `logs/codex_loop.log` | Codex cycle çıktıları | Debug için | `codex_loop.sh` |
| `logs/structured.jsonl` | Yapılandırılmış event log | Analytics | Tüm scriptler |

---

## ⚙️ scripts/ Özeti

| Script | Ne Yapar |
|---|---|
| `codex_loop.sh` | Her 35 dakikada cron çalışır. Codex'i `codex_prompt.txt` ile başlatır. Singleton lock. |
| `glm_loop.sh` | GLM tabanlı alternatif loop (parallel çalışır) |
| `create_product.sh` | `<slug>` alır, `products/<slug>/` klasörü oluşturur, şablondan `product.json` + `api/` + `public/` yaratır |
| `deploy_product.sh` | `<slug>` alır: git push → Vercel deploy → Telegram bildirim → STATE.json günceller |
| `health_check.py` | Canlı ürünleri kontrol eder, `STATE_SUMMARY.json` günceller |
| `update_state.py` | STATE.json'u güvenli şekilde günceller |
| `update_summary.py` | STATE_SUMMARY.json'u STATE.json'dan hesaplar |
| `seo_optimize_auto.py` | Canlı ürünlerin meta/SEO'sunu otomatik optimize eder |
| `batch_seo_update.py` | Toplu SEO güncellemesi |
| `product_state_sync.py` | Vercel ↔ STATE.json senkronizasyonu |
| `codex_auth_manager.py` | Codex multi-account auth state yönetimi |
| `deploy_readiness.py` | Spec-ready ürünlerin deploy hazırlık kontrolü (read-only) |
| `qa_dispatch.py` | qa_pending sinyalini qa-tester inbox'ına yönlendirir |
| `checkout_metadata.py` | Checkout metadata yardımcı fonksiyonları |
| `standardize_checkout_fields.py` | Ürün checkout alanlarını standardize eder |
| `audit_portfolio_health.py` | Backward-compat health audit entrypoint |
| `log_rotation.sh` | Log dosyalarını sıkıştırır/temizler |

---

## 🎯 skills/ Özeti

### Agent Rolleri (`skills/agents/`)
| Agent | Rolü |
|---|---|
| `builder.md` | Spec'ten çalışan Vercel ürünü inşa eder |
| `analyst.md` | Portföy analizi, fırsat/sorun tespiti |
| `optimizer.md` | Canlı ürünleri iyileştirir, sağlık sorunlarını çözer |
| `researcher.md` | Pazar araştırması, yeni ürün fırsatları bulur |
| `toolsmith.md` | Yeni skill/capability ekler, sistemi geliştirir |

### Temel Skill'ler (`skills/`)
| Skill | Açıklama |
|---|---|
| `FACTORY.md` | **Ana çalışma protokolü** — sıfır menü, tam otomasyon |
| `EVOLUTION.md` | Capability engineering protokolü |
| `web_research/` | DuckDuckGo + Jina Reader ile web araması |
| `bounty_hunter/` | GitHub bounty/PR fırsatları tarama |
| `task_finisher/` | Yarım kalan görevleri tamamlama protokolü |
| `content_creator/` | Ürün için landing page / blog içeriği |
| `code_executor/` | Güvenli kod çalıştırma |
| `ultrathink/` | Derin analiz modu |

---

## 🔄 Anahtar Akış: Ürün Nasıl Oluşturulur?

```
1. ARAŞTIRMA
   researcher agent → research/<cycle>_opportunities.md
   Değerlendirme kriterleri: feasibility, mvp_complexity, price, demand

2. SPEC OLUŞTURMA
   → products/<slug>/spec.json  (araştırma çıktısı)
   İçerik: name, tagline, slug, tech_stack, features, price_justification

3. İNŞA
   scripts/create_product.sh <slug> "<Name>" "<Desc>" "<Price>"
   → products/<slug>/
       ├── product.json      (meta: name, slug, price, status, urls)
       ├── index.html        (landing page)
       ├── vercel.json       (deploy config)
       ├── api/index.js      (backend endpoint)
       └── public/           (static assets)

4. DEPLOY
   scripts/deploy_product.sh <slug>
   → git push → github.com/universe7creator/<slug>
   → vercel deploy → <slug>.vercel.app
   → STATE.json güncellenir (status: "live", vercel_url set)

5. CHECKOUT
   LemonSqueezy'de ürün linki → product.json checkout_url alanına yazılır
   → STATE_SUMMARY.json güncellenir

6. OPTİMİZASYON
   optimizer agent → seo_optimize_auto.py → health_check.py
   → logs/structured.jsonl event kaydı
```

---

## 📊 Mevcut Durum (Cycle 1108)

| Metrik | Değer |
|---|---|
| Toplam ürün | 144 aktif |
| Canlı (live) | 88 |
| Sağlıklı | 85 (%96.6) |
| Unhealthy | 3 (jwt-generator, diffmaster, timestamp-converter) |
| Canonical drift | 4 (pdf-forge, webhook-tester, email-validator-pro, html-entity-encoder) |
| Deploy gap | 20 |
| Spec hazır | 26 |
| Mod | `OPTIMIZE` |
