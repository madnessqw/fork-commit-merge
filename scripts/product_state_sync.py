#!/usr/bin/env python3
"""Reconcile STATE active records with product.json manifests.

STATE.json is operational cache, not the durable source of truth. Product
manifests often carry the latest status while STATE keeps stale live URLs or
health data. These helpers merge both views without pretending manual deploy /
payment steps are already solved.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_metadata import get_checkout_url, has_value, normalize_checkout_metadata


PRODUCTS_DIR = ROOT / "products"

PRE_DEPLOY_STATUSES = {"building", "spec_ready", "ready_to_deploy"}
HEALTH_CHECKABLE_STATUSES = {"live", "ready_for_payment"}
HEALTHY_URL_STATUSES = {"healthy", "alternate_healthy"}
CANONICAL_REDIRECTED_PREVIEW_STATUS = "redirected_preview_alias"
FAILURE_HEALTH_STATUS_BY_CODE = {
    0: "timeout",
    401: "unauthorized",
    402: "deployment_disabled",
    404: "not_found",
}
HEALTH_METADATA_FIELDS = (
    "health_status",
    "last_health_code",
    "last_health_url",
    "health_probe_url",
    "effective_health_url",
    "last_health_check",
    "health_checked_at",
    "canonical_health_status",
    "canonical_health_code",
    "canonical_health_url",
    "canonical_probe_url",
    "canonical_health_checked_at",
)


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _pick(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = record.get(key)
        if has_value(value):
            return value
    return None


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    normalized["name"] = _clean_text(_pick(record, "name", "n"))
    normalized["slug"] = _clean_text(_pick(record, "slug", "s"))
    normalized["status"] = _clean_text(_pick(record, "status", "st"))
    normalized["vercel_url"] = normalize_url(_pick(record, "vercel_url", "v"))
    normalized["deployment_url"] = normalize_url(_pick(record, "deployment_url"))
    normalized["checkout_url"] = get_checkout_url(record)
    return normalized


def normalize_url(value: Any) -> str | None:
    url = _clean_text(value)
    if url is None:
        return None
    return url.rstrip("/")


def _url_hostname(value: Any) -> str | None:
    url = normalize_url(value)
    if url is None:
        return None
    hostname = urlparse(url).hostname
    if hostname is None:
        return None
    return hostname.lower()


def _is_vercel_preview_alias(url: Any, slug: str | None) -> bool:
    host = _url_hostname(url)
    if host is None or not host.endswith(".vercel.app"):
        return False

    canonical_host = _url_hostname(canonical_vercel_url(slug))
    if canonical_host is None:
        return False

    return host != canonical_host


def _preview_probe_candidate(url: Any, slug: str | None) -> str | None:
    normalized = normalize_url(url)
    if normalized is None:
        return None
    if not _is_vercel_preview_alias(normalized, slug):
        return None
    return normalized


def _record_key(record: dict[str, Any]) -> str | None:
    slug = _clean_text(_pick(record, "slug", "s"))
    if slug is not None:
        return f"slug:{slug}"

    name = _clean_text(_pick(record, "name", "n"))
    if name is not None:
        return f"name:{name}"

    return None


def _record_quality_score(record: dict[str, Any]) -> int:
    return sum(1 for value in record.values() if has_value(value))


def _dedupe_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    anonymous: list[dict[str, Any]] = []

    for record in records:
        key = _record_key(record)
        if key is None:
            anonymous.append(record)
            continue

        if key not in deduped:
            deduped[key] = record
            order.append(key)
            continue

        if _record_quality_score(record) > _record_quality_score(deduped[key]):
            deduped[key] = record

    return [deduped[key] for key in order] + anonymous


def _clear_health_metadata(record: dict[str, Any]) -> dict[str, Any]:
    cleared = dict(record)
    for field in HEALTH_METADATA_FIELDS:
        cleared[field] = None
    return cleared


def _parse_timestamp(value: Any) -> datetime | None:
    text = _clean_text(value)
    if text is None:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _sync_health_timestamps(record: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    last_health_check = _clean_text(_pick(record, "last_health_check"))
    health_checked_at = _clean_text(_pick(record, "health_checked_at"))

    if last_health_check is None and health_checked_at is None:
        normalized["last_health_check"] = None
        normalized["health_checked_at"] = None
        return normalized

    parsed_last = _parse_timestamp(last_health_check)
    parsed_checked = _parse_timestamp(health_checked_at)

    if parsed_last is not None and parsed_checked is not None:
        chosen = _format_timestamp(max(parsed_last, parsed_checked))
    elif parsed_last is not None:
        chosen = _format_timestamp(parsed_last)
    elif parsed_checked is not None:
        chosen = _format_timestamp(parsed_checked)
    else:
        chosen = last_health_check or health_checked_at

    normalized["last_health_check"] = chosen
    normalized["health_checked_at"] = chosen
    return normalized


def _health_status_for_code(code: int) -> str:
    if code == 200:
        return "healthy"
    return FAILURE_HEALTH_STATUS_BY_CODE.get(code, f"error_{code}")


def canonical_vercel_url(slug: str | None) -> str | None:
    clean_slug = _clean_text(slug)
    if clean_slug is None:
        return None
    return f"https://{clean_slug}.vercel.app"


def canonical_target_vercel_url(record: dict[str, Any]) -> str | None:
    status = _clean_text(_pick(record, "status", "st"))
    if status not in HEALTH_CHECKABLE_STATUSES:
        return normalize_url(_pick(record, "ideal_vercel_url"))

    slug = _clean_text(_pick(record, "slug", "s"))
    canonical_url = canonical_vercel_url(slug)
    if canonical_url is not None:
        return canonical_url
    return normalize_url(_pick(record, "ideal_vercel_url"))


def successful_health_url(record: dict[str, Any]) -> str | None:
    status = _clean_text(_pick(record, "health_status"))
    if status not in HEALTHY_URL_STATUSES:
        return None

    raw_code = _pick(record, "last_health_code")
    try:
        code = int(raw_code)
    except (TypeError, ValueError):
        return None

    if code != 200:
        return None

    slug = _clean_text(_pick(record, "slug", "s"))
    canonical_url = canonical_vercel_url(slug)
    if status == "alternate_healthy":
        # Fallback aliases are the truth here. Prefer the most recent visible
        # fallback URL and refuse to let a stale canonical URL shadow it.
        for candidate in (
            _pick(record, "last_health_url"),
            _pick(record, "health_probe_url"),
            _pick(record, "effective_health_url"),
            _pick(record, "deployment_url"),
            _pick(record, "v"),
            _pick(record, "vercel_url"),
        ):
            normalized = normalize_url(candidate)
            if normalized is None:
                continue
            if canonical_url is not None and normalized == canonical_url:
                continue
            return normalized

        return canonical_url

    explicit_health_url = normalize_url(
        _pick(record, "effective_health_url", "last_health_url", "health_probe_url")
    )
    if explicit_health_url is not None:
        return explicit_health_url

    # Some legacy snapshots only keep the reachable alias in compact `v`,
    # `deployment_url`, or `vercel_url` after the canonical slug has failed.
    # Preserve that alias here so sync/state refreshes do not "normalize" a
    # live fallback back to the dead canonical URL.
    for candidate in (_pick(record, "deployment_url"), _pick(record, "v"), _pick(record, "vercel_url")):
        normalized = normalize_url(candidate)
        if (
            normalized is not None
            and _is_vercel_preview_alias(normalized, slug)
        ):
            return normalized

    return None


def _successful_snapshot_url(record: dict[str, Any]) -> str | None:
    raw_code = _pick(record, "last_health_code")
    try:
        code = int(raw_code) if raw_code is not None else None
    except (TypeError, ValueError):
        return None

    if code != 200:
        return None

    health_checked_at = _clean_text(_pick(record, "last_health_check", "health_checked_at"))
    current_health_status = _clean_text(_pick(record, "health_status"))
    if current_health_status == "alternate_healthy":
        visible_success = successful_health_url(record)
        if visible_success is not None:
            return visible_success

    explicit_health_url = normalize_url(
        _pick(record, "effective_health_url", "last_health_url", "health_probe_url")
    )
    if explicit_health_url is not None:
        return explicit_health_url

    slug = _pick(record, "slug", "s")
    compact_url = normalize_url(_pick(record, "v"))
    if compact_url is not None and _is_vercel_preview_alias(compact_url, slug):
        # Older summary/state snapshots sometimes kept the reachable fallback
        # alias only in compact `v` while verbose `vercel_url` had already been
        # normalized back to the canonical slug. With no explicit probe URL, the
        # conservative move is to preserve that fallback instead of declaring the
        # canonical URL healthy without proof.
        return compact_url

    # Some live snapshots only persist the fallback alias in deployment_url.
    # If we have a real health timestamp but no explicit health URL, keep that
    # alias visible instead of collapsing back to the dead canonical slug.
    deployment_url = normalize_url(_pick(record, "deployment_url"))
    if health_checked_at is not None and current_health_status == "healthy" and deployment_url is not None:
        if _is_vercel_preview_alias(deployment_url, slug):
            return deployment_url

    for candidate in (_pick(record, "vercel_url", "v"), _pick(record, "deployment_url")):
        normalized = normalize_url(candidate)
        if (
            normalized is not None
            and _is_vercel_preview_alias(normalized, slug)
            and current_health_status == "alternate_healthy"
        ):
            return normalized

    return normalize_url(_pick(record, "vercel_url", "v", "deployment_url"))


def normalize_health_snapshot(record: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    status = _clean_text(_pick(record, "status", "st"))
    if status not in HEALTH_CHECKABLE_STATUSES:
        return _clear_health_metadata(normalized)

    normalized = _sync_health_timestamps(normalized)

    canonical_target = canonical_target_vercel_url(normalized)
    if canonical_target is not None:
        normalized["ideal_vercel_url"] = canonical_target
        normalized["canonical_health_url"] = canonical_target
        normalized["canonical_probe_url"] = normalize_url(_pick(record, "canonical_probe_url")) or canonical_target

    public_checked_text = _clean_text(_pick(normalized, "health_checked_at", "last_health_check"))
    public_checked_at = _parse_timestamp(public_checked_text)

    canonical_checked_at = _clean_text(_pick(record, "canonical_health_checked_at"))
    canonical_checked_dt = _parse_timestamp(canonical_checked_at)
    if canonical_checked_at is None:
        canonical_checked_at = public_checked_text
        canonical_checked_dt = public_checked_at
    normalized["canonical_health_checked_at"] = canonical_checked_at

    raw_canonical_code = _pick(record, "canonical_health_code")
    try:
        canonical_code = int(raw_canonical_code) if raw_canonical_code is not None else None
    except (TypeError, ValueError):
        canonical_code = None

    raw_canonical_status = _clean_text(_pick(record, "canonical_health_status"))
    current_health_status = _clean_text(_pick(record, "health_status"))
    raw_code = _pick(record, "last_health_code")
    try:
        public_code = int(raw_code) if raw_code is not None else None
    except (TypeError, ValueError):
        public_code = None

    successful_snapshot_url = _successful_snapshot_url(record)
    explicit_canonical_probe_url = normalize_url(_pick(record, "canonical_probe_url"))
    legacy_probe_url = normalize_url(_pick(record, "health_probe_url"))
    canonical_probe_url = explicit_canonical_probe_url or (
        legacy_probe_url if legacy_probe_url == canonical_target else None
    )
    preserve_redirected_canonical_status = (
        canonical_code == 200
        and current_health_status == "alternate_healthy"
        and canonical_target is not None
        and successful_snapshot_url is not None
        and successful_snapshot_url != canonical_target
        and (
            raw_canonical_status == CANONICAL_REDIRECTED_PREVIEW_STATUS
            or canonical_probe_url == canonical_target
        )
    )
    canonical_failure_is_newer_than_public_success = (
        public_code == 200
        and canonical_code not in (None, 200)
        and canonical_checked_dt is not None
        and public_checked_at is not None
        and canonical_checked_dt > public_checked_at
    )
    if canonical_failure_is_newer_than_public_success:
        # A stale fallback 200 is not proof that the product is still alive.
        # If the canonical probe failed later than the public/fallback probe,
        # make the newer canonical failure the active health truth and let the
        # next health_check cycle retry recorded fallback candidates explicitly.
        normalized["health_status"] = _health_status_for_code(canonical_code)
        normalized["last_health_code"] = canonical_code
        normalized["last_health_url"] = canonical_target
        normalized["effective_health_url"] = canonical_target
        normalized["last_health_check"] = canonical_checked_at
        normalized["health_checked_at"] = canonical_checked_at
        current_health_status = normalized["health_status"]
        public_code = canonical_code
        successful_snapshot_url = None
        return normalized

    has_successful_preview_snapshot = (
        public_code == 200
        and canonical_code is None
        and canonical_target is not None
        and successful_snapshot_url is not None
        and successful_snapshot_url != canonical_target
        and _is_vercel_preview_alias(successful_snapshot_url, _pick(record, "slug", "s"))
    )
    if has_successful_preview_snapshot:
        # A preview/alias URL answering 200 is useful, but it is not proof that
        # the canonical slug URL is fixed. Keep the fallback visible until the
        # canonical probe records its own 200.
        normalized["health_status"] = "alternate_healthy"
        normalized["canonical_health_code"] = None
        normalized["canonical_health_status"] = raw_canonical_status or "pending"
        normalized["last_health_url"] = successful_snapshot_url
        if normalized.get("effective_health_url") is None:
            normalized["effective_health_url"] = successful_snapshot_url
        current_health_status = "alternate_healthy"

    canonical_success_is_newer_than_stale_failure = (
        public_code == 200
        and canonical_target is not None
        and successful_snapshot_url == canonical_target
        and canonical_code not in (None, 200)
        and (
            canonical_checked_dt is None
            or public_checked_at is None
            or public_checked_at >= canonical_checked_dt
        )
    )
    if canonical_success_is_newer_than_stale_failure:
        normalized["canonical_health_code"] = 200
        normalized["canonical_health_status"] = "healthy"
        normalized["canonical_health_url"] = canonical_target
        normalized["canonical_probe_url"] = normalize_url(_pick(record, "canonical_probe_url")) or canonical_target
        normalized["canonical_health_checked_at"] = public_checked_text or canonical_checked_at
        normalized["health_status"] = "healthy"
        normalized["last_health_url"] = canonical_target
        if normalized.get("effective_health_url") is None:
            normalized["effective_health_url"] = canonical_target
        current_health_status = "healthy"
        canonical_code = 200

    canonical_snapshot_code = canonical_code
    if public_code is not None and current_health_status != "alternate_healthy":
        if public_code == 200 and canonical_code not in (None, 200):
            canonical_snapshot_code = canonical_code
        else:
            canonical_snapshot_code = public_code

    if canonical_snapshot_code is not None:
        normalized["canonical_health_code"] = canonical_snapshot_code
        if preserve_redirected_canonical_status:
            normalized["canonical_health_status"] = CANONICAL_REDIRECTED_PREVIEW_STATUS
        else:
            normalized["canonical_health_status"] = _health_status_for_code(canonical_snapshot_code)
    else:
        normalized["canonical_health_code"] = None
        normalized["canonical_health_status"] = raw_canonical_status or normalized.get("canonical_health_status")

    if public_code == 200 and canonical_code not in (None, 200):
        # Canonical failed but the live fallback still answers 200. Keep the
        # record honest so stale canonical state does not hide the reachable URL.
        normalized["health_status"] = "alternate_healthy"
        current_health_status = "alternate_healthy"

    effective_canonical_code = normalized.get("canonical_health_code")
    effective_health_url = normalize_url(_pick(normalized, "effective_health_url", "last_health_url"))
    preserve_redirected_fallback = (
        effective_canonical_code == 200
        and current_health_status == "alternate_healthy"
        and canonical_target is not None
        and successful_snapshot_url is not None
        and successful_snapshot_url != canonical_target
        and canonical_probe_url == canonical_target
        and effective_health_url == successful_snapshot_url
    )
    if effective_canonical_code == 200 and not preserve_redirected_fallback:
        final_canonical_checked_at = _clean_text(
            _pick(normalized, "canonical_health_checked_at", "health_checked_at", "last_health_check")
        ) or canonical_checked_at
        normalized["ideal_vercel_url"] = canonical_target
        normalized["canonical_health_url"] = canonical_target
        normalized["canonical_probe_url"] = normalize_url(_pick(record, "canonical_probe_url")) or canonical_target
        normalized["canonical_health_checked_at"] = final_canonical_checked_at
        normalized["canonical_health_code"] = 200
        normalized["canonical_health_status"] = "healthy"
        normalized["health_status"] = "healthy"
        normalized["last_health_code"] = 200
        normalized["last_health_url"] = canonical_target
        normalized["last_health_check"] = final_canonical_checked_at
        normalized["health_checked_at"] = final_canonical_checked_at
        if canonical_target is not None:
            normalized["vercel_url"] = canonical_target
        return normalized

    if preserve_redirected_fallback:
        normalized["health_status"] = "alternate_healthy"
        normalized["last_health_code"] = 200
        normalized["last_health_url"] = successful_snapshot_url
        if normalized.get("effective_health_url") is None:
            normalized["effective_health_url"] = successful_snapshot_url

    raw_code = _pick(record, "last_health_code")
    try:
        code = int(raw_code)
    except (TypeError, ValueError):
        return normalized

    normalized["last_health_code"] = code

    # Preserve any earlier alternate_healthy promotion instead of re-reading the
    # stale raw record. Otherwise a live 200 fallback paired with a broken
    # canonical URL gets rewritten back to "healthy" and the reachable URL gets
    # hidden behind the dead canonical alias.
    current_health_status = _clean_text(normalized.get("health_status"))
    if code == 200:
        if current_health_status not in HEALTHY_URL_STATUSES:
            normalized["health_status"] = "healthy"
        return normalized

    normalized["health_status"] = FAILURE_HEALTH_STATUS_BY_CODE.get(code, f"error_{code}")
    return normalized


def resolved_public_vercel_url(record: dict[str, Any]) -> str | None:
    return choose_public_vercel_url(
        slug=_pick(record, "slug", "s"),
        state_status=_pick(record, "status", "st"),
        state_url=_pick(record, "vercel_url", "v"),
        manifest_url=None,
        deployment_url=_pick(record, "deployment_url"),
        status=_pick(record, "status", "st"),
        health_status=_pick(record, "health_status"),
        last_health_code=_pick(record, "last_health_code"),
        health_url=successful_health_url(record),
    )


def display_vercel_url(record: dict[str, Any]) -> str | None:
    return resolved_public_vercel_url(record)


def load_product_catalog(products_dir: Path = PRODUCTS_DIR) -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}

    if not products_dir.exists():
        return catalog

    for path in sorted(products_dir.glob("*/product.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        slug = _clean_text(record.get("slug")) or path.parent.name
        catalog[slug] = record

    return catalog


def choose_public_vercel_url(
    *,
    slug: str | None,
    state_status: str | None = None,
    state_url: Any,
    manifest_url: Any,
    deployment_url: Any = None,
    status: str | None = None,
    health_status: str | None = None,
    last_health_code: Any = None,
    health_url: Any = None,
) -> str | None:
    normalized_status = _clean_text(status)
    normalized_manifest_url = normalize_url(manifest_url)
    if normalized_status in PRE_DEPLOY_STATUSES:
        return None

    normalized_state_url = normalize_url(state_url)
    normalized_deployment_url = normalize_url(deployment_url)
    normalized_health_url = (
        normalize_url(health_url)
        if _clean_text(health_status) in HEALTHY_URL_STATUSES
        else None
    )
    if normalized_health_url is not None:
        try:
            if int(last_health_code) != 200:
                normalized_health_url = None
        except (TypeError, ValueError):
            normalized_health_url = None

    canonical_url = canonical_vercel_url(slug)
    if (
        normalized_status in HEALTH_CHECKABLE_STATUSES
        and _clean_text(health_status) == "alternate_healthy"
        and normalized_health_url is not None
    ):
        # The canonical probe lost, but a fallback URL answered 200.
        # Keep the actual reachable URL so state does not lie about reality.
        return normalized_health_url

    if normalized_status in HEALTH_CHECKABLE_STATUSES and _clean_text(health_status) == "alternate_healthy":
        for candidate in (normalized_state_url, normalized_deployment_url, normalized_manifest_url):
            if candidate is not None and _is_vercel_preview_alias(candidate, slug):
                # Some snapshots only keep the fallback alias in deployment_url
                # or vercel_url and never persisted last_health_url. Preserve
                # that reachable alias instead of canonicalizing it away.
                return candidate

    if (
        normalized_status in HEALTH_CHECKABLE_STATUSES
        and _clean_text(health_status) == "healthy"
        and normalized_health_url is None
    ):
        for candidate in (normalized_state_url, normalized_deployment_url):
            if candidate is not None and _is_vercel_preview_alias(candidate, slug):
                return candidate

    if canonical_url is not None:
        for candidate in (
            normalized_state_url,
            normalized_deployment_url,
            normalized_manifest_url,
            normalized_health_url,
        ):
            if candidate == canonical_url:
                return canonical_url

    if normalized_status == "live":
        original_state_status = _clean_text(state_status)
        if canonical_url is not None and normalized_health_url is None:
            for candidate in (normalized_state_url, normalized_deployment_url, normalized_manifest_url):
                if candidate is None:
                    continue
                candidate_host = _url_hostname(candidate)
                if candidate_host is None:
                    continue
                if not candidate_host.endswith(".vercel.app"):
                    return candidate
            if any(
                _is_vercel_preview_alias(candidate, slug)
                for candidate in (normalized_state_url, normalized_deployment_url, normalized_manifest_url)
            ):
                return canonical_url
        if (
            canonical_url is not None
            and original_state_status in PRE_DEPLOY_STATUSES
            and normalized_health_url is None
            and normalized_state_url is None
        ):
            return canonical_url
        return (
            normalized_state_url
            or normalized_deployment_url
            or normalized_health_url
            or normalized_manifest_url
            or canonical_url
        )

    return normalized_state_url or normalized_deployment_url or normalized_manifest_url


def _promote_canonical_preview_for_predeploy(
    merged: dict[str, Any],
    *,
    source_state_status: str | None,
    source_state_canonical_url: str | None,
    source_state_explicit_health_url: str | None,
) -> dict[str, Any]:
    if source_state_status not in PRE_DEPLOY_STATUSES:
        return merged
    if source_state_explicit_health_url is not None:
        return merged

    slug = _clean_text(_pick(merged, "slug", "s"))
    public_url = resolved_public_vercel_url(merged)
    if public_url is None or not _is_vercel_preview_alias(public_url, slug):
        return merged

    canonical_url = source_state_canonical_url or canonical_vercel_url(slug)
    if canonical_url is None:
        return merged

    promoted = dict(merged)
    promoted["health_status"] = "healthy"
    promoted["last_health_url"] = canonical_url
    promoted["effective_health_url"] = canonical_url
    promoted["health_probe_url"] = canonical_url
    promoted["vercel_url"] = canonical_url
    promoted["v"] = canonical_url
    return promoted


def merge_product_record(
    state_record: dict[str, Any],
    manifest_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source_state = normalize_record(state_record)
    source_state_status = source_state.get("status")
    source_state_vercel_url = normalize_url(source_state.get("vercel_url"))
    source_state_deployment_url = normalize_url(source_state.get("deployment_url"))
    source_state_explicit_health_url = normalize_url(
        source_state.get("last_health_url")
        or source_state.get("effective_health_url")
        or source_state.get("health_probe_url")
    )
    source_state_canonical_url = canonical_vercel_url(source_state.get("slug"))
    merged = normalize_checkout_metadata(
        source_state,
        force_canonical_key=True,
        prune_legacy=True,
    )

    manifest = (
        normalize_checkout_metadata(
            normalize_record(manifest_record),
            force_canonical_key=True,
            prune_legacy=True,
        )
        if manifest_record is not None
        else None
    )

    if manifest is None:
        if (
            source_state_status == "live"
            and source_state_vercel_url is not None
            and source_state_canonical_url is not None
            and source_state_vercel_url == source_state_canonical_url
            and source_state_deployment_url is not None
            and _is_vercel_preview_alias(source_state_deployment_url, source_state.get("slug"))
            and source_state_explicit_health_url is None
            and _clean_text(merged.get("health_status")) == "healthy"
            and _pick(merged, "last_health_code") == 200
        ):
            # Some live products only keep the reachable fallback alias in
            # deployment_url. Keep that alias visible instead of normalizing
            # back to the canonical slug when no explicit health probe URL was
            # ever stored.
            merged["health_status"] = "alternate_healthy"
            merged["last_health_url"] = source_state_deployment_url
            merged["effective_health_url"] = source_state_deployment_url
            merged["health_probe_url"] = source_state_deployment_url

        merged = normalize_health_snapshot(merged)
        merged = _promote_canonical_preview_for_predeploy(
            merged,
            source_state_status=source_state_status,
            source_state_canonical_url=source_state_canonical_url,
            source_state_explicit_health_url=source_state_explicit_health_url,
        )
        merged["vercel_url"] = resolved_public_vercel_url(merged)
        return normalize_checkout_metadata(
            {
                **merged,
                "n": merged.get("name"),
                "s": merged.get("slug"),
                "st": merged.get("status"),
                "v": merged.get("vercel_url"),
                "c": get_checkout_url(merged),
            },
            force_canonical_key=True,
            prune_legacy=True,
        )

    for field in ("name", "slug", "status", "category", "price", "github_url"):
        manifest_value = manifest.get(field)
        if has_value(manifest_value):
            merged[field] = manifest_value

    effective_status = merged.get("status")
    merged["deployment_url"] = (
        normalize_url(manifest.get("deployment_url")) or normalize_url(merged.get("deployment_url"))
    )
    if merged.get("deployment_url") is None and effective_status in HEALTH_CHECKABLE_STATUSES:
        fallback_probe_url = (
            _preview_probe_candidate(source_state.get("deployment_url"), merged.get("slug"))
            or _preview_probe_candidate(source_state.get("vercel_url"), merged.get("slug"))
            or _preview_probe_candidate(manifest.get("deployment_url"), merged.get("slug"))
            or _preview_probe_candidate(manifest.get("vercel_url"), merged.get("slug"))
        )
        if fallback_probe_url is not None:
            merged["deployment_url"] = fallback_probe_url
    manifest_last_health_url = normalize_url(manifest.get("last_health_url"))
    if merged.get("last_health_url") is None and manifest_last_health_url is not None:
        merged["last_health_url"] = manifest_last_health_url
    merged["vercel_url"] = choose_public_vercel_url(
        slug=merged.get("slug"),
        state_status=source_state_status,
        state_url=merged.get("vercel_url"),
        manifest_url=manifest.get("vercel_url"),
        deployment_url=merged.get("deployment_url"),
        status=effective_status,
        health_status=merged.get("health_status"),
        last_health_code=merged.get("last_health_code"),
        health_url=merged.get("last_health_url"),
    )

    manifest_checkout_url = get_checkout_url(manifest)
    if effective_status in PRE_DEPLOY_STATUSES and manifest_checkout_url is None:
        merged["checkout_url"] = None
        merged.pop("payment_provider", None)
    elif manifest_checkout_url is not None:
        merged["checkout_url"] = manifest_checkout_url
        payment_provider = manifest.get("payment_provider")
        if has_value(payment_provider):
            merged["payment_provider"] = payment_provider

    manifest_health_status = manifest.get("health_status")
    manifest_health_code = manifest.get("last_health_code")
    if merged.get("health_status") is None and has_value(manifest_health_status):
        merged["health_status"] = manifest_health_status
    if merged.get("last_health_code") is None and has_value(manifest_health_code):
        merged["last_health_code"] = manifest_health_code

    if (
        source_state_status == "live"
        and source_state_vercel_url is not None
        and source_state_canonical_url is not None
        and source_state_vercel_url == source_state_canonical_url
        and source_state_deployment_url is not None
        and _is_vercel_preview_alias(source_state_deployment_url, source_state.get("slug"))
        and source_state_explicit_health_url is None
        and _clean_text(merged.get("health_status")) == "healthy"
        and _pick(merged, "last_health_code") == 200
    ):
        # Some live products only keep the reachable fallback alias in
        # deployment_url. Keep that alias visible instead of normalizing back to
        # the canonical slug when no explicit health probe URL was ever stored.
        merged["health_status"] = "alternate_healthy"
        merged["last_health_url"] = source_state_deployment_url
        merged["effective_health_url"] = source_state_deployment_url
        merged["health_probe_url"] = source_state_deployment_url

    merged = normalize_health_snapshot(merged)
    merged = _promote_canonical_preview_for_predeploy(
        merged,
        source_state_status=source_state_status,
        source_state_canonical_url=source_state_canonical_url,
        source_state_explicit_health_url=source_state_explicit_health_url,
    )
    merged["vercel_url"] = resolved_public_vercel_url(merged)

    return normalize_checkout_metadata(
        {
            **merged,
            "n": merged.get("name"),
            "s": merged.get("slug"),
            "st": merged.get("status"),
            "v": merged.get("vercel_url"),
            "c": get_checkout_url(merged),
        },
        force_canonical_key=True,
        prune_legacy=True,
    )


def sync_state_products(
    products: list[dict[str, Any]],
    product_catalog: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    catalog = product_catalog or {}
    synced: list[dict[str, Any]] = []

    for product in products:
        normalized = normalize_record(product)
        slug = normalized.get("slug")
        manifest = catalog.get(slug) if slug else None
        synced.append(merge_product_record(product, manifest))

    return _dedupe_records(synced)


def sync_state_snapshot(
    state: dict[str, Any],
    product_catalog: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a normalized copy of STATE with synced product records."""
    synced_state = dict(state)
    products = state.get("products")

    if isinstance(products, dict):
        synced_products = dict(products)
        synced_products["active"] = sync_state_products(products.get("active", []), product_catalog)
        synced_products["spec_ready"] = sync_state_products(products.get("spec_ready", []), product_catalog)
        synced_state["products"] = synced_products
    elif isinstance(products, list):
        synced_state["products"] = sync_state_products(products, product_catalog)

    return synced_state


def health_check_url(product: dict[str, Any]) -> str | None:
    status = _clean_text(_pick(product, "status", "st"))
    if status not in HEALTH_CHECKABLE_STATUSES:
        return None
    target_url = canonical_target_vercel_url(product)
    if target_url is not None:
        return target_url
    return normalize_url(_pick(product, "vercel_url", "v", "deployment_url"))
