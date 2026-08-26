# Requirement: SEC-1
"""임시 로그 구현. 마스킹 후 이벤트만 받으므로 로그에 원문이 실릴 경로가 없다. 3주차에 MySQL 어댑터로 교체."""

from __future__ import annotations

import logging

from hub.app.dtos.transcript_dto import TranscriptEvent
from hub.app.ports.output.transcript_ingest_record_port import TranscriptIngestRecordPort

logger = logging.getLogger(__name__)


class LogTranscriptIngestRecordAdapter(TranscriptIngestRecordPort):
    def record(self, event: TranscriptEvent) -> None:
        logger.info(
            "transcript ingested call_id=%s segment_id=%s speaker=%s is_final=%s masked=%d",
            event.call_id, event.segment_id, event.speaker, event.is_final, len(event.masked),
        )
