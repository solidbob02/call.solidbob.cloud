# Requirement: D-4
"""KnowledgeGapPort 의 MySQL 구현. `status` 는 접수 시점에 항상 `open` 이다 —
닫는 것은 지식베이스를 보강한 뒤의 일이라 여기서 정하지 않는다."""

from __future__ import annotations

from datetime import datetime, timezone

from hub.app.dtos.knowledge_gap_dto import KnowledgeGapReport
from hub.app.ports.output.knowledge_gap_port import KnowledgeGapPort

from .connection import ConnectionFactory

_INSERT = """
INSERT INTO `knowledge_gap`
    (`module`, `description`, `call_id`, `segment_id`, `closure_id`, `created_at`, `status`)
VALUES (%s, %s, %s, %s, %s, %s, 'open')
"""


class MySqlKnowledgeGapRepository(KnowledgeGapPort):
    def __init__(self, connect: ConnectionFactory) -> None:
        self._connect = connect

    async def save(self, report: KnowledgeGapReport) -> int:
        async with self._connect() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    _INSERT,
                    (
                        report.module,
                        report.description,
                        report.call_id,
                        report.segment_id,
                        report.closure_id,
                        datetime.now(timezone.utc),
                    ),
                )
                gap_id = cur.lastrowid
            await conn.commit()
        return int(gap_id)
