import json
import sys
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


MOCK_SUMMARY = {
    "gaps": {
        "canonical_url_drift": [
            {
                "slug": "terraink",
                "url": "https://terraink-flax.vercel.app",
                "ideal_url": "https://terraink.vercel.app",
                "health_code": 200,
                "health_status": "alternate_healthy",
                "canonical_url": "https://terraink.vercel.app",
                "canonical_code": 404,
                "canonical_status": "not_found",
            },
            {
                "slug": "terminal-os",
                "url": "https://terminal-os-green.vercel.app",
                "ideal_url": "https://terminal-os.vercel.app",
                "health_code": 200,
                "health_status": "alternate_healthy",
                "canonical_url": "https://terminal-os.vercel.app",
                "canonical_code": 500,
                "canonical_status": "error_500",
            },
        ]
    }
}


def test_load_drift_from_summary_filters_drift_entries():
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_SUMMARY))):
        from scripts.canonical_drift_report import load_drift_from_summary
        products = load_drift_from_summary(Path("/fake/summary.json"))

    slugs = [p["slug"] for p in products]
    assert "terraink" in slugs
    assert "terminal-os" in slugs
    assert len(products) == 2


def test_load_drift_from_summary_sorts_by_severity():
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_SUMMARY))):
        from scripts.canonical_drift_report import load_drift_from_summary
        products = load_drift_from_summary(Path("/fake/summary.json"))

    for p in products:
        assert p["severity"] == "high"


def test_load_drift_from_summary_diagnosis():
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_SUMMARY))):
        from scripts.canonical_drift_report import load_drift_from_summary
        products = load_drift_from_summary(Path("/fake/summary.json"))

    terraink = [p for p in products if p["slug"] == "terraink"][0]
    assert terraink["diagnosis_label"] == "not_found"
    assert terraink["canonical_health_code"] == 404


def test_load_drift_from_summary_handles_missing_file():
    from scripts.canonical_drift_report import load_drift_from_summary
    products = load_drift_from_summary(Path("/nonexistent/summary.json"))
    assert products == []


MOCK_TREND_LINES = (
    '{"ts":"2026-04-25T10:00:00Z","cycle":1155,"canonical_drift":4,"fallback_healthy":4}\n'
    '{"ts":"2026-04-25T11:00:00Z","cycle":1156,"canonical_drift":6,"fallback_healthy":6}\n'
    '{"ts":"2026-04-25T12:00:00Z","cycle":1157,"canonical_drift":0,"fallback_healthy":6}\n'
)


def test_drift_history_summary_active_drift(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text(MOCK_TREND_LINES)
    from scripts.canonical_drift_report import drift_history_summary
    result = drift_history_summary(trend_file=trend_file)
    assert "Peak drift: 6" in result
    assert "cycle 1155" in result


def test_drift_history_summary_cleared_drift(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text(MOCK_TREND_LINES)
    from scripts.canonical_drift_report import drift_history_summary
    result = drift_history_summary(trend_file=trend_file)
    assert "Current: 0" in result


def test_drift_history_summary_no_file(tmp_path):
    from scripts.canonical_drift_report import drift_history_summary
    result = drift_history_summary(trend_file=tmp_path / "nonexistent.jsonl")
    assert "yok" in result


def test_drift_history_summary_all_zero(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text(
        '{"ts":"2026-04-25T10:00:00Z","cycle":1155,"canonical_drift":0,"fallback_healthy":0}\n'
        '{"ts":"2026-04-25T11:00:00Z","cycle":1156,"canonical_drift":0,"fallback_healthy":0}\n'
    )
    from scripts.canonical_drift_report import drift_history_summary
    result = drift_history_summary(trend_file=trend_file)
    assert "NO DRIFT" in result


def test_drift_history_data_returns_entries(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text(MOCK_TREND_LINES)
    from scripts.canonical_drift_report import drift_history_data
    entries = drift_history_data(trend_file=trend_file)
    assert len(entries) == 3
    assert entries[0]["cycle"] == 1155
    assert entries[1]["canonical_drift"] == 6


def test_drift_history_data_missing_file(tmp_path):
    from scripts.canonical_drift_report import drift_history_data
    entries = drift_history_data(trend_file=tmp_path / "nonexistent.jsonl")
    assert entries == []


def test_export_trend_json_flag(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text(MOCK_TREND_LINES)
    from scripts.canonical_drift_report import drift_history_data
    entries = drift_history_data(trend_file=trend_file)
    assert len(entries) == 3
    json_output = json.dumps(entries, ensure_ascii=False)
    parsed = json.loads(json_output)
    assert parsed[0]["cycle"] == 1155


MOCK_TREND_WITH_SLUGS = (
    '{"ts":"2026-04-25T10:00:00Z","cycle":1155,"canonical_drift":2,"fallback_healthy":2,"drift_slugs":["terraink","terminal-os"]}\n'
    '{"ts":"2026-04-25T11:00:00Z","cycle":1156,"canonical_drift":3,"fallback_healthy":3,"drift_slugs":["terraink","terminal-os","nginx-config"]}\n'
    '{"ts":"2026-04-25T12:00:00Z","cycle":1157,"canonical_drift":2,"fallback_healthy":2,"drift_slugs":["terraink","terminal-os"]}\n'
)


def test_drift_persistence_counts_consecutive(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text(MOCK_TREND_WITH_SLUGS)
    from scripts.canonical_drift_report import drift_persistence
    result = drift_persistence(trend_file=trend_file)
    assert result["total_persistent"] == 2
    assert "terraink" in result["slugs"]
    assert "terminal-os" in result["slugs"]
    assert result["slugs"]["terraink"] == 3
    assert result["slugs"]["terminal-os"] == 3
    assert "nginx-config" not in result["slugs"]


def test_drift_persistence_empty_file(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text("")
    from scripts.canonical_drift_report import drift_persistence
    result = drift_persistence(trend_file=trend_file)
    assert result["total_persistent"] == 0
    assert result["slugs"] == {}


def test_drift_persistence_text_format(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text(MOCK_TREND_WITH_SLUGS)
    from scripts.canonical_drift_report import drift_persistence_text
    text = drift_persistence_text(trend_file=trend_file)
    assert "terraink" in text
    assert "3 consecutive" in text
    assert "Persistent slugs: 2" in text


def test_drift_persistence_no_persistent(tmp_path):
    trend_file = tmp_path / "health_trend.jsonl"
    trend_file.write_text(
        '{"ts":"2026-04-25T10:00:00Z","cycle":1155,"canonical_drift":0,"drift_slugs":[]}\n'
        '{"ts":"2026-04-25T11:00:00Z","cycle":1156,"canonical_drift":0,"drift_slugs":[]}\n'
    )
    from scripts.canonical_drift_report import drift_persistence, drift_persistence_text
    result = drift_persistence(trend_file=trend_file)
    assert result["total_persistent"] == 0
    text = drift_persistence_text(trend_file=trend_file)
    assert "No persistent" in text


def test_main_export_trend_json_no_file(tmp_path):
    from scripts.canonical_drift_report import drift_history_data
    entries = drift_history_data(trend_file=tmp_path / "nonexistent.jsonl")
    assert entries == []
    json_output = json.dumps(entries)
    assert json_output == "[]"
