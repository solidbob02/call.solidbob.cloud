# Requirement: B-2, B-3
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.retrieved_doc_dto import RetrievedDoc


class RetrievalPort(ABC):
    """B-2·B-3. 발화를 받아 순위가 매겨진 조항 목록을 돌려준다. ES 호출 → async."""

    @abstractmethod
    async def retrieve(self, utterance: str, top_k: int = 5) -> list[RetrievedDoc]: ...
