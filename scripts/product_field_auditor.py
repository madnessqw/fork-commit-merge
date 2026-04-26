#!/usr/bin/env python3
"""Product field coverage auditor for UniverseCreator portfolio.

Analyzes product.json files across all products, identifies missing
or empty required fields, and generates actionable reports.

Modes:
  audit   — report field coverage gaps (default)
  fix     — auto-fill fields where possible (slug from dir, status from state)
  report  — full coverage summary with per-field breakdown
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_FIELDS = [
    "name",
    "slug",
    "tagline",
    "description",
    "price",
    "features",
    "tech_stack",
    "status",
    "vercel_url",
    "checkout_url",
]

RECOMMENDED_FIELDS = [
    "github_url",
    "created_cycle",
    "deployed_cycle",
    "seo_optimized",
    "spec_version",
    "payment_provider",
]

PRODUCTS_DIR = Path(__file__).resolve().parent.parent / "products"


def load_product(slug: str) -> dict | None:
    path = PRODUCTS_DIR / slug / "product.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save_product(slug: str, data: dict) -> None:
    path = PRODUCTS_DIR / slug / "product.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_all_slugs() -> list[str]:
    if not PRODUCTS_DIR.is_dir():
        return []
    return sorted(
        d
        for d in os.listdir(PRODUCTS_DIR)
        if (PRODUCTS_DIR / d).is_dir() and (PRODUCTS_DIR / d / "product.json").is_file()
    )


def audit_products(slugs: list[str] | None = None) -> dict:
    target = slugs or get_all_slugs()
    results = {
        "total": len(target),
        "field_gaps": {},
        "product_scores": {},
        "empty_fields": {},
    }

    for slug in target:
        product = load_product(slug)
        if product is None:
            results["product_scores"][slug] = {"score": 0, "missing": REQUIRED_FIELDS + RECOMMENDED_FIELDS}
            continue

        missing_required = []
        missing_recommended = []
        empty_values = []

        all_fields = REQUIRED_FIELDS + RECOMMENDED_FIELDS
        for field in all_fields:
            val = product.get(field)
            if val is None:
                if field in REQUIRED_FIELDS:
                    missing_required.append(field)
                else:
                    missing_recommended.append(field)
                results["field_gaps"].setdefault(field, []).append(slug)
            elif isinstance(val, str) and not val.strip():
                empty_values.append(field)
                results["empty_fields"].setdefault(field, []).append(slug)
            elif isinstance(val, list) and len(val) == 0:
                empty_values.append(field)
                results["empty_fields"].setdefault(field, []).append(slug)

        total = len(all_fields)
        filled = total - len(missing_required) - len(missing_recommended) - len(empty_values)
        score = round(filled / total * 100, 1) if total > 0 else 0

        results["product_scores"][slug] = {
            "score": score,
            "missing": missing_required + missing_recommended,
            "empty": empty_values,
        }

    return results


def fix_products(slugs: list[str] | None = None, dry_run: bool = False) -> dict:
    target = slugs or get_all_slugs()
    fixes_applied = {}

    for slug in target:
        product = load_product(slug)
        if product is None:
            continue

        changed = False

        if not product.get("slug"):
            product["slug"] = slug
            changed = True

        if not product.get("status"):
            if product.get("vercel_url"):
                product["status"] = "live"
                changed = True
            else:
                product["status"] = "active"
                changed = True

        if not product.get("spec_version"):
            product["spec_version"] = "1.0"
            changed = True

        if not product.get("payment_provider"):
            if product.get("checkout_url", "").startswith("https://buy.polar.sh"):
                product["payment_provider"] = "polar"
                changed = True

        if not product.get("name"):
            product["name"] = slug.replace("-", " ").title()
            changed = True

        if changed:
            fixes_applied[slug] = list(set(
                k for k, v in product.items()
                if k in {"slug", "status", "spec_version", "payment_provider", "name"} and v
            ))
            if not dry_run:
                save_product(slug, product)

    return {"fixed": len(fixes_applied), "dry_run": dry_run, "products": fixes_applied}


def generate_report(results: dict) -> str:
    lines = []
    lines.append(f"# Product Field Coverage Report")
    lines.append(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Products:** {results['total']}")
    lines.append("")

    scores = results["product_scores"]
    if not scores:
        return "\n".join(lines) + "\n_No products found._\n"

    avg_score = sum(s["score"] for s in scores.values()) / len(scores) if scores else 0
    low_score = {k: v for k, v in scores.items() if v["score"] < 50}
    high_score = {k: v for k, v in scores.items() if v["score"] >= 90}

    lines.append(f"## Summary")
    lines.append(f"- Average coverage: **{avg_score:.1f}%**")
    lines.append(f"- High coverage (>=90%): **{len(high_score)}** products")
    lines.append(f"- Low coverage (<50%): **{len(low_score)}** products")
    lines.append("")

    lines.append("## Field Gaps (Missing)")
    for field, slugs in sorted(results["field_gaps"].items(), key=lambda x: -len(x[1])):
        pct = len(slugs) / results["total"] * 100
        marker = "🔴" if pct > 40 else "🟡" if pct > 15 else "🟢"
        lines.append(f"- {marker} `{field}`: {len(slugs)}/{results['total']} ({pct:.0f}%)")
        if len(slugs) <= 5:
            for s in slugs:
                lines.append(f"  - {s}")
    lines.append("")

    if results["empty_fields"]:
        lines.append("## Empty Fields (Present but empty)")
        for field, slugs in sorted(results["empty_fields"].items(), key=lambda x: -len(x[1])):
            lines.append(f"- `{field}`: {len(slugs)} products")
        lines.append("")

    lines.append("## Lowest Coverage Products")
    for slug, info in sorted(scores.items(), key=lambda x: x[1]["score"])[:10]:
        lines.append(f"- `{slug}`: {info['score']}% — missing: {', '.join(info['missing'][:5])}")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Product field coverage auditor")
    parser.add_argument("mode", nargs="?", default="audit", choices=["audit", "fix", "report"])
    parser.add_argument("--slug", action="append", help="Specific product slug(s)")
    parser.add_argument("--dry-run", action="store_true", help="Preview fixes without writing")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    slugs = args.slug or None

    if args.mode == "audit":
        results = audit_products(slugs)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(generate_report(results))

    elif args.mode == "fix":
        results = fix_products(slugs, dry_run=args.dry_run)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            dr = " (dry-run)" if args.dry_run else ""
            print(f"Fixed {results['fixed']} products{dr}")
            for slug, fields in results["products"].items():
                print(f"  {slug}: {', '.join(fields)}")

    elif args.mode == "report":
        results = audit_products(slugs)
        report = generate_report(results)
        report_path = Path(__file__).resolve().parent.parent / "analysis" / "field_coverage_report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        print(f"Report written to {report_path}")
        if args.json:
            print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
