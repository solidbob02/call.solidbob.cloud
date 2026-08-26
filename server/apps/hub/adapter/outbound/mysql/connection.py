# Requirement: SEC-2
"""MySQL 커넥션 팩토리. 설정 '값'은 여기서만 읽고 어디에도 로깅하지 않는다.

리포지토리는 이 모듈의 `ConnectionFactory` 타입만 알고 aiomysql 을 직접 import 하지 않는다 —
테스트가 가짜 커넥션을 꽂을 수 있어야 실제 MySQL 없이도 SEC-1 을 검증할 수 있다.
"""

from __future__ import annotations

from typing import Any, AsyncContextManager, Protocol


class Cursor(Protocol):
    async def execute(self, sql: str, args: Any = None) -> Any: ...
    async def executemany(self, sql: str, args: Any) -> Any: ...


class Connection(Protocol):
    def cursor(self) -> AsyncContextManager[Cursor]: ...
    async def commit(self) -> None: ...


class ConnectionFactory(Protocol):
    """호출하면 커넥션을 여는 async 컨텍스트 매니저를 돌려준다."""

    def __call__(self) -> AsyncContextManager[Connection]: ...


def build_connection_factory(settings: Any) -> ConnectionFactory:
    """`core.config.Settings` 로 aiomysql 커넥션 팩토리를 만든다.

    aiomysql 은 이 함수 안에서만 import 한다 — 드라이버가 깔려 있지 않은 환경(CI 의 단위 테스트)에서도
    이 모듈을 import 할 수 있어야 한다.
    """
    if not settings.mysql_configured:
        raise RuntimeError("MySQL 설정이 없습니다 — .env 의 MYSQL_* 를 확인하세요 (SEC-2)")

    import aiomysql  # noqa: PLC0415  (선택적 의존성 — 위 주석 참고)

    def factory() -> AsyncContextManager[Connection]:
        return aiomysql.connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password,
            db=settings.mysql_db_name,
            autocommit=False,
            charset="utf8mb4",
        )

    return factory
