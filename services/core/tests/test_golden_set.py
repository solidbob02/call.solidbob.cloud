# Requirement: E-1, QUA-1
from services.core.eval.golden_set import load_golden_set


def test_loads_all_ten_items():
    items = load_golden_set()
    assert len(items) == 10
    assert [it.id for it in items] == [f"GS-{i:03d}" for i in range(1, 11)]


def test_f2_case_parses_evidence_dict():
    items = {it.id: it for it in load_golden_set()}
    gs009 = items["GS-009"]
    assert gs009.f2_case is not None
    assert gs009.f2_case.expected_verdict == "blocked"
    assert gs009.f2_case.evidence["중도해지수수료_안내"] is True
    assert gs009.f2_case.evidence["약정혜택소멸_안내"] is False


def test_pii_patterns_parse_for_masking_cases():
    items = {it.id: it for it in load_golden_set()}
    gs007 = items["GS-007"]
    assert len(gs007.pii_patterns) == 1
    assert gs007.pii_patterns[0].pattern == "P4"
    assert gs007.pii_patterns[0].masked_expected is True


def test_domain_field_parses_and_covers_all_four_domains():
    items = load_golden_set()
    domains = {it.domain for it in items}
    assert domains == {"finance", "dasan", "shopping", "health"}


def test_f2_cases_only_appear_in_domains_with_closure_flows():
    items = load_golden_set()
    f2_domains = {it.domain for it in items if it.f2_case is not None}
    assert f2_domains == {"finance", "shopping"}
