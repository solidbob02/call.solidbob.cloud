# Requirement: D-4
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.knowledge_gap_dto import KnowledgeGapReceipt, KnowledgeGapReport


class KnowledgeGapUseCase(ABC):
    """지식베이스 공백 신고 접수 (D-4).

    **수집만 한다.** 집계·우선순위 판단은 `ai/` 몫이다 — "품질을 만들거나 재는 코드인가?"
    기준으로 갈린다(영역 규칙).
    """

    @abstractmethod
    async def report(self, report: KnowledgeGapReport) -> KnowledgeGapReceipt: ...
