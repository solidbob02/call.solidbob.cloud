# Requirement: E-1, QUA-1
from evaluation.golden_set import load_golden_set


def test_loads_all_ten_items():
    items = load_golden_set()
    assert len(items) == 10
    assert [it.id for it in items] == [f"GS-{i:03d}" for i in range(1, 11)]


def test_f2_case_parses_evidence_dict():
    items = {it.id: it for it in load_golden_set()}
    gs009 = items["GS-009"]
    assert gs009.f2_case is not None
    assert gs009.f2_case.expected_verdict == "blocked"
    assert gs009.f2_case.evidence["위약금_안내"] is True
    assert gs009.f2_case.evidence["잔여할부_안내"] is False


def test_pii_patterns_parse_for_masking_cases():
    items = {it.id: it for it in load_golden_set()}
    gs007 = items["GS-007"]
    assert len(gs007.pii_patterns) == 1
    assert gs007.pii_patterns[0].pattern == "P4"
    assert gs007.pii_patterns[0].masked_expected is True
