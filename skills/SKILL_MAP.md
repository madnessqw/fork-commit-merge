# SKILL MAP — UniverseCreator Swarm

Her agent, her görev türü için **hangi skill'i nasıl kullanacağını** buradan öğrenir.

---

## Temel Ayrım

| Tür | Konum | Nasıl Kullanılır | Kim Erişir |
|---|---|---|---|
| **Capability Skill** | `~/.claude/skills/` | Claude ortamında otomatik inject. Teammate session'da `available_skills` içinde görünür. | Sadece Claude + Claude teammates |
| **Repo Skill / Tool** | `skills/*.md` veya `skills/<tool>/` | Explicit `cat` veya script çağrısı. | Tüm agent'lar: Claude, Codex, GLM |

> **Kural:** Codex ve GLM için ASLA Claude skill referansı verme. Onlara her zaman repo araçlarını göster.

---

## 1. Araştırma / Keşif

| Görev | Claude Teammates | Codex | GLM |
|---|---|---|---|
| Web araştırma (derin, kapsamlı) | `derin-arastirma` skill (auto-available) | `skills/web_research/` klasörü + curl/ddg | `skills/web_research/` |
| Hızlı web arama | `agent-reach` skill | `skills/curlsearch/` veya `skills/ddg-web-search/` | `skills/ddg-web-search/` |
| Akademik / teknik araştırma | `derin-arastirma` (ArXiv + YouTube adımları dahil) | `skills/web_research/` | `skills/web_research/` |
| Pazar araştırma / rekabet analizi | `derin-arastirma` + `skills/market_research.md` okuma | `skills/market_research.md` | `skills/market_research.md` |
| Proje fikirleri / ilham | `cat sistem-planlama/projeler.txt` + `derin-arastirma` | `cat sistem-planlama/projeler.txt` | `cat sistem-planlama/projeler.txt` |
| Tarihsel araştırma arşivi | `cat sistem-planlama/arastirma*.md` (son 5) | `cat sistem-planlama/arastirma*.md` | `cat sistem-planlama/arastirma*.md` |

### Araştırma Arşivi Nasıl Okunur
```bash
# Son 5 araştırmayı oku (tarihsel bağlam + tekrar önleme)
ls -t /home/gokhan/UniverseCreator/sistem-planlama/arastirma*.md | head -5 | xargs -I{} sh -c 'echo "=== {} ===" && head -30 {}'

# Planlama notlarını oku
ls -t /home/gokhan/UniverseCreator/sistem-planlama/planlama*.md | head -3 | xargs -I{} sh -c 'echo "=== {} ===" && head -20 {}'

# Tüm proje fikirleri
cat /home/gokhan/UniverseCreator/sistem-planlama/projeler.txt
```

---

## 2. Düşünme / Planlama / Sentez

| Görev | Claude Teammates | Codex |
|---|---|---|
| Karmaşık plan üretimi | Yerleşik reasoning (no skill gerekli) | `skills/ultrathink/` referans al |
| Execution planı yazımı | `skills/agents/planner.md` oku | `skills/agents/planner.md` oku |
| Sistem mimarisi çıkarma | `skills/agents/planner.md` oku | `skills/agents/planner.md` oku |
| Strateji / ROI kararı | `skills/agents/strategist.md` oku | `skills/codex_skill.md` → STRATEGY mode |

---

## 3. Kod Yazma / Build

| Görev | Claude Teammates (Builder) | Codex |
|---|---|---|
| Yeni ürün inşası | `skills/agents/builder.md` oku | `skills/codex_skill.md` → EXECUTION mode |
| Build kontrol listesi | `skills/build_checklist.md` oku | `skills/build_checklist.md` oku |
| Code execution / doğrulama | `skills/code_executor/` | Yerleşik (bash, node, python3) |
| Mevcut ürün optimizasyonu | `skills/agents/optimizer.md` oku | `skills/codex_skill.md` → EXECUTION mode |

---

## 4. QA / Test

| Görev | Claude Teammates (QA-Tester) | Codex |
|---|---|---|
| Ürün QA gate | `skills/agents/qa_tester.md` oku | `skills/agents/qa_tester.md` oku (sinyal bekle) |
| Syntax doğrulama | `node --check`, `python3 -m py_compile`, `bash -n` | Aynı |
| Secret scan | `grep -r "sk_\|pk_\|ghp_\|api_key"` | Aynı |
| Vercel deploy testi | `curl -s {url}/api/health` | Aynı |

---

## 5. İçerik / Landing Page

| Görev | Claude Teammates | Codex |
|---|---|---|
| Landing page yazımı | `skills/content_creator/` + `skills/landing_page_template.md` | `skills/landing_page_template.md` |
| SEO / meta tags | `skills/content_creator/` | `skills/landing_page_template.md` SEO bölümü |
| İçerik yayınlama | `skills/content_publisher/` | Direkt deploy script |

---

## 6. Sistem Yönetimi

| Görev | Claude (Orchestrator) | GLM | Codex |
|---|---|---|---|
| Portföy sağlığı | `STATE_SUMMARY.json` oku | `skills/glm_analyst.md` oku | `STATE_SUMMARY.json` oku |
| Run log takibi | `logs/run_ledger.jsonl` | `scripts/ledger_summary.sh` | `logs/run_ledger.jsonl` append |
| Sinyal kontrol | `.signals/` klasörü | `.signals/` klasörü | `.signals/` klasörü |
| Team status | `analysis/team_status.md` | `analysis/team_status.md` | `analysis/team_status.md` |

---

## Mevcut Capability Skills (`~/.claude/skills/`)

> Bu skill'ler sadece Claude ve Claude teammates için geçerlidir.

| Skill Adı | Kullanım | Kim Çağırır |
|---|---|---|
| `derin-arastirma` | Kapsamlı web + ArXiv + YouTube araştırması | Researcher, Strategist |
| `agent-reach` | Hızlı web/sosyal medya arama | Researcher |
| `web-intelligence` | Web sayfası okuma + özetleme | Researcher, Strategist |
| `browser-otomasyonlari` | Sayfa scraping, form doldurma | Codex hariç |
| `orchestrating-swarms` | Multi-agent koordinasyon | Orchestrator (Claude ana) |
| `derin-arastirma` | Araştırma pipeline | Researcher |

---

## Repo Tools (`skills/<tool>/` veya `skills/<tool>.md`)

> Tüm agent'lar bu araçlara erişebilir.

| Araç | Konum | Kim Kullanır |
|---|---|---|
| `web_research` | `skills/web_research/` | Codex (STRATEGY), GLM, Researcher fallback |
| `ddg-web-search` | `skills/ddg-web-search/` | Codex, GLM |
| `curlsearch` | `skills/curlsearch/` | Codex, GLM |
| `code_executor` | `skills/code_executor/` | Builder (Claude), Codex |
| `build_checklist` | `skills/build_checklist.md` | Builder, Codex (pre/post build) |
| `market_research` | `skills/market_research.md` | Strategist, Researcher |
| `landing_page_template` | `skills/landing_page_template.md` | Builder, Codex |
| `ultrathink` | `skills/ultrathink/` | Planner, Codex (SELF-PLAN) |
| `content_creator` | `skills/content_creator/` | Builder (landing page) |
| `economic_protocol` | `skills/economic_protocol/` | Strategist (fiyatlandırma) |
| `task_finisher` | `skills/task_finisher/` | Codex (incomplete task cleanup) |

---

## Hızlı Karar Ağacı

```
Araştırma mı gerekiyor?
  └── Claude teammate misin?
        ├── EVET → /derin-arastirma kullan
        └── HAYIR (Codex/GLM) → skills/web_research/ veya ddg-web-search kullan

Kod yazmak mı gerekiyor?
  ├── Claude Builder → skills/agents/builder.md + build_checklist.md
  └── Codex → codex_skill.md EXECUTION mode + build_checklist.md

Proje fikri mi lazım?
  └── Her zaman: sistem-planlama/projeler.txt + araştırma arşivi oku

Strateji mi gerekiyor?
  ├── Claude Strategist → strategist.md + derin-arastirma
  └── Codex STRATEGY mode → codex_skill.md + sistem-planlama/ okuma

Hangi skill bilinmiyor?
  └── Bu dosyayı (SKILL_MAP.md) oku
```
