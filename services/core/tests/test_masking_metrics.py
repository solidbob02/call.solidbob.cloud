# Requirement: C-5, QUA-1
from services.core.eval.metrics.masking import MaskingCase, find_misses, over_masking_rate, score_masking


def test_no_misses_passes_absolute_rule():
    cases = [
        MaskingCase("GS-006", "P1", should_be_masked=True, was_masked=True),
        MaskingCase("GS-006", "P2", should_be_masked=True, was_masked=True),
    ]
    result = score_masking(cases)
    assert result["miss_count"] == 0
    assert result["absolute_rule_passed"] is True


def test_single_miss_fails_absolute_rule():
    # 절대 규칙(6.2절 원칙 4) — 999개 맞아도 1개 놓치면 실패.
    cases = [MaskingCase(f"GS-{i}", "P4", should_be_masked=True, was_masked=True) for i in range(999)]
    cases.append(MaskingCase("GS-999", "P4", should_be_masked=True, was_masked=False))
    result = score_masking(cases)
    assert result["miss_count"] == 1
    assert result["absolute_rule_passed"] is False
    assert result["missed_items"] == ["GS-999"]


def test_find_misses_ignores_correctly_unmasked_cases():
    cases = [MaskingCase("GS-001", "P1", should_be_masked=False, was_masked=False)]
    assert find_misses(cases) == []


def test_over_masking_rate_is_reference_only():
    cases = [
        MaskingCase("GS-001", "P1", should_be_masked=False, was_masked=True),  # 과잉 마스킹
        MaskingCase("GS-002", "P1", should_be_masked=False, was_masked=False),
    ]
    assert over_masking_rate(cases) == 0.5
