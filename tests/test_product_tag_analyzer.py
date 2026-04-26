import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.product_tag_analyzer import (
    CATEGORY_PRIORITY,
    CATEGORY_RULES,
    TAG_RULES,
    _has_keyword,
    _slug_text,
    audit,
    classify_category,
    generate_report,
    get_products,
    suggest_tags,
)


class TestSlugText:
    def test_basic(self):
        result = _slug_text("json-formatter", "JSON Formatter")
        assert "json" in result
        assert "formatter" in result

    def test_underscore(self):
        result = _slug_text("my_tool", "My Tool")
        assert "my" in result
        assert "tool" in result

    def test_camelcase_name(self):
        result = _slug_text("webterminal-pro", "WebTerminal Pro")
        assert "pro" in result

    def test_padded(self):
        result = _slug_text("abc", "ABC")
        assert result.startswith(" ")
        assert result.endswith(" ")


class TestHasKeyword:
    def test_exact_word(self):
        assert _has_keyword(" json ", "json") is True

    def test_substring_no_match(self):
        assert _has_keyword(" jsonl ", "json") is False

    def test_start_of_string(self):
        text = " json formatter "
        assert _has_keyword(text, "json") is True

    def test_end_of_string(self):
        text = " format json "
        assert _has_keyword(text, "json") is True


class TestClassifyCategory:
    def test_json_formatter(self):
        assert classify_category("json-formatter", "JSON Formatter") == "developer-tools"

    def test_password_checker(self):
        assert classify_category("password-strength-checker", "Password Strength Checker") == "security"

    def test_cron_builder(self):
        assert classify_category("cron-expression-builder", "Cron Expression Builder") == "devops"

    def test_color_picker(self):
        result = classify_category("color-picker", "Color Picker")
        assert result in ("design-tools", "utilities", "developer-tools")

    def test_api_generator(self):
        assert classify_category("api-doc-generator", "API Doc Generator") == "developer-tools"

    def test_uuid_generator(self):
        assert classify_category("uuid-generator-pro", "UUID Generator Pro") == "developer-tools"

    def test_sql_formatter(self):
        assert classify_category("sql-query-formatter", "SQL Query Formatter") == "developer-tools"

    def test_hash_tool(self):
        assert classify_category("sha256-hash", "SHA256 Hash") == "security"

    def test_unknown_defaults_to_utilities(self):
        assert classify_category("xyzzy", "Xyzzy") == "utilities"


class TestSuggestTags:
    def test_formatter(self):
        tags = suggest_tags("json-formatter", "JSON Formatter")
        assert "formatter" in tags

    def test_encoder_decoder(self):
        tags = suggest_tags("url-encoder-decoder", "URL Encoder Decoder")
        assert "encoder-decoder" in tags

    def test_generator(self):
        tags = suggest_tags("uuid-generator", "UUID Generator")
        assert "generator" in tags

    def test_security(self):
        tags = suggest_tags("password-checker", "Password Checker")
        assert "security" in tags

    def test_devops(self):
        tags = suggest_tags("docker-manager", "Docker Manager")
        assert "devops" in tags

    def test_no_tags_for_unknown(self):
        tags = suggest_tags("xyzzy", "Xyzzy")
        assert isinstance(tags, list)


class TestAudit:
    def test_all_categorized(self):
        products = [
            {"slug": "a", "name": "A", "category": "developer-tools", "tags": ["formatter"]},
        ]
        result = audit(products)
        assert result == []

    def test_uncategorized(self):
        products = [
            {"slug": "json-tool", "name": "JSON Tool", "category": "uncategorized", "tags": ["formatter"]},
        ]
        result = audit(products)
        assert len(result) == 1
        assert result[0]["needs_category"] is True

    def test_no_tags(self):
        products = [
            {"slug": "a", "name": "A", "category": "developer-tools", "tags": []},
        ]
        result = audit(products)
        assert len(result) == 1
        assert result[0]["needs_tags"] is True

    def test_both_missing(self):
        products = [
            {"slug": "json-tool", "name": "JSON Tool", "category": "uncategorized", "tags": []},
        ]
        result = audit(products)
        assert len(result) == 1
        assert result[0]["needs_category"] is True
        assert result[0]["needs_tags"] is True
        assert result[0]["suggested_category"] == "developer-tools"


class TestGenerateReport:
    def test_basic_report(self):
        products = [
            {"slug": "a", "name": "A", "category": "developer-tools", "tags": ["formatter"]},
            {"slug": "b", "name": "B", "category": "uncategorized", "tags": []},
        ]
        report = generate_report(products)
        assert report["total"] == 2
        assert report["uncategorized"] == 1
        assert report["no_tags"] == 1
        assert "developer-tools" in report["category_distribution"]

    def test_empty_products(self):
        report = generate_report([])
        assert report["total"] == 0
        assert report["uncategorized"] == 0


class TestGetProducts:
    def test_with_active(self):
        state = {"products": {"active": [{"slug": "a"}]}}
        assert len(get_products(state)) == 1

    def test_empty(self):
        state = {}
        assert get_products(state) == []


class TestSlugTextEdgeCases:
    def test_digits_separated(self):
        result = _slug_text("base64-encoder", "Base64 Encoder")
        assert "base" in result
        assert "64" in result
        assert "encoder" in result

    def test_multiple_hyphens(self):
        result = _slug_text("jwt-token-generator-pro", "JWT Token Generator Pro")
        assert "jwt" in result
        assert "token" in result
        assert "generator" in result
        assert "pro" in result

    def test_all_caps_name(self):
        result = _slug_text("ssl-checker", "SSL Checker")
        assert "ssl" in result
        assert "checker" in result


class TestClassifyCategoryEdgeCases:
    def test_ai_tool_priority_over_developer(self):
        assert classify_category("llm-token-counter", "LLM Token Counter") == "ai-tools"

    def test_security_priority_over_developer(self):
        assert classify_category("jwt-debugger", "JWT Debugger") == "security"

    def test_devops_priority_over_developer(self):
        assert classify_category("docker-compose-validator", "Docker Compose Validator") == "devops"

    def test_mixed_keywords_returns_highest_priority(self):
        result = classify_category("ssl-api-validator", "SSL API Validator")
        assert result in ("security", "api-services", "developer-tools")

    def test_empty_strings(self):
        assert classify_category("", "") == "utilities"

    def test_numeric_only_slug(self):
        result = classify_category("12345", "12345")
        assert isinstance(result, str)


class TestSuggestTagsEdgeCases:
    def test_multiple_tag_matches(self):
        tags = suggest_tags("json-validator-generator", "JSON Validator Generator")
        assert isinstance(tags, list)
        assert len(tags) >= 2

    def test_data_tag(self):
        tags = suggest_tags("yaml-converter", "YAML Converter")
        assert "data" in tags

    def test_visual_tag(self):
        tags = suggest_tags("css-gradient-studio", "CSS Gradient Studio")
        assert "visual" in tags

    def test_analyzer_tag(self):
        tags = suggest_tags("code-complexity-analyzer", "Code Complexity Analyzer")
        assert "analyzer" in tags


class TestAuditShortFieldNames:
    def test_s_field_for_slug(self):
        products = [
            {"s": "json-tool", "n": "JSON Tool", "category": "uncategorized", "tags": []},
        ]
        result = audit(products)
        assert len(result) == 1
        assert result[0]["slug"] == "json-tool"

    def test_n_field_for_name(self):
        products = [
            {"s": "docker-builder", "n": "Docker Builder", "category": "devops", "tags": []},
        ]
        result = audit(products)
        assert len(result) == 1
        assert result[0]["suggested_tags"] is not None

    def test_empty_category_string(self):
        products = [
            {"slug": "test", "name": "Test", "category": "", "tags": ["formatter"]},
        ]
        result = audit(products)
        assert len(result) == 1
        assert result[0]["needs_category"] is True

    def test_none_category(self):
        products = [
            {"slug": "test", "name": "Test", "category": None, "tags": ["formatter"]},
        ]
        result = audit(products)
        assert len(result) == 1
        assert result[0]["needs_category"] is True


class TestGenerateReportEdgeCases:
    def test_category_distribution_sorted(self):
        products = [
            {"slug": "a", "name": "A", "category": "utilities", "tags": []},
            {"slug": "b", "name": "B", "category": "developer-tools", "tags": []},
            {"slug": "c", "name": "C", "category": "developer-tools", "tags": []},
        ]
        report = generate_report(products)
        dist = report["category_distribution"]
        assert dist["developer-tools"] == 2
        assert dist["utilities"] == 1

    def test_top_tags_limit(self):
        products = [{"slug": f"p{i}", "name": f"P{i}", "category": "dev", "tags": [f"tag-{i}"]} for i in range(20)]
        report = generate_report(products)
        assert len(report["top_tags"]) <= 15

    def test_by_category_grouping(self):
        products = [
            {"slug": "a", "name": "A", "category": "security", "tags": []},
            {"slug": "b", "name": "B", "category": "security", "tags": []},
            {"slug": "c", "name": "C", "category": "devops", "tags": []},
        ]
        report = generate_report(products)
        assert len(report["by_category"]["security"]) == 2
        assert len(report["by_category"]["devops"]) == 1


class TestCategoryRulesIntegrity:
    def test_all_categories_in_priority(self):
        rule_cats = {cat for cat, _ in CATEGORY_RULES}
        priority_set = set(CATEGORY_PRIORITY)
        assert rule_cats == priority_set, f"Missing from priority: {rule_cats - priority_set}"

    def test_no_duplicate_keywords_within_category(self):
        for cat, keywords in CATEGORY_RULES:
            seen = set()
            for kw in keywords:
                assert kw not in seen, f"Duplicate keyword '{kw}' in category '{cat}'"
                seen.add(kw)
