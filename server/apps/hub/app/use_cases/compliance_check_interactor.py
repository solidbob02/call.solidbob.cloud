# Requirement: C-1, C-2, C-3, C-4
"""컴플라이언스 검사 인터랙터. CompliancePort 를 부르고 결과를 감싸는 것이 전부다.

**여기서 하지 않는 것**:
- 발견 건수로 등급·점수를 만들지 않는다 (부록 A-1 — "위험도 78%" 금지).
- 애매한 건을 걸러내지 않는다. 재현율 우선이라 판단은 스포크가 하고 허브는 나른다.
- 고객 발화를 검사하지 않는다 — 커맨드가 `agent_utterance` 만 받는 이유다.
"""

from __future__ import annotations

from hub.app.dtos.compliance_dto import ComplianceCheckCommand, ComplianceCheckResult
from hub.app.ports.input.compliance_check_use_case import ComplianceCheckUseCase
from hub.app.ports.output.compliance_port import CompliancePort


class ComplianceCheckInteractor(ComplianceCheckUseCase):
    def __init__(self, compliance: CompliancePort) -> None:
        self._compliance = compliance

    async def check(self, command: ComplianceCheckCommand) -> ComplianceCheckResult:
        utterance = command.agent_utterance.strip()
        if not utterance:
            raise ValueError("상담원 발화가 비어 있습니다")

        findings = await self._compliance.detect(utterance)
        return ComplianceCheckResult(
            call_id=command.call_id,
            segment_id=command.segment_id,
            findings=tuple(findings),
        )
