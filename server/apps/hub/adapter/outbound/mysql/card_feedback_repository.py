# Requirement: E-1
"""CardFeedbackPort 의 MySQL 구현. append-only — UPDATE 하지 않는다."""

from __future__ import annotations

from datetime import datetime, timezone

from hub.app.dtos.card_feedback_dto import CardFeedback
from hub.app.ports.output.card_feedback_port import CardFeedbackPort

from .connection import ConnectionFactory

_INSERT = """
INSERT INTO `card_feedback` (`card_id`, `action`, `created_at`)
VALUES (%s, %s, %s)
"""


class MySqlCardFeedbackRepository(CardFeedbackPort):
    def __init__(self, connect: ConnectionFactory) -> None:
        self._connect = connect

    async def append(self, feedback: CardFeedback) -> int:
        async with self._connect() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    _INSERT, (feedback.card_id, feedback.action, datetime.now(timezone.utc))
                )
                feedback_id = cur.lastrowid
            await conn.commit()
        return int(feedback_id)
