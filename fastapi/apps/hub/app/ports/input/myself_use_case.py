# Requirement: 부록 A-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.myself_dto import MyselfQuery, MyselfResult


class MyselfUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, query: MyselfQuery) -> MyselfResult: ...
