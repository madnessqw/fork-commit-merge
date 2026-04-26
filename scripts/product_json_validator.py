#!/usr/bin/env python3
"""Validate product.json files across the portfolio for data quality.

Checks required fields, URL formats, price consistency, slug matching,
and cross-references with STATE_SUMMARY.json for discrepancies.

Usage:
    python3 scripts/product_json_validator.py
    python3 scripts/product_json_validator.py --status live
    python3 scripts/product_json_validator.py --fix-flags
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PRODUCTS_DIR = ROOT / "products"
STATE_SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"

REQUIRED_LIVE = ["name", "slug", "status", "price", "vercel_url", "checkout_url"]
REQUIRED_BUILDING = ["name", "slug", "status"]
OPTIONAL_LIVE = [
    "description",
    "tagline",
    "features",
    "github_url",
    "polar_product_id",
    "payment_provider",
    "seo_optimized",
]

URL_FIELDS = ["vercel_url", "checkout_url", "github_url"]
VALID_STATUSES = {"building", "live", "pending", "archived", "spec", "spec_ready"}
VALID_PAYMENT_PROVIDERS = {"polar", "stripe", "gumroad", "manual"}

CHECKOUT_PATTERN = re.compile(r"https://buy\.polar\.sh/polar_cl_[A-Za-z0-9]+")
VERCEL_URL_PATTERN = re.compile(r"https://[a-z0-9\-]+\.vercel\.app")
GITHUB_URL_PATTERN = re.compile(r"https://github\.com/[^/]+/[^/]+")


def _load_product(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _validate_url(value: str | None, field: str) -> list[str]:
    if not value:
        return []
    issues: list[str] = []
    if field == "checkout_url" and not CHECKOUT_PATTERN.match(value):
        issues.append(f"checkout_url format mismatch: {value[:60]}")
    elif field == "vercel_url" and not VERCEL_URL_PATTERN.match(value):
        issues.append(f"vercel_url format mismatch: {value[:60]}")
    elif field == "github_url" and value and not GITHUB_URL_PATTERN.match(value):
        issues.append(f"github_url format mismatch: {value[:60]}")
    return issues


def _validate_price(price: Any) -> list[str]:
    if price is None:
        return ["price missing"]
    issues: list[str] = []
    price_str = str(price).lstrip("$")
    if not re.match(r"^\d+(\.\d{1,2})?$", price_str):
        issues.append(f"price format invalid: {price_str}")
    elif float(price_str) <= 0:
        issues.append(f"price must be positive: {price_str}")
    elif float(price_str) > 999:
        issues.append(f"price suspiciously high: {price_str}")
    return issues


def _validate_slug(slug: str | None, dir_name: str) -> list[str]:
    if not slug:
        return ["slug missing"]
    issues: list[str] = []
    if slug != dir_name:
        issues.append(f"slug/dir mismatch: slug={slug} dir={dir_name}")
    if not re.match(r"^[a-z0-9][a-z0-9\-]*[a-z0-9]$", slug) and len(slug) > 1:
        issues.append(f"slug format invalid: {slug}")
    return issues


def validate_product(
    data: dict[str, Any],
    dir_name: str,
    fix_flags: bool = False,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "slug": data.get("slug", dir_name),
        "status": data.get("status", "unknown"),
        "errors": [],
        "warnings": [],
    }

    status = data.get("status", "unknown")
    if status not in VALID_STATUSES:
        result["errors"].append(f"invalid status: {status}")

    required = REQUIRED_LIVE if status == "live" else REQUIRED_BUILDING
    for field in required:
        if field not in data or data[field] is None:
            result["errors"].append(f"required field missing: {field}")

    slug_issues = _validate_slug(data.get("slug"), dir_name)
    result["errors"].extend(slug_issues)

    if status == "live":
        for field in URL_FIELDS:
            val = data.get(field)
            if val:
                url_issues = _validate_url(val, field)
                result["errors"].extend(url_issues)

        price_issues = _validate_price(data.get("price"))
        result["errors"].extend(price_issues)

        for field in OPTIONAL_LIVE:
            if field not in data or data[field] is None:
                result["warnings"].append(f"optional field missing: {field}")

        provider = data.get("payment_provider")
        if provider and provider not in VALID_PAYMENT_PROVIDERS:
            result["errors"].append(f"invalid payment_provider: {provider}")

    if status == "building":
        price_issues = _validate_price(data.get("price"))
        result["warnings"].extend(price_issues)

    result["valid"] = len(result["errors"]) == 0
    return result


def validate_all(
    status_filter: str | None = None,
    fix_flags: bool = False,
) -> dict[str, Any]:
    if not PRODUCTS_DIR.exists():
        return {"error": "products directory not found", "results": []}

    summary_products: dict[str, dict] = {}
    if STATE_SUMMARY_PATH.exists():
        try:
            summary = json.loads(STATE_SUMMARY_PATH.read_text(encoding="utf-8"))
            for p in summary.get("products", []):
                summary_products[p.get("s", "")] = p
        except (json.JSONDecodeError, OSError):
            pass

    results: list[dict[str, Any]] = []
    errors_count = 0
    warnings_count = 0
    status_counts: dict[str, int] = {}

    for product_dir in sorted(PRODUCTS_DIR.iterdir()):
        if not product_dir.is_dir():
            continue
        pj = product_dir / "product.json"
        if not pj.exists():
            continue

        data = _load_product(pj)
        if data is None:
            results.append({
                "slug": product_dir.name,
                "status": "unknown",
                "errors": ["product.json unreadable"],
                "warnings": [],
                "valid": False,
            })
            errors_count += 1
            continue

        result = validate_product(data, product_dir.name, fix_flags)
        status_counts[result["status"]] = status_counts.get(result["status"], 0) + 1

        if status_filter and result["status"] != status_filter:
            continue

        slug = data.get("slug", product_dir.name)
        if slug in summary_products:
            sp = summary_products[slug]
            if result["status"] == "live" and sp.get("st") != "live":
                result["warnings"].append(
                    f"STATE_SUMMARY status mismatch: local=live summary={sp.get('st')}"
                )
            if sp.get("v") and data.get("vercel_url") and sp["v"] != data["vercel_url"]:
                result["warnings"].append(
                    f"vercel_url drift: product.json={data['vercel_url']} summary={sp['v']}"
                )
            if (
                sp.get("c")
                and data.get("checkout_url")
                and sp["c"] != data["checkout_url"]
            ):
                result["warnings"].append(
                    f"checkout_url drift: product.json={data['checkout_url'][:40]} summary={sp['c'][:40]}"
                )
        elif result["status"] == "live":
            result["warnings"].append("not found in STATE_SUMMARY")

        errors_count += len(result["errors"])
        warnings_count += len(result["warnings"])
        results.append(result)

    invalid = [r for r in results if not r["valid"]]
    warned = [r for r in results if r["valid"] and r["warnings"]]

    return {
        "total": len(results),
        "valid": len(results) - len(invalid),
        "invalid": len(invalid),
        "warned": len(warned),
        "errors_count": errors_count,
        "warnings_count": warnings_count,
        "status_counts": status_counts,
        "invalid_products": invalid,
        "warned_products": warned,
        "results": results,
    }


def main() -> int:
    status_filter = None
    fix_flags = False
    for arg in sys.argv[1:]:
        if arg.startswith("--status="):
            status_filter = arg.split("=", 1)[1]
        elif arg == "--status" and sys.argv.index(arg) + 1 < len(sys.argv):
            status_filter = sys.argv[sys.argv.index(arg) + 1]
        elif arg == "--fix-flags":
            fix_flags = True

    report = validate_all(status_filter=status_filter, fix_flags=fix_flags)

    print(f"Product JSON Validation Report")
    print(f"{'=' * 40}")
    print(f"Total products: {report['total']}")
    print(f"Valid: {report['valid']} | Invalid: {report['invalid']} | Warned: {report['warned']}")
    print(f"Errors: {report['errors_count']} | Warnings: {report['warnings_count']}")
    print(f"Status breakdown: {json.dumps(report['status_counts'])}")
    print()

    if report["invalid_products"]:
        print(f"INVALID PRODUCTS ({len(report['invalid_products'])}):")
        for p in report["invalid_products"][:20]:
            print(f"  {p['slug']} ({p['status']}):")
            for e in p["errors"]:
                print(f"    ERROR: {e}")
        if len(report["invalid_products"]) > 20:
            print(f"  ... and {len(report['invalid_products']) - 20} more")
        print()

    if report["warned_products"]:
        print(f"WARNED PRODUCTS ({len(report['warned_products'])}):")
        for p in report["warned_products"][:10]:
            print(f"  {p['slug']} ({p['status']}):")
            for w in p["warnings"]:
                print(f"    WARN: {w}")
        if len(report["warned_products"]) > 10:
            print(f"  ... and {len(report['warned_products']) - 10} more")

    return 1 if report["invalid"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
