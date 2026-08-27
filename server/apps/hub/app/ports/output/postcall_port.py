# Requirement: D-1, D-2, D-3
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.call_summary_dto import CallSummaryDraft
from hub.app.dtos.transcript_dto import TranscriptEvent


class PostcallPort(ABC):
    """D-1~D-3. 통화가 끝난 뒤 전사 전체로 요약·유형 제안·후속조치를 만든다. 모델 추론 → async.

    **마스킹된 전사만 받는다** (SEC-1). 통화 후 처리라고 원문을 다시 꺼내오지 않는다 —
    원문은 애초에 저장돼 있지 않다.

    돌려주는 것은 `CallSummaryDraft` 다. 확정본이 아니라 초안이라는 사실이 타입에 박혀 있다.
    """

    @abstractmethod
    async def summarize(self, call_id: str, segments: list[TranscriptEvent]) -> CallSummaryDraft: ...
