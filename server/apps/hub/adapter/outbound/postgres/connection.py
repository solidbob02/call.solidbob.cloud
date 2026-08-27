# Requirement: SEC-2
"""PostgreSQL 커넥션 팩토리. 설정 '값'은 여기서만 읽고 어디에도 로깅하지 않는다.

2026-08-27 MySQL 에서 전환 — `_project/decisions/018-DB-PostgreSQL-전환.md`.
리포지토리는 이 모듈의 `ConnectionFactory` 타입만 알고 psycopg 를 직접 import 하지 않는다 —
테스트가 가짜 커넥션을 꽂을 수 있어야 실제 DB 없이도 SEC-1 을 검증할 수 있다.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, Protocol


class Cursor(Protocol):
    async def execute(self, sql: str, args: Any = None) -> Any: ...
    async def executemany(self, sql: str, args: Any) -> Any: ...
    async def fetchone(self) -> Any: ...
    async def fetchall(self) -> Any: ...


class Connection(Protocol):
    def cursor(self) -> AsyncContextManager[Cursor]: ...
    async def commit(self) -> None: ...


class ConnectionFactory(Protocol):
    """호출하면 커넥션을 여는 async 컨텍스트 매니저를 돌려준다."""

    def __call__(self) -> AsyncContextManager[Connection]: ...


def build_connection_factory(settings: Any) -> ConnectionFactory:
    """`core.config.Settings` 로 psycopg 커넥션 팩토리를 만든다.

    psycopg 는 이 함수 안에서만 import 한다 — 드라이버가 깔려 있지 않은 환경에서도
    이 모듈을 import 할 수 있어야 한다.
    """
    if not settings.postgres_configured:
        raise RuntimeError("PostgreSQL 설정이 없습니다 — .env 의 POSTGRES_* 를 확인하세요 (SEC-2)")

    import psycopg  # noqa: PLC0415  (선택적 의존성 — 위 주석 참고)

    conninfo = psycopg.conninfo.make_conninfo(
        host=settings.postgres_host,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        dbname=settings.postgres_db_name,
    )

    @asynccontextmanager
    async def factory():
        # psycopg 의 connect() 는 코루틴이라 await 한 뒤에야 컨텍스트 매니저가 된다.
        # 여기서 감싸두면 리포지토리는 `async with self._connect()` 한 줄로 끝난다.
        conn = await psycopg.AsyncConnection.connect(conninfo, autocommit=False)
        try:
            yield conn
        finally:
            await conn.close()

    return factory
