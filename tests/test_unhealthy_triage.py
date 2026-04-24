"""Tests for scripts.unhealthy_triage"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.unhealthy_triage import (
    _triage_entry,
    generate_triage,
    sort_by_severity,
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
