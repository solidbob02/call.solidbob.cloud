# Requirement: 부록 A-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.myself_dto import MyselfQuery


class MyselfRecordPort(ABC):
    """자기소개 조회 활동 기록 (누가 언제 물었는지). 지금은 로그 어댑터."""

    @abstractmethod
    async def record(self, query: MyselfQuery) -> None: ...
