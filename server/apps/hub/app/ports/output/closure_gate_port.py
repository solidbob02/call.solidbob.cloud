# Requirement: F-2
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.closure_verdict_dto import ClosureType, ClosureVerdict


class ClosureGatePort(ABC):
    """F-2. 처리유형과 근거 필드로 종결 가능 여부를 판정한다. 규칙 계산 → def.
    ClosureVerdict 가 스스로 verdict/missing 정합성을 검사하므로 구현체가 평균으로 통과시킬 수 없다."""

    @abstractmethod
    def evaluate(
        self, call_id: str, closure_type: ClosureType, evidence: dict[str, bool], reason: str | None = None
    ) -> ClosureVerdict: ...
