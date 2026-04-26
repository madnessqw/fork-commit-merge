#!/usr/bin/env python3
"""Validate Polar checkout links across the portfolio.

Checks every product in STATE_SUMMARY.json for:
- URL format correctness (must be ``https://buy.polar.sh/polar_cl_...``)
- Polar ID extraction and uniqueness
- Provider consistency (all should be ``polar``)
- Missing or malformed checkout URLs on live products

Typical usage::

    python3 -m scripts.checkout_link_validator
    python3 -m scripts.checkout_link_validator --json
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "STATE_SUMMARY.json"

POLAR_URL_PATTERN = re.compile(
    r"^https://buy\.polar\.sh/polar_cl_[A-Za-z0-9]+$"
)
POLAR_ID_PATTERN = re.compile(r"polar_cl_[A-Za-z0-9]+")


def _slug_of(product: dict[str, Any]) -> str:
    return product.get("s") or product.get("slug") or product.get("n") or "unknown"


def _checkout_of(product: dict[str, Any]) -> str:
    return (product.get("c") or product.get("checkout_url") or "").strip()


def _status_of(product: dict[str, Any]) -> str:
    return (product.get("st") or product.get("status") or "").strip()


def _name_of(product: dict[str, Any]) -> str:
    return product.get("n") or product.get("name") or _slug_of(product)


def extract_polar_id(url: str) -> str | None:
    """Extract the Polar checkout ID from a URL."""
    match = POLAR_ID_PATTERN.search(url)
    return match.group(0) if match else None


def validate_url_format(url: str) -> dict[str, Any]:
    """Check if a checkout URL matches the expected Polar format."""
    issues: list[str] = []
    is_valid = bool(POLAR_URL_PATTERN.match(url))

    if not url:
        issues.append("missing")
        return {"valid": False, "issues": issues}

    if not url.startswith("https://"):
        issues.append("not_https")

    if "polar.sh" not in url and "buy.polar.sh" not in url:
        issues.append("not_polar_domain")

    if not POLAR_ID_PATTERN.search(url):
        issues.append("no_polar_id")

    polar_id = extract_polar_id(url)
    if polar_id and len(polar_id) < 20:
        issues.append("suspicious_short_id")

    return {"valid": is_valid, "issues": issues, "polar_id": polar_id}


def validate_portfolio(
    summary_path: Path = SUMMARY_PATH,
) -> dict[str, Any]:
    """Run full checkout link validation across all products."""
    raw: dict[str, Any] = {}
    try:
        raw = json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "missing": 0,
            "duplicate_ids": 0,
            "issues": ["STATE_SUMMARY.json could not be read"],
            "products": [],
        }

    products = raw.get("products", [])
    if not isinstance(products, list):
        return {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "missing": 0,
            "duplicate_ids": 0,
            "issues": ["products is not a list"],
            "products": [],
        }

    seen_ids: dict[str, list[str]] = {}
    results: list[dict[str, Any]] = []
    valid_count = 0
    invalid_count = 0
    missing_count = 0

    for product in products:
        if not isinstance(product, dict):
            continue

        slug = _slug_of(product)
        name = _name_of(product)
        status = _status_of(product)
        checkout_url = _checkout_of(product)

        validation = validate_url_format(checkout_url)

        if not checkout_url:
            missing_count += 1
        elif validation["valid"]:
            valid_count += 1
        else:
            invalid_count += 1

        polar_id = validation.get("polar_id")
        if polar_id:
            seen_ids.setdefault(polar_id, []).append(slug)

        results.append(
            {
                "slug": slug,
                "name": name,
                "status": status,
                "checkout_url": checkout_url,
                "valid": validation["valid"],
                "issues": validation["issues"],
                "polar_id": polar_id,
            }
        )

    duplicate_groups = {
        pid: slugs for pid, slugs in seen_ids.items() if len(slugs) > 1
    }

    live_missing = [
        r for r in results if r["status"] == "live" and not r["checkout_url"]
    ]
    live_invalid = [
        r for r in results if r["status"] == "live" and r["checkout_url"] and not r["valid"]
    ]

    return {
        "total": len(results),
        "valid": valid_count,
        "invalid": invalid_count,
        "missing": missing_count,
        "duplicate_id_count": len(duplicate_groups),
        "duplicate_ids": duplicate_groups,
        "live_missing_checkout": len(live_missing),
        "live_invalid_checkout": len(live_invalid),
        "products": results,
    }


def health_score(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    """Compute a checkout health score (0-100) for the portfolio."""
    report = validate_portfolio(summary_path)
    total = report["total"]
    if total == 0:
        return {"score": 0, "grade": "F", "details": "no products found"}

    valid_ratio = report["valid"] / total
    penalty_missing = report["missing"] * 5
    penalty_invalid = report["invalid"] * 3
    penalty_dupes = report["duplicate_id_count"] * 2
    penalty_live = (report["live_missing_checkout"] + report["live_invalid_checkout"]) * 10

    raw_score = valid_ratio * 100
    score = max(0, min(100, raw_score - penalty_missing - penalty_invalid - penalty_dupes - penalty_live))

    if score >= 95:
        grade = "A+"
    elif score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    return {
        "score": round(score, 1),
        "grade": grade,
        "total": total,
        "valid": report["valid"],
        "invalid": report["invalid"],
        "missing": report["missing"],
        "duplicate_ids": report["duplicate_id_count"],
        "live_issues": report["live_missing_checkout"] + report["live_invalid_checkout"],
    }


if __name__ == "__main__":
    import sys

    as_json = "--json" in sys.argv
    do_health = "--health" in sys.argv

    if do_health:
        result = health_score()
        if as_json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Checkout Health: {result['score']}/100 (Grade: {result['grade']})")
            print(f"  Valid: {result['valid']}/{result['total']}")
            print(f"  Invalid: {result['invalid']}")
            print(f"  Missing: {result['missing']}")
            print(f"  Duplicate IDs: {result['duplicate_ids']}")
            print(f"  Live issues: {result['live_issues']}")
    else:
        report = validate_portfolio()
        if as_json:
            summary = {k: v for k, v in report.items() if k != "products"}
            summary["sample_invalid"] = [
                {"slug": r["slug"], "url": r["checkout_url"], "issues": r["issues"]}
                for r in report["products"]
                if not r["valid"] and r["checkout_url"]
            ][:10]
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print(f"Total: {report['total']} | Valid: {report['valid']} | Invalid: {report['invalid']} | Missing: {report['missing']}")
            print(f"Duplicate IDs: {report['duplicate_id_count']}")
            print(f"Live missing checkout: {report['live_missing_checkout']}")
            print(f"Live invalid checkout: {report['live_invalid_checkout']}")

            if report["duplicate_ids"]:
                print("\nDuplicate Polar IDs:")
                for pid, slugs in report["duplicate_ids"].items():
                    print(f"  {pid[:20]}... -> {slugs}")
