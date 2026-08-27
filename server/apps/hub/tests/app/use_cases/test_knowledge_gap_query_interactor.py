# Requirement: D-4, QUA-1
"""공백 리포트 조회 인터랙터. **판정하지 않고 세고 나른다**는 것을 고정한다.

async 는 `asyncio.run` 으로 돈다 — 이 저장소는 `pytest-asyncio` 를 쓰지 않는다.
"""

import asyncio

from datetime import datetime, timezone

import pytest

from hub.app.dtos.knowledge_gap_query_dto import (
    MAX_LIMIT,
    GapCount,
    GapResolution,
    KnowledgeGapQuery,
    KnowledgeGapRecord,
)
from hub.app.ports.output.knowledge_gap_query_port import KnowledgeGapQueryPort
from hub.app.use_cases.knowledge_gap_query_interactor import KnowledgeGapQueryInteractor

NOW = datetime(2026, 8, 27, tzinfo=timezone.utc)


def _record(gap_id: int, module: str = "B", status: str = "open") -> KnowledgeGapRecord:
    return KnowledgeGapRecord(gap_id=gap_id, module=module, description=f"신고 {gap_id}",
                              status=status, created_at=NOW)


class _Fake(KnowledgeGapQueryPort):
    def __init__(self, records=(), total=0, by_module=(), by_domain=(), moved=True):
        self.records, self.total = list(records), total
        self.by_module, self.by_domain, self.moved = list(by_module), list(by_domain), moved
        self.seen: list = []

    async def list_gaps(self, query): self.seen.append(query); return self.records
    async def count_gaps(self, query): return self.total
    async def count_by_module(self): return self.by_module
    async def count_by_domain(self): return self.by_domain
    async def update_status(self, gap_id, status): self.seen.append((gap_id, status)); return self.moved


def test_필터를_그대로_포트에_넘긴다():
    """인터랙터가 조건을 다시 해석하지 않는다 — 해석이 두 곳에 생긴다."""
    fake = _Fake(records=[_record(1)], total=1)
    q = KnowledgeGapQuery(module="B", status="open", limit=10, offset=20)
    page = asyncio.run(KnowledgeGapQueryInteractor(fake).list_gaps(q))
    assert fake.seen[0] == q
    assert page.total == 1 and page.limit == 10 and page.offset == 20


def test_신고를_묶거나_걸러내지_않는다():
    """중복이든 애매하든 그대로 보여준다 — 무엇이 같은 공백인지는 `ai/` 가 판단한다.
    입구에서 거르지 않기로 한 것과 같은 이유다: 거르면 그 판단의 재료가 사라진다."""
    same = [_record(1), _record(2), _record(3)]   # 설명이 사실상 같은 신고 3건
    page = asyncio.run(
        KnowledgeGapQueryInteractor(_Fake(records=same, total=3)).list_gaps(KnowledgeGapQuery()))
    assert len(page.gaps) == 3


@pytest.mark.parametrize("query", [
    KnowledgeGapQuery(limit=0),
    KnowledgeGapQuery(limit=MAX_LIMIT + 1),
    KnowledgeGapQuery(offset=-1),
    KnowledgeGapQuery(module="Z"),
    KnowledgeGapQuery(status="닫힘"),
])
def test_잘못된_조건은_거절한다(query):
    with pytest.raises(ValueError):
        asyncio.run(KnowledgeGapQueryInteractor(_Fake()).list_gaps(query))


def test_총계는_모듈_축에서만_센다():
    """도메인 축은 통화가 없는 신고(call_id 가 null)를 놓친다 —
    두 축의 합이 다를 수 있으므로 **다른 값을 같은 이름으로 쓰지 않는다.**"""
    fake = _Fake(
        by_module=[GapCount("B", open=3, resolved=1), GapCount("C", open=2)],   # 6건
        by_domain=[GapCount("finance", open=2, resolved=1)],                    # 3건만 연결됨
    )
    summary = asyncio.run(KnowledgeGapQueryInteractor(fake).summarize())
    assert summary.total == 6
    assert sum(c.total for c in summary.by_domain) == 3


def test_요약에_우선순위나_심각도가_없다():
    """부록 A-1 — 건수가 많다는 사실과 그것이 중요하다는 판단은 다르다."""
    summary = asyncio.run(KnowledgeGapQueryInteractor(_Fake(by_module=[GapCount("B", open=1)])).summarize())
    fields = set(vars(summary))
    assert not fields & {"priority", "severity", "risk", "score", "우선순위"}


def test_상태를_되돌릴_수_있다():
    """보강했다고 눌렀는데 아니었던 경우를 기록에서 지우지 않고 되돌린다."""
    fake = _Fake()
    assert asyncio.run(KnowledgeGapQueryInteractor(fake).resolve(GapResolution(7, "open"))) is True
    assert fake.seen[0] == (7, "open")


def test_없는_신고는_옮겼다고_하지_않는다():
    moved = asyncio.run(KnowledgeGapQueryInteractor(_Fake(moved=False)).resolve(GapResolution(999, "resolved")))
    assert moved is False


def test_모르는_상태로는_옮기지_않는다():
    with pytest.raises(ValueError):
        asyncio.run(KnowledgeGapQueryInteractor(_Fake()).resolve(GapResolution(1, "보류")))
