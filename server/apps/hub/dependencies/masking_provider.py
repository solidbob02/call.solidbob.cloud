# Requirement: C-5
"""MaskingPort 프로바이더. masking 스포크가 아직 없으므로 기본은 501 — 마스킹 없이 원문을 흘려보내는
'임시 통과' 구현은 만들지 않는다 (SEC-1: 그 경로가 생기는 순간 원문이 새는 길이 된다).
masking 스포크가 생기면 main.py 에서 `app.dependency_overrides[get_masking_port] = ...` 로 꽂는다."""

from __future__ import annotations

from fastapi import HTTPException, status

from hub.app.ports.output.masking_port import MaskingPort


def get_masking_port() -> MaskingPort:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="masking 스포크가 등록되지 않았습니다 — 마스킹 없이는 전사를 받지 않습니다 (C-5/SEC-1)",
    )
