import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.sync_from_vercel import sync_html_files


def _make_state(products, tmp_path):
    state_file = tmp_path / "STATE.json"
    state_file.write_text(json.dumps({"products": {"active": products}}))
    return state_file


def test_no_missing_html(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    slug = "existing-prod"
    prod_dir = tmp_path / "products" / slug
    prod_dir.mkdir(parents=True)
    (prod_dir / "index.html").write_text("<html>ok</html>" * 100)

    _make_state([{"slug": slug, "vercel_url": f"https://{slug}.vercel.app"}], tmp_path)

    synced, failed = sync_html_files()
    assert synced == 0
    assert failed == []


def test_missing_html_sync_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    slug = "missing-prod"
    _make_state([{"slug": slug, "vercel_url": f"https://{slug}.vercel.app"}], tmp_path)

    mock_result = MagicMock()
    mock_result.returncode = 0

    html_content = b"<html><body>" + b"x" * 2000 + b"</body></html>"
    written_files = {}

    def fake_run(cmd, **kwargs):
        outfile = None
        for i, arg in enumerate(cmd):
            if arg == "-o" and i + 1 < len(cmd):
                outfile = cmd[i + 1]
        if outfile:
            Path(outfile).write_bytes(html_content)
            written_files["path"] = outfile
        return mock_result

    with patch("scripts.sync_from_vercel.subprocess.run", side_effect=fake_run):
        synced, failed = sync_html_files(batch_size=5)

    assert synced == 1
    assert failed == []
    assert "written_files" in dir() or synced > 0


def test_missing_html_sync_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    slug = "fail-prod"
    _make_state([{"slug": slug, "vercel_url": f"https://{slug}.vercel.app"}], tmp_path)

    mock_result = MagicMock()
    mock_result.returncode = 1

    with patch("scripts.sync_from_vercel.subprocess.run", return_value=mock_result):
        synced, failed = sync_html_files(batch_size=5)

    assert synced == 0
    assert slug in failed


def test_empty_products(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _make_state([], tmp_path)

    synced, failed = sync_html_files()
    assert synced == 0
    assert failed == []


def test_batch_size_limit(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    products = [{"slug": f"prod-{i}", "vercel_url": f"https://prod-{i}.vercel.app"} for i in range(20)]
    _make_state(products, tmp_path)

    mock_result = MagicMock()
    mock_result.returncode = 0

    html_content = b"<html><body>" + b"y" * 2000 + b"</body></html>"

    def fake_run(cmd, **kwargs):
        outfile = None
        for i, arg in enumerate(cmd):
            if arg == "-o" and i + 1 < len(cmd):
                outfile = cmd[i + 1]
        if outfile:
            Path(outfile).write_bytes(html_content)
        return mock_result

    with patch("scripts.sync_from_vercel.subprocess.run", side_effect=fake_run):
        synced, failed = sync_html_files(batch_size=3)

    assert synced == 3


def test_non_dict_products_skipped(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _make_state(["not-a-dict", None, 42], tmp_path)

    synced, failed = sync_html_files()
    assert synced == 0
    assert failed == []


def test_small_file_treated_as_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    slug = "tiny-prod"
    _make_state([{"slug": slug, "vercel_url": f"https://{slug}.vercel.app"}], tmp_path)

    mock_result = MagicMock()
    mock_result.returncode = 0

    tiny_html = b"<html>tiny</html>"

    def fake_run(cmd, **kwargs):
        outfile = None
        for i, arg in enumerate(cmd):
            if arg == "-o" and i + 1 < len(cmd):
                outfile = cmd[i + 1]
        if outfile:
            Path(outfile).write_bytes(tiny_html)
        return mock_result

    with patch("scripts.sync_from_vercel.subprocess.run", side_effect=fake_run):
        synced, failed = sync_html_files(batch_size=5)

    assert synced == 0
    assert slug in failed
