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
    assert cc.get('canonical_url_override') is not None, "croncraft missing override"
    assert 'croncraft' in cc['canonical_url_override']


def test_chmod_calculator_override_set():
    state = _load_state()
    products = state.get('products', {}).get('active', [])
    ch = next((p for p in products if p.get('slug') == 'chmod-calculator'), None)
    assert ch is not None, "chmod-calculator not found"
    assert ch.get('canonical_url_override') is not None, "chmod-calculator missing override"
    assert 'chmod-calculator' in ch['canonical_url_override']
