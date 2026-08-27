# Requirement: D-4
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.knowledge_gap_query_dto import (
    GapResolution,
    KnowledgeGapPage,
    KnowledgeGapQuery,
    KnowledgeGapSummary,
)


class KnowledgeGapQueryUseCase(ABC):
    @abstractmethod
    async def list_gaps(self, query: KnowledgeGapQuery) -> KnowledgeGapPage: ...

    @abstractmethod
    async def summarize(self) -> KnowledgeGapSummary: ...

    @abstractmethod
    async def resolve(self, resolution: GapResolution) -> bool: ...
