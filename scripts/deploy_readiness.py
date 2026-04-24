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
STATE_PATH = ROOT / "STATE.json"
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"

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


def _missing_fields(
    record: dict[str, Any] | None, fields: tuple[str, ...]
) -> list[str]:
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
            if status in ("spec_ready", "ready_to_deploy"):
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
        manifest = (
            normalize_record(raw_manifest) if isinstance(raw_manifest, dict) else None
        )

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

        if any(
            (
                manifest_problem,
                missing_manifest_fields,
                missing_url_fields,
                missing_state_fields,
            )
        ):
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
            -(
                len(item.get("missing_manifest_fields", []))
                + len(item.get("missing_url_fields", []))
                + len(item.get("missing_state_fields", []))
            ),
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


def suggest_vercel_url(slug: str) -> str:
    """Return the canonical Vercel URL for a given product slug.

    Convention: ``https://{slug}.vercel.app``
    """
    cleaned = slug.strip().lower()
    return f"https://{cleaned}.vercel.app"


def batch_suggest_vercel_urls(slugs: list[str]) -> dict[str, str]:
    """Return a mapping of slug → suggested Vercel URL.

    Useful for agents that need to quickly populate missing vercel_url fields
    without querying the Vercel API.
    """
    return {slug: suggest_vercel_url(slug) for slug in slugs}


def auto_fix_suggestions(
    state: dict[str, Any],
    *,
    root: Path = ROOT,
) -> list[dict[str, Any]]:
    """Generate concrete auto-fix suggestions for spec-ready products.

    For each spec-ready product missing URL fields, produces a list of
    vercel_url suggestions and identifies which STATE fields can be
    auto-populated from the product manifest.

    Returns a list of fix records suitable for downstream agents to apply.
    """
    readiness = collect_spec_ready_deploy_readiness(state, root=root)
    suggestions: list[dict[str, Any]] = []

    for issue in readiness.get("issues", []):
        slug = issue.get("slug", "unknown")
        url_gaps = issue.get("missing_url_fields", [])
        state_gaps = issue.get("missing_state_fields", [])
        manifest_gaps = issue.get("missing_manifest_fields", [])

        if not (url_gaps or state_gaps):
            continue

        fix: dict[str, Any] = {
            "slug": slug,
            "suggested_vercel_url": suggest_vercel_url(slug),
            "url_fields_missing": url_gaps,
            "state_fields_missing": state_gaps,
            "manifest_ok": not manifest_gaps and issue.get("manifest_problem") is None,
            "auto_fillable": {},
        }

        if "vercel_url" in url_gaps or "deployment_url" in url_gaps:
            url = suggest_vercel_url(slug)
            fillable = {}
            if "vercel_url" in url_gaps:
                fillable["vercel_url"] = url
            if "deployment_url" in url_gaps:
                fillable["deployment_url"] = url
            fix["auto_fillable"].update(fillable)

        manifest_path = root / "products" / slug / "product.json"
        raw_manifest = _load_json(manifest_path)
        if isinstance(raw_manifest, dict):
            manifest = normalize_record(raw_manifest)
            if "github_url" in url_gaps and has_value(manifest.get("github_url")):
                fix["auto_fillable"]["github_url"] = manifest["github_url"]
            if "checkout_url" in url_gaps and has_value(manifest.get("checkout_url")):
                fix["auto_fillable"]["checkout_url"] = manifest["checkout_url"]

        suggestions.append(fix)

    suggestions.sort(key=lambda s: (0 if s["manifest_ok"] else 1, str(s["slug"])))
    return suggestions


def readiness_summary(
    state_path: Path = STATE_PATH,
    summary_path: Path = SUMMARY_PATH,
    *,
    root: Path = ROOT,
) -> dict[str, Any]:
    """One-call deploy-readiness overview merging STATE and STATE_SUMMARY data.

    Returns a compact dict that downstream agents can use for quick triage
    without parsing the full STATE_SUMMARY or running the full readiness check.

    Example output::

        {
            "total_spec_ready": 24,
            "issues_count": 20,
            "manifest_gap": 0,
            "url_gap": 20,
            "state_gap": 20,
            "deploy_missing_or_bad_url": 18,
            "live_count": 89,
            "healthy_count": 86,
            "health_pct": 96.6,
            "top_url_gap_slugs": ["slug-a", "slug-b"],
        }
    """
    state = _load_json(state_path) or {}
    summary = _load_json(summary_path) or {}

    readiness = collect_spec_ready_deploy_readiness(state, root=root)

    live_count = summary.get("live_count", 0)
    healthy_count = summary.get("healthy_count", 0)
    health_pct = round(healthy_count / live_count * 100, 1) if live_count else 0.0

    top_url_gap_slugs: list[str] = []
    for issue in readiness.get("issues", [])[:5]:
        if issue.get("missing_url_fields"):
            top_url_gap_slugs.append(issue.get("slug", "unknown"))

    return {
        "total_spec_ready": summary.get("spec_ready_count", 0),
        "issues_count": readiness["count"],
        "manifest_gap": readiness["manifest_gap_count"],
        "url_gap": readiness["url_gap_count"],
        "state_gap": readiness["state_gap_count"],
        "deploy_missing_or_bad_url": summary.get("deploy_missing_or_bad_url", 0),
        "live_count": live_count,
        "healthy_count": healthy_count,
        "health_pct": health_pct,
        "top_url_gap_slugs": top_url_gap_slugs,
    }


PAYMENT_BLOCKERS = {
    "missing_checkout_url": "Polar checkout link missing — run polar_checkout_sync.py",
    "missing_vercel_url": "Not deployed — deploy via Vercel first",
    "missing_health_check": "No health check recorded — run health_check.py",
    "unhealthy": "Deployed but unhealthy — triage via unhealthy_triage.py",
}


def _payment_blockers(record: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    c_url = record.get("checkout_url") or record.get("c")
    if not has_value(c_url) or not str(c_url).startswith("http"):
        blockers.append("missing_checkout_url")
    v_url = record.get("vercel_url") or record.get("v") or record.get("deployment_url")
    if not has_value(v_url) or not str(v_url).startswith("http"):
        blockers.append("missing_vercel_url")
    last_hc = record.get("last_health_code")
    if last_hc is None:
        blockers.append("missing_health_check")
    elif isinstance(last_hc, int) and last_hc >= 400:
        blockers.append("unhealthy")
    return blockers


def ready_for_payment_audit(
    state_path: Path = STATE_PATH,
) -> dict[str, Any]:
    """Audit ready_for_payment products and identify blockers to going live.

    Scans STATE.json for products with status ``ready_for_payment`` and
    reports which ones can be fast-tracked to live vs. which need action.

    Returns a dict with keys:
        - ``total``: number of ready_for_payment products
        - ``live_ready``: products with no blockers (can go live)
        - ``blocked``: products with one or more blockers
        - ``blocker_counts``: how many products have each blocker type
    """
    state = _load_json(state_path)
    if not state:
        return {
            "total": 0,
            "live_ready": [],
            "blocked": [],
            "blocker_counts": {},
        }

    products = state.get("products", {})
    collections: list[list[dict[str, Any]]] = []
    if isinstance(products, dict):
        for key in ("active", "spec_ready"):
            coll = products.get(key, [])
            if isinstance(coll, list):
                collections.append(coll)
    elif isinstance(products, list):
        collections.append(products)

    seen: set[str] = set()
    live_ready: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    blocker_counts: dict[str, int] = {}

    for collection in collections:
        for item in collection:
            if not isinstance(item, dict):
                continue
            normalized = normalize_record(item)
            status = str(normalized.get("status") or "").strip()
            if status != "ready_for_payment":
                continue
            slug = _pick_slug(normalized) or "unknown"
            if slug in seen:
                continue
            seen.add(slug)

            product_blockers = _payment_blockers(normalized)
            entry = {
                "slug": slug,
                "name": normalized.get("name") or normalized.get("n", slug),
                "vercel_url": normalized.get("vercel_url") or normalized.get("v", ""),
                "checkout_url": normalized.get("checkout_url") or normalized.get("c", ""),
                "last_health_code": normalized.get("last_health_code"),
                "blockers": product_blockers,
            }

            if product_blockers:
                blocked.append(entry)
                for b in product_blockers:
                    blocker_counts[b] = blocker_counts.get(b, 0) + 1
            else:
                live_ready.append(entry)

    live_ready.sort(key=lambda e: str(e["slug"]))
    blocked.sort(key=lambda e: (len(e["blockers"]), str(e["slug"])))

    return {
        "total": len(live_ready) + len(blocked),
        "live_ready": live_ready,
        "blocked": blocked,
        "blocker_counts": blocker_counts,
    }

