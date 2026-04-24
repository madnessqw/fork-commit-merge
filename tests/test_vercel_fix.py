"""Tests for scripts.vercel_fix"""

import json
import re
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.vercel_fix import HASH_PAT, fix_hash_urls


def test_hash_pat_matches_madnessqws_projects():
    url = "https://chmod-calculator-5atogp6t7-madnessqws-projects.vercel.app"
    assert HASH_PAT.search(url) is not None


def test_hash_pat_matches_html_entity_encoder():
    url = "https://html-entity-encoder-1p2e2xs77-madnessqws-projects.vercel.app"
    assert HASH_PAT.search(url) is not None


def test_hash_pat_no_match_canonical():
    url = "https://chmod-calculator.vercel.app"
    assert HASH_PAT.search(url) is None


def test_hash_pat_no_match_bare_domain():
    url = "https://example.com"
    assert HASH_PAT.search(url) is None


def test_hash_pat_no_match_empty():
    assert HASH_PAT.search("") is None


def test_fix_hash_urls_no_hash_urls(tmp_path, capsys):
    state = {
        "products": {
            "active": [
                {"slug": "clean-app", "vercel_url": "https://clean-app.vercel.app"},
                {"slug": "another-app", "vercel_url": "https://another-app.vercel.app"},
            ]
        }
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))

    with patch("scripts.vercel_fix.os.environ", {}):
        with patch("scripts.vercel_fix.subprocess.run"):
            monkeypatch_chdir = patch("builtins.open", lambda f, *a, **kw: open(f, *a, **kw) if str(f) != "STATE.json" else open(state_file, *a, **kw))
            original_open = open

            calls = []
            def fake_open(path, *args, **kwargs):
                if str(path) == "STATE.json":
                    return original_open(state_file, *args, **kwargs)
                return original_open(path, *args, **kwargs)

            with patch("builtins.open", fake_open):
                fix_hash_urls()

    captured = capsys.readouterr()
    assert "No hash URLs to fix" in captured.out


def test_fix_hash_urls_with_hash_url(tmp_path, capsys):
    state = {
        "products": {
            "active": [
                {
                    "slug": "chmod-calculator",
                    "vercel_url": "https://chmod-calculator-5atogp6t7-madnessqws-projects.vercel.app",
                },
                {
                    "slug": "good-app",
                    "vercel_url": "https://good-app.vercel.app",
                },
            ]
        }
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stderr = ""

    original_open = open

    def fake_open(path, *args, **kwargs):
        if str(path) == "STATE.json":
            return original_open(state_file, *args, **kwargs)
        return original_open(path, *args, **kwargs)

    with patch("builtins.open", fake_open):
        with patch("scripts.vercel_fix.subprocess.run", return_value=mock_result) as mock_run:
            with patch("scripts.vercel_fix.os.environ", {"VERCEL_TOKEN": "test-token"}):
                fix_hash_urls()

    captured = capsys.readouterr()
    assert "Hash URL found: chmod-calculator" in captured.out
    assert "Alias set: chmod-calculator.vercel.app" in captured.out
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert any("chmod-calculator-5atogp6t7-madnessqws-projects.vercel.app" in arg for arg in cmd)
    assert any("chmod-calculator.vercel.app" in arg for arg in cmd)
    assert "--token" in cmd
    assert "test-token" in cmd

    updated = json.loads(state_file.read_text())
    chmod_prod = next(p for p in updated["products"]["active"] if p["slug"] == "chmod-calculator")
    assert chmod_prod["vercel_url"] == "https://chmod-calculator.vercel.app"
    assert chmod_prod.get("note") == "Alias fixed"


def test_fix_hash_urls_alias_failure(tmp_path, capsys):
    state = {
        "products": {
            "active": [
                {
                    "slug": "broken-app",
                    "vercel_url": "https://broken-app-abc123-madnessqws-projects.vercel.app",
                },
            ]
        }
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))

    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Alias failed: not found"

    original_open = open

    def fake_open(path, *args, **kwargs):
        if str(path) == "STATE.json":
            return original_open(state_file, *args, **kwargs)
        return original_open(path, *args, **kwargs)

    with patch("builtins.open", fake_open):
        with patch("scripts.vercel_fix.subprocess.run", return_value=mock_result):
            with patch("scripts.vercel_fix.os.environ", {}):
                fix_hash_urls()

    captured = capsys.readouterr()
    assert "Hash URL found: broken-app" in captured.out
    assert "Alias failed" in captured.out

    updated = json.loads(state_file.read_text())
    broken_prod = next(p for p in updated["products"]["active"] if p["slug"] == "broken-app")
    assert broken_prod["vercel_url"] == "https://broken-app-abc123-madnessqws-projects.vercel.app"


def test_fix_hash_urls_subprocess_exception(tmp_path, capsys):
    state = {
        "products": {
            "active": [
                {
                    "slug": "error-app",
                    "vercel_url": "https://error-app-xyz789-madnessqws-projects.vercel.app",
                },
            ]
        }
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))

    original_open = open

    def fake_open(path, *args, **kwargs):
        if str(path) == "STATE.json":
            return original_open(state_file, *args, **kwargs)
        return original_open(path, *args, **kwargs)

    with patch("builtins.open", fake_open):
        with patch("scripts.vercel_fix.subprocess.run", side_effect=Exception("vercel not found")):
            with patch("scripts.vercel_fix.os.environ", {}):
                fix_hash_urls()

    captured = capsys.readouterr()
    assert "Error: vercel not found" in captured.out


def test_fix_hash_urls_no_token(tmp_path, capsys):
    state = {
        "products": {
            "active": [
                {
                    "slug": "test-app",
                    "vercel_url": "https://test-app-abc-madnessqws-projects.vercel.app",
                },
            ]
        }
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stderr = ""

    original_open = open

    def fake_open(path, *args, **kwargs):
        if str(path) == "STATE.json":
            return original_open(state_file, *args, **kwargs)
        return original_open(path, *args, **kwargs)

    with patch("builtins.open", fake_open):
        with patch("scripts.vercel_fix.subprocess.run", return_value=mock_result) as mock_run:
            with patch("scripts.vercel_fix.os.environ", {"VERCEL_TOKEN": ""}):
                fix_hash_urls()

    cmd = mock_run.call_args[0][0]
    assert "--token" not in cmd


def test_fix_hash_urls_non_dict_product(tmp_path, capsys):
    state = {
        "products": {
            "active": [
                "not-a-dict",
                42,
                None,
                {"slug": "good", "vercel_url": "https://good.vercel.app"},
            ]
        }
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))

    original_open = open

    def fake_open(path, *args, **kwargs):
        if str(path) == "STATE.json":
            return original_open(state_file, *args, **kwargs)
        return original_open(path, *args, **kwargs)

    with patch("builtins.open", fake_open):
        with patch("scripts.vercel_fix.subprocess.run"):
            with patch("scripts.vercel_fix.os.environ", {}):
                fix_hash_urls()

    captured = capsys.readouterr()
    assert "No hash URLs to fix" in captured.out


def test_fix_hash_urls_empty_vercel_url(tmp_path, capsys):
    state = {
        "products": {
            "active": [
                {"slug": "no-url-app", "vercel_url": ""},
                {"slug": "null-url-app", "vercel_url": None},
                {"slug": "missing-url-app"},
            ]
        }
    }
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps(state))

    original_open = open

    def fake_open(path, *args, **kwargs):
        if str(path) == "STATE.json":
            return original_open(state_file, *args, **kwargs)
        return original_open(path, *args, **kwargs)

    with patch("builtins.open", fake_open):
        with patch("scripts.vercel_fix.subprocess.run"):
            with patch("scripts.vercel_fix.os.environ", {}):
                fix_hash_urls()

    captured = capsys.readouterr()
    assert "No hash URLs to fix" in captured.out
