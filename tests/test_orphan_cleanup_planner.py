from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from scripts.orphan_cleanup_planner import (
    ARCHIVE_DIR,
    apply_archive,
    format_plan,
    plan_cleanup,
)


def _orphan(slug: str, category: str, size_bytes: int = 0, **kw: Any) -> dict[str, Any]:
    return {
        "slug": slug,
        "category": category,
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        **kw,
    }


class TestPlanCleanup:
    def test_empty(self) -> None:
        result = plan_cleanup([])
        assert result["total_orphans"] == 0
        assert result["archive_count"] == 0
        assert result["integrate_count"] == 0

    def test_dead_archived(self) -> None:
        orphans = [_orphan("dead-1", "dead", 1024)]
        result = plan_cleanup(orphans)
        assert result["archive_count"] == 1
        assert result["plans"]["archive"][0]["slug"] == "dead-1"

    def test_minimal_archived(self) -> None:
        orphans = [_orphan("mini-1", "minimal", 512)]
        result = plan_cleanup(orphans)
        assert result["archive_count"] == 1
        assert result["plans"]["archive"][0]["action"] == "archive"

    def test_has_spec_review(self) -> None:
        orphans = [_orphan("spec-only", "has_spec", 2048)]
        result = plan_cleanup(orphans)
        assert result["review_count"] == 1
        assert result["plans"]["review"][0]["action"] == "review"

    def test_has_code_review(self) -> None:
        orphans = [_orphan("code-only", "has_code", 8192)]
        result = plan_cleanup(orphans)
        assert result["review_count"] == 1

    def test_deployable_integrate(self) -> None:
        orphans = [_orphan("ready-to-go", "deployable", 16384)]
        result = plan_cleanup(orphans)
        assert result["integrate_count"] == 1
        assert result["plans"]["integrate"][0]["action"] == "integrate"

    def test_mixed_categories(self) -> None:
        orphans = [
            _orphan("d1", "dead", 100),
            _orphan("d2", "dead", 200),
            _orphan("m1", "minimal", 50),
            _orphan("s1", "has_spec", 1000),
            _orphan("c1", "has_code", 2000),
            _orphan("dp1", "deployable", 5000),
        ]
        result = plan_cleanup(orphans)
        assert result["archive_count"] == 3
        assert result["review_count"] == 2
        assert result["integrate_count"] == 1
        assert result["total_orphans"] == 6

    def test_reclaimable_bytes(self) -> None:
        orphans = [
            _orphan("d1", "dead", 1024),
            _orphan("m1", "minimal", 2048),
            _orphan("s1", "has_spec", 4096),
        ]
        result = plan_cleanup(orphans)
        assert result["reclaimable_bytes"] == 1024 + 2048
        assert result["reclaimable_mb"] >= 0

    def test_ts_present(self) -> None:
        result = plan_cleanup([_orphan("x", "dead", 0)])
        assert "ts" in result
        assert "T" in result["ts"] or ":" in result["ts"]


class TestApplyArchive:
    def test_dry_run_no_move(self, tmp_path: Path) -> None:
        src = tmp_path / "products" / "dead-1"
        src.mkdir(parents=True)
        (src / "file.txt").write_text("data")

        archive_dir = tmp_path / "products" / "_archived"

        plan_result = {
            "plans": {
                "archive": [{"slug": "dead-1", "category": "dead"}],
            }
        }

        import scripts.orphan_cleanup_planner as mod

        orig_root = mod.ROOT
        orig_archive = mod.ARCHIVE_DIR
        try:
            mod.ROOT = tmp_path
            mod.ARCHIVE_DIR = archive_dir
            result = apply_archive(plan_result, dry_run=True)
        finally:
            mod.ROOT = orig_root
            mod.ARCHIVE_DIR = orig_archive

        assert result["archived"] == 1
        assert result["dry_run"] is True
        assert src.is_dir()

    def test_empty_plan(self) -> None:
        result = apply_archive({"plans": {"archive": []}}, dry_run=True)
        assert result["archived"] == 0


class TestFormatPlan:
    def test_empty(self) -> None:
        plan = plan_cleanup([])
        text = format_plan(plan)
        assert "Orphan Cleanup Plan" in text
        assert "**Total orphans:** 0" in text

    def test_sections_present(self) -> None:
        orphans = [
            _orphan("dead1", "dead", 100),
            _orphan("spec1", "has_spec", 200),
            _orphan("deploy1", "deployable", 300),
        ]
        plan = plan_cleanup(orphans)
        text = format_plan(plan)
        assert "ARCHIVE" in text
        assert "REVIEW" in text
        assert "INTEGRATE" in text
        assert "dead1" in text
        assert "spec1" in text
        assert "deploy1" in text

    def test_next_steps(self) -> None:
        plan = plan_cleanup([_orphan("d", "dead", 0)])
        text = format_plan(plan)
        assert "Next Steps" in text
