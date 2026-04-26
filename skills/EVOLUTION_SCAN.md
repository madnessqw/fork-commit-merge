# EVOLUTION SCAN — UniverseCreator Capability Engineering
**Version:** 2.1 | **Owner:** toolsmith | **Cycle:** Her cycle okunur (sadece scan)

> projeler.txt tara + gap tespit. Gap varsa: `cat skills/EVOLUTION_INSTALL.md` (18K kurulum prosedürleri)

> **ASLA mevcut sağlıklı capability'leri bozmadan yeni olanları ekle.**
> **HER işlem sonrası team-lead'e Teammate() ile raporla.**

---

## 🔴 ZORUNLU İLK ADIM — projeler.txt'yi Tara

Araştırmaya başlamadan önce kullanıcının araştırma notlarını tara:

```bash
cd /home/gokhan/UniverseCreator

# En önemli projeler ([***] işaretli):
grep "\[\*\*\*\]" projeler.txt

# Önemli projeler ([**] işaretli):
grep "\[\*\*\]" projeler.txt

# MCP/agent/skill ile ilgili notlar:
grep -i "mcp\|skill\|agent\|tool" projeler.txt | grep "\[" | head -30

# Belirli konuda ara:
grep -B1 -A3 "fastmcp\|n8n-mcp\|playwright\|browser" projeler.txt | head -60
```

**Bu notlardan ne çıkar:**
- Yeni kurulacak MCP fikirleri → `capabilities.json`'a gap ekle
- Kullanıcının ilgilendiği frameworks → araştır, dene
- `[***]` projeler kullanıcının en çok ilgilendiği → bu konuda yeni yetenekler kazan
- Mevcut gapleri projeler.txt'deki çözümlerle eşleştir

---

## NASIL ÇALIŞIR

Evrim döngüsü her cycle'da şu sırayla çalışır:

```
0. projeler.txt TARA    → [***]/[**] projeleri oku, yeni gap fikirleri çıkar
1. GAP TESPİT           → capabilities.json'daki "gaps" listesini oku
2. SINIFLANDIR          → Gerçekten capability gap mi, yoksa başka sorun mu?
3. ARAŞTIR              → Çözüm için web/GitHub/npm araştır
4. KUR                  → npm/pip/uv ile yükle VEYA skill dosyası yaz
5. KAYDET               → ~/.claude/settings.json + capabilities.json güncelle
6. TEST                 → Smoke test yap; geçerse "healthy" yap
7. TEAM-LEAD'E RAPOR    → Teammate() ile team-lead'e raporla (format aşağıda)
8. NOTLA                → restart_required varsa yaz, agent'lara bildir
```

---

## GAP TESPİT SİSTEMİ

### 1. capabilities.json'u Oku
```bash
cat /home/gokhan/UniverseCreator/config/capabilities.json | python3 -m json.tool
```

`gaps` dizisindeki her nesneye bak:
- `"status": "pending"` → **ÇÖZÜLECEK**
- `"status": "blocked"` → `"note"` alanını oku, sebebini anla
- `"status": "wont_fix"` → Atla

### 2. Gap Türlerini Sınıflandır

| Tür | Belirti | Çözüm |
|-----|---------|-------|
| `mcp_missing` | Bir araç erişilemiyor, tool bulunamıyor | MCP kur, settings'e ekle |
| `skill_missing` | Tekrar eden görevde rehber yok | Yeni .md skill dosyası yaz |
| `script_missing` | Otomasyon scriptine ihtiyaç var | scripts/ altına yaz |
| `credential_blocker` | API key eksik, token geçersiz | USER.md veya gokhan'a sor |
| `infra_bug` | Deploy/build hatası | builder/deploy skill'ini güncelle |
| `state_drift` | STATE.json tutarsız | STATE.json'u düzelt |

### 3. Gerçek Gap mi Kontrol Et
Bir şeyi kurmadan önce şunu sor:
- Bu capability zaten var mı? (`cat ~/.claude/settings.json | grep -i "<tool_name>"`)
- Bu işi halihazırda başka bir araç yapıyor mu?
- Bu gerçekten gerekli mi, yoksa nice-to-have mi?

---
