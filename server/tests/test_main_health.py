# Requirement: [Task 1], SEC-2, QUA-1
"""앱이 뜨고 /health 가 설정 '여부'만 알리는지 — 값(호스트·비밀번호·URL)이 응답에 새지 않는지."""

from fastapi.testclient import TestClient

from main import app


def test_health_reports_configured_flags_without_values(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:secret-pw@db.internal:5432/callguard")
    monkeypatch.setenv("ELASTICSEARCH_URL", "http://es.internal:9200")
    with TestClient(app) as client:
        body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["postgres_configured"] is True and body["elasticsearch_configured"] is True
    # ES 가 설정돼 있으면 검색 스포크(ai/)까지 꽂힌다 — 합성 루트가 하는 일이다
    assert body["spokes"] == ["masking", "closure_gate", "retrieval"]
    dumped = str(body)
    assert "secret-pw" not in dumped and "db.internal" not in dumped and "es.internal" not in dumped


def test_health_when_nothing_configured(monkeypatch):
    for k in ("DATABASE_URL", "MYSQL_HOST", "MYSQL_DB_NAME", "MYSQL_USER", "MYSQL_PASSWORD", "ELASTICSEARCH_URL"):
        monkeypatch.delenv(k, raising=False)
    with TestClient(app) as client:
        body = client.get("/health").json()
    assert body["postgres_configured"] is False and body["elasticsearch_configured"] is False
    # 규칙 기반 스포크는 외부 자원이 없어도 붙는다. 검색은 ES 가 없으면 안 붙고 501 로 남는다.
    assert body["spokes"] == ["masking", "closure_gate"]


def test_스포크_목록이_설정_값을_흘리지_않는다(monkeypatch):
    """`/health` 는 설정 '여부'만 알린다(SEC-2). 스포크 이름에 URL·인덱스명이 섞이면 안 된다."""
    monkeypatch.setenv("ELASTICSEARCH_URL", "http://es.internal:9200")
    with TestClient(app) as client:
        spokes = client.get("/health").json()["spokes"]
    assert all(s.isidentifier() for s in spokes), f"스포크 이름이 식별자가 아니다: {spokes}"
