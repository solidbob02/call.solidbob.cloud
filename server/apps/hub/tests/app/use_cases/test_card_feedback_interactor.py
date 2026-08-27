# Requirement: E-1, QUA-1
"""스텁 포트로 배선 검증. 집계는 ai/(평가 하네스) 몫이라 여기서 하지 않는다."""

import asyncio

import pytest

from hub.app.dtos.card_feedback_dto import CardFeedback
from hub.app.ports.output import CardFeedbackPort
from hub.app.use_cases.card_feedback_interactor import CardFeedbackInteractor


class _Spy(CardFeedbackPort):
    def __init__(self):
        self.appended = []

    async def append(self, feedback):
        self.appended.append(feedback)
        return 100 + len(self.appended)


def _run(port, card_id=42, action="adopted"):
    return asyncio.run(CardFeedbackInteractor(feedback_port=port).record(
        CardFeedback(card_id=card_id, action=action)))


@pytest.mark.parametrize("action", ["adopted", "ignored"])
def test_두_반응을_모두_기록한다(action):
    port = _Spy()
    receipt = _run(port, action=action)
    assert port.appended[0].action == action
    assert receipt.action == action


def test_같은_카드에_여러_번_붙을_수_있다():
    """채택 → 취소 같은 변경 이력이 남아야 한다 — append-only."""
    port = _Spy()
    _run(port, action="adopted")
    _run(port, action="ignored")
    assert [f.action for f in port.appended] == ["adopted", "ignored"]


def test_접수_id를_돌려준다():
    assert _run(_Spy()).feedback_id == 101


@pytest.mark.parametrize("card_id", [0, -1])
def test_잘못된_card_id는_거부한다(card_id):
    port = _Spy()
    with pytest.raises(ValueError):
        _run(port, card_id=card_id)
    assert port.appended == []


def test_상담원_식별자를_받지_않는다():
    """부록 A-1 — 상담원 단위로 집계해 점수·순위를 만들 수 없게 한다. 받지 않으면 만들 수도 없다."""
    fields = CardFeedback.__dataclass_fields__
    assert set(fields) == {"card_id", "action"}
    assert "agent_id" not in fields
