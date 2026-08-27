# Requirement: D-4
"""공백 리포트 조회 인터랙터. 포트를 부르고 페이지 껍데기를 씌우는 것이 전부다.

**여기서 하지 않는 것**:
- 무엇이 진짜 공백인지, 어느 것이 먼저인지 판정하지 않는다 — `ai/` 몫이다
- 신고를 묶거나 걸러내지 않는다. 중복이든 애매하든 그대로 보여준다.
  입구에서 거르지 않기로 한 것과 같은 이유다 — **거르면 그 판단의 재료가 사라진다**
"""

from __future__ import annotations

from hub.app.dtos.knowledge_gap_query_dto import (
    MAX_LIMIT,
    OPEN,
    RESOLVED,
    GapResolution,
    KnowledgeGapPage,
    KnowledgeGapQuery,
    KnowledgeGapSummary,
)
from hub.app.ports.input.knowledge_gap_query_use_case import KnowledgeGapQueryUseCase
from hub.app.ports.output.knowledge_gap_query_port import KnowledgeGapQueryPort

_VALID_MODULES = ("B", "C", "F")
_VALID_STATUSES = (OPEN, RESOLVED)


class KnowledgeGapQueryInteractor(KnowledgeGapQueryUseCase):
    def __init__(self, gaps: KnowledgeGapQueryPort) -> None:
        self._gaps = gaps

    async def list_gaps(self, query: KnowledgeGapQuery) -> KnowledgeGapPage:
        if query.limit < 1 or query.limit > MAX_LIMIT:
            raise ValueError(f"limit 은 1~{MAX_LIMIT} 사이여야 합니다")
        if query.offset < 0:
            raise ValueError("offset 은 0 이상이어야 합니다")
        if query.module is not None and query.module not in _VALID_MODULES:
            raise ValueError(f"module 은 {', '.join(_VALID_MODULES)} 중 하나여야 합니다")
        if query.status is not None and query.status not in _VALID_STATUSES:
            raise ValueError(f"status 는 {', '.join(_VALID_STATUSES)} 중 하나여야 합니다")

        records = await self._gaps.list_gaps(query)
        total = await self._gaps.count_gaps(query)
        return KnowledgeGapPage(
            gaps=tuple(records), total=total, limit=query.limit, offset=query.offset
        )

    async def summarize(self) -> KnowledgeGapSummary:
        by_module = await self._gaps.count_by_module()
        by_domain = await self._gaps.count_by_domain()
        # 총계는 모듈 축에서만 센다. 도메인 축은 통화가 없는 신고(call_id 가 null)를
        # 놓치므로 두 축의 합이 다를 수 있다 — 다른 값을 같은 이름으로 쓰지 않는다.
        return KnowledgeGapSummary(
            by_module=tuple(by_module),
            by_domain=tuple(by_domain),
            total=sum(c.total for c in by_module),
        )

    async def resolve(self, resolution: GapResolution) -> bool:
        if resolution.status not in _VALID_STATUSES:
            raise ValueError(f"status 는 {', '.join(_VALID_STATUSES)} 중 하나여야 합니다")
        return await self._gaps.update_status(resolution.gap_id, resolution.status)
