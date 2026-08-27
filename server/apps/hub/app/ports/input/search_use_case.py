# Requirement: B-2, B-3
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.search_dto import SearchQuery, SearchResult


class SearchUseCase(ABC):
    """상담원 수동 검색. 자동 추천이 빗나간 건을 사람이 직접 찾는 폴백이다.

    [6.1절](/docs/06/) Recall@5 목표가 0.70 이라는 것은 10건 중 3건은 자동으로 못 찾는다는 뜻이고,
    그 3건에서 상담원이 막히지 않으려면 이 경로가 있어야 한다.
    """

    @abstractmethod
    async def search(self, query: SearchQuery) -> SearchResult: ...
