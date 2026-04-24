#!/usr/bin/env python3
"""Plan and sync Polar catalog checkout links for UniverseCreator products.

Use checkout links for fixed catalog products (static product pages).
Use checkout sessions separately for ad-hoc / custom work.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.checkout_metadata import infer_payment_provider

PRODUCTS_DIR = ROOT / "products"
DEFAULT_STATUSES = ("live", "ready_for_payment")
POLAR_API = "https://api.polar.sh/v1"
POLAR_PROVIDER = "polar"


@dataclass
class LocalProduct:
    path: Path
    slug: str
    name: str
    description: str
    price_cents: int
    price_display: str
    price_source: str
    status: str
    vercel_url: str | None
    checkout_url: str | None
    payment_provider: str | None
    selection_reason: str
    raw: dict[str, Any]


class PolarAPIError(RuntimeError):
    pass


class PolarClient:
    def __init__(self, token: str, *, base_url: str = POLAR_API) -> None:
        self.token = token
        self.base_url = base_url.rstrip("/")

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any]:
        url = f"{self.base_url}{path}"
        if query:
            qp = {k: v for k, v in query.items() if v is not None}
            url = f"{url}?{urllib.parse.urlencode(qp)}"

        data = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise PolarAPIError(f"{method} {path} failed: HTTP {exc.code} — {body}") from exc
        except urllib.error.URLError as exc:
            raise PolarAPIError(f"{method} {path} failed: {exc}") from exc

        if not raw.strip():
            return {}
        return json.loads(raw)

    def list_products(self) -> list[dict[str, Any]]:
        data = self.request("GET", "/products", query={"limit": 200})
        if isinstance(data, dict) and isinstance(data.get("items"), list):
            return list(data["items"])
        if isinstance(data, list):
            return list(data)
        raise PolarAPIError(f"Unexpected products payload: {type(data).__name__}")

    def list_checkout_links(self) -> list[dict[str, Any]]:
        data = self.request("GET", "/checkout-links", query={"limit": 200})
        if isinstance(data, dict) and isinstance(data.get("items"), list):
            return list(data["items"])
        if isinstance(data, list):
            return list(data)
        raise PolarAPIError(f"Unexpected checkout-links payload: {type(data).__name__}")

    def create_product(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = self.request("POST", "/products", payload=payload)
        if not isinstance(data, dict):
            raise PolarAPIError("Unexpected create product payload")
        return data

    def update_product(self, product_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = self.request("PATCH", f"/products/{product_id}", payload=payload)
        if not isinstance(data, dict):
            raise PolarAPIError("Unexpected update product payload")
        return data

    def create_checkout_link(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = self.request("POST", "/checkout-links", payload=payload)
        if not isinstance(data, dict):
            raise PolarAPIError("Unexpected create checkout link payload")
        return data


def slugify_name(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_price_to_cents(value: Any) -> int:
    if isinstance(value, (int, float)):
        amount = float(value)
        return int(round(amount * 100))

    if value is None:
        raise ValueError("price is missing")

    text = str(value).strip()
    if not text:
        raise ValueError("price is empty")

    cleaned = text.lower().replace("usd", "").replace("$", "")
    cleaned = cleaned.replace("one-time", "").replace("one time", "")
    cleaned = cleaned.replace("lifetime", "")
    cleaned = cleaned.strip()
    match = re.search(r"\d+(?:\.\d{1,2})?", cleaned)
    if not match:
        raise ValueError(f"could not parse price: {value!r}")
    amount = float(match.group(0))
    return int(round(amount * 100))


def find_price_in_text(text: str) -> tuple[int, str] | None:
    patterns = [
        r"\$\s*(\d+(?:\.\d{1,2})?)",
        r'"price"\s*:\s*"?(\\?\$?\d+(?:\.\d{1,2})?)',
        r'price_amount"\s*:\s*(\d+)',
        r"Get [^\\n\\r$]{0,40}\$\s*(\d+(?:\.\d{1,2})?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue
        raw = match.group(1)
        if pattern.endswith(r'(\d+)'):
            amount = int(raw)
            if amount >= 100:
                return amount, f"text:{pattern}"
        cents = parse_price_to_cents(raw)
        return cents, f"text:{pattern}"
    return None


def discover_price_from_files(product_dir: Path) -> tuple[int, str] | None:
    candidate_files = [
        product_dir / "index.html",
        product_dir / "public" / "index.html",
        product_dir / "README.md",
        product_dir / "product-spec.md",
        product_dir / "spec.json",
        product_dir / "spec.md",
        product_dir / "api" / "process.js",
    ]
    for path in candidate_files:
        if not path.exists() or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        found = find_price_in_text(text)
        if found is not None:
            cents, source = found
            try:
                location = str(path.relative_to(ROOT))
            except ValueError:
                location = str(path)
            return cents, f"{location}:{source}"
    return None


def polar_checkout_requires_link_repair(
    raw: dict[str, Any],
    *,
    checkout_url: str | None,
    payment_provider: str | None,
) -> bool:
    if payment_provider != POLAR_PROVIDER:
        return False
    if not checkout_url:
        return True
    if not str(raw.get("polar_checkout_link_id") or "").strip():
        return True
    if not str(raw.get("polar_product_id") or "").strip():
        return True
    return False


def load_local_products(
    *,
    statuses: set[str],
    include_existing: bool,
    replace_non_polar: bool,
) -> list[LocalProduct]:
    products: list[LocalProduct] = []
    for path in sorted(PRODUCTS_DIR.glob("*/product.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        slug = str(raw.get("slug") or path.parent.name).strip()
        status = str(raw.get("status") or "").strip().lower()
        if statuses and status not in statuses:
            continue

        if not raw.get("vercel_url"):
            continue

        checkout_url = raw.get("checkout_url")
        checkout_url_normalized = str(checkout_url).strip() if checkout_url else None
        provider_normalized = infer_payment_provider(raw, checkout_url=checkout_url_normalized)
        should_replace_non_polar = replace_non_polar and provider_normalized not in (None, POLAR_PROVIDER)
        should_repair_polar_link = polar_checkout_requires_link_repair(
            raw,
            checkout_url=checkout_url_normalized,
            payment_provider=provider_normalized,
        )
        selection_reason = "missing_checkout"
        if checkout_url_normalized:
            if include_existing:
                selection_reason = "include_existing"
            elif should_replace_non_polar:
                selection_reason = "replace_non_polar"
            elif should_repair_polar_link:
                selection_reason = "repair_polar_link"
            else:
                continue

        # Price resolution: spec.json (authoritative) → product.json → file text discovery
        # spec.json is the design document and matches what's displayed on the website
        spec_price_cents: int | None = None
        spec_price_raw: str | None = None
        spec_path = path.parent / "spec.json"
        if spec_path.exists():
            try:
                spec_raw = json.loads(spec_path.read_text(encoding="utf-8"))
                spec_price_field = spec_raw.get("price")
                if spec_price_field:
                    spec_price_cents = parse_price_to_cents(spec_price_field)
                    spec_price_raw = str(spec_price_field)
            except (OSError, json.JSONDecodeError, ValueError):
                pass

        product_price_cents: int | None = None
        try:
            product_price_cents = parse_price_to_cents(raw.get("price"))
        except ValueError:
            pass

        if spec_price_cents is not None and product_price_cents is not None:
            if spec_price_cents != product_price_cents:
                # spec.json is more authoritative (design document = website price)
                price_cents = spec_price_cents
                price_source = f"spec.json:price (product.json={raw.get('price')} overridden)"
            else:
                price_cents = spec_price_cents
                price_source = "spec.json:price"
        elif spec_price_cents is not None:
            price_cents = spec_price_cents
            price_source = "spec.json:price"
        elif product_price_cents is not None:
            price_cents = product_price_cents
            price_source = "product.json:price"
        else:
            discovered = discover_price_from_files(path.parent)
            if discovered is None:
                continue
            price_cents, price_source = discovered

        price_display = spec_price_raw if spec_price_raw else str(raw.get("price", ""))

        name = str(raw.get("name") or slug).strip()
        description = str(raw.get("description") or raw.get("tagline") or name).strip()
        products.append(
            LocalProduct(
                path=path,
                slug=slug,
                name=name,
                description=description,
                price_cents=price_cents,
                price_display=price_display,
                price_source=price_source,
                status=status,
                vercel_url=str(raw.get("vercel_url") or "").strip() or None,
                checkout_url=checkout_url_normalized,
                payment_provider=provider_normalized,
                selection_reason=selection_reason,
                raw=raw,
            )
        )
    return products


def fixed_price_for_product(product: dict[str, Any], expected_cents: int) -> dict[str, Any] | None:
    prices = product.get("prices") or []
    for price in prices:
        if price.get("is_archived"):
            continue
        if str(price.get("price_currency") or "").lower() != "usd":
            continue
        amount = price.get("price_amount")
        if amount == expected_cents:
            return price
    return None


def local_product_metadata(product: LocalProduct) -> dict[str, Any]:
    return {
        "source": "universecreator",
        "local_slug": product.slug,
        "local_status": product.status,
    }


def product_needs_update(remote: dict[str, Any], local: LocalProduct) -> bool:
    remote_name = str(remote.get("name") or "").strip()
    remote_description = str(remote.get("description") or "").strip()
    remote_visibility = str(remote.get("visibility") or "").strip().lower()
    remote_price = fixed_price_for_product(remote, local.price_cents)
    return (
        remote_name != local.name
        or remote_description != local.description
        or remote_visibility != "public"
        or remote_price is None
    )


def find_remote_product(remote_products: list[dict[str, Any]], local: LocalProduct) -> dict[str, Any] | None:
    slug_match = None
    name_match = None
    local_name_slug = slugify_name(local.name)
    for product in remote_products:
        metadata = product.get("metadata") or {}
        if metadata.get("local_slug") == local.slug:
            slug_match = product
            break
        product_name_slug = slugify_name(str(product.get("name") or ""))
        if product_name_slug == local_name_slug:
            name_match = product
    return slug_match or name_match


def link_matches_product(link: dict[str, Any], product_id: str, local_slug: str) -> bool:
    metadata = link.get("metadata") or {}
    if metadata.get("local_slug") == local_slug:
        return True
    for product in link.get("products") or []:
        if product.get("id") == product_id:
            return True
    return False


def ensure_remote_product(client: PolarClient, remote_products: list[dict[str, Any]], local: LocalProduct) -> dict[str, Any]:
    remote = find_remote_product(remote_products, local)
    price_payload = {
        "amount_type": "fixed",
        "price_amount": local.price_cents,
        "price_currency": "usd",
    }
    payload = {
        "name": local.name,
        "description": local.description,
        "visibility": "public",
        "metadata": local_product_metadata(local),
        "prices": [price_payload],
    }

    if remote is None:
        created = client.create_product(payload)
        remote_products.append(created)
        return created

    if product_needs_update(remote, local):
        updated = client.update_product(remote["id"], payload)
        remote_products[:] = [updated if item.get("id") == updated.get("id") else item for item in remote_products]
        return updated

    return remote


def ensure_checkout_link(
    client: PolarClient,
    checkout_links: list[dict[str, Any]],
    *,
    remote_product: dict[str, Any],
    local: LocalProduct,
) -> dict[str, Any]:
    product_id = str(remote_product["id"])
    existing = next(
        (link for link in checkout_links if link_matches_product(link, product_id, local.slug)),
        None,
    )
    if existing is not None:
        return existing

    price = fixed_price_for_product(remote_product, local.price_cents)
    if price is None:
        raise PolarAPIError(f"No active fixed USD price on Polar product for {local.slug}")

    success_url = f"{local.vercel_url}?checkout=success&checkout_id={{CHECKOUT_ID}}" if local.vercel_url else None
    return_url = local.vercel_url
    created = client.create_checkout_link(
        {
            "product_price_id": price["id"],
            "payment_processor": "stripe",
            "label": f"universecreator:{local.slug}",
            "metadata": {
                "source": "universecreator",
                "local_slug": local.slug,
            },
            "success_url": success_url,
            "return_url": return_url,
            "allow_discount_codes": True,
        }
    )
    checkout_links.append(created)
    return created


def update_local_product(
    local: LocalProduct,
    *,
    remote_product: dict[str, Any],
    checkout_link: dict[str, Any],
) -> None:
    data = dict(local.raw)
    data["checkout_url"] = checkout_link.get("url")
    data["payment_provider"] = POLAR_PROVIDER
    data["polar_product_id"] = remote_product.get("id")
    price = fixed_price_for_product(remote_product, local.price_cents)
    data["polar_product_price_id"] = price.get("id") if price else None
    data["polar_checkout_link_id"] = checkout_link.get("id")
    local.path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_report(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def cmd_plan(args: argparse.Namespace) -> int:
    products = load_local_products(
        statuses=set(args.status),
        include_existing=args.include_existing,
        replace_non_polar=args.replace_non_polar,
    )
    report_lines = [
        "# Polar Checkout Rollout Plan",
        "",
        f"- total_candidates: {len(products)}",
        f"- statuses: {', '.join(args.status)}",
        f"- include_existing: {args.include_existing}",
        f"- replace_non_polar: {args.replace_non_polar}",
        "",
        "| Slug | Name | Price | Price Source | Status | Existing Checkout | Provider | Selection |",
        "|---|---|---:|---|---|---|---|---|",
    ]
    for product in products:
        report_lines.append(
            f"| {product.slug} | {product.name} | ${product.price_cents/100:.2f} | {product.price_source} | {product.status} | {'yes' if product.checkout_url else 'no'} | {product.payment_provider or '-'} | {product.selection_reason} |"
        )

    if args.output:
        write_report(Path(args.output), report_lines)
    print("\n".join(report_lines))
    return 0


def cmd_sync_links(args: argparse.Namespace) -> int:
    token = os.environ.get(args.token_env)
    if not token:
        raise SystemExit(f"{args.token_env} env var missing")

    client = PolarClient(token)
    products = load_local_products(
        statuses=set(args.status),
        include_existing=args.include_existing,
        replace_non_polar=args.replace_non_polar,
    )
    remote_products = client.list_products()
    checkout_links = client.list_checkout_links()

    changed: list[str] = []
    report_lines = [
        "# Polar Checkout Sync Report",
        "",
        f"- candidates: {len(products)}",
        f"- statuses: {', '.join(args.status)}",
        f"- include_existing: {args.include_existing}",
        f"- replace_non_polar: {args.replace_non_polar}",
        "",
        "| Slug | Action | Price Source | Checkout URL |",
        "|---|---|---|---|",
    ]

    for product in products:
        remote_product = ensure_remote_product(client, remote_products, product)
        checkout_link = ensure_checkout_link(client, checkout_links, remote_product=remote_product, local=product)
        previous_url = product.checkout_url
        update_local_product(product, remote_product=remote_product, checkout_link=checkout_link)
        action = "kept" if previous_url == checkout_link.get("url") else "updated"
        if product.selection_reason == "repair_polar_link" and action == "updated":
            action = "relinked"
        if action == "updated":
            changed.append(product.slug)
        elif action == "relinked":
            changed.append(product.slug)
        report_lines.append(f"| {product.slug} | {action} | {product.price_source} | {checkout_link.get('url')} |")

    if args.output:
        write_report(Path(args.output), report_lines)

    print(f"synced={len(products)} changed={len(changed)}")
    for slug in changed[:50]:
        print(slug)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    def add_shared_flags(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "--status",
            action="append",
            default=None,
            help="Eligible local product statuses (repeatable). Default: live + ready_for_payment",
        )
        p.add_argument(
            "--include-existing",
            action="store_true",
            help="Include products that already have checkout URLs.",
        )
        p.add_argument(
            "--replace-non-polar",
            action="store_true",
            help="Also include products whose existing checkout/payment provider is not Polar.",
        )
        p.add_argument("--output", help="Optional markdown report output path.")

    plan = sub.add_parser("plan", help="Preview which local products are eligible for Polar checkout rollout.")
    add_shared_flags(plan)
    plan.set_defaults(func=cmd_plan)

    sync = sub.add_parser("sync-links", help="Create/update Polar products + checkout links and write checkout URLs locally.")
    add_shared_flags(sync)
    sync.add_argument(
        "--token-env",
        default="POLAR_OAT",
        help="Environment variable that stores the Polar Organization Access Token.",
    )
    sync.set_defaults(func=cmd_sync_links)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.status is None:
        args.status = list(DEFAULT_STATUSES)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
