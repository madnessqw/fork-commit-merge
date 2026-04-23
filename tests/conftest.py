"""Test bootstrap for local imports.

Pytest in this workspace can pick up another `scripts` namespace path first.
Force the repo root onto sys.path so the health/canonical pipeline tests always
exercise the local code instead of drifting into whatever else is installed on
the machine.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

