# Requirement: E-1
"""POST /hub/cards/{card_id}/feedback — 추천 카드 채택·무시 기록."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from hub.adapter.inbound.api.schemas.card_feedback_schema import (
    CardFeedbackRequest,
    CardFeedbackResponse,
)
from hub.app.dtos.card_feedback_dto import CardFeedback
from hub.app.ports.input.card_feedback_use_case import CardFeedbackUseCase
from hub.dependencies.card_feedback_provider import get_card_feedback_use_case

card_feedback_router = APIRouter(prefix="/hub", tags=["hub"])


@card_feedback_router.post(
    "/cards/{card_id}/feedback", response_model=CardFeedbackResponse, status_code=status.HTTP_201_CREATED
)
async def record_card_feedback(
    card_id: int,
    body: CardFeedbackRequest,
    use_case: CardFeedbackUseCase = Depends(get_card_feedback_use_case),
) -> CardFeedbackResponse:
    try:
        receipt = await use_case.record(CardFeedback(card_id=card_id, action=body.action))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc

    return CardFeedbackResponse(
        feedback_id=receipt.feedback_id, card_id=receipt.card_id, action=receipt.action
    )
