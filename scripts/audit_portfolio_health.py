#!/usr/bin/env python3
"""Backward-compatible health audit entrypoint.

Legacy docs and automation still reference ``scripts/audit_portfolio_health.py``.
Keep that name alive and delegate to the real health pipeline so the old path
doesn't rot into another broken breadcrumb.
"""

from __future__ import annotations

import sys

from scripts.health_check import main as health_check_main


if __name__ == "__main__":
    result = health_check_main()
    sys.exit(0 if result["unhealthy"] == 0 else 1)
