# Requirement: E-1, B-2
"""합성 루트 테스트 — 스포크를 hub 포트에 꽂는 배선만 본다 (`scripts/run_eval.py` 소관).

**여기가 `apps/` 밖인 이유**: `.importlinter` 의 module-independence 계약이
`evaluation` ↔ `retrieval` 직접 참조를 막는다. 두 모듈의 접점은 hub 포트(추상)뿐이고,
구체 구현을 꽂는 일은 두 모듈 **밖에서** 해야 한다. 그 배선을 검증하는 테스트도 밖에 둔다 —
`server/tests/` 가 `main.py` 에 대해 하는 역할과 같다.

ES 없이 돈다. 가짜 클라이언트로 하네스가 실제로 숫자를 내는지만 확인한다.
"""

from __future__ import annotations

from pathlib import Path

from evaluation.golden_set import load_golden_set
from evaluation.harness import NOT_IMPLEMENTED, Ports, run_eval
from retrieval.adapter.outbound.es_bm25_retriever import EsBm25Retriever

GOLDEN_SET = Path(__file__).resolve().parents[2] / "golden-set" / "v1-50.json"


class StubClient:
    """항상 첫 정답 문서를 1위로 돌려주는 ES 대역. 하네스 배선만 보는 것이라 이걸로 충분하다."""

    def __init__(self, doc_id: str):
        self._doc_id = doc_id

    def search(self, **kwargs):
        return {
            "hits": {
                "hits": [
                    {
                        "_id": self._doc_id,
                        "_score": 1.0,
                        "_source": {"doc_id": self._doc_id, "title": "제목", "text": "본문"},
                    }
                ]
            }
        }


def test_포트를_꽂지_않으면_미구현으로_보고한다():
    """목표 수치를 지어내지 않는다 — 절대 원칙 2를 하네스가 지키는지 본다."""
    report = run_eval(load_golden_set(GOLDEN_SET), Ports())
    assert report["retrieval"] == NOT_IMPLEMENTED


def test_검색을_꽂으면_Recall과_MRR이_나온다():
    """w2-naive-rag 의 완료 조건 — Ports(retrieval=...) 에 꽂으면 숫자가 나온다."""
    items = load_golden_set(GOLDEN_SET)
    answer = next(it.expected_doc_ids[0] for it in items if it.expected_doc_ids)

    report = run_eval(items, Ports(retrieval=EsBm25Retriever(StubClient(answer))))

    assert isinstance(report["retrieval"], dict), "검색이 '미구현'으로 보고됐다"
    result = report["retrieval"]
    assert result["n"] > 0, "채점된 항목이 없다"
    assert 0.0 <= result["recall_at_k"] <= 1.0
    assert 0.0 <= result["mrr"] <= 1.0
    # 그 한 건은 1위로 맞혔으므로 0 보다 커야 한다 — 배선이 끊겨 있으면 0 이 나온다
    assert result["recall_at_k"] > 0


def test_채점_단위는_chunk_id_가_아니라_doc_id_다():
    """조항이 쪼개져 `_id` 에 `#1` 이 붙어도 골든셋과 대조되는 값은 조항 ID 여야 한다."""
    items = load_golden_set(GOLDEN_SET)
    answer = next(it.expected_doc_ids[0] for it in items if it.expected_doc_ids)

    class SplitChunkClient(StubClient):
        def search(self, **kwargs):
            resp = super().search(**kwargs)
            resp["hits"]["hits"][0]["_id"] = f"{self._doc_id}#1"  # 청크는 쪼개졌지만
            return resp                                            # doc_id 는 그대로다

    report = run_eval(items, Ports(retrieval=EsBm25Retriever(SplitChunkClient(answer))))
    assert report["retrieval"]["recall_at_k"] > 0
