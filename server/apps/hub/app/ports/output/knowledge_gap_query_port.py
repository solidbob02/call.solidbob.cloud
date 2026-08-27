# Requirement: D-4
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.knowledge_gap_query_dto import (
    GapCount,
    GapStatus,
    KnowledgeGapQuery,
    KnowledgeGapRecord,
)


class KnowledgeGapQueryPort(ABC):
    """쌓인 공백 신고를 읽고 상태를 옮긴다. 접수 포트(`KnowledgeGapPort`)와 분리한 이유는
    전사 쪽과 같다 — 쓰기는 상담 중에, 읽기는 지식베이스를 보강할 때 일어난다.

    **집계도 여기서 한다.** 신고가 수만 건이 되어도 SQL 이 세는 편이 낫고, 애플리케이션이
    전부 읽어와 세면 페이지네이션과 집계가 서로 어긋난다(한쪽은 50건만 보고 센다).
    """

    @abstractmethod
    async def list_gaps(self, query: KnowledgeGapQuery) -> list[KnowledgeGapRecord]: ...

    @abstractmethod
    async def count_gaps(self, query: KnowledgeGapQuery) -> int: ...

    @abstractmethod
    async def count_by_module(self) -> list[GapCount]: ...

    @abstractmethod
    async def count_by_domain(self) -> list[GapCount]: ...

    @abstractmethod
    async def update_status(self, gap_id: int, status: GapStatus) -> bool:
        """옮겼으면 True, 그런 id 가 없으면 False. **없는 것을 옮겼다고 하지 않는다.**"""
