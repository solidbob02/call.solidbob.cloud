# Requirement: 7.3절 전사 이벤트, C-5, SEC-1, QUA-1
"""가짜 커넥션으로 리포지토리를 검증한다 — 실제 MySQL 없이 SEC-1 과 interim 규칙을 고정한다.

진짜 DB 를 쓰는 검증은 @pytest.mark.integration 으로 따로 둔다(기본 실행에서 빠진다).
"""

import asyncio
from contextlib import asynccontextmanager

from hub.adapter.outbound.mysql.transcript_segment_repository import MySqlTranscriptSegmentRepository
from hub.app.dtos import MaskedSpan, TranscriptEvent

RAW = "제 번호는 01012345678 입니다"
MASKED = "제 번호는 *********** 입니다"


class _FakeCursor:
    def __init__(self, log: list):
        self._log = log

    async def execute(self, sql, args=None):
        self._log.append(("execute", " ".join(sql.split())[:40], args))

    async def executemany(self, sql, args):
        self._log.append(("executemany", " ".join(sql.split())[:40], args))


class _FakeConnection:
    def __init__(self, log: list):
        self._log = log
        self.committed = False

    @asynccontextmanager
    async def cursor(self):
        yield _FakeCursor(self._log)

    async def commit(self):
        self.committed = True
        self._log.append(("commit", "", None))


def _factory(log: list, holder: list):
    @asynccontextmanager
    async def _connect():
        conn = _FakeConnection(log)
        holder.append(conn)
        yield conn

    return _connect


def _record(event: TranscriptEvent):
    log, holder = [], []
    repo = MySqlTranscriptSegmentRepository(_factory(log, holder))
    asyncio.run(repo.record(event))
    return log, holder


def _final(**kw) -> TranscriptEvent:
    base = dict(call_id="c_001", segment_id=31, speaker="customer", text=MASKED,
                is_final=True, utterance_end_ms=2600,
                masked=(MaskedSpan(type="P4", span=(6, 17)),))
    return TranscriptEvent(**{**base, **kw})


def test_interim은_저장하지_않는다():
    """7.3절: DB 에는 is_final=true 만 저장한다. 20초에 199건(V4 실측)이 그대로 쌓이면 안 된다."""
    log, holder = _record(_final(is_final=False))
    assert log == []
    assert holder == []  # 커넥션조차 열지 않는다


def test_확정본은_저장하고_커밋한다():
    log, holder = _record(_final())
    kinds = [k for k, _, _ in log]
    assert kinds == ["execute", "execute", "executemany", "commit"]
    assert holder[0].committed is True


def test_마스킹된_텍스트만_넘긴다():
    """SEC-1 — 원문이 쿼리 인자 어디에도 없어야 한다."""
    log, _ = _record(_final())
    flat = repr(log)
    assert MASKED in flat
    assert RAW not in flat
    assert "01012345678" not in flat


def test_마스킹_구간을_다시_넣기_전에_지운다():
    """같은 segment 를 다시 받으면 이전 구간이 남아 새 마스킹과 섞인다."""
    log, _ = _record(_final())
    delete = [row for row in log if "DELETE FROM masking_event" in row[1]]
    assert len(delete) == 1
    assert delete[0][2] == (31,)


def test_마스킹_구간이_없으면_insert하지_않는다():
    log, _ = _record(_final(masked=()))
    assert not any(k == "executemany" for k, _, _ in log)


def test_구간은_문자_오프셋_그대로_저장한다():
    """7.3절: span 은 문자(코드포인트) 오프셋이다. byte 로 바꾸면 한글에서 프론트와 어긋난다."""
    log, _ = _record(_final())
    spans = [row for row in log if row[0] == "executemany"][0][2]
    assert spans[0][1:4] == ("P4", 6, 17)


# ── 실제 MySQL 이 필요한 검증 (기본 실행에서 제외 — pytest.ini addopts) ────────────────

import pytest  # noqa: E402


@pytest.mark.integration
def test_실제_DB에_원문이_남지_않는다():
    """SEC-1 최종 확인 — 스키마 리뷰가 아니라 실제 저장 결과로 본다.

    전제: MySQL 이 떠 있고 db/schema.sql 이 적용돼 있어야 한다(2026-08-27 기준 마이그레이션 미착수).
    실행: cd server && pytest -m integration
    """
    pytest.skip("MySQL 마이그레이션 미착수 — db/schema.sql 적용 후 활성화한다")
