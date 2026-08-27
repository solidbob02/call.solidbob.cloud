# Requirement: F-2, QUA-1
"""HTTP 표면. 2026-08-27 부터 실제 게이트(closure_gate 스포크)가 기본으로 붙어 있다.

그 전에는 501 을 확인하는 테스트였다 — 스포크가 없을 때 통과시키지 않는 것이 절대 규칙이라서다.
이제 구현이 있으므로 **기본 배선으로 실제 판정이 나오는지**를 본다. 지키려는 성질은 그대로다:
**근거가 미충족이면 어떤 경로로도 `approved` 가 나오지 않는다.**
"""

from fastapi.testclient import TestClient

from hub.app.dtos import ClosureVerdict
from hub.app.ports.output import ClosureGatePort
from hub.dependencies.closure_provider import get_closure_gate_port
from main import app

BODY = {"call_id": "c_001", "closure_type": "상품해지",
        "evidence": {"중도해지수수료_안내": True, "약정혜택소멸_안내": False}, "reason": "고지 완료"}


class _Stub(ClosureGatePort):
    def evaluate(self, call_id, closure_type, evidence, reason=None):
        missing = tuple(k for k, v in evidence.items() if not v)
        return ClosureVerdict(call_id=call_id, closure_type=closure_type, evidence=dict(evidence),
                              verdict="blocked" if missing else "approved", missing=missing, reason=reason)


def test_기본_배선으로_실제_게이트가_판정한다():
    """스텁 없이 — `main.py` 가 조립한 그대로. 미충족 근거는 `approved` 가 될 수 없다."""
    with TestClient(app) as client:
        r = client.post("/hub/closure-checks", json=BODY)
    assert r.status_code == 200
    body = r.json()
    assert body["verdict"] == "blocked"
    assert "approved" not in r.text
    # 규칙표에 있는 세 필드 중 요청이 채우지 못한 둘. 키가 빠진 것도 미충족이다.
    assert body["missing"] == ["약정혜택소멸_안내", "고객확인_기록"]
    assert body["source"]["doc_id"] == "FIN-POLICY-CLOSE-1"


def test_규칙표에_없는_처리유형은_판정하지_않고_422다():
    """`approved` 는 절대 규칙 위반이고 `blocked` 도 거짓말이다 — 판정할 규칙이 없는 것이지
    근거가 빠진 것이 아니다. F-2 미적용 도메인(다산·질병관리본부)은 이 경로를 부르지 않는다."""
    with TestClient(app) as client:
        r = client.post("/hub/closure-checks", json={**BODY, "closure_type": "민원접수"})
    assert r.status_code == 422
    assert "approved" not in r.text


def test_미충족이면_blocked와_missing을_돌려준다():
    app.dependency_overrides[get_closure_gate_port] = lambda: _Stub()
    try:
        with TestClient(app) as client:
            r = client.post("/hub/closure-checks", json=BODY)
        b = r.json()
        assert b["verdict"] == "blocked"
        assert b["missing"] == ["약정혜택소멸_안내"]
    finally:
        app.dependency_overrides.clear()


def test_전부_충족이면_approved다():
    app.dependency_overrides[get_closure_gate_port] = lambda: _Stub()
    try:
        with TestClient(app) as client:
            r = client.post("/hub/closure-checks",
                            json={**BODY, "evidence": {"중도해지수수료_안내": True}})
        b = r.json()
        assert b["verdict"] == "approved" and b["missing"] == []
    finally:
        app.dependency_overrides.clear()


def test_빈_근거는_422다():
    app.dependency_overrides[get_closure_gate_port] = lambda: _Stub()
    try:
        with TestClient(app) as client:
            r = client.post("/hub/closure-checks", json={**BODY, "evidence": {}})
        assert r.status_code == 422
    finally:
        app.dependency_overrides.clear()
