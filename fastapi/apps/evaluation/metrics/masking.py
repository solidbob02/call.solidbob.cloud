# Requirement: C-5, E-1
"""C-5 개인정보 마스킹 채점. [평가 설계 6.1절] P1~P7 패턴 마스킹 누락은 **0건 — 절대
규칙**이다. [6.2절 원칙 4]에 따라 평균값이 아니라 1건 단위로 실패 처리한다. 과잉
마스킹률은 참고 기록일 뿐 목표가 아니다."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MaskingCase:
    item_id: str
    pattern: str  # P1~P7
    should_be_masked: bool
    was_masked: bool


def find_misses(cases: list[MaskingCase]) -> list[MaskingCase]:
    """마스킹됐어야 하는데 안 된 케이스 — 절대 규칙 위반. 하나라도 있으면 안 된다."""
    return [c for c in cases if c.should_be_masked and not c.was_masked]


def over_masking_rate(cases: list[MaskingCase]) -> float:
    """마스킹 안 됐어야 하는데 된 케이스 비율. 목표 수치 없음 — 참고 기록만."""
    negatives = [c for c in cases if not c.should_be_masked]
    if not negatives:
        return float("nan")
    return sum(1 for c in negatives if c.was_masked) / len(negatives)


def score_masking(cases: list[MaskingCase]) -> dict:
    misses = find_misses(cases)
    return {
        "miss_count": len(misses),
        "missed_items": [c.item_id for c in misses],
        "absolute_rule_passed": len(misses) == 0,
        "over_masking_rate": over_masking_rate(cases),
        "n": len(cases),
    }
