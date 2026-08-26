# Requirement: B-2, B-3
"""수동 검색 인터랙터. RetrievalPort 를 부르고 결과를 계약 형태로 감싸는 것이 전부다.

순위 매기기·리랭킹·병합은 retrieval 스포크(`ai/`) 몫이다 — 여기서 다시 정렬하지 않는다.
허브가 순서를 건드리면 자동 추천과 수동 검색이 서로 다른 순위를 내놓게 된다.
"""

from __future__ import annotations

from hub.app.dtos.search_dto import MAX_TOP_K, SearchQuery, SearchResult
from hub.app.ports.input.search_use_case import SearchUseCase
from hub.app.ports.output.retrieval_port import RetrievalPort


class SearchInteractor(SearchUseCase):
    def __init__(self, retrieval: RetrievalPort) -> None:
        self._retrieval = retrieval

    async def search(self, query: SearchQuery) -> SearchResult:
        utterance = query.utterance.strip()
        if not utterance:
            raise ValueError("검색어가 비어 있습니다")
        if not 1 <= query.top_k <= MAX_TOP_K:
            raise ValueError(f"top_k 는 1~{MAX_TOP_K} 사이여야 합니다: {query.top_k}")

        docs = await self._retrieval.retrieve(utterance, top_k=query.top_k)
        return SearchResult(query=utterance, docs=tuple(docs))
