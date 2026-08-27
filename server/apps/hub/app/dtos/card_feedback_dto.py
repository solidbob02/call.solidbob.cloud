# Requirement: E-1
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# db `card_feedback.action` ENUM 과 같다.
FeedbackAction = Literal["adopted", "ignored"]


@dataclass(frozen=True)
class CardFeedback:
    """카드 하나에 대한 상담원 반응 1건.

    **카드 품질을 재는 데이터다.** 상담원 단위로 집계해 점수·순위를 만들지 않는다(부록 A-1) —
    같은 데이터로 사람을 줄 세우는 것은 다른 일이고, Cresta 식 실시간 코칭 점수는 금지 범위다.
    그래서 `agent_id` 를 받지 않는다 — 받지 않으면 만들 수도 없다.
    """

    card_id: int
    action: FeedbackAction


@dataclass(frozen=True)
class CardFeedbackReceipt:
    feedback_id: int
    card_id: int
    action: FeedbackAction
