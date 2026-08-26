# Requirement: 부록 A-1
from __future__ import annotations

import logging

from hub.app.dtos.myself_dto import MyselfQuery
from hub.app.ports.output.myself_record_port import MyselfRecordPort

logger = logging.getLogger(__name__)


class LogMyselfRecordAdapter(MyselfRecordPort):
    async def record(self, query: MyselfQuery) -> None:
        logger.info("myself queried name=%s", query.name)
