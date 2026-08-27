# 016 — 관계형 DB 를 MySQL → PostgreSQL 로 전환

**날짜**: 2026-08-27
**상태**: 확정 (사용자 지시)

## 맥락

기획서 rev.4 는 관계형 DB 를 **MySQL** 로 지정했다(`plan.md` 417행 투입자원 표, 180행 C-5
적용 지점, 428행 캐시 전략). 08-25 에 `.env.example` 을 CallGuard 스택으로 재작성하면서
이전 AdPass 의 Aurora PostgreSQL(pgvector) 템플릿을 MySQL 로 교체한 이력이 있다.

2026-08-27 도커로 MySQL 8.4 를 띄우고 스키마를 처음 적용하는 데까지 갔고, 17개 테이블·FK
16개·`server/` 리포지토리 4종·integration 테스트(SEC-1)가 MySQL 기준으로 돌아가고 있었다.

## 선택지

| | 방법 | 비용 |
|---|---|---|
| A | MySQL 유지 | 0 — 이미 동작한다 |
| **B** | **PostgreSQL 전환** | 스키마 생성기 방언 · 드라이버 · 리포지토리 SQL · 인프라 · 문서 45개 파일 |

## 결정

**B — PostgreSQL 로 전환한다.** 사용자 지시, 2026-08-27.

> 검토 시 **A(MySQL 유지)를 권고**했다. 근거는 ① 기획서가 MySQL 로 지정했고 ② PostgreSQL 의
> 대표 강점인 pgvector 가 이 프로젝트에서는 **Elasticsearch 의 `dense_vector` 와 중복**이며
> ③ MySQL 로 이미 동작하는 상태였다는 점이다. 사용자가 재확인해 B 로 확정했다.
> 이 기록은 **되돌릴 때 필요한 정보**로 남긴다.

## 이 전환이 실제로 바꾸는 것

방언 차이가 스키마 전반에 걸린다 — 이름만 바꾸는 작업이 아니다.

| MySQL | PostgreSQL |
|---|---|
| `` `식별자` `` (백틱) | `"식별자"` (큰따옴표) |
| `AUTO_INCREMENT` | `GENERATED ALWAYS AS IDENTITY` |
| `ENUM('a','b')` | `CHECK (col IN ('a','b'))` — 타입을 새로 만들지 않는다 |
| `TINYINT` / `DATETIME` | `SMALLINT` / `TIMESTAMPTZ` |
| 컬럼 뒤 `COMMENT '...'` | 별도 `COMMENT ON COLUMN` 문 |
| `ON DUPLICATE KEY UPDATE` | `ON CONFLICT (...) DO UPDATE` |
| `cursor.lastrowid` | `INSERT ... RETURNING id` |
| 드라이버 `aiomysql` | `psycopg` (async) |

`CALL`·`RANK` 예약어 문제(2026-08-27 발견)는 **PostgreSQL 에서도 그대로**다 — 식별자 인용은
계속 필요하다. 인용 문자만 백틱에서 큰따옴표로 바뀐다.

## 기획서 처리

`_project/plan.md` 는 **수정하지 않는다**(`CLAUDE.md` §3). 대신 `rev4-보완지시서.md` 에
항목을 추가해 덮는다 — 보완지시서가 plan.md 보다 우선한다는 기존 규칙을 그대로 쓴다.

## 되돌리는 법

이 커밋 범위를 revert 하면 된다. 되돌릴 때 확인할 것:
`db/generate_schema_docs.py` 방언 · `server/apps/hub/adapter/outbound/postgres/` ·
`server/core/config.py` 키 이름 · `infra/docker-compose.yml` · `.env.example` ·
`server/requirements.txt` 드라이버 · `.importlinter` 금지 목록.
