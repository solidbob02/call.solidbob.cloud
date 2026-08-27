# Requirement: F-2
"""ClosureGatePort 프로바이더. 스포크가 없으면 501 — **절대 통과시키지 않는다**.

F-2 는 "필수 근거 미기재 시 종결 100% 차단"이 절대 규칙이다. 게이트가 없는 상태를 approved 로
돌려주면 차단해야 할 건을 통과시키는 것이고, 그건 F-2 를 만들지 않은 것보다 나쁘다 —
화면에는 검증을 통과한 것처럼 보이기 때문이다.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status

from hub.app.ports.input.closure_check_use_case import ClosureCheckUseCase
from hub.app.ports.output.closure_gate_port import ClosureGatePort
from hub.app.use_cases.closure_check_interactor import ClosureCheckInteractor


def get_closure_gate_port() -> ClosureGatePort:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="closure_gate 스포크가 등록되지 않았습니다 — 검증 없이 종결을 통과시키지 않습니다 (F-2)",
    )


def get_closure_check_use_case(
    closure_gate: ClosureGatePort = Depends(get_closure_gate_port),
) -> ClosureCheckUseCase:
    return ClosureCheckInteractor(closure_gate=closure_gate)
