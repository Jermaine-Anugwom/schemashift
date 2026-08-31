import pytest

from schemashift.core import normalize


@pytest.mark.parametrize("key", ["case_id", "case", "ticket", "request_id", "id"])
def test_case_aliases(key):
    result = normalize({key: "A-1", "created": "2026-08-31", "type": "road", "details": "pothole"})
    assert result.values["case_id"] == "A-1"


@pytest.mark.parametrize("missing", ["case_id", "opened_at", "category", "description"])
def test_missing_fields_are_visible(missing):
    base = {"case_id": "1", "opened_at": "now", "category": "road", "description": "x"}
    base.pop(missing)
    assert f"missing:{missing}" in normalize(base).review_reasons


def test_strips_values():
    assert (
        normalize({"id": " 1 ", "created": "x", "type": "y", "notes": " z "}).values["description"]
        == "z"
    )


def test_preserves_provenance():
    assert (
        normalize({"ticket": "1", "created": "x", "type": "y", "notes": "z"}).provenance["case_id"]
        == "ticket"
    )


def test_full_confidence():
    assert normalize({"id": "1", "created": "x", "type": "y", "notes": "z"}).confidence == 1.0


def test_unknown_fields_do_not_break():
    assert (
        normalize({"id": "1", "created": "x", "type": "y", "notes": "z", "extra": 9}).confidence
        == 1.0
    )
