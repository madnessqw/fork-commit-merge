import json
import pytest
import os

STATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'STATE.json')


def _load_state():
    with open(STATE_PATH, 'r') as f:
        return json.load(f)


def test_state_json_is_valid():
    state = _load_state()
    products = state.get('products', {}).get('active', [])
    assert isinstance(products, list)
    assert len(products) > 0


def test_no_canonical_url_drift_products_without_override():
    state = _load_state()
    drift_list = state.get('canonical_url_drift_products', [])
    products = state.get('products', {}).get('active', [])
    
    for slug in drift_list:
        product = next((p for p in products if p.get('slug') == slug), None)
        assert product is not None, f"Drift product {slug} not found in STATE.json"
        assert product.get('canonical_url_override'), \
            f"Drift product {slug} has no canonical_url_override set"


def test_canonical_override_urls_are_http():
    state = _load_state()
    products = state.get('products', {}).get('active', [])
    
    for p in products:
        override = p.get('canonical_url_override')
        if override:
            assert override.startswith('http'), \
                f"{p['slug']} override URL does not start with http: {override}"


def test_croncraft_override_set():
    state = _load_state()
    products = state.get('products', {}).get('active', [])
    cc = next((p for p in products if p.get('slug') == 'croncraft'), None)
    assert cc is not None, "croncraft not found"
    override = cc.get('canonical_url_override')
    assert override is not None, "croncraft missing override"
    assert override.startswith('http'), f"croncraft override is not a valid URL: {override}"
    assert 'vercel.app' in override, f"croncraft override is not a Vercel URL: {override}"


def test_chmod_calculator_override_set():
    state = _load_state()
    products = state.get('products', {}).get('active', [])
    ch = next((p for p in products if p.get('slug') == 'chmod-calculator'), None)
    assert ch is not None, "chmod-calculator not found"
    assert ch.get('canonical_url_override') is not None, "chmod-calculator missing override"
    assert 'chmod-calculator' in ch['canonical_url_override']


FALLBACK_URL_PATTERNS = [
    "-37cz7b6yo-",
    "-azjwwgvl6-",
    "-egj3ho5tp-",
    "-1p2e2xs77-",
]

KNOWN_DRIFT_SLUGS = {
    "html-entity-encoder",
    "chmod-calculator",
    "nginx-config",
}


def _is_fallback_vercel_url(url: str) -> bool:
    if not url:
        return False
    host = url.split("//")[-1].split("/")[0].lower()
    base = host.replace(".vercel.app", "")
    return any(pat in base for pat in FALLBACK_URL_PATTERNS)


def test_canonical_overrides_are_not_fallback_urls():
    state = _load_state()
    products = state.get('products', {}).get('active', [])
    violations = []
    for p in products:
        override = p.get('canonical_url_override', '')
        slug = p.get('slug', '')
        if slug in KNOWN_DRIFT_SLUGS:
            continue
        if override and _is_fallback_vercel_url(override):
            violations.append(f"{slug}: {override}")
    assert not violations, (
        f"canonical_url_override should be the ideal/canonical URL, not a fallback. "
        f"Violations: {violations}"
    )
