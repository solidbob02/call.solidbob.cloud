# Requirement: C-1, C-2, C-3, C-4
from __future__ import annotations

from dataclasses import dataclass

from .compliance_finding_dto import ComplianceFinding


@dataclass(frozen=True)
class ComplianceCheckCommand:
    """컴플라이언스 검사 입력. **상담원 발화만** 받는다.

    고객 발화는 검사하지 않는다 — C-1~C-4 는 상담원이 하지 말아야 할 말을 잡는 규칙이고,
    고객이 한 말을 위반으로 잡으면 화면에 고객을 탓하는 경고가 뜬다.
    """

    call_id: str
    segment_id: int
    agent_utterance: str


@dataclass(frozen=True)
class ComplianceCheckResult:
    """검사 결과. `findings` 가 비어 있으면 **"잡힌 것이 없다"**이지 "안전하다"가 아니다.

    부록 A-1 이 금지한 것이 바로 그 비약이다 — 화면·로그·응답 어디에도 "안전합니다" 류
    단정을 만들지 않는다. 재현율 0.90 목표라는 것은 10건 중 1건은 놓친다는 뜻이다.
    """

    call_id: str
    segment_id: int
    findings: tuple[ComplianceFinding, ...] = ()

    @property
    def has_findings(self) -> bool:
        return bool(self.findings)
