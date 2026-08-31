from __future__ import annotations

from dataclasses import dataclass
from typing import Any

ALIASES = {
    "case_id": {"case_id", "case", "ticket", "request_id", "id"},
    "opened_at": {"opened_at", "created", "created_at", "date_opened"},
    "category": {"category", "type", "service", "request_type"},
    "description": {"description", "details", "summary", "notes"},
}


@dataclass(frozen=True)
class NormalizedRecord:
    values: dict[str, Any]
    provenance: dict[str, str]
    confidence: float
    review_reasons: tuple[str, ...]


def normalize(record: dict[str, Any]) -> NormalizedRecord:
    lowered = {str(k).strip().lower(): v for k, v in record.items()}
    values, provenance, reasons = {}, {}, []
    for canonical, aliases in ALIASES.items():
        matches = [key for key in lowered if key in aliases]
        if len(matches) == 1:
            key = matches[0]
            value = lowered[key]
            if isinstance(value, str):
                value = value.strip()
            values[canonical], provenance[canonical] = value, key
        elif not matches:
            reasons.append(f"missing:{canonical}")
        else:
            reasons.append(f"ambiguous:{canonical}")
    confidence = round(max(0.0, 1.0 - len(reasons) * 0.2), 2)
    return NormalizedRecord(values, provenance, confidence, tuple(reasons))
