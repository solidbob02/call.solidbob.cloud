# Requirement: A-1, SEC-1, QUA-1
"""스텁 포트로 배선·경계 검증. 실제 조회는 integration 테스트가 DB 로 본다."""

import asyncio

import pytest

from hub.app.dtos import MaskedSpan, TranscriptEvent
from hub.app.dtos.transcript_query_dto import MAX_LIMIT, TranscriptQuery
from hub.app.ports.output import TranscriptQueryPort
from hub.app.use_cases.transcript_query_interactor import TranscriptQueryInteractor

SEGMENTS = [
    TranscriptEvent(call_id="c_001", segment_id=1, speaker="customer", text="카드 분실했어요", is_final=True),
    TranscriptEvent(call_id="c_001", segment_id=2, speaker="agent", text="번호는 ***********",
                    is_final=True, masked=(MaskedSpan(type="P4", span=(4, 15)),)),
]


class _Spy(TranscriptQueryPort):
    def __init__(self, segments=None, total=None):
        self.segments = SEGMENTS if segments is None else segments
        self.total = len(self.segments) if total is None else total
        self.calls = []

    async def list_segments(self, call_id, limit, offset):
        self.calls.append((call_id, limit, offset))
        return list(self.segments)

    async def count_segments(self, call_id):
        return self.total


def _run(port, **kw):
    q = TranscriptQuery(call_id=kw.pop("call_id", "c_001"), **kw)
    return asyncio.run(TranscriptQueryInteractor(query_port=port).list(q))


def test_페이지_인자를_포트에_그대로_넘긴다():
    port = _Spy()
    _run(port, limit=50, offset=100)
    assert port.calls == [("c_001", 50, 100)]


def test_기본_limit은_100이다():
    port = _Spy()
    _run(port)
    assert port.calls[0][1] == 100


def test_마스킹_구간을_그대로_싣는다():
    page = _run(_Spy())
    assert page.segments[1].masked[0].type == "P4"
    assert page.segments[1].masked[0].span == (4, 15)


def test_포트가_준_순서를_유지한다():
    """정렬은 리포지토리 몫이다 — 허브가 다시 정렬하면 페이지 경계에서 어긋난다."""
    page = _run(_Spy())
    assert [s.segment_id for s in page.segments] == [1, 2]


def test_전체_건수를_함께_준다():
    page = _run(_Spy(total=199))
    assert page.total == 199


def test_결과가_없어도_예외가_아니다():
    page = _run(_Spy(segments=[], total=0))
    assert page.segments == () and page.total == 0


@pytest.mark.parametrize("limit", [0, -1, MAX_LIMIT + 1])
def test_범위를_벗어난_limit은_거부한다(limit):
    port = _Spy()
    with pytest.raises(ValueError):
        _run(port, limit=limit)
    assert port.calls == []


def test_음수_offset은_거부한다():
    port = _Spy()
    with pytest.raises(ValueError):
        _run(port, offset=-1)
    assert port.calls == []


def test_빈_call_id는_거부한다():
    port = _Spy()
    with pytest.raises(ValueError):
        _run(port, call_id="")
    assert port.calls == []
