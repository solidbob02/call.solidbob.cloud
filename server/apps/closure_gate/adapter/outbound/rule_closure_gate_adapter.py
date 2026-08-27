# Requirement: F-2
"""ClosureGatePort 구현 — 허브 계약과 closure_gate 도메인을 잇는다.

도메인의 `GateDecision` 을 허브 DTO `ClosureVerdict` 로 옮기는 것이 전부다.
**판정은 도메인이 한다** — 이 어댑터에는 `if evidence[...]` 가 없다(절대 원칙 9).

`reason` 은 상담원이 적어 보낸 종결 사유를 **그대로 나른다.** 게이트가 문장을 만들지 않는다 —
설명을 LLM 이 붙이는 것은 [부록 A-2](/docs/12/)가 허용하지만, 그건 판정 뒤의 별도 단계다.
"""

from __future__ import annotations

from hub.app.dtos.closure_verdict_dto import ClosureType, ClosureVerdict
from hub.app.dtos.recommendation_card_dto import Source
from hub.app.ports.output.closure_gate_port import ClosureGatePort

from ...domain.services.gate import evaluate

# 이 어댑터가 판정할 수 있는 처리유형. 평가 하네스가 "무엇을 못 보는지" 알아야 한다.
from ...domain.value_objects.closure_rule import RULES

SUPPORTED_CLOSURE_TYPES = tuple(RULES)


class RuleClosureGateAdapter(ClosureGatePort):
    def evaluate(
        self,
        call_id: str,
        closure_type: ClosureType,
        evidence: dict[str, bool],
        reason: str | None = None,
    ) -> ClosureVerdict:
        decision = evaluate(closure_type, evidence)
        return ClosureVerdict(
            call_id=call_id,
            closure_type=closure_type,
            evidence=dict(evidence),
            verdict=decision.verdict,
            missing=decision.missing,
            reason=reason,
            source=Source(
                doc_id=decision.rule.source_doc_id,
                title=decision.rule.source_title,
            ),
        )
