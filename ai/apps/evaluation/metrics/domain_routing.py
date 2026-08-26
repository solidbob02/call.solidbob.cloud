# Requirement: B-0, E-1
"""도메인 라우팅(자동 분류) 정확도. [평가 설계 6.1절] 목표: 정확도 ≥0.95 — 도메인을
잘못 분류하면 엉뚱한 인덱스 전체에서 검색하는 셈이라 Recall@5 자체가 무의미해지므로,
같은 도메인 안의 검색 지표보다 엄격하게 잡는다. 규칙으로만 계산한다(LLM 채점 배제,
6.2절 원칙 1). 도메인 라우팅을 자동 분류로 하기로 한 결정은
_project/decisions/007-도메인-라우팅-자동분류-확정.md 참고.
"""

from __future__ import annotations

DOMAINS = ("finance", "dasan", "shopping", "health")


def score_domain_routing(expected: list[str], predicted: list[str]) -> dict:
    """(expected_domain, predicted_domain) 쌍 목록에 대한 정확도 + 오분류 행렬."""
    if len(expected) != len(predicted):
        raise ValueError("expected와 predicted 길이가 다르다")
    n = len(expected)
    if n == 0:
        return {"accuracy": float("nan"), "n": 0, "confusion": {}}

    confusion: dict[str, dict[str, int]] = {d: {d2: 0 for d2 in DOMAINS} for d in DOMAINS}
    correct = 0
    for e, p in zip(expected, predicted):
        if e == p:
            correct += 1
        if e in confusion and p in confusion[e]:
            confusion[e][p] += 1

    return {"accuracy": correct / n, "n": n, "confusion": confusion}
