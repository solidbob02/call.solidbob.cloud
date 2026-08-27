# Requirement: D-4
"""KnowledgeGapQueryPort 의 PostgreSQL 구현.

**집계를 SQL 이 한다.** 애플리케이션이 전부 읽어와 세면 페이지네이션과 집계가 어긋난다 —
한쪽은 50건만 보고 세게 된다. 신고가 수만 건이 되어도 이쪽이 맞다.

`domain` 은 `call` 에서 따라온다. **LEFT JOIN 이다** — `knowledge_gap.call_id` 는 NULL 을
허용하므로(통화와 무관한 신고도 받는다) INNER JOIN 하면 그 신고가 조용히 사라진다.
"""

from __future__ import annotations

from hub.app.dtos.knowledge_gap_query_dto import (
    GapCount,
    GapStatus,
    KnowledgeGapQuery,
    KnowledgeGapRecord,
)
from hub.app.ports.output.knowledge_gap_query_port import KnowledgeGapQueryPort

from .connection import ConnectionFactory

# 필터는 `%s IS NULL OR 컬럼 = %s` 로 둔다 — SQL 을 문자열로 조립하지 않는다.
_WHERE = '''
WHERE (%s::text IS NULL OR g."module" = %s)
  AND (%s::text IS NULL OR g."status" = %s)
'''

_LIST = f'''
SELECT g."id", g."module", g."description", g."status", g."created_at",
       g."call_id", g."segment_id", g."closure_id", c."domain"
FROM "knowledge_gap" g
LEFT JOIN "call" c ON c."call_id" = g."call_id"
{_WHERE}
ORDER BY g."created_at" DESC, g."id" DESC
LIMIT %s OFFSET %s
'''

_COUNT = f'SELECT COUNT(*) FROM "knowledge_gap" g {_WHERE}'

# 축별 집계. status 를 행이 아니라 열로 뽑는다 — 화면이 한 줄에 open/resolved 를 같이 쓴다.
_BY_MODULE = '''
SELECT g."module",
       COUNT(*) FILTER (WHERE g."status" = 'open')     AS open_count,
       COUNT(*) FILTER (WHERE g."status" = 'resolved') AS resolved_count
FROM "knowledge_gap" g
GROUP BY g."module"
ORDER BY g."module"
'''

_BY_DOMAIN = '''
SELECT c."domain",
       COUNT(*) FILTER (WHERE g."status" = 'open')     AS open_count,
       COUNT(*) FILTER (WHERE g."status" = 'resolved') AS resolved_count
FROM "knowledge_gap" g
JOIN "call" c ON c."call_id" = g."call_id"
GROUP BY c."domain"
ORDER BY c."domain"
'''

_UPDATE = 'UPDATE "knowledge_gap" SET "status" = %s WHERE "id" = %s'


def _filters(query: KnowledgeGapQuery) -> tuple:
    return (query.module, query.module, query.status, query.status)


class PostgresKnowledgeGapQueryRepository(KnowledgeGapQueryPort):
    def __init__(self, connect: ConnectionFactory) -> None:
        self._connect = connect

    async def list_gaps(self, query: KnowledgeGapQuery) -> list[KnowledgeGapRecord]:
        async with self._connect() as conn:
            async with conn.cursor() as cur:
                await cur.execute(_LIST, (*_filters(query), query.limit, query.offset))
                rows = await cur.fetchall()
        return [
            KnowledgeGapRecord(
                gap_id=int(r[0]), module=r[1], description=r[2], status=r[3], created_at=r[4],
                call_id=r[5], segment_id=r[6], closure_id=r[7], domain=r[8],
            )
            for r in rows
        ]

    async def count_gaps(self, query: KnowledgeGapQuery) -> int:
        async with self._connect() as conn:
            async with conn.cursor() as cur:
                await cur.execute(_COUNT, _filters(query))
                row = await cur.fetchone()
        return int(row[0])

    async def count_by_module(self) -> list[GapCount]:
        return await self._counts(_BY_MODULE)

    async def count_by_domain(self) -> list[GapCount]:
        return await self._counts(_BY_DOMAIN)

    async def _counts(self, sql: str) -> list[GapCount]:
        async with self._connect() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                rows = await cur.fetchall()
        return [GapCount(key=r[0], open=int(r[1]), resolved=int(r[2])) for r in rows]

    async def update_status(self, gap_id: int, status: GapStatus) -> bool:
        async with self._connect() as conn:
            async with conn.cursor() as cur:
                await cur.execute(_UPDATE, (status, gap_id))
                moved = cur.rowcount
            await conn.commit()
        # 없는 id 를 옮겼다고 하지 않는다 — 화면이 "처리했다"고 표시하면 거짓이 된다.
        return bool(moved)
