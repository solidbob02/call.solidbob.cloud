# Requirement: E-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.card_feedback_dto import CardFeedback


class CardFeedbackPort(ABC):
    """카드 반응을 append 한다. 갱신하지 않는다 — 채택 후 취소도 이력으로 남아야 한다."""

    @abstractmethod
    async def append(self, feedback: CardFeedback) -> int: ...
