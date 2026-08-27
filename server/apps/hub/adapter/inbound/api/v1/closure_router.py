# Requirement: F-2
"""POST /hub/closure-checks — 종결 요건 검증. 스키마 ↔ DTO 변환은 여기서만 한다.

스포크가 없으면 501 이다. 검증 없이 종결을 통과시키지 않는다 — 절대 규칙.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hub.adapter.inbound.api.schemas.closure_schema import ClosureCheckRequest, ClosureVerdictResponse
from hub.adapter.inbound.api.schemas.recommendation_schema import SourceSchema
from hub.app.dtos.closure_dto import ClosureCheckCommand
from hub.app.ports.input.closure_check_use_case import ClosureCheckUseCase
from hub.dependencies.closure_provider import get_closure_check_use_case

closure_router = APIRouter(prefix="/hub", tags=["hub"])


@closure_router.post("/closure-checks", response_model=ClosureVerdictResponse)
async def check_closure(
    body: ClosureCheckRequest,
    use_case: ClosureCheckUseCase = Depends(get_closure_check_use_case),
) -> ClosureVerdictResponse:
    try:
        verdict = await use_case.check(
            ClosureCheckCommand(
                call_id=body.call_id,
                closure_type=body.closure_type,
                evidence=body.evidence,
                reason=body.reason,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    return ClosureVerdictResponse(
        call_id=verdict.call_id,
        closure_type=verdict.closure_type,
        evidence=verdict.evidence,
        verdict=verdict.verdict,
        missing=list(verdict.missing),
        reason=verdict.reason,
        source=(
            SourceSchema(doc_id=verdict.source.doc_id, title=verdict.source.title)
            if verdict.source
            else None
        ),
    )
