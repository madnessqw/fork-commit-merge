# Capability Engineering Checklist
**Version:** 1.0 | **Owner:** toolsmith

## Amaç
Sistemin eksik capability yüzeylerini tespit etmek, güvenli şekilde kurmak ve kayıt altına almak.

## Capability Loop Checklist
- [ ] Sorunu sınıflandır: credential blocker / infra bug / product bug / state drift / capability gap
- [ ] Capability gap değilse doğru owner'a geri yönlendir
- [ ] Gerekirse researcher'dan `/derin-arastirma` ile çözüm araştırması iste
- [ ] Yeni MCP/plugin/tool/script gerçekten gerekli mi doğrula
- [ ] Kurulum veya yazım sonrası smoke test yap
- [ ] `config/capabilities.json` güncelle
- [ ] `issues/issues.jsonl` kaydı yaz
- [ ] Reload gerekiyorsa `restart_required` kaydı üret
- [ ] Kullanan agent'lara kısa kullanım notu bırak

## Restart Required Koşulları
- yeni MCP/plugin/skill kurulduysa
- settings uyumu değiştiyse
- aynı agent eski capability yüzeyiyle çalışmaya devam ediyorsa

## YAPMA
- Sağlıklı agent'ı keyfi kapatma
- Smoke test yapmadan capability'yi hazır sayma
- Registry güncellemeden kurulumu bitmiş sayma
