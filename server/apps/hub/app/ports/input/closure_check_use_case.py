# Requirement: F-2
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.closure_dto import ClosureCheckCommand
from hub.app.dtos.closure_verdict_dto import ClosureVerdict


class ClosureCheckUseCase(ABC):
    """F-2 종결 요건 검증. **필수 근거가 없으면 종결을 100% 차단한다 — 절대 규칙**이다.

    평균·부분 점수가 없다. 1건이라도 어긋나면 실패로 처리한다([6.2절](/docs/06/)).
    판정은 규칙이 하고 허브는 나르기만 한다(절대 원칙 9).
    """

    @abstractmethod
    async def check(self, command: ClosureCheckCommand) -> ClosureVerdict: ...
