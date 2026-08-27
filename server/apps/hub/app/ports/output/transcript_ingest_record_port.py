# Requirement: 7.3절 전사 이벤트, SEC-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.transcript_dto import TranscriptEvent


class TranscriptIngestRecordPort(ABC):
    """전사 수신 활동 기록. 마스킹 **후** 이벤트만 받는다 — 원문을 받는 시그니처는 만들지 않는다 (SEC-1).
    지금은 로그 어댑터, 3주차에 PostgreSQL transcript_segment 어댑터로 교체. I/O 포트라 async (구현체도 async — LSP)."""

    @abstractmethod
    async def record(self, event: TranscriptEvent) -> None: ...
