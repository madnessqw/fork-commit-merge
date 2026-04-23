#!/usr/bin/env python3
"""Read-only deploy readiness checks for spec-ready products.

This validator does not mutate state. It only surfaces which spec-ready
products are still missing manifest, URL, or state fields so Codex can stop
pretending manual deploy/payment steps are already done.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.checkout_metadata import has_value
from scripts.product_state_sync import normalize_record


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "products"

MANIFEST_REQUIRED_FIELDS = (
    "name",
    "slug",
    "tagline",
    "description",
    "price",
    "features",
    "tech_stack",
    "category",
    "status",
    "spec_version",
)
URL_REQUIRED_FIELDS = (
    "vercel_url",
    "deployment_url",
    "github_url",
    "webhook_url",
    "checkout_url",
)
STATE_REQUIRED_FIELDS = (
    "payment_provider",
    "created_cycle",
    "deployed_cycle",
    "lemonsqueezy_product_id",
)


def _pick_slug(record: dict[str, Any]) -> str | None:
    for key in ("slug", "s", "name", "n"):
        value = record.get(key)
        if has_value(value):
            return str(value).strip()
    return None


def _quality_score(record: dict[str, Any]) -> int:
    return sum(1 for value in record.values() if has_value(value))


def _dedupe_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    order: list[str] = []

    for record in records:
        slug = _pick_slug(record)
        if slug is None:
            continue
        if slug not in deduped:
            deduped[slug] = record
            order.append(slug)
            continue
        if _quality_score(record) > _quality_score(deduped[slug]):
            deduped[slug] = record

    return [deduped[slug] for slug in order]


def _missing_fields(record: dict[str, Any] | None, fields: tuple[str, ...]) -> list[str]:
    if record is None:
        return list(fields)
    return [field for field in fields if not has_value(record.get(field))]


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _collect_spec_ready_records(state: dict[str, Any]) -> list[dict[str, Any]]:
    products = state.get("products", {})
    records: list[dict[str, Any]] = []

    if isinstance(products, dict):
        collections = [products.get("active", []), products.get("spec_ready", [])]
    elif isinstance(products, list):
        collections = [products]
    else:
        collections = []

    for collection in collections:
        if not isinstance(collection, list):
            continue
        for item in collection:
            if not isinstance(item, dict):
                continue
            normalized = normalize_record(item)
            status = str(normalized.get("status") or "").strip()
            if status == "spec_ready":
                records.append(normalized)

    return _dedupe_records(records)


def collect_spec_ready_deploy_readiness(
    state: dict[str, Any],
    *,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Return readiness issues for spec-ready products.

    The report is intentionally blunt:
    - manifest gaps come from the product manifest itself
    - URL gaps are computed from the merged manifest/state view
    - state gaps come from the raw STATE record
    """

    issues: list[dict[str, Any]] = []
    manifest_gap_count = 0
    url_gap_count = 0
    state_gap_count = 0

    for record in _collect_spec_ready_records(state):
        slug = _pick_slug(record) or "unknown"
        manifest_path = root / "products" / slug / "product.json"
        manifest_exists = manifest_path.exists()
        raw_manifest = _load_json(manifest_path) if manifest_exists else None
        manifest = normalize_record(raw_manifest) if isinstance(raw_manifest, dict) else None

        missing_manifest_fields = _missing_fields(manifest, MANIFEST_REQUIRED_FIELDS)
        missing_url_fields = _missing_fields(
            {**(manifest or {}), **record},
            URL_REQUIRED_FIELDS,
        )
        missing_state_fields = _missing_fields(record, STATE_REQUIRED_FIELDS)

        manifest_problem = None
        if not manifest_exists:
            manifest_problem = "missing"
        elif not isinstance(raw_manifest, dict):
            manifest_problem = "invalid_json"

        if manifest_problem is not None and not missing_manifest_fields:
            missing_manifest_fields = list(MANIFEST_REQUIRED_FIELDS)

        issue = {
            "slug": slug,
            "name": record.get("name") or record.get("n"),
            "manifest_path": str(manifest_path),
            "manifest_problem": manifest_problem,
            "missing_manifest_fields": missing_manifest_fields,
            "missing_url_fields": missing_url_fields,
            "missing_state_fields": missing_state_fields,
        }

        if any((manifest_problem, missing_manifest_fields, missing_url_fields, missing_state_fields)):
            issues.append(issue)

        if missing_manifest_fields:
            manifest_gap_count += 1
        if missing_url_fields:
            url_gap_count += 1
        if missing_state_fields:
            state_gap_count += 1

    issues.sort(
        key=lambda item: (
            0 if item.get("manifest_problem") else 1,
            -(len(item.get("missing_manifest_fields", [])) + len(item.get("missing_url_fields", [])) + len(item.get("missing_state_fields", []))),
            str(item.get("slug") or ""),
        )
    )

    return {
        "count": len(issues),
        "manifest_gap_count": manifest_gap_count,
        "url_gap_count": url_gap_count,
        "state_gap_count": state_gap_count,
        "issues": issues,
    }
