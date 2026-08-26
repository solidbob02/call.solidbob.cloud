# Requirement: 부록 A-1, QUA-1

import asyncio

from hub.app.dtos import MyselfQuery
from hub.app.ports.output import MyselfRecordPort
from hub.app.use_cases.myself_interactor import MyselfInteractor

FORBIDDEN_PHRASES = ("안전합니다", "위험도", "완벽히", "불변 감사")  # 부록 A-1 금지 표현


class _SpyRecord(MyselfRecordPort):
    def __init__(self):
        self.queries = []

    async def record(self, query: MyselfQuery) -> None:
        self.queries.append(query)


def test_myself_states_real_endpoints_and_limits_without_forbidden_phrases():
    record = _SpyRecord()
    result = asyncio.run(MyselfInteractor(record).introduce_myself(MyselfQuery(name="허브 (hub)")))
    assert record.queries == [MyselfQuery(name="허브 (hub)")]
    assert any("/hub/transcripts" in e for e in result.endpoints)
    assert result.does_not  # 하지 않는 것을 반드시 말한다
    text = " ".join((result.introduction, *result.endpoints, *result.does_not))
    assert not any(p in text for p in FORBIDDEN_PHRASES)
