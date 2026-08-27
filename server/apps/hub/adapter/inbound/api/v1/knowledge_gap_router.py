# Requirement: D-4
"""POST /hub/knowledge-gaps — 「이 답을 못 찾았다」 신고 수집."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hub.adapter.inbound.api.schemas.knowledge_gap_schema import (
    KnowledgeGapRequest,
    KnowledgeGapResponse,
)
from hub.app.dtos.knowledge_gap_dto import KnowledgeGapReport
from hub.app.ports.input.knowledge_gap_use_case import KnowledgeGapUseCase
from hub.dependencies.knowledge_gap_provider import get_knowledge_gap_use_case

knowledge_gap_router = APIRouter(prefix="/hub", tags=["hub"])


@knowledge_gap_router.post(
    "/knowledge-gaps", response_model=KnowledgeGapResponse, status_code=status.HTTP_201_CREATED
)
async def report_knowledge_gap(
    body: KnowledgeGapRequest,
    use_case: KnowledgeGapUseCase = Depends(get_knowledge_gap_use_case),
) -> KnowledgeGapResponse:
    try:
        receipt = await use_case.report(
            KnowledgeGapReport(
                module=body.module,
                description=body.description,
                call_id=body.call_id,
                segment_id=body.segment_id,
                closure_id=body.closure_id,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc

    return KnowledgeGapResponse(gap_id=receipt.gap_id, module=receipt.module)
