# Requirement: E-1
from __future__ import annotations

from abc import ABC, abstractmethod

from hub.app.dtos.card_feedback_dto import CardFeedback, CardFeedbackReceipt


class CardFeedbackUseCase(ABC):
    """추천 카드 채택·무시 기록 (E-1).

    골든셋 Recall@5 와 **별개 신호**다 — 골든셋은 "정답을 찾았는가"를, 이쪽은
    "현장에서 실제로 쓸모 있었는가"를 잰다. 둘이 갈리는 지점이 지식베이스 보강 후보다.
    """

    @abstractmethod
    async def record(self, feedback: CardFeedback) -> CardFeedbackReceipt: ...
