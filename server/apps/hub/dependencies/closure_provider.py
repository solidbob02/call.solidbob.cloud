# Requirement: F-2
"""ClosureGatePort 프로바이더. 2026-08-27 부터 규칙 기반 게이트가 기본이다.

그 전까지는 501 이었다 — 게이트가 없는 상태를 `approved` 로 돌려주면 차단해야 할 건을
통과시키는 것이고, 그건 F-2 를 만들지 않은 것보다 나쁘다(화면에는 검증을 통과한 것처럼
보인다). 이제 실제 구현이 있으므로 501 이 아니다.

**판정 규칙표는 도메인별 내부처리규정(`*-POLICY-*`)이 소유한다.** 이 프로바이더도,
허브도 어떤 키가 필수인지 모른다 — 여기서 알면 규칙이 두 곳에 생긴다.
"""

from __future__ import annotations

from closure_gate.adapter.outbound.rule_closure_gate_adapter import RuleClosureGateAdapter
from fastapi import Depends

from hub.app.ports.input.closure_check_use_case import ClosureCheckUseCase
from hub.app.ports.output.closure_gate_port import ClosureGatePort
from hub.app.use_cases.closure_check_interactor import ClosureCheckInteractor


def get_closure_gate_port() -> ClosureGatePort:
    return RuleClosureGateAdapter()


def get_closure_check_use_case(
    closure_gate: ClosureGatePort = Depends(get_closure_gate_port),
) -> ClosureCheckUseCase:
    return ClosureCheckInteractor(closure_gate=closure_gate)
