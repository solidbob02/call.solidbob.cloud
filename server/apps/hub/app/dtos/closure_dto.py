# Requirement: F-2
from __future__ import annotations

from dataclasses import dataclass

from .closure_verdict_dto import ClosureType


@dataclass(frozen=True)
class ClosureCheckCommand:
    """종결 요청. `evidence` 는 `closure_type` 별 부분집합만 담는다 (decisions/003 ③).

    허브는 어떤 키가 필수인지 모른다 — 그 규칙표는 도메인별 내부처리규정(`*-POLICY-*`)이 갖고
    closure_gate 스포크가 읽는다. 여기서 키를 검사하면 규칙이 두 곳에 생긴다.
    """

    call_id: str
    closure_type: ClosureType
    evidence: dict[str, bool]
    reason: str | None = None
