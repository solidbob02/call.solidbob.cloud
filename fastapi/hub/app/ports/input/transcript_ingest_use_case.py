# Requirement: 7.3절 전사 이벤트, C-5, SEC-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.transcript_dto import TranscriptEvent
from hub.app.dtos.transcript_ingest_dto import TranscriptIngestCommand


class TranscriptIngestUseCase(ABC):
    """전사 1건 수신 → 마스킹 → 계약 형태(TranscriptEvent)로 돌려준다. 파이프라인의 입구."""

    @abstractmethod
    def ingest(self, command: TranscriptIngestCommand) -> TranscriptEvent: ...
