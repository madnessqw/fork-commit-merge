"""Tests for scripts.unhealthy_triage"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.unhealthy_triage import _triage_entry, generate_triage, write_triage_report


def test_triage_entry_known_code():
    entry = _triage_entry("jwt-generator", 500)
    assert entry["slug"] == "jwt-generator"
    assert entry["http_code"] == 500
    assert entry["label"] == "server_error"
    assert "logs" in entry["suggested_action"]


def test_triage_entry_unknown_code():
    entry = _triage_entry("foo", 503)
    assert entry["label"] == "error_503"
    assert entry["http_code"] == 503


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
    assert out.exists()
    content = out.read_text()
    assert "| diffmaster |" in content
