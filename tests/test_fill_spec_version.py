import json
from pathlib import Path

from scripts.fill_spec_version import fill_missing_spec_versions


def test_fill_spec_version(tmp_path):
    (tmp_path / "has_sv").mkdir()
    (tmp_path / "has_sv" / "product.json").write_text(
        json.dumps({"name": "A", "spec_version": "2.0"})
    )

    (tmp_path / "no_sv").mkdir()
    (tmp_path / "no_sv" / "product.json").write_text(json.dumps({"name": "B"}))

    (tmp_path / "empty_dir").mkdir()

    result = fill_missing_spec_versions(tmp_path, dry_run=True)
    assert result["fixed"] == 1
    assert result["skipped"] == 1
    assert "no_sv" in result["fixed_slugs"]

    data = json.loads((tmp_path / "no_sv" / "product.json").read_text())
    assert "spec_version" not in data

    result = fill_missing_spec_versions(tmp_path, dry_run=False)
    assert result["fixed"] == 1

    data = json.loads((tmp_path / "no_sv" / "product.json").read_text())
    assert data["spec_version"] == "1.0"

    data = json.loads((tmp_path / "has_sv" / "product.json").read_text())
    assert data["spec_version"] == "2.0"


def test_fill_spec_version_invalid_json(tmp_path):
    (tmp_path / "bad").mkdir()
    (tmp_path / "bad" / "product.json").write_text("NOT JSON")

    result = fill_missing_spec_versions(tmp_path)
    assert result["errors"] == 1
    assert result["fixed"] == 0
