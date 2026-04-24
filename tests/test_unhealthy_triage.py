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
    CODEX_ONLY_CODES,
    GLM_BRIEF_TEMPLATES,
    HEALTH_GRADE_THRESHOLDS,
    _grade_from_pct,
    _triage_entry,
    canonical_drift_fix_suggestions,
    generate_glm_brief,
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


def test_generate_triage_canonical_url_drift_included(tmp_path):
    """Current canonical_url_drift summaries should also be triaged."""
    summary = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "jwt-generator", "code": 500},
            ],
            "canonical_url_drift": [
                {
                    "slug": "pdf-forge",
                    "canonical_code": 500,
                    "canonical_status": "error_500",
                },
            ],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert len(entries) == 2
    slugs = {e["slug"] for e in entries}
    assert slugs == {"jwt-generator", "pdf-forge"}
    pdf = next(e for e in entries if e["slug"] == "pdf-forge")
    assert pdf["label"].startswith("canonical_drift/")
    assert pdf["severity"] == "medium"


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


def test_portfolio_health_score_uses_top_level_canonical_drift_when_gap_detail_missing(tmp_path):
    summary = {
        "live_count": 10,
        "healthy_count": 9,
        "unhealthy_count": 1,
        "checkout_gap_count": 0,
        "deploy_missing_or_bad_url": 1,
        "canonical_url_drift": 4,
        "gaps": {
            "unhealthy_live": [{"slug": "jwt-generator", "code": 500}],
            "canonical_drift": [],
        },
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary), encoding="utf-8")

    result = portfolio_health_score(summary_path=summary_file)
    assert result["canonical_drift"] == 4


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


def test_generate_glm_brief_empty(tmp_path):
    summary = {"gaps": {"unhealthy_live": [], "canonical_drift": []}}
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = generate_glm_brief(summary_path=summary_file)
    assert result["glm_scope"] == []
    assert result["codex_scope"] == []
    assert "sağlıklı" in result["markdown"]


def test_generate_glm_brief_mixed_severity(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "jwt-generator", "code": 500},
                {"slug": "diffmaster", "code": 401},
                {"slug": "timestamp-converter", "code": 451},
            ],
            "canonical_drift": [
                {"slug": "pdf-forge", "canonical_code": 500, "canonical_status": "error_500"},
            ],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = generate_glm_brief(summary_path=summary_file)
    assert len(result["glm_scope"]) == 2  # jwt-generator + pdf-forge
    assert set(result["codex_scope"]) == {"diffmaster", "timestamp-converter"}
    assert "jwt-generator" in result["markdown"]
    assert "pdf-forge" in result["markdown"]
    assert "Codex Scope" in result["markdown"]
    assert "diffmaster" in result["markdown"]


def test_generate_glm_brief_all_codex_scope(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "diffmaster", "code": 401},
                {"slug": "geo-tool", "code": 451},
            ],
            "canonical_drift": [],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = generate_glm_brief(summary_path=summary_file)
    assert result["glm_scope"] == []
    assert set(result["codex_scope"]) == {"diffmaster", "geo-tool"}


def test_generate_glm_brief_canonical_drift_entry(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [],
            "canonical_drift": [
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

    result = generate_glm_brief(summary_path=summary_file)
    assert len(result["glm_scope"]) == 1
    assert "canonical_drift" in result["glm_scope"][0]
    assert "webhook-tester" in result["markdown"]


def test_generate_glm_brief_unknown_code_fallback(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [{"slug": "weird-app", "code": 503}],
            "canonical_drift": [],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = generate_glm_brief(summary_path=summary_file)
    assert len(result["glm_scope"]) == 1
    assert "weird-app" in result["markdown"]


def test_codex_only_codes():
    assert 401 in CODEX_ONLY_CODES
    assert 451 in CODEX_ONLY_CODES
    assert 500 not in CODEX_ONLY_CODES
    assert 404 not in CODEX_ONLY_CODES


def test_glm_brief_templates_have_placeholders():
    for key, template in GLM_BRIEF_TEMPLATES.items():
        assert "{slug}" in template or "slug" in template


def test_main_json_output_no_unhealthy(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        "scripts.unhealthy_triage.generate_triage",
        lambda **kw: [],
    )
    from scripts.unhealthy_triage import main

    result = main(["--json"])
    assert result["unhealthy"] == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["unhealthy"] == 0
    assert data["entries"] == []


def test_main_json_output_with_entries(tmp_path, monkeypatch, capsys):
    fake_entries = [
        _triage_entry("jwt-generator", 500),
        _triage_entry("diffmaster", 401),
    ]
    monkeypatch.setattr(
        "scripts.unhealthy_triage.generate_triage",
        lambda **kw: fake_entries,
    )
    from scripts.unhealthy_triage import main

    result = main(["--json"])
    assert result["unhealthy"] == 2
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["unhealthy"] == 2
    assert len(data["entries"]) == 2
    slugs = {e["slug"] for e in data["entries"]}
    assert slugs == {"jwt-generator", "diffmaster"}


def test_main_json_output_with_summary(tmp_path, monkeypatch, capsys):
    summary = {
        "gaps": {
            "unhealthy_live": [{"slug": "jwt-generator", "code": 500}],
            "canonical_drift": [],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))
    monkeypatch.setattr(
        "scripts.unhealthy_triage.ROOT", tmp_path
    )
    from scripts.unhealthy_triage import main

    result = main(["--json", "--summary"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "summary" in data
    assert data["summary"]["total_unhealthy"] == 1
    assert data["summary"]["high"] == 1


def test_main_default_output(tmp_path, monkeypatch, capsys):
    fake_entries = [_triage_entry("jwt-generator", 500)]
    monkeypatch.setattr(
        "scripts.unhealthy_triage.generate_triage",
        lambda **kw: fake_entries,
    )
    monkeypatch.setattr(
        "scripts.unhealthy_triage.write_triage_report",
        lambda *a, **kw: "# mock report",
    )
    from scripts.unhealthy_triage import main

    result = main([])
    assert result["unhealthy"] == 1
    captured = capsys.readouterr()
    assert "mock report" in captured.out


def test_main_health_score_flag(tmp_path, monkeypatch, capsys):
    fake_score = {
        "live_count": 91,
        "healthy_count": 88,
        "unhealthy_count": 3,
        "health_pct": 96.7,
        "grade": "A",
        "checkout_covered": True,
        "deploy_gap": 5,
        "canonical_drift": 4,
    }
    monkeypatch.setattr(
        "scripts.unhealthy_triage.portfolio_health_score",
        lambda **kw: fake_score,
    )
    from scripts.unhealthy_triage import main

    result = main(["--health-score"])
    assert "health_score" in result
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["grade"] == "A"
    assert data["live_count"] == 91
    assert data["health_pct"] == 96.7


def test_main_health_score_json_output(tmp_path, monkeypatch, capsys):
    fake_score = {
        "live_count": 10,
        "healthy_count": 7,
        "unhealthy_count": 3,
        "health_pct": 70.0,
        "grade": "C",
        "checkout_covered": False,
        "deploy_gap": 2,
        "canonical_drift": 1,
    }
    monkeypatch.setattr(
        "scripts.unhealthy_triage.portfolio_health_score",
        lambda **kw: fake_score,
    )
    from scripts.unhealthy_triage import main

    result = main(["--health-score"])
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["grade"] == "C"
    assert data["checkout_covered"] is False


def test_generate_glm_brief_sorted_by_severity(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [
                {"slug": "low-tool", "code": 0},
                {"slug": "high-tool", "code": 500},
            ],
            "canonical_drift": [],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = generate_glm_brief(summary_path=summary_file)
    md = result["markdown"]
    high_pos = md.find("high-tool")
    low_pos = md.find("low-tool")
    assert high_pos < low_pos


def test_main_drift_fix_flag(tmp_path, monkeypatch, capsys):
    fake_suggestions = [
        {
            "slug": "pdf-forge",
            "fallback_url": "https://pdf-forge-five.vercel.app",
            "ideal_url": "https://pdf-forge.vercel.app",
            "canonical_status": "error_500",
            "fix_command": "Redeploy via: cd products/pdf-forge && vercel --prod --yes",
        },
        {
            "slug": "webhook-tester",
            "fallback_url": "https://webhook-tester-alt.vercel.app",
            "ideal_url": "https://webhook-tester.vercel.app",
            "canonical_status": "not_found",
            "fix_command": "Link project: cd products/webhook-tester && vercel link --yes && vercel --prod --yes",
        },
    ]
    monkeypatch.setattr(
        "scripts.unhealthy_triage.canonical_drift_fix_suggestions",
        lambda **kw: fake_suggestions,
    )
    from scripts.unhealthy_triage import main

    result = main(["--drift-fix"])
    assert "drift_fix" in result
    assert result["drift_fix"] == 2
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert len(data) == 2
    assert data[0]["slug"] == "pdf-forge"
    assert data[1]["slug"] == "webhook-tester"
    assert "vercel --prod" in data[0]["fix_command"]


def test_main_drift_fix_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        "scripts.unhealthy_triage.canonical_drift_fix_suggestions",
        lambda **kw: [],
    )
    from scripts.unhealthy_triage import main

    result = main(["--drift-fix"])
    assert result["drift_fix"] == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data == []


def test_main_drift_fix_does_not_call_generate_triage(tmp_path, monkeypatch, capsys):
    call_count = {"n": 0}

    def fake_generate_triage(**kw):
        call_count["n"] += 1
        return []

    def fake_drift_fix(**kw):
        return [{"slug": "test", "fallback_url": "", "ideal_url": "", "canonical_status": "x", "fix_command": "x"}]

    monkeypatch.setattr(
        "scripts.unhealthy_triage.generate_triage",
        fake_generate_triage,
    )
    monkeypatch.setattr(
        "scripts.unhealthy_triage.canonical_drift_fix_suggestions",
        fake_drift_fix,
    )
    from scripts.unhealthy_triage import main

    main(["--drift-fix"])
    assert call_count["n"] == 0


def test_generate_triage_rfp_unhealthy_included(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [],
            "canonical_drift": [],
            "ready_for_payment_health": [
                {
                    "slug": "code-formatter-universal",
                    "code": 404,
                    "health_status": "not_found",
                    "url": "https://code-formatter-universal.vercel.app",
                },
            ],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert len(entries) == 1
    assert entries[0]["slug"] == "code-formatter-universal"
    assert entries[0]["label"].startswith("rfp_unhealthy/")
    assert entries[0]["severity"] == "high"
    assert "ready_for_payment" in entries[0]["suggested_action"]


def test_generate_triage_rfp_unhealthy_no_duplicate(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [{"slug": "code-formatter-universal", "code": 404}],
            "canonical_drift": [],
            "ready_for_payment_health": [
                {"slug": "code-formatter-universal", "code": 404},
            ],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert len(entries) == 1
    assert not entries[0]["label"].startswith("rfp_unhealthy/")


def test_generate_triage_rfp_unhealthy_with_canonical_drift(tmp_path):
    summary = {
        "gaps": {
            "unhealthy_live": [],
            "canonical_drift": [
                {"slug": "pdf-forge", "canonical_code": 500},
            ],
            "ready_for_payment_health": [
                {"slug": "code-formatter-universal", "code": 404},
            ],
        }
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    entries = generate_triage(summary_path=summary_file)
    assert len(entries) == 2
    slugs = {e["slug"] for e in entries}
    assert slugs == {"pdf-forge", "code-formatter-universal"}


def test_portfolio_health_score_includes_rfp_unhealthy(tmp_path):
    summary = {
        "live_count": 91,
        "healthy_count": 91,
        "unhealthy_count": 0,
        "checkout_gap_count": 0,
        "deploy_missing_or_bad_url": 2,
        "ready_for_payment_unhealthy_count": 1,
        "gaps": {},
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = portfolio_health_score(summary_path=summary_file)
    assert result["rfp_unhealthy"] == 1
    assert result["grade"] == "A"


def test_portfolio_health_score_rfp_unhealthy_missing_key(tmp_path):
    summary = {
        "live_count": 10,
        "healthy_count": 10,
        "unhealthy_count": 0,
        "checkout_gap_count": 0,
        "deploy_missing_or_bad_url": 0,
        "gaps": {},
    }
    summary_file = tmp_path / "STATE_SUMMARY.json"
    summary_file.write_text(json.dumps(summary))

    result = portfolio_health_score(summary_path=summary_file)
    assert result["rfp_unhealthy"] == 0
