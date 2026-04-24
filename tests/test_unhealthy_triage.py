"""Tests for scripts.unhealthy_triage"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.unhealthy_triage import (
    CANONICAL_DRIFT_FIXES,
    HEALTH_GRADE_THRESHOLDS,
    _grade_from_pct,
    _triage_entry,
    canonical_drift_fix_suggestions,
    generate_triage,
    portfolio_health_score,
    quick_fix_suggestion,
    sort_by_severity,
    triage_summary,
    write_triage_report,
)


def test_triage_entry_known_code():
    entry = _triage_entry("jwt-generator", 500)
    assert entry["slug"] == "jwt-generator"
    assert entry["http_code"] == 500
    assert entry["label"] == "server_error"
    assert entry["severity"] == "high"
    assert "logs" in entry["suggested_action"]


def test_triage_entry_geo_block_low_severity():
    entry = _triage_entry("timestamp-converter", 451)
    assert entry["label"] == "geo_block"
    assert entry["severity"] == "low"


def test_triage_entry_rate_limited():
    entry = _triage_entry("some-tool", 429)
    assert entry["label"] == "rate_limited"
    assert entry["http_code"] == 429
    assert entry["severity"] == "medium"
    assert "plan limits" in entry["suggested_action"]


def test_triage_entry_unknown_code():
    entry = _triage_entry("foo", 503)
    assert entry["label"] == "error_503"
    assert entry["http_code"] == 503
    assert entry["severity"] == "medium"


def test_sort_by_severity():
    entries = [
        _triage_entry("geo-product", 451),
        _triage_entry("server-product", 500),
        _triage_entry("notfound-product", 404),
        _triage_entry("auth-product", 401),
    ]
    sorted_entries = sort_by_severity(entries)
    assert sorted_entries[0]["slug"] in ("server-product", "auth-product")
    assert sorted_entries[-1]["slug"] == "geo-product"


def test_generate_triage_from_file(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "a", "code": 401},
                {"slug": "b", "code": 500},
            ]
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert len(entries) == 2
    assert entries[0]["slug"] == "a"
    assert entries[0]["label"] == "sso_protection"
    assert entries[1]["slug"] == "b"
    assert entries[1]["label"] == "server_error"


def test_generate_triage_empty(tmp_path):
    summary = {"gaps": {"unhealthy_live": []}}
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert entries == []


def test_generate_triage_canonical_drift_included(tmp_path):
    """Canonical-drift products should appear in triage entries."""
    summary = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "jwt-generator", "code": 500},
            ],
            "canonical_drift": [
                {
                    "slug": "pdf-forge",
                    "canonical_code": 500,
                    "canonical_status": "error_500",
                },
                {
                    "slug": "webhook-tester",
                    "canonical_code": 404,
                    "canonical_status": "not_found",
                },
            ],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert len(entries) == 3

    slugs = {e["slug"] for e in entries}
    assert slugs == {"jwt-generator", "pdf-forge", "webhook-tester"}

    # Canonical-drift entries should have prefixed label
    pf = next(e for e in entries if e["slug"] == "pdf-forge")
    assert pf["label"].startswith("canonical_drift/")
    assert pf["severity"] == "medium"
    assert "fallback alias" in pf["suggested_action"]


def test_generate_triage_no_duplicate_on_overlap(tmp_path):
    """If a slug appears in both unhealthy_live and canonical_drift, only one entry."""
    summary = {
        "gaps": {
            "unhealthy_live": [{"slug": "jwt-generator", "code": 500}],
            "canonical_drift": [{"slug": "jwt-generator", "canonical_code": 500}],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert len(entries) == 1
    assert entries[0]["slug"] == "jwt-generator"
    # Should keep the direct unhealthy entry, not the canonical-drift version
    assert not entries[0]["label"].startswith("canonical_drift/")


def test_generate_triage_canonical_drift_only(tmp_path):
    """Only canonical-drift, no unhealthy_live."""
    summary = {
        "gaps": {
            "unhealthy_live": [],
            "canonical_drift": [
                {"slug": "html-entity-encoder", "canonical_code": 402},
            ],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert len(entries) == 1
    assert entries[0]["slug"] == "html-entity-encoder"
    assert entries[0]["label"] == "canonical_drift/deployment_disabled"


def test_write_triage_report(tmp_path):
    entries = [
        _triage_entry("jwt-generator", 500),
        _triage_entry("diffmaster", 401),
        _triage_entry("timestamp-converter", 451),
    ]
    out = tmp_path / "triage.md"
    report = write_triage_report(entries, output_path=out)

    assert "jwt-generator" in report
    assert "server_error" in report
    assert "sso_protection" in report
    assert "geo_block" in report
    assert "high" in report
    assert "low" in report
    assert out.exists()
    content = out.read_text()
    assert "| diffmaster |" in content
    assert "Severity breakdown:" in content


def test_quick_fix_suggestion_500():
    entry = _triage_entry("jwt-generator", 500)
    fix = quick_fix_suggestion(entry)
    assert "jwt-generator" in fix
    assert "vercel logs" in fix


def test_quick_fix_suggestion_401():
    entry = _triage_entry("diffmaster", 401)
    fix = quick_fix_suggestion(entry)
    assert "diffmaster" in fix
    assert "Authentication" in fix or "vercel" in fix


def test_quick_fix_suggestion_404():
    entry = _triage_entry("missing-app", 404)
    fix = quick_fix_suggestion(entry)
    assert "missing-app" in fix
    assert "vercel --prod" in fix


def test_quick_fix_suggestion_451():
    entry = _triage_entry("geo-blocked", 451)
    fix = quick_fix_suggestion(entry)
    assert "Firewall" in fix or "Geo" in fix


def test_quick_fix_suggestion_unknown_code():
    entry = _triage_entry("weird-app", 999)
    fix = quick_fix_suggestion(entry)
    assert "Investigate" in fix


def test_write_triage_report_includes_quick_fix(tmp_path):
    entries = [
        _triage_entry("jwt-generator", 500),
        _triage_entry("diffmaster", 401),
    ]
    out = tmp_path / "triage.md"
    report = write_triage_report(entries, output_path=out)
    assert "Quick Fix" in report
    assert "vercel logs" in report


def test_triage_summary_empty(tmp_path):
    summary = {"gaps": {"unhealthy_live": [], "canonical_drift": []}}
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = triage_summary(summary_path=summary_file)
    assert result["total_unhealthy"] == 0
    assert result["high"] == 0
    assert result["medium"] == 0
    assert result["low"] == 0
    assert result["top_high_slugs"] == []
    assert result["codex_handoff_recommended"] is False
    assert result["triage_entries"] == []


def test_triage_summary_with_mixed_severity(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "jwt-generator", "code": 500},
                {"slug": "diffmaster", "code": 401},
                {"slug": "timestamp-converter", "code": 451},
            ],
            "canonical_drift": [
                {"slug": "pdf-forge", "canonical_code": 500},
            ],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = triage_summary(summary_path=summary_file)
    assert result["total_unhealthy"] == 4
    assert result["high"] == 2
    assert result["low"] == 1
    assert result["codex_handoff_recommended"] is True
    assert "jwt-generator" in result["top_high_slugs"]
    assert len(result["triage_entries"]) == 4


def test_triage_summary_no_high_means_no_handoff(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "timestamp-converter", "code": 451},
            ],
            "canonical_drift": [],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = triage_summary(summary_path=summary_file)
    assert result["high"] == 0
    assert result["codex_handoff_recommended"] is False


def test_canonical_drift_fix_suggestions_from_file(tmp_path):
    summary = {
        "gaps": {
            "canonical_url_drift": [
                {
                    "slug": "pdf-forge",
                    "url": "https://pdf-forge-five.vercel.app",
                    "ideal_url": "https://pdf-forge.vercel.app",
                    "canonical_code": 500,
                    "canonical_status": "error_500",
                },
                {
                    "slug": "webhook-tester",
                    "url": "https://webhook-tester-beryl.vercel.app",
                    "ideal_url": "https://webhook-tester.vercel.app",
                    "canonical_code": 404,
                    "canonical_status": "not_found",
                },
            ]
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = canonical_drift_fix_suggestions(summary_path=summary_file)
    assert len(result) == 2

    pdf = next(r for r in result if r["slug"] == "pdf-forge")
    assert pdf["fallback_url"] == "https://pdf-forge-five.vercel.app"
    assert pdf["ideal_url"] == "https://pdf-forge.vercel.app"
    assert pdf["canonical_status"] == "error_500"
    assert "vercel --prod" in pdf["fix_command"]
    assert "pdf-forge" in pdf["fix_command"]

    wh = next(r for r in result if r["slug"] == "webhook-tester")
    assert wh["canonical_status"] == "not_found"
    assert "vercel link" in wh["fix_command"]


def test_canonical_drift_fix_suggestions_empty(tmp_path):
    summary = {"gaps": {"canonical_url_drift": []}}
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = canonical_drift_fix_suggestions(summary_path=summary_file)
    assert result == []


def test_canonical_drift_fix_suggestions_missing_file(tmp_path):
    result = canonical_drift_fix_suggestions(
        summary_path=tmp_path / "nonexistent.json"
    )
    assert result == []


def test_canonical_drift_fix_suggestions_unknown_status(tmp_path):
    summary = {
        "gaps": {
            "canonical_url_drift": [
                {
                    "slug": "odd-product",
                    "url": "https://odd-product-alt.vercel.app",
                    "ideal_url": "https://odd-product.vercel.app",
                    "canonical_status": "some_weird_status",
                },
            ]
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = canonical_drift_fix_suggestions(summary_path=summary_file)
    assert len(result) == 1
    assert "Investigate" in result[0]["fix_command"]
    assert "odd-product" in result[0]["fix_command"]


def test_canonical_drift_fix_suggestions_deployment_disabled(tmp_path):
    summary = {
        "gaps": {
            "canonical_url_drift": [
                {
                    "slug": "html-entity-encoder",
                    "url": "https://html-entity-encoder-1p2e2xs77.vercel.app",
                    "ideal_url": "https://html-entity-encoder.vercel.app",
                    "canonical_status": "deployment_disabled",
                },
            ]
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = canonical_drift_fix_suggestions(summary_path=summary_file)
    assert len(result) == 1
    assert "Re-enable" in result[0]["fix_command"]
    assert "html-entity-encoder" in result[0]["fix_command"]


def test_canonical_drift_fixes_dict_has_expected_keys():
    assert "error_500" in CANONICAL_DRIFT_FIXES
    assert "not_found" in CANONICAL_DRIFT_FIXES
    assert "deployment_disabled" in CANONICAL_DRIFT_FIXES
    for key, template in CANONICAL_DRIFT_FIXES.items():
        formatted = template.format(slug="test-slug")
        assert "test-slug" in formatted


def test_grade_from_pct_a():
    assert _grade_from_pct(97.0) == "A"


def test_grade_from_pct_b():
    assert _grade_from_pct(90.0) == "B"


def test_grade_from_pct_c():
    assert _grade_from_pct(75.0) == "C"


def test_grade_from_pct_d():
    assert _grade_from_pct(60.0) == "D"


def test_grade_from_pct_f():
    assert _grade_from_pct(30.0) == "F"


def test_grade_from_pct_boundary():
    assert _grade_from_pct(94.9) == "B"
    assert _grade_from_pct(100.0) == "A"


def test_portfolio_health_score_full(tmp_path):
    summary = {
        "live_count": 90,
        "healthy_count": 87,
        "unhealthy_count": 3,
        "checkout_gap_count": 0,
        "deploy_missing_or_bad_url": 6,
        "gaps": {
            "canonical_url_drift": [
                {"slug": "pdf-forge"},
                {"slug": "webhook-tester"},
            ]
        },
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = portfolio_health_score(summary_path=summary_file)
    assert result["live_count"] == 90
    assert result["healthy_count"] == 87
    assert result["unhealthy_count"] == 3
    assert result["health_pct"] == 96.7
    assert result["grade"] == "A"
    assert result["checkout_covered"] is True
    assert result["deploy_gap"] == 6
    assert result["canonical_drift"] == 2


def test_portfolio_health_score_zero_live(tmp_path):
    summary = {"live_count": 0, "healthy_count": 0, "unhealthy_count": 0}
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = portfolio_health_score(summary_path=summary_file)
    assert result["health_pct"] == 0.0
    assert result["grade"] == "F"
    assert result["checkout_covered"] is True


def test_portfolio_health_score_missing_file(tmp_path):
    result = portfolio_health_score(
        summary_path=tmp_path / "nonexistent.json"
    )
    assert result["live_count"] == 0
    assert result["grade"] == "F"


def test_portfolio_health_score_checkout_uncovered(tmp_path):
    summary = {
        "live_count": 10,
        "healthy_count": 8,
        "unhealthy_count": 2,
        "checkout_gap_count": 3,
        "deploy_missing_or_bad_url": 0,
        "gaps": {},
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = portfolio_health_score(summary_path=summary_file)
    assert result["checkout_covered"] is False
    assert result["health_pct"] == 80.0
    assert result["grade"] == "C"


def test_health_grade_thresholds_complete():
    grades = set()
    for (lo, hi), grade in HEALTH_GRADE_THRESHOLDS.items():
        grades.add(grade)
    assert grades == {"A", "B", "C", "D", "F"}
