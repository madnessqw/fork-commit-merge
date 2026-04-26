import json
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.product_meta_seo_auditor import (
    MetaExtractor,
    audit_all,
    audit_product,
    cmd_audit,
    cmd_fix_dry_run,
    cmd_report,
    extract_meta,
    score_meta,
)


@pytest.fixture
def tmp_product(tmp_path):
    def _make(slug="test-product", html=None, product_json=None):
        pdir = tmp_path / slug
        pdir.mkdir(parents=True, exist_ok=True)
        if html is None:
            html = textwrap.dedent("""\
            <!DOCTYPE html><html><head>
            <title>Test Product</title>
            <meta name="description" content="A great test product for developers and power users with amazing features.">
            <meta property="og:title" content="Test Product">
            <meta property="og:description" content="A great test product">
            <meta name="keywords" content="test, product, developer, tool">
            <meta name="canonical" content="https://test-product.vercel.app">
            <meta name="robots" content="index, follow">
            <meta property="og:image" content="https://example.com/og.png">
            </head><body></body></html>
            """)
        (pdir / "index.html").write_text(html)
        if product_json is None:
            product_json = {"name": "Test Product", "slug": slug, "category": "developer-tools"}
        (pdir / "product.json").write_text(json.dumps(product_json))
        return pdir
    return _make


class TestMetaExtractor:
    def test_extracts_title(self):
        p = MetaExtractor()
        p.feed("<html><head><title>Hello World</title></head></html>")
        assert p.title_text == "Hello World"

    def test_extracts_meta_name(self):
        p = MetaExtractor()
        p.feed('<meta name="description" content="test desc">')
        assert p.metas["description"] == "test desc"

    def test_extracts_meta_property(self):
        p = MetaExtractor()
        p.feed('<meta property="og:title" content="OG Title">')
        assert p.metas["og:title"] == "OG Title"

    def test_empty_html(self):
        p = MetaExtractor()
        p.feed("")
        assert p.title_text == ""
        assert p.metas == {}

    def test_malformed_html_no_crash(self):
        p = MetaExtractor()
        p.feed("<html><head><meta><meta name='desc' content='x'")
        assert True


class TestExtractMeta:
    def test_reads_file(self, tmp_path):
        f = tmp_path / "test.html"
        f.write_text("<html><head><title>T</title></head></html>")
        result = extract_meta(f)
        assert result["title"] == "T"

    def test_missing_file(self, tmp_path):
        result = extract_meta(tmp_path / "nonexistent.html")
        assert result == {}


class TestScoreMeta:
    def test_perfect_meta(self):
        meta = {
            "title": "Test Product Pro Tool for Developers Everywhere",
            "description": "A great test product for developers and power users with amazing features and capabilities built for modern development workflows and team productivity.",
            "og:title": "Test Product",
            "og:description": "A great test product for developers everywhere",
            "keywords": "test, product, developer, tool, utility, online",
            "canonical": "https://example.com",
            "robots": "index, follow",
            "og:image": "https://example.com/img.png",
        }
        result = score_meta(meta)
        assert result["score"] == result["max_score"]
        assert result["issues"] == []

    def test_empty_meta(self):
        result = score_meta({})
        assert result["score"] == 0
        assert len(result["issues"]) > 5

    def test_typo_detection(self):
        meta = {
            "title": "X",
            "description": "Agentmpt engineer tool by Universe7Creator",
            "og:title": "X",
            "og:description": "X",
            "keywords": "a",
            "canonical": "https://x.com",
            "robots": "index",
            "og:image": "https://x.com/img.png",
        }
        result = score_meta(meta)
        assert "typo_agentmpt" in result["issues"]
        assert "typo_universe7creator" in result["issues"]

    def test_short_title(self):
        meta = {"title": "X", "description": "D" * 130, "og:title": "X", "og:description": "D", "keywords": "a", "canonical": "u", "robots": "i", "og:image": "i"}
        result = score_meta(meta)
        assert any(i.startswith("title_short") for i in result["issues"])

    def test_short_description(self):
        meta = {"title": "T" * 35, "description": "Short", "og:title": "T", "og:description": "D", "keywords": "a", "canonical": "u", "robots": "i", "og:image": "i"}
        result = score_meta(meta)
        assert any(i.startswith("desc_short") for i in result["issues"])

    def test_noindex_flagged(self):
        meta = {"title": "T" * 35, "description": "D" * 140, "robots": "noindex, nofollow"}
        result = score_meta(meta)
        assert "noindex_set" in result["issues"]

    def test_excessive_keywords(self):
        kws = ", ".join(f"kw{i}" for i in range(15))
        meta = {"title": "T" * 35, "description": "D" * 140, "keywords": kws, "og:title": "T", "og:description": "D", "canonical": "u", "robots": "i", "og:image": "i"}
        result = score_meta(meta)
        assert any(i.startswith("keywords_excessive") for i in result["issues"])


class TestAuditProduct:
    def test_full_product(self, tmp_product):
        pdir = tmp_product("full-prod")
        result = audit_product(pdir)
        assert result["slug"] == "full-prod"
        assert result["score"] > 0
        assert result["product_name"] == "Test Product"

    def test_no_html(self, tmp_path):
        pdir = tmp_path / "empty-prod"
        pdir.mkdir()
        (pdir / "product.json").write_text('{"name":"E","slug":"empty-prod"}')
        result = audit_product(pdir)
        assert result["score"] == 0

    def test_minimal_html(self, tmp_product):
        html = "<html><head><title>Min</title></head><body></body></html>"
        pdir = tmp_product("min-prod", html=html)
        result = audit_product(pdir)
        assert result["meta"]["title"] == "Min"
        assert result["score"] > 0


class TestAuditAll:
    def test_with_products(self, tmp_product, monkeypatch):
        import scripts.product_meta_seo_auditor as mod
        monkeypatch.setattr(mod, "PRODUCTS_DIR", tmp_product.__self__ if hasattr(tmp_product, '__self__') else tmp_product)
        p1 = tmp_product("prod-a")
        p2 = tmp_product("prod-b")
        monkeypatch.setattr(mod, "PRODUCTS_DIR", p1.parent)
        results = audit_all()
        assert len(results) == 2

    def test_empty_dir(self, tmp_path, monkeypatch):
        import scripts.product_meta_seo_auditor as mod
        monkeypatch.setattr(mod, "PRODUCTS_DIR", tmp_path)
        results = audit_all()
        assert results == []


class TestCmdAudit:
    def test_output(self, capsys, tmp_product, monkeypatch):
        import scripts.product_meta_seo_auditor as mod
        p = tmp_product("audit-prod")
        monkeypatch.setattr(mod, "PRODUCTS_DIR", p.parent)
        cmd_audit([])
        out = capsys.readouterr().out
        assert "SEO Meta Audit" in out

    def test_json_output(self, capsys, tmp_product, monkeypatch):
        import scripts.product_meta_seo_auditor as mod
        p = tmp_product("json-prod")
        monkeypatch.setattr(mod, "PRODUCTS_DIR", p.parent)
        cmd_audit(["--json"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert isinstance(data, list)


class TestCmdFixDryRun:
    def test_no_typos(self, capsys, tmp_product, monkeypatch):
        import scripts.product_meta_seo_auditor as mod
        p = tmp_product("clean-prod")
        monkeypatch.setattr(mod, "PRODUCTS_DIR", p.parent)
        cmd_fix_dry_run([])
        out = capsys.readouterr().out
        assert "No typo issues" in out

    def test_with_typos(self, capsys, tmp_product, monkeypatch):
        import scripts.product_meta_seo_auditor as mod
        html = '<html><head><title>T</title><meta name="description" content="Agentmpt tool"></head></html>'
        p = tmp_product("typo-prod", html=html)
        monkeypatch.setattr(mod, "PRODUCTS_DIR", p.parent)
        cmd_fix_dry_run([])
        out = capsys.readouterr().out
        assert "typo" in out.lower()


class TestCmdReport:
    def test_report_output(self, capsys, tmp_product, monkeypatch):
        import scripts.product_meta_seo_auditor as mod
        p = tmp_product("report-prod")
        monkeypatch.setattr(mod, "PRODUCTS_DIR", p.parent)
        cmd_report([])
        out = capsys.readouterr().out
        assert "SEO Meta Audit Report" in out
        assert "Average" in out
        assert "Distribution" in out
