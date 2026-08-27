# Requirement: B-1
"""TriggerPort 프로바이더. 스포크가 없으면 501 — "일단 항상 발동" 같은 임시 구현을 만들지 않는다.

항상 발동시키면 [6.1절](/docs/06/) 트리거 적절 발동률이 측정 대상에서 사라지고, 발동 시각(`at_ms`)이
없어 p50/p95 분포도 못 잰다. 측정할 수 없는 상태를 만들지 않는다(절대 원칙 10).
"""

from __future__ import annotations

from fastapi import HTTPException, status

from hub.app.ports.output.trigger_port import TriggerPort


def get_trigger_port() -> TriggerPort:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="trigger 스포크가 등록되지 않았습니다 (B-1)",
    )
