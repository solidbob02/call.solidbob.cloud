# Requirement: E-1
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class CardFeedbackRequest(BaseModel):
    action: Literal["adopted", "ignored"] = Field(description="상담원이 이 카드를 썼는지")
    # agent_id 를 받지 않는다 — 상담원 단위 집계를 만들 수 없게 하기 위해서다 (부록 A-1)


class CardFeedbackResponse(BaseModel):
    feedback_id: int
    card_id: int
    action: Literal["adopted", "ignored"]
