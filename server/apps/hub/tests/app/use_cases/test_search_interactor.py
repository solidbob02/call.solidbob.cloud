# Requirement: B-2, B-3, QUA-1
"""스텁 포트로 인터랙터만 검증. 실제 검색 품질(Recall@5·MRR)은 retrieval 스포크가
골든셋으로 채점받는다 — 여기서는 배선과 입력 검증만 본다."""

import asyncio

import pytest

from hub.app.dtos import RetrievedDoc
from hub.app.dtos.search_dto import MAX_TOP_K, SearchQuery
from hub.app.ports.output import RetrievalPort
from hub.app.use_cases.search_interactor import SearchInteractor


class _SpyRetrieval(RetrievalPort):
    """받은 인자를 기록하고 고정 결과를 돌려준다."""

    def __init__(self, docs: list[RetrievedDoc] | None = None):
        self.calls: list[tuple[str, int]] = []
        self._docs = docs if docs is not None else [
            RetrievedDoc(doc_id="FIN-TERM-2.2", title="부정사용 보상 기준", snippet="…", score=0.87),
            RetrievedDoc(doc_id="FIN-TERM-2.1", title="분실·도난 신고", snippet="…", score=0.61),
        ]

    async def retrieve(self, utterance: str, top_k: int = 5) -> list[RetrievedDoc]:
        self.calls.append((utterance, top_k))
        return list(self._docs)


def _run(port, query):
    return asyncio.run(SearchInteractor(retrieval=port).search(query))


def test_포트에_발화와_top_k를_그대로_넘긴다():
    port = _SpyRetrieval()
    _run(port, SearchQuery(utterance="카드 분실 보상", top_k=3))
    assert port.calls == [("카드 분실 보상", 3)]


def test_검색어_앞뒤_공백을_제거한다():
    port = _SpyRetrieval()
    result = _run(port, SearchQuery(utterance="  반품 배송비  "))
    assert port.calls[0][0] == "반품 배송비"
    assert result.query == "반품 배송비"


def test_기본_top_k는_5다():
    port = _SpyRetrieval()
    _run(port, SearchQuery(utterance="배송 지연"))
    assert port.calls[0][1] == 5


def test_포트가_준_순서를_그대로_유지한다():
    """순위는 retrieval 스포크 몫이다 — 허브가 다시 정렬하면 자동 추천과 순위가 갈린다."""
    port = _SpyRetrieval()
    result = _run(port, SearchQuery(utterance="카드"))
    assert [d.doc_id for d in result.docs] == ["FIN-TERM-2.2", "FIN-TERM-2.1"]


@pytest.mark.parametrize("utterance", ["", "   ", "\n"])
def test_빈_검색어는_거부한다(utterance):
    port = _SpyRetrieval()
    with pytest.raises(ValueError):
        _run(port, SearchQuery(utterance=utterance))
    assert port.calls == []


@pytest.mark.parametrize("top_k", [0, -1, MAX_TOP_K + 1])
def test_범위를_벗어난_top_k는_거부한다(top_k):
    port = _SpyRetrieval()
    with pytest.raises(ValueError):
        _run(port, SearchQuery(utterance="카드", top_k=top_k))
    assert port.calls == []


def test_결과가_없어도_예외가_아니다():
    """'관련 문서 없음'(B-6)은 정상 응답이다. 빈 결과와 검색 실패를 구분한다."""
    result = _run(_SpyRetrieval(docs=[]), SearchQuery(utterance="없는 내용"))
    assert result.docs == ()
