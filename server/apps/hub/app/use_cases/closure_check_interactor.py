# Requirement: F-2
"""종결 게이트 인터랙터. ClosureGatePort 를 부르는 것이 전부다.

**여기서 절대 하지 않는 것**:
- `evidence` 값을 보고 스스로 approved/blocked 를 정하지 않는다. 그 규칙표는 도메인별
  내부처리규정이 갖고 closure_gate 스포크의 `domain/services` 가 소유한다(architecture.md §2).
- 판정을 생성 모델에 맡기지 않는다(절대 원칙 9). 설명(reason)만 나른다.
- 스포크가 없을 때 "일단 통과"시키지 않는다 — 그 순간 F-2 의 존재 이유가 사라진다.
"""

from __future__ import annotations

from hub.app.dtos.closure_dto import ClosureCheckCommand
from hub.app.dtos.closure_verdict_dto import ClosureVerdict
from hub.app.ports.input.closure_check_use_case import ClosureCheckUseCase
from hub.app.ports.output.closure_gate_port import ClosureGatePort


class ClosureCheckInteractor(ClosureCheckUseCase):
    def __init__(self, closure_gate: ClosureGatePort) -> None:
        self._closure_gate = closure_gate

    async def check(self, command: ClosureCheckCommand) -> ClosureVerdict:
        if not command.closure_type:
            raise ValueError("처리유형이 비어 있습니다")
        if not command.evidence:
            raise ValueError("근거 필드가 비어 있습니다 — 빈 근거로는 종결을 판정할 수 없습니다")

        return self._closure_gate.evaluate(
            call_id=command.call_id,
            closure_type=command.closure_type,
            evidence=dict(command.evidence),
            reason=command.reason,
        )
