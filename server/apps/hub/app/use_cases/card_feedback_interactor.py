# Requirement: E-1
"""카드 피드백 인터랙터. 검증하고 append 하는 것이 전부다.

**집계하지 않는다.** 채택률·순위 계산은 `ai/`(평가 하네스) 몫이고, 여기서 하면
[부록 A-1](/docs/12/)이 금지한 점수가 허브에서 만들어진다.
"""

from __future__ import annotations

from hub.app.dtos.card_feedback_dto import CardFeedback, CardFeedbackReceipt
from hub.app.ports.input.card_feedback_use_case import CardFeedbackUseCase
from hub.app.ports.output.card_feedback_port import CardFeedbackPort


class CardFeedbackInteractor(CardFeedbackUseCase):
    def __init__(self, feedback_port: CardFeedbackPort) -> None:
        self._feedback = feedback_port

    async def record(self, feedback: CardFeedback) -> CardFeedbackReceipt:
        if feedback.card_id <= 0:
            raise ValueError(f"card_id 가 올바르지 않습니다: {feedback.card_id}")

        feedback_id = await self._feedback.append(feedback)
        return CardFeedbackReceipt(
            feedback_id=feedback_id, card_id=feedback.card_id, action=feedback.action
        )
