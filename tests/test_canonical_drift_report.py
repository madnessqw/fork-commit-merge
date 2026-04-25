import json
import textwrap
from pathlib import Path
from unittest.mock import mock_open, patch

ROOT = Path(__file__).resolve().parents[1]

MOCK_STATE = {
    "canonical_url_drift_products": ["croncraft", "terminal-os"],
    "products": {
        "active": [
            {
                "slug": "croncraft",
                "name": "CronCraft",
                "vercel_url": "https://quickcron.vercel.app",
                "ideal_vercel_url": "https://croncraft.vercel.app",
                "canonical_health_url": "https://croncraft.vercel.app",
                "canonical_health_code": 200,
                "canonical_health_status": "healthy",
                "last_health_code": 200,
                "checkout_url": "https://buy.polar.sh/polar_cl_test",
                "checkout_status": "active",
            },
            {
                "slug": "terminal-os",
                "name": "Terminal OS",
                "vercel_url": "https://terminal-os-green.vercel.app",
                "ideal_vercel_url": "https://terminal-os.vercel.app",
                "canonical_health_url": "https://terminal-os.vercel.app",
                "canonical_health_code": 500,
                "canonical_health_status": "unhealthy",
                "last_health_code": 200,
                "checkout_url": "",
                "checkout_status": "unknown",
            },
            {
                "slug": "healthy-product",
                "name": "Healthy",
                "vercel_url": "https://healthy-product.vercel.app",
                "ideal_vercel_url": "https://healthy-product.vercel.app",
                "canonical_health_code": 200,
                "last_health_code": 200,
            },
        ]
    },
}


def test_load_drift_products_filters_by_drift_list():
    with patch("scripts.canonical_drift_report.STATE_PATH", Path("/fake/state.json")), \
         patch("builtins.open", mock_open(read_data=json.dumps(MOCK_STATE))):
        from scripts.canonical_drift_report import load_drift_products
        products = load_drift_products(Path("/fake/state.json"))

    slugs = [p["slug"] for p in products]
    assert "croncraft" in slugs
    assert "terminal-os" in slugs
    assert "healthy-product" not in slugs


def test_load_drift_products_sorts_by_severity():
    with patch("scripts.canonical_drift_report.STATE_PATH", Path("/fake/state.json")), \
         patch("builtins.open", mock_open(read_data=json.dumps(MOCK_STATE))):
        from scripts.canonical_drift_report import load_drift_products
        products = load_drift_products(Path("/fake/state.json"))

    assert products[0]["slug"] == "terminal-os"
    assert products[0]["severity"] == "high"
    assert products[1]["slug"] == "croncraft"


def test_load_drift_products_diagnosis():
    with patch("scripts.canonical_drift_report.STATE_PATH", Path("/fake/state.json")), \
         patch("builtins.open", mock_open(read_data=json.dumps(MOCK_STATE))):
        from scripts.canonical_drift_report import load_drift_products
        products = load_drift_products(Path("/fake/state.json"))

    terminal_os = products[0]
    assert terminal_os["diagnosis_label"] == "server_error"
    assert terminal_os["canonical_health_code"] == 500


def test_load_drift_products_handles_missing_file():
    from scripts.canonical_drift_report import load_drift_products
    products = load_drift_products(Path("/nonexistent/path.json"))
    assert products == []


def test_load_drift_products_handles_invalid_json():
    with patch("builtins.open", mock_open(read_data="not json")):
        from scripts.canonical_drift_report import load_drift_products
        products = load_drift_products(Path("/fake/state.json"))
    assert products == []


def test_to_markdown_includes_all_products():
    from scripts.canonical_drift_report import to_markdown
    products = [
        {
            "slug": "test-prod",
            "name": "Test Product",
            "vercel_url": "https://test-prod-alias.vercel.app",
            "ideal_vercel_url": "https://test-prod.vercel.app",
            "canonical_health_url": "https://test-prod.vercel.app",
            "canonical_health_code": 404,
            "canonical_health_status": "unhealthy",
            "last_health_code": 200,
            "checkout_url": "https://buy.polar.sh/test",
            "checkout_status": "active",
            "diagnosis_label": "not_found",
            "severity": "high",
            "fix_command": "cd products/test-prod && vercel --prod --yes",
        }
    ]
    md = to_markdown(products)
    assert "test-prod" in md
    assert "404" in md
    assert "not_found" in md
    assert "vercel --prod --yes" in md
    assert "Batch Fix Commands" in md


def test_to_markdown_empty_products():
    from scripts.canonical_drift_report import to_markdown
    md = to_markdown([])
    assert "No canonical drift" in md


def test_write_codex_task_creates_file(tmp_path):
    from scripts.canonical_drift_report import write_codex_task
    products = [
        {
            "slug": "demo-prod",
            "canonical_health_code": 500,
            "diagnosis_label": "server_error",
            "fix_command": "cd products/demo-prod && vercel --prod --yes",
        }
    ]
    output = tmp_path / "codex_task.md"
    result = write_codex_task(products, output_path=output)
    assert output.exists()
    content = output.read_text()
    assert "demo-prod" in content
    assert "vercel --prod --yes" in content
    assert "Acceptance Criteria" in content


def test_write_codex_task_empty_products(tmp_path):
    from scripts.canonical_drift_report import write_codex_task
    output = tmp_path / "codex_task.md"
    result = write_codex_task([], output_path=output)
    assert "No drift products" in result


def test_fix_command_includes_slug():
    from scripts.canonical_drift_report import load_drift_products
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_STATE))):
        products = load_drift_products(Path("/fake/state.json"))

    for p in products:
        if p["canonical_health_code"] == 500:
            assert "terminal-os" in p["fix_command"]


def test_severity_order():
    from scripts.canonical_drift_report import SEVERITY_ORDER
    assert SEVERITY_ORDER["high"] < SEVERITY_ORDER["medium"]
    assert SEVERITY_ORDER["medium"] < SEVERITY_ORDER["low"]
    assert SEVERITY_ORDER["low"] < SEVERITY_ORDER["info"]
