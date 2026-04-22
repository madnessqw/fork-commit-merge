#!/usr/bin/env python3
"""Refresh Codex context artifacts from live state.

Codex automation was reading stale analysis notes and even a missing root
`sorun_analizi.md`. This script rebuilds the Codex-facing analysis files from
the current STATE_SUMMARY snapshot plus unresolved issues, so the next run gets
fresh context instead of archaeology.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.product_state_sync import load_product_catalog
from scripts.update_summary import build_summary


SUMMARY_FILE = ROOT / "STATE_SUMMARY.json"
STATE_FILE = ROOT / "STATE.json"
ISSUES_FILE = ROOT / "issues" / "issues.jsonl"
ANALYSIS_DIR = ROOT / "analysis"
ONERI_FILE = ANALYSIS_DIR / "oneri.md"
SORUN_FILE = ANALYSIS_DIR / "sorun_analizi.md"
CODEX_TASK_FILE = ANALYSIS_DIR / "codex_task.md"

RESOLVED_STATUSES = {"resolved", "closed", "done"}


@dataclass(frozen=True)
class Focus:
    key: str
    title: str
    summary: str
    codex_task_title: str
    codex_task_body: str


def _write_summary(summary: dict[str, Any], path: Path | None = None) -> None:
    if path is None:
        path = SUMMARY_FILE
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def refresh_live_health() -> None:
    """Run the live health audit before rebuilding Codex context."""
    audit_script = ROOT / "scripts" / "audit_portfolio_health.py"
    try:
        subprocess.run([sys.executable, str(audit_script)], cwd=ROOT, check=False)
    except OSError as exc:
        print(f"[refresh_codex_context] health audit skipped: {exc}", file=sys.stderr)


def load_summary() -> dict[str, Any]:
    refresh_live_health()
    if SUMMARY_FILE.exists():
        try:
            summary = json.loads(SUMMARY_FILE.read_text(encoding="utf-8"))
            if isinstance(summary, dict):
                return summary
        except json.JSONDecodeError:
            pass

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    summary = build_summary(state, product_catalog=load_product_catalog(), raw_state=state)
    _write_summary(summary)
    return summary


def load_unresolved_issues(path: Path = ISSUES_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    issues: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        status = str(item.get("status", "")).strip().lower()
        if status in RESOLVED_STATUSES:
            continue
        issues.append(item)
    return issues


def _health_percent(summary: dict[str, Any]) -> float:
    live_count = int(summary.get("live_count", 0) or 0)
    healthy_count = int(summary.get("healthy_count", 0) or 0)
    if live_count <= 0:
        return 0.0
    return healthy_count / live_count * 100


def _issue_map(issues: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for issue in issues:
        issue_type = str(issue.get("issue_type", "unknown")).strip() or "unknown"
        grouped.setdefault(issue_type, []).append(issue)
    return grouped


def determine_focus(summary: dict[str, Any], issues: list[dict[str, Any]]) -> Focus:
    grouped = _issue_map(issues)
    unhealthy_live = list(summary.get("gaps", {}).get("unhealthy_live", []))
    pending_health = list(summary.get("gaps", {}).get("pending_health", []))
    missing_checkout = list(summary.get("gaps", {}).get("missing_checkout", []))
    missing_url = list(summary.get("gaps", {}).get("missing_url", []))
    canonical_drift = list(summary.get("gaps", {}).get("canonical_url_drift", []))
    deploy_readiness = list(summary.get("gaps", {}).get("deploy_readiness", []))

    if unhealthy_live:
        sample = unhealthy_live[0]
        slug = sample.get("slug") or "unknown"
        code = sample.get("code")
        drift_count = len(canonical_drift)
        pending_clause = (
            f" Ayrıca {len(pending_health)} canlı ürün health snapshot bekliyor."
            if pending_health
            else ""
        )
        pending_body = (
            f" {len(pending_health)} ürün health snapshot bekliyor; onları outage diye sayma."
            if pending_health
            else ""
        )
        drift_clause = (
            f" Ayrıca {drift_count} canlı ürün fallback alias ile ayakta."
            if drift_count
            else ""
        )
        drift_body = (
            f" Şu an {drift_count} ürün fallback alias ile canlı; manuel Vercel korumasını "
            "çözüldü gibi gösterme."
            if drift_count
            else " Canonical drift yok; gerçek HTTP 404/402 outage'larını doğrula."
        )
        return Focus(
            key="live_health",
            title="Canlı sağlık açığı",
            summary=(
                f"{len(unhealthy_live)} canlı ürün gerçekten sağlıksız.{pending_clause}"
                f"{drift_clause} İlk örnek `{slug}` (HTTP {code})."
            ),
            codex_task_title=(
                "Health/canonical drift düzeltmesi"
                if drift_count
                else "Canlı sağlık açığını düzelt"
            ),
            codex_task_body=(
                "Canlı ürünlerin health alanları ile canonical/vercel URL gerçekliğini "
                "senkron tutan scripti güçlendir."
                f"{pending_body}"
                f"{drift_body} Önce mevcut health pipeline'ını oku, sonra yalnız otomasyon "
                "tarafını düzelt."
            ),
        )

    if pending_health:
        sample = pending_health[0]
        slug = sample.get("slug") or "unknown"
        return Focus(
            key="health_pending",
            title="Health metadata bekliyor",
            summary=f"{len(pending_health)} canlı ürün health snapshot bekliyor; ilk örnek `{slug}`.",
            codex_task_title="Health snapshot senkronizasyonu",
            codex_task_body=(
                "Canlı ürünlerin health snapshot'ını summary/state tarafında ayrı takip et. "
                "Eksik health metadata'yı outage diye sayma; önce health pipeline'ını çalıştırıp sonuçları geri yaz."
            ),
        )

    if missing_checkout:
        return Focus(
            key="checkout_gap",
            title="Checkout kapsam boşluğu",
            summary=f"{len(missing_checkout)} live/ready_for_payment ürün checkout URL'siz.",
            codex_task_title="Checkout alan standardizasyonu",
            codex_task_body=(
                "Checkout metadata okumayı tek kanala indir. `checkout_url`, "
                "`lemon_checkout_url` ve `lemonsqueezy_checkout_url` varyantlarını güvenli biçimde "
                "normalize eden utility/script yaz veya mevcut akışı düzelt. Production checkout URL'lerini uydurma."
            ),
        )

    if canonical_drift:
        sample = canonical_drift[0]
        slug = sample.get("slug") or "unknown"
        current_url = sample.get("url") or sample.get("current_url") or "unknown"
        ideal_url = sample.get("ideal_url") or sample.get("canonical_url") or "unknown"
        return Focus(
            key="canonical_url_drift",
            title="Canonical URL drift",
            summary=(
                f"{len(canonical_drift)} live ürün canonical URL'den sapmış; "
                f"ilk örnek `{slug}` ({current_url} → {ideal_url})."
            ),
            codex_task_title="Canonical URL drift düzeltmesi",
            codex_task_body=(
                "Live ürünlerin public URL'si ile ideal canonical URL'sini aynı tut. "
                "Önce health pipeline'ını ve summary sync'ini doğrula; "
                "alias/redirect farkını manuel Vercel fix gibi saklamaya çalışma."
            ),
        )

    if deploy_readiness:
        sample = deploy_readiness[0]
        slug = sample.get("slug") or "unknown"
        manifest_problem = sample.get("manifest_problem")
        manifest_missing = ", ".join(sample.get("missing_manifest_fields", [])) or "none"
        url_missing = ", ".join(sample.get("missing_url_fields", [])) or "none"
        state_missing = ", ".join(sample.get("missing_state_fields", [])) or "none"
        manifest_clause = (
            f" manifest={manifest_problem}"
            if manifest_problem
            else f" manifest eksikleri: {manifest_missing}"
        )
        return Focus(
            key="deploy_readiness",
            title="Spec-ready deploy readiness gap",
            summary=(
                f"{len(deploy_readiness)} spec-ready ürün hâlâ deploy-ready değil; "
                f"ilk örnek `{slug}`{manifest_clause}."
            ),
            codex_task_title="Spec-ready deploy readiness doğrulaması",
            codex_task_body=(
                "Spec-ready ürünleri deploy-ready saymadan önce read-only bir validator ile tara. "
                "Eksik manifest/URL/state alanlarını raporla; manuel Vercel/LemonSqueezy adımlarını "
                "çözülmüş gibi yazma. "
                f"İlk örnekte manifest eksikleri: {manifest_missing}; URL eksikleri: {url_missing}; "
                f"state eksikleri: {state_missing}."
            ),
        )

    if grouped.get("checkout_field_inconsistency"):
        return Focus(
            key="checkout_field_inconsistency",
            title="Checkout field drift",
            summary=(
                "Canlı checkout gap sıfır olsa da metadata hâlâ üç farklı alan adıyla taşınıyor; "
                "bu state drift'i ve gelecekte yanlış rapor üretir."
            ),
            codex_task_title="Checkout metadata standardizasyonu",
            codex_task_body=(
                "Product metadata için tek okuma/yazma sözleşmesi oluştur. Küçük ama kalıcı fix hedefle: "
                "normalizer, migration helper veya doğrulama testi ekle. Live checkout coverage'ı bozma."
            ),
        )

    if missing_url:
        return Focus(
            key="deploy_backlog",
            title="Spec-ready deploy backlog",
            summary=(
                f"{len(missing_url)} ürünün deploy/canonical URL'si yok. Canlı portföy sağlıklı, "
                "yani bu bir live outage değil; deploy hazırlık/backlog problemi."
            ),
            codex_task_title="Spec-ready deploy hazırlık otomasyonu",
            codex_task_body=(
                "Spec-ready ürünler için deploy readiness kontrolünü otomatikleştir. "
                "Eksik manifest/URL/state alanlarını raporlayan güvenli bir doğrulama katmanı ekle; "
                "token veya manuel deploy gerektiren adımları sahte tamamlandı göstermeden bırak."
            ),
        )

    if grouped.get("state_drift"):
        return Focus(
            key="state_drift",
            title="State drift riski",
            summary="Canlı portföy iyi görünse de açık issue kaydı state drift'in tekrar ettiğini söylüyor.",
            codex_task_title="State/summary guard'ı sertleştirme",
            codex_task_body=(
                "STATE ve summary katmanlarının birbirini yalanlamasını zorlaştıran test/guard ekle. "
                "Hardcoded cycle/script drift'lerini temizle, destructive overwrite yapma."
            ),
        )

    return Focus(
        key="context_freshness",
        title="Context freshness",
        summary="Canlı portföy stabil; asıl risk stale analiz/prompt dosyalarının yanlış karar üretmesi.",
        codex_task_title="Kod ajanı context tazeleme otomasyonu",
        codex_task_body=(
            "Codex'in okuduğu prompt ve analiz dosyalarını live state'ten otomatik üreten küçük bir pipeline kur. "
            "Amaç: gelecekte codex eski raporlarla saçmalamasın."
        ),
    )


def top_issues(issues: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}

    def sort_key(item: dict[str, Any]) -> tuple[int, str]:
        severity = str(item.get("severity", "low")).lower()
        ts = str(item.get("ts", ""))
        return (severity_rank.get(severity, 9), ts)

    return sorted(issues, key=sort_key)[:limit]


def render_oneri(summary: dict[str, Any], issues: list[dict[str, Any]], focus: Focus, now: datetime) -> str:
    health_percent = _health_percent(summary)
    unresolved = top_issues(issues)
    canonical_drift = list(summary.get("gaps", {}).get("canonical_url_drift", []))
    pending_health = list(summary.get("gaps", {}).get("pending_health", []))
    deploy_readiness = list(summary.get("gaps", {}).get("deploy_readiness", []))
    lines = [
        f"# Codex Analiz Özeti — {now.strftime('%Y-%m-%d %H:%M')} UTC",
        "",
        "## Canlı State",
        f"- Cycle: **{summary.get('cycle')}**",
        f"- Mode: **{summary.get('mode')}**",
        f"- Live sağlık: **{summary.get('healthy_count')}/{summary.get('live_count')}** (%{health_percent:.1f})",
        f"- Health pending: **{summary.get('pending_health_count', 0)}**",
        f"- Checkout gap: **{summary.get('checkout_gap_count')}**",
        f"- Deploy readiness gap: **{summary.get('deploy_readiness_count', 0)}**",
        f"- Deploy/url gap: **{summary.get('deploy_missing_or_bad_url')}**",
        f"- Canonical drift: **{summary.get('canonical_url_drift', 0)}**",
        f"- Spec-ready: **{summary.get('spec_ready_count')}**",
        f"- Next action: `{summary.get('next_action')}`",
        "",
        "## Ana Darboğaz",
        f"- **{focus.title}:** {focus.summary}",
        "",
        "## Kod için Öneri",
        f"1. **{focus.codex_task_title}**",
        f"   - {focus.codex_task_body}",
        "2. Production'da manuel Vercel/LemonSqueezy adımlarını script ile 'çözüldü' gibi göstermeden bırak.",
        "3. Kod değişikliği sonrası summary/context jenerasyonunu tekrar çalıştır; stale rapor bırakma.",
    ]

    if unresolved:
        lines.extend(["", "## Açık Issue Sinyalleri"])
        for issue in unresolved:
            lines.append(
                f"- **{issue.get('issue_type')}** [{issue.get('severity')}/{issue.get('status')}] — {issue.get('description')}"
            )

    if canonical_drift:
        lines.extend(["", "## Canonical Drift Ürünleri"])
        for item in canonical_drift[:10]:
            lines.append(
                f"- `{item.get('slug')}` — current={item.get('url')} ideal={item.get('ideal_url')}"
            )

    if pending_health:
        lines.extend(["", "## Health Bekleyen Ürünler"])
        for item in pending_health[:10]:
            lines.append(
                f"- `{item.get('slug')}` — status={item.get('health_status')} url={item.get('url')}"
            )

    if deploy_readiness:
        lines.extend(["", "## Deploy Readiness Issues"])
        lines.append(
            f"- Count: **{summary.get('deploy_readiness_count', len(deploy_readiness))}** "
            f"| Manifest gaps: **{summary.get('deploy_readiness_manifest_gap_count', 0)}** "
            f"| URL gaps: **{summary.get('deploy_readiness_url_gap_count', 0)}** "
            f"| State gaps: **{summary.get('deploy_readiness_state_gap_count', 0)}**"
        )
        for item in deploy_readiness[:10]:
            manifest_problem = item.get("manifest_problem")
            manifest_missing = ", ".join(item.get("missing_manifest_fields", [])) or "none"
            url_missing = ", ".join(item.get("missing_url_fields", [])) or "none"
            state_missing = ", ".join(item.get("missing_state_fields", [])) or "none"
            manifest_suffix = f" manifest={manifest_problem}" if manifest_problem else ""
            lines.append(
                f"- `{item.get('slug')}`{manifest_suffix} — manifest={manifest_missing}; "
                f"url={url_missing}; state={state_missing}"
            )

    missing_url = list(summary.get("gaps", {}).get("missing_url", []))
    if missing_url:
        preview = ", ".join(missing_url[:6])
        if len(missing_url) > 6:
            preview += ", ..."
        lines.extend(
            [
                "",
                "## Deploy/URL Gap Preview",
                f"- {preview}",
            ]
        )

    return "\n".join(lines) + "\n"


def render_sorun_analizi(summary: dict[str, Any], issues: list[dict[str, Any]], focus: Focus, now: datetime) -> str:
    unhealthy = list(summary.get("gaps", {}).get("unhealthy_live", []))
    pending_health = list(summary.get("gaps", {}).get("pending_health", []))
    missing_checkout = list(summary.get("gaps", {}).get("missing_checkout", []))
    missing_url = list(summary.get("gaps", {}).get("missing_url", []))
    canonical_drift = list(summary.get("gaps", {}).get("canonical_url_drift", []))
    deploy_readiness = list(summary.get("gaps", {}).get("deploy_readiness", []))

    def format_unhealthy_item(item: dict[str, Any]) -> str:
        canonical_bits: list[str] = []
        canonical_url = item.get("canonical_url") or item.get("canonical_health_url")
        if canonical_url and canonical_url != item.get("url"):
            canonical_bits.append(f"canonical_url={canonical_url}")

        canonical_code = item.get("canonical_code")
        if canonical_code is None:
            canonical_code = item.get("canonical_health_code")
        if canonical_code is not None and canonical_code != item.get("code"):
            canonical_bits.append(f"canonical_code={canonical_code}")

        canonical_status = item.get("canonical_status") or item.get("canonical_health_status")
        if canonical_status and canonical_status != item.get("health_status"):
            canonical_bits.append(f"canonical_status={canonical_status}")

        probe_url = item.get("probe_url")
        probe_suffix = (
            f" probe_url={probe_url}"
            if probe_url and probe_url != item.get("url")
            else ""
        )
        effective_url = item.get("effective_url")
        effective_suffix = (
            f" effective_url={effective_url}"
            if effective_url and effective_url not in {item.get("url"), probe_url}
            else ""
        )
        canonical_suffix = f" {' '.join(canonical_bits)}" if canonical_bits else ""
        return (
            f"- `{item.get('slug')}` — code={item.get('code')} status={item.get('health_status')} "
            f"url={item.get('url')}{probe_suffix}{effective_suffix}{canonical_suffix}"
        )

    lines = [
        f"# Sorun Analizi — Cycle {summary.get('cycle')} | {now.strftime('%Y-%m-%d %H:%M')} UTC",
        "",
        "## Ana Darboğaz",
        f"- **{focus.key}** — {focus.summary}",
        "",
        "## Summary'den Gelen Gerçekler",
        f"- Healthy live: {summary.get('healthy_count')}/{summary.get('live_count')}",
        f"- Health pending: {summary.get('pending_health_count', 0)}",
        f"- Checkout gap: {summary.get('checkout_gap_count')}",
        f"- Deploy readiness gap: {summary.get('deploy_readiness_count', 0)}",
        f"- Deploy/url gap: {summary.get('deploy_missing_or_bad_url')}",
        f"- Canonical drift: {summary.get('canonical_url_drift', 0)}",
        f"- Spec-ready backlog: {summary.get('spec_ready_count')}",
    ]

    if unhealthy:
        lines.extend(["", "## Canlı Sağlıksız Ürünler"])
        for item in unhealthy[:10]:
            lines.append(format_unhealthy_item(item))

    if pending_health:
        lines.extend(["", "## Health Bekleyen Ürünler"])
        for item in pending_health[:10]:
            lines.append(
                f"- `{item.get('slug')}` — code={item.get('code')} status={item.get('health_status')} url={item.get('url')}"
            )

    if missing_checkout:
        preview = ", ".join(missing_checkout[:12])
        if len(missing_checkout) > 12:
            preview += ", ..."
        lines.extend(["", "## Checkout Eksikleri", f"- {preview}"])

    if missing_url:
        preview = ", ".join(missing_url[:12])
        if len(missing_url) > 12:
            preview += ", ..."
        lines.extend(["", "## URL/Deploy Eksikleri", f"- {preview}"])

    if canonical_drift:
        lines.extend(["", "## Canonical Drift Ürünleri"])
        for item in canonical_drift[:10]:
            lines.append(
                f"- `{item.get('slug')}` — current={item.get('url')} ideal={item.get('ideal_url')}"
            )

    if deploy_readiness:
        lines.extend(["", "## Deploy Readiness Issues"])
        lines.append(
            f"- Count: {summary.get('deploy_readiness_count', len(deploy_readiness))} "
            f"| Manifest gaps: {summary.get('deploy_readiness_manifest_gap_count', 0)} "
            f"| URL gaps: {summary.get('deploy_readiness_url_gap_count', 0)} "
            f"| State gaps: {summary.get('deploy_readiness_state_gap_count', 0)}"
        )
        for item in deploy_readiness[:10]:
            manifest_problem = item.get("manifest_problem")
            manifest_missing = ", ".join(item.get("missing_manifest_fields", [])) or "none"
            url_missing = ", ".join(item.get("missing_url_fields", [])) or "none"
            state_missing = ", ".join(item.get("missing_state_fields", [])) or "none"
            manifest_suffix = f" manifest={manifest_problem}" if manifest_problem else ""
            lines.append(
                f"- `{item.get('slug')}`{manifest_suffix} — manifest={manifest_missing}; "
                f"url={url_missing}; state={state_missing}"
            )

    if issues:
        lines.extend(["", "## Açık Issue Kayıtları"])
        for issue in top_issues(issues, limit=8):
            lines.append(
                f"- **{issue.get('issue_type')}** [{issue.get('severity')}/{issue.get('status')}] — {issue.get('description')}"
            )

    lines.extend(
        [
            "",
            "## Not",
            "- Bu dosya live `STATE.json` → `STATE_SUMMARY.json` ve unresolved issue kayıtlarından üretildi.",
            "- Manuel ödeme/auth gerektiren adımlar rapora kodla çözülmüş gibi yazılmamalı.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_codex_task(summary: dict[str, Any], focus: Focus, now: datetime) -> str:
    health_percent = _health_percent(summary)
    return "\n".join(
        [
            f"# Codex Task — Generated {now.strftime('%Y-%m-%d %H:%M')} UTC",
            "",
            "## MOD: PRODUCTION SAFE INFRA",
            "",
            "Bu görev dosyası live `STATE.json` → `STATE_SUMMARY.json` üzerinden üretildi. Eski araştırma/no-code talimatı",
            "stale sayılır; doğrudan insan kod+commit istediğinde güvenli altyapı iyileştirmesi seçilir.",
            "",
            "## Aktif Görev",
            f"**{focus.codex_task_title}**",
            "",
            focus.codex_task_body,
            "",
            "## Canlı State Özeti",
            f"- Cycle: {summary.get('cycle')}",
            f"- Live sağlık: {summary.get('healthy_count')}/{summary.get('live_count')} (%{health_percent:.1f})",
            f"- Health pending: {summary.get('pending_health_count', 0)}",
            f"- Checkout gap: {summary.get('checkout_gap_count')}",
            f"- Deploy readiness gap: {summary.get('deploy_readiness_count', 0)}",
            f"- Deploy/url gap: {summary.get('deploy_missing_or_bad_url')}",
            f"- Canonical drift: {summary.get('canonical_url_drift', 0)}",
            f"- Spec-ready count: {summary.get('spec_ready_count')}",
            f"- Next action: {summary.get('next_action')}",
            "",
            "## Guardrails",
            "- Dosyaları okumadan edit yapma.",
            "- Production canlı ürün davranışını bozma.",
            "- Manual Vercel/LemonSqueezy aksiyonlarını çözüldü gibi gösterme.",
            "- Cerrahi değişiklik + test/verification + `analysis/codex_result.md` + commit.",
        ]
    ) + "\n"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def refresh_context(now: datetime | None = None) -> dict[str, Any]:
    current_time = now or datetime.now(timezone.utc)
    summary = load_summary()
    issues = load_unresolved_issues()
    focus = determine_focus(summary, issues)

    write_file(ONERI_FILE, render_oneri(summary, issues, focus, current_time))
    write_file(SORUN_FILE, render_sorun_analizi(summary, issues, focus, current_time))
    write_file(CODEX_TASK_FILE, render_codex_task(summary, focus, current_time))

    return {
        "focus": focus,
        "summary": summary,
        "issues": issues,
    }


def main() -> int:
    result = refresh_context()
    focus: Focus = result["focus"]
    summary = result["summary"]
    print(
        "Codex context refreshed: "
        f"cycle={summary.get('cycle')} focus={focus.key} "
        f"live={summary.get('live_count')} healthy={summary.get('healthy_count')} "
        f"checkout_gap={summary.get('checkout_gap_count')} deploy_gap={summary.get('deploy_missing_or_bad_url')} "
        f"canonical_drift={summary.get('canonical_url_drift', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
