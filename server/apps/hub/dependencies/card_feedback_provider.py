# Requirement: E-1, SEC-2
"""CardFeedbackPort 프로바이더. PostgreSQL 이 없으면 501 — 받아놓고 버리지 않는다."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status

from hub.adapter.outbound.postgres.card_feedback_repository import PostgresCardFeedbackRepository
from hub.adapter.outbound.postgres.connection import build_connection_factory
from hub.app.ports.input.card_feedback_use_case import CardFeedbackUseCase
from hub.app.ports.output.card_feedback_port import CardFeedbackPort
from hub.app.use_cases.card_feedback_interactor import CardFeedbackInteractor


def get_card_feedback_port(request: Request) -> CardFeedbackPort:
    settings = request.app.state.settings
    if not settings.postgres_configured:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="PostgreSQL 이 설정되지 않았습니다 — 피드백을 저장할 곳이 없습니다 (infra/README.md)",
        )
    return PostgresCardFeedbackRepository(build_connection_factory(settings))


def get_card_feedback_use_case(
    feedback_port: CardFeedbackPort = Depends(get_card_feedback_port),
) -> CardFeedbackUseCase:
    return CardFeedbackInteractor(feedback_port=feedback_port)
