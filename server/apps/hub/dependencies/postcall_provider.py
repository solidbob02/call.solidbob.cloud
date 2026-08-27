# Requirement: D-1, D-2, D-3
"""PostcallPort 프로바이더. 스포크가 없으면 501 — 빈 요약을 만들지 않는다.

빈 문자열이나 "요약 없음"을 돌려주면 화면에는 **요약이 생성됐는데 내용이 없는 것**으로 보인다.
모듈이 없는 상태와 구분되지 않아 D-1 이 도는지조차 알 수 없게 된다(절대 원칙 10).
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status

from hub.app.ports.input.postcall_use_case import PostcallUseCase
from hub.app.ports.output.postcall_port import PostcallPort
from hub.app.use_cases.postcall_interactor import PostcallInteractor


def get_postcall_port() -> PostcallPort:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="postcall 스포크가 등록되지 않았습니다 (D-1~D-3)",
    )


def get_postcall_use_case(postcall: PostcallPort = Depends(get_postcall_port)) -> PostcallUseCase:
    return PostcallInteractor(postcall=postcall)
