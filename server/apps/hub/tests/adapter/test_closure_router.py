# Requirement: F-2, QUA-1
"""HTTP 표면: 스포크가 없으면 501 — 검증 없이 종결을 통과시키지 않는다 (절대 규칙)."""

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


def test_스포크가_없으면_501이고_통과시키지_않는다():
    with TestClient(app) as client:
        r = client.post("/hub/closure-checks", json=BODY)
    assert r.status_code == 501
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
