# Requirement: 7.3절 전사 이벤트, C-5, SEC-1, QUA-1
"""HTTP 표면: 마스킹 스포크가 없으면 501 (원문 통과 없음), 있으면 계약 형태로 응답."""

from fastapi.testclient import TestClient

from hub.app.dtos import MaskedSpan
from hub.app.ports.output import MaskingPort
from hub.dependencies.masking_provider import get_masking_port
from main import app

BODY = {"call_id": "c_001", "segment_id": 1, "speaker": "customer",
        "text": "제 번호는 01012345678이고 문자로 남겨주세요", "is_final": True, "utterance_end_ms": 2600}


class _StubMasking(MaskingPort):
    def mask(self, text: str):
        idx = text.find("01012345678")
        return text[:idx] + "*" * 11 + text[idx + 11:], (MaskedSpan(type="P4", span=(idx, idx + 11)),)


def test_returns_501_when_masking_spoke_not_registered():
    with TestClient(app) as client:
        r = client.post("/hub/transcripts", json=BODY)
    assert r.status_code == 501
    assert "01012345678" not in r.text


def test_returns_masked_contract_when_masking_registered():
    app.dependency_overrides[get_masking_port] = lambda: _StubMasking()
    try:
        with TestClient(app) as client:
            r = client.post("/hub/transcripts", json=BODY)
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    body = r.json()
    assert "01012345678" not in body["text"]
    assert body["masked"] == [{"type": "P4", "span": [6, 17]}]
    assert body["segment_id"] == 1 and body["utterance_end_ms"] == 2600


def test_myself_is_served():
    with TestClient(app) as client:
        body = client.get("/hub/myself").json()
    assert body["name"] == "허브 (hub)" and body["does_not"]
