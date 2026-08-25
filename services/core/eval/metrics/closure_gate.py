# Requirement: F-2, E-1
"""F-2 종결 요건 게이트 채점. [평가 설계 6.1절] 종결 요건 판정 정확도 **100% — 절대
규칙**(조건부 착수), 근거 규정 검색 정확도 ≥0.90. 판정은 [knowledge-base/policy/POLICY.md]
를 그대로 따르는 규칙 로직이어야 하며, 이 채점기는 그 출력을 검증만 한다."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class F2Prediction:
    item_id: str
    expected_verdict: str
    predicted_verdict: str
    expected_missing: list[str]
    predicted_missing: list[str]


def is_exact_match(pred: F2Prediction) -> bool:
    return (
        pred.predicted_verdict == pred.expected_verdict
        and sorted(pred.predicted_missing) == sorted(pred.expected_missing)
    )


def score_closure_gate(predictions: list[F2Prediction]) -> dict:
    failures = [p for p in predictions if not is_exact_match(p)]
    accuracy = 1.0 - (len(failures) / len(predictions)) if predictions else float("nan")
    return {
        "accuracy": accuracy,
        "absolute_rule_passed": len(failures) == 0,
        "failed_items": [p.item_id for p in failures],
        "n": len(predictions),
    }
