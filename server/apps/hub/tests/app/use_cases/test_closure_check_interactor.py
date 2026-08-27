# Requirement: F-2, QUA-1
"""스텁 포트로 배선만 검증. 판정 규칙은 closure_gate 스포크의 domain/services 가 소유한다."""

import asyncio

import pytest

from hub.app.dtos import ClosureVerdict
from hub.app.dtos.closure_dto import ClosureCheckCommand
from hub.app.ports.output import ClosureGatePort
from hub.app.use_cases.closure_check_interactor import ClosureCheckInteractor

EVIDENCE = {"중도해지수수료_안내": True, "약정혜택소멸_안내": False, "고객확인_기록": False}


class _Spy(ClosureGatePort):
    def __init__(self):
        self.calls = []

    def evaluate(self, call_id, closure_type, evidence, reason=None):
        self.calls.append((call_id, closure_type, dict(evidence), reason))
        missing = tuple(k for k, v in evidence.items() if not v)
        return ClosureVerdict(call_id=call_id, closure_type=closure_type, evidence=dict(evidence),
                              verdict="blocked" if missing else "approved", missing=missing, reason=reason)


def _run(port, evidence=None, closure_type="상품해지"):
    cmd = ClosureCheckCommand(call_id="c_001", closure_type=closure_type,
                              evidence=EVIDENCE if evidence is None else evidence, reason="고지 완료")
    return asyncio.run(ClosureCheckInteractor(closure_gate=port).check(cmd))


def test_포트에_그대로_넘긴다():
    port = _Spy()
    _run(port)
    call_id, ctype, evidence, reason = port.calls[0]
    assert (call_id, ctype, reason) == ("c_001", "상품해지", "고지 완료")
    assert evidence == EVIDENCE


def test_허브가_판정하지_않는다():
    """evidence 를 보고 스스로 approved/blocked 를 정하지 않는다 — 규칙표는 스포크가 갖는다."""
    verdict = _run(_Spy())
    assert verdict.verdict == "blocked"
    assert set(verdict.missing) == {"약정혜택소멸_안내", "고객확인_기록"}


def test_전부_충족이면_승인이_그대로_나온다():
    verdict = _run(_Spy(), {"중도해지수수료_안내": True, "고객확인_기록": True})
    assert verdict.verdict == "approved" and verdict.missing == ()


def test_빈_근거는_거부한다():
    """빈 근거로 통과시키면 필수 근거 미기재를 승인하는 셈이다 — 절대 규칙 위반."""
    port = _Spy()
    with pytest.raises(ValueError):
        _run(port, {})
    assert port.calls == []


def test_처리유형이_비면_거부한다():
    port = _Spy()
    with pytest.raises(ValueError):
        _run(port, closure_type="")
    assert port.calls == []


def test_evidence를_복사해_넘긴다():
    """호출 후 원본을 바꿔도 스포크가 받은 값이 흔들리지 않는다."""
    port = _Spy()
    evidence = {"고객확인_기록": True}
    asyncio.run(ClosureCheckInteractor(closure_gate=port).check(
        ClosureCheckCommand(call_id="c", closure_type="반품", evidence=evidence)))
    evidence["고객확인_기록"] = False
    assert port.calls[0][2] == {"고객확인_기록": True}
