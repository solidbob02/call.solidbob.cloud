# Requirement: A-1, SEC-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.transcript_dto import TranscriptEvent


class TranscriptQueryPort(ABC):
    """저장된 전사를 읽는다. 기록 포트(`TranscriptIngestRecordPort`)와 분리한 이유:

    쓰기는 파이프라인 입구(마스킹 직후)에서 일어나고, 읽기는 상담원이 화면에서 되돌아볼 때
    일어난다. 한 포트에 묶으면 쓰기만 필요한 곳도 조회 구현을 갖게 된다.

    **돌려주는 것은 마스킹 완료본뿐이다** (SEC-1). 원문은 애초에 저장돼 있지 않다.
    """

    @abstractmethod
    async def list_segments(self, call_id: str, limit: int, offset: int) -> list[TranscriptEvent]: ...

    @abstractmethod
    async def count_segments(self, call_id: str) -> int: ...
