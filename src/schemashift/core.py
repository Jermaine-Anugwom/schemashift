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
    entries = [(str(key).strip(), str(key).strip().lower(), value) for key, value in record.items()]
    values, provenance, reasons = {}, {}, []
    for canonical, aliases in ALIASES.items():
        matches = [entry for entry in entries if entry[1] in aliases]
        if len(matches) == 1:
            original_key, normalized_key, value = matches[0]
            if isinstance(value, str):
                value = value.strip()
            values[canonical], provenance[canonical] = value, original_key or normalized_key
        elif not matches:
            reasons.append(f"missing:{canonical}")
        else:
            reasons.append(f"ambiguous:{canonical}")
    confidence = round(max(0.0, 1.0 - len(reasons) * 0.2), 2)
    return NormalizedRecord(values, provenance, confidence, tuple(reasons))
