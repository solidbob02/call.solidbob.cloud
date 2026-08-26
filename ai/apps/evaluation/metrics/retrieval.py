# Requirement: B-2, E-1
"""검색 지표 — Recall@k, MRR. [평가 설계 6.1절] 목표: Recall@5 ≥0.70(오류 없음)/≥0.60
(오류 10%), MRR ≥0.55. 규칙으로만 계산한다 (LLM 채점 배제, 6.2절 원칙 1)."""

from __future__ import annotations


def hit_at_k(expected_ids: list[str], retrieved_ids: list[str], k: int = 5) -> bool:
    """정답 문서 중 하나라도 상위 k개 안에 있으면 True."""
    if not expected_ids:
        return True  # 정답이 없는 항목(C/F-2 전용 케이스)은 검색 채점 대상이 아니다.
    return any(doc_id in retrieved_ids[:k] for doc_id in expected_ids)


def reciprocal_rank(expected_ids: list[str], retrieved_ids: list[str]) -> float:
    """정답이 처음 등장하는 순위의 역수. 정답이 없으면 0."""
    for rank, doc_id in enumerate(retrieved_ids, start=1):
        if doc_id in expected_ids:
            return 1.0 / rank
    return 0.0


def aggregate_recall_mrr(
    pairs: list[tuple[list[str], list[str]]], k: int = 5
) -> dict[str, float]:
    """(expected_ids, retrieved_ids) 쌍 목록 전체에 대한 Recall@k, MRR 평균."""
    scored = [(e, r) for e, r in pairs if e]  # 정답 없는 항목은 분모에서 제외
    if not scored:
        return {"recall_at_k": float("nan"), "mrr": float("nan"), "n": 0}
    recall = sum(hit_at_k(e, r, k) for e, r in scored) / len(scored)
    mrr = sum(reciprocal_rank(e, r) for e, r in scored) / len(scored)
    return {"recall_at_k": recall, "mrr": mrr, "n": len(scored)}
