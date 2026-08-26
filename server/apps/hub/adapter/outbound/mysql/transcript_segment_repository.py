# Requirement: 7.3절 전사 이벤트, C-5, SEC-1
"""TranscriptIngestRecordPort 의 MySQL 구현. LogTranscriptIngestRecordAdapter 를 대체한다.

**두 가지를 지킨다.**

1. **SEC-1 — 마스킹 완료본만 저장한다.** 이 어댑터는 `TranscriptEvent` 만 받는데, 그 안의 `text` 는
   이미 MaskingPort 를 거친 것이다. 원문(`TranscriptIngestCommand.raw_text`)은 인터랙터 밖으로
   나오지 않으므로 여기서는 손에 넣을 방법 자체가 없다. `transcript_segment.text` 컬럼 주석과 같은 규칙이다.

2. **interim 은 저장하지 않는다.** [7.3절](/docs/07/)이 정한 규칙 —
   *"DB에는 `is_final: true`만 저장 — interim까지 저장하면 통화 1건에 수천 행이 쌓인다."*
   [V4 실측](/docs/05/)상 20초 발화에 interim 이 199건 온다. 화면은 `segment_id` 로 교체해 보여주고,
   DB 는 확정본만 남긴다.
"""

from __future__ import annotations

from datetime import datetime, timezone

from hub.app.dtos.transcript_dto import TranscriptEvent
from hub.app.ports.output.transcript_ingest_record_port import TranscriptIngestRecordPort

from .connection import ConnectionFactory

_UPSERT_SEGMENT = """
INSERT INTO transcript_segment
    (segment_id, call_id, speaker, text, is_final, utterance_end_ms, created_at)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    text = VALUES(text),
    is_final = VALUES(is_final),
    utterance_end_ms = VALUES(utterance_end_ms)
"""

_DELETE_SPANS = "DELETE FROM masking_event WHERE segment_id = %s"

_INSERT_SPAN = """
INSERT INTO masking_event (segment_id, pattern, span_start, span_end, created_at)
VALUES (%s, %s, %s, %s, %s)
"""


class MySqlTranscriptSegmentRepository(TranscriptIngestRecordPort):
    def __init__(self, connect: ConnectionFactory) -> None:
        self._connect = connect

    async def record(self, event: TranscriptEvent) -> None:
        if not event.is_final:
            return  # interim 은 화면 갱신용 — 저장하지 않는다 (7.3절)

        now = datetime.now(timezone.utc)
        async with self._connect() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    _UPSERT_SEGMENT,
                    (
                        event.segment_id,
                        event.call_id,
                        event.speaker,
                        event.text,  # 마스킹 완료본 (SEC-1)
                        event.is_final,
                        event.utterance_end_ms,
                        now,
                    ),
                )
                # 같은 segment 를 다시 받으면 구간도 갈아끼운다 — 남아 있으면 이전 마스킹과 섞인다
                await cur.execute(_DELETE_SPANS, (event.segment_id,))
                if event.masked:
                    await cur.executemany(
                        _INSERT_SPAN,
                        [(event.segment_id, s.type, s.span[0], s.span[1], now) for s in event.masked],
                    )
            await conn.commit()
