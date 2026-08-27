# Requirement: D-1, D-2, D-3
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.call_summary_dto import CallSummaryDraft
from hub.app.dtos.postcall_dto import PostcallCommand


class PostcallUseCase(ABC):
    """통화 종료 → 요약·유형 제안·후속조치 초안 (D-1~D-3).

    실시간 경로가 아니다 — [4.1절](/docs/04/) p95 ≤1,000ms 는 여기에 걸리지 않는다.
    """

    @abstractmethod
    async def close(self, command: PostcallCommand) -> CallSummaryDraft: ...
