# Requirement: D-4
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.knowledge_gap_dto import KnowledgeGapReport


class KnowledgeGapPort(ABC):
    """공백 신고를 저장한다. 저장한 행의 id 를 돌려준다 — 화면이 접수를 확인할 수 있어야 한다."""

    @abstractmethod
    async def save(self, report: KnowledgeGapReport) -> int: ...
