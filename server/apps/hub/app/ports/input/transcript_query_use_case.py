# Requirement: A-1, SEC-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.transcript_query_dto import TranscriptPage, TranscriptQuery


class TranscriptQueryUseCase(ABC):
    """상담원이 지나간 발화를 되돌아본다. 실시간 경로가 아니다."""

    @abstractmethod
    async def list(self, query: TranscriptQuery) -> TranscriptPage: ...
