"""Tests for scripts.product_field_gap_analyzer"""

import json

from scripts.product_field_gap_analyzer import (
    _is_missing,
    analyze_gaps,
    format_gap_markdown,
    format_gap_telegram,
    load_products,
    PLACEHOLDER_VALUES,
)


def _make_products():
    return [
        {"slug": "tool-a", "name": "Tool A", "price": "$19", "description": "A great tool",
         "category": "dev", "tags": ["tool"], "checkout_url": "https://co.sh/a",
         "url": "https://a.vercel.app"},
        {"slug": "tool-b", "name": "Tool B", "price": "", "description": "",
         "category": "design", "tags": [], "checkout_url": "https://co.sh/b",
         "url": "https://b.vercel.app"},
        {"slug": "tool-c", "name": "Tool C", "price": "0", "description": None,
         "category": "", "tags": None, "checkout_url": "",
         "url": ""},
        {"slug": "tool-d", "name": "", "price": None, "description": "todo",
         "category": "N/A", "tags": [], "checkout_url": None,
         "url": "https://d.vercel.app"},
    ]


def test_is_missing_none():
    assert _is_missing(None) is True


def test_is_missing_empty_string():
    assert _is_missing("") is True


def test_is_missing_placeholder():
    for val in PLACEHOLDER_VALUES:
        assert _is_missing(val) is True


def test_is_missing_valid_string():
    assert _is_missing("hello") is False


def test_is_missing_zero_number():
    assert _is_missing(0) is False


def test_is_missing_empty_list():
    assert _is_missing([]) is True


def test_is_missing_valid_list():
    assert _is_missing(["tag"]) is False


def test_is_missing_valid_number():
    assert _is_missing(42) is False


def test_analyze_gaps_basic():
    prods = _make_products()
    report = analyze_gaps(prods)
    assert report["total_products"] == 4
    assert "field_gaps" in report


def test_analyze_gaps_price():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["price"])
    gaps = report["field_gaps"]["price"]
    assert gaps["missing_count"] == 2


def test_analyze_gaps_description():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["description"])
    gaps = report["field_gaps"]["description"]
    assert gaps["missing_count"] == 3


def test_analyze_gaps_slug():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["slug"])
    gaps = report["field_gaps"]["slug"]
    assert gaps["missing_count"] == 0


def test_analyze_gaps_url():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["url"])
    gaps = report["field_gaps"]["url"]
    assert gaps["missing_count"] == 1


def test_analyze_gaps_gap_pct():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["price"])
    assert report["field_gaps"]["price"]["gap_pct"] == 50.0


def test_analyze_gaps_empty_products():
    report = analyze_gaps([])
    assert report["total_products"] == 0
    assert report["gap_score"] == 0


def test_analyze_gaps_readiness_critical():
    prods = [
        {"slug": "x", "price": None, "description": None, "category": None,
         "tags": None, "checkout_url": None, "url": None, "name": None},
    ]
    report = analyze_gaps(prods)
    assert report["readiness"] == "critical"


def test_analyze_gaps_readiness_ready():
    prods = [
        {"slug": "x", "price": 19, "description": "A tool", "category": "dev",
         "tags": ["a"], "checkout_url": "https://co.sh/x", "url": "https://x.sh",
         "name": "X"},
    ]
    report = analyze_gaps(prods)
    assert report["readiness"] == "ready"


def test_analyze_gaps_readiness_needs_work():
    prods = [
        {"slug": "a", "price": 19, "description": "ok", "category": "dev",
         "tags": [], "checkout_url": "https://co.sh/a", "url": "https://a.sh",
         "name": "A"},
        {"slug": "b", "price": 19, "description": "", "category": "dev",
         "tags": [], "checkout_url": "", "url": "", "name": "B"},
    ]
    report = analyze_gaps(prods)
    assert report["readiness"] in ("needs_work", "good", "ready", "critical")


def test_analyze_gaps_custom_fields():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["name", "slug"])
    assert report["fields_analyzed"] == 2
    assert "name" in report["field_gaps"]
    assert "slug" in report["field_gaps"]


def test_analyze_gaps_name_field():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["name"])
    gaps = report["field_gaps"]["name"]
    assert gaps["missing_count"] == 1


def test_format_gap_markdown():
    report = analyze_gaps(_make_products())
    md = format_gap_markdown(report)
    assert "Field Gap" in md
    assert "Missing" in md
    assert "readiness" in md.lower() or "Readiness" in md


def test_format_gap_markdown_empty():
    report = analyze_gaps([])
    md = format_gap_markdown(report)
    assert "Field Gap" in md


def test_format_gap_telegram():
    report = analyze_gaps(_make_products())
    text = format_gap_telegram(report)
    assert "Gap" in text
    assert "Score" in text
    assert "products" in text.lower()


def test_format_gap_telegram_empty():
    report = analyze_gaps([])
    text = format_gap_telegram(report)
    assert "0 products" in text


def test_load_products_missing_file(tmp_path):
    result = load_products(tmp_path / "nope.json")
    assert result == []


def test_load_products_valid(tmp_path):
    state = {"products": {"active": [{"slug": "x", "status": "live"}]}}
    p = tmp_path / "STATE.json"
    p.write_text(json.dumps(state))
    result = load_products(p)
    assert len(result) == 1


def test_load_products_invalid_json(tmp_path):
    p = tmp_path / "STATE.json"
    p.write_text("{broken")
    result = load_products(p)
    assert result == []


def test_analyze_gaps_top_gapped_in_markdown():
    prods = [
        {"slug": "full", "name": "Full", "price": 19, "description": "ok",
         "category": "dev", "tags": ["a"], "checkout_url": "https://co.sh",
         "url": "https://f.sh"},
        {"slug": "empty", "name": "", "price": None, "description": None,
         "category": "", "tags": [], "checkout_url": None, "url": "",
         "extra": "val"},
    ]
    report = analyze_gaps(prods)
    md = format_gap_markdown(report)
    assert "empty" in md


def test_analyze_gaps_gap_score():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["price", "slug"])
    expected = report["field_gaps"]["price"]["missing_count"] + report["field_gaps"]["slug"]["missing_count"]
    assert report["gap_score"] == expected


def test_analyze_gaps_checkout_url():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["checkout_url"])
    gaps = report["field_gaps"]["checkout_url"]
    assert gaps["missing_count"] == 2


def test_analyze_gaps_tags_field():
    prods = _make_products()
    report = analyze_gaps(prods, fields=["tags"])
    gaps = report["field_gaps"]["tags"]
    assert gaps["missing_count"] == 3


def test_analyze_gaps_missing_slugs_capped():
    prods = [
        {"slug": f"s{i}", "price": None} for i in range(50)
    ]
    report = analyze_gaps(prods, fields=["price"])
    assert len(report["field_gaps"]["price"]["missing_slugs"]) == 20


def test_analyze_gaps_category_placeholder():
    prods = [
        {"slug": "a", "category": "N/A"},
        {"slug": "b", "category": "valid"},
        {"slug": "c", "category": "-"},
    ]
    report = analyze_gaps(prods, fields=["category"])
    assert report["field_gaps"]["category"]["missing_count"] == 2
