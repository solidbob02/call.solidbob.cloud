# Requirement: [Task 1], SEC-2, QUA-1
"""앱이 뜨고 /health 가 설정 '여부'만 알리는지 — 값(호스트·비밀번호·URL)이 응답에 새지 않는지."""

from fastapi.testclient import TestClient

from main import app


def test_health_reports_configured_flags_without_values(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "mysql://u:secret-pw@db.internal:3306/callguard")
    monkeypatch.setenv("ELASTICSEARCH_URL", "http://es.internal:9200")
    with TestClient(app) as client:
        body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["mysql_configured"] is True and body["elasticsearch_configured"] is True
    assert body["spokes"] == []
    dumped = str(body)
    assert "secret-pw" not in dumped and "db.internal" not in dumped and "es.internal" not in dumped


def test_health_when_nothing_configured(monkeypatch):
    for k in ("DATABASE_URL", "MYSQL_HOST", "MYSQL_DB_NAME", "MYSQL_USER", "MYSQL_PASSWORD", "ELASTICSEARCH_URL"):
        monkeypatch.delenv(k, raising=False)
    with TestClient(app) as client:
        body = client.get("/health").json()
    assert body["mysql_configured"] is False and body["elasticsearch_configured"] is False
