from __future__ import annotations

import json
from dataclasses import asdict

from .core import normalize


def main() -> None:
    record = {
        "Ticket": "SYN-204",
        "Created": "2026-08-31",
        "Service": "drainage",
        "Notes": "Standing water at a synthetic crossing",
    }
    print(json.dumps({"synthetic": True, "result": asdict(normalize(record))}, indent=2))
