# Requirement: C-1, C-2, C-3, C-4, E-1
"""컴플라이언스 탐지 재현율/정밀도. [평가 설계 6.1절] 목표: 재현율 ≥0.90, 정밀도 ≥0.60
— 재현율 우선([4.1절 재현율 우선 설계](/docs/02/)이 아니라 [기능 명세 2.4절] 원칙과 동일:
놓치는 것이 과잉 경고보다 위험하다)."""

from __future__ import annotations


def precision_recall(true_positive: int, false_positive: int, false_negative: int) -> dict[str, float]:
    precision = (
        true_positive / (true_positive + false_positive)
        if (true_positive + false_positive) > 0
        else float("nan")
    )
    recall = (
        true_positive / (true_positive + false_negative)
        if (true_positive + false_negative) > 0
        else float("nan")
    )
    return {"precision": precision, "recall": recall, "tp": true_positive, "fp": false_positive, "fn": false_negative}


def score_binary_predictions(expected: list[bool], predicted: list[bool]) -> dict[str, float]:
    """항목별 "위반 있음/없음" 이진 라벨 목록으로 TP/FP/FN을 센다."""
    if len(expected) != len(predicted):
        raise ValueError("expected와 predicted 길이가 다르다")
    tp = sum(1 for e, p in zip(expected, predicted) if e and p)
    fp = sum(1 for e, p in zip(expected, predicted) if not e and p)
    fn = sum(1 for e, p in zip(expected, predicted) if e and not p)
    return precision_recall(tp, fp, fn)
