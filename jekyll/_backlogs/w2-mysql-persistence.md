---
title: "MySQL 영속성 계층 — 로그 어댑터를 리포지토리로 교체"
assignee: "장민석"
role: "ai"
status: "in-progress"
sprint: 2
priority: 1
date: 2026-08-26
requirement:
  - "SEC-1"
paths:
  - "server/apps/hub/adapter/outbound/*"
  - "server/core/config.py"
---

`db/schema.sql` 에 테이블 16개가 있는데 **저장하는 코드가 하나도 없다.** 아웃바운드
어댑터는 `log_transcript_ingest_record_adapter.py`·`log_myself_record_adapter.py` 둘뿐이고
둘 다 로그로 찍고 끝난다. `transcript_ingest_interactor` 가 마스킹까지 제대로 하고도
결과가 **어디에도 남지 않는다.**

DB 저장은 [`server/` 담당](https://github.com/solidbob02/call.solidbob.cloud/blob/main/server/CLAUDE.md)이다.
이 티켓이 아래 세 티켓의 전제다 — 조회할 데이터가 DB 에 없으면 어떤 화면도 만들 수 없다.

## 할 것

```
server/apps/hub/adapter/outbound/mysql/       ← 신규
  transcript_segment_repository.py             log_transcript_ingest_record_adapter 를 대체
  masking_event_repository.py                  C-5 마스킹 구간 기록
```

- `core/config.py` 의 `mysql_*` 는 이미 준비돼 있다([SEC-2](/docs/07/) — `.env.example` 키 이름 1:1).
  **새 키를 만들면 `.env.example` 에도 이름만 등록한다.**
- 어댑터는 `dependencies/` 에서만 포트에 결합한다. 로그 어댑터는 지우지 말고 남겨둔다 —
  DB 없이 도는 테스트 경로가 필요하다.

## ⚠ SEC-1 — 이 티켓의 핵심 검증

**`transcript_segment` 에 마스킹 전 원문이 들어가면 안 된다.** 인터랙터가 `command.raw_text` 를
`record()` 에 넘기지 않는 구조는 이미 잡혀 있으니, **리포지토리가 그 경계를 유지하는지**가 관건이다.

원문이 DB·로그 어디에도 남지 않는 것을 테스트로 고정한다 — 스키마 리뷰만으로는 부족하다.

## 완료 조건

`POST /hub/transcripts` 로 들어온 전사가 마스킹된 형태로 `transcript_segment` 에 저장되고,
원문이 어디에도 남지 않음을 테스트가 검증한다. `cd server && pytest` 통과.

## 2026-08-27 — 어댑터·테스트 완료, 실제 연결은 마이그레이션 대기

```
adapter/outbound/mysql/connection.py                    커넥션 팩토리 (Protocol 로 추상화)
adapter/outbound/mysql/transcript_segment_repository.py TranscriptIngestRecordPort 구현
dependencies/transcript_record_provider.py              MySQL 설정 있으면 리포지토리, 없으면 로그 어댑터
tests/adapter/outbound/                                 7건 (가짜 커넥션 6 + integration 1)
```

**실제 MySQL 없이 SEC-1 을 검증한다.** 커넥션을 `Protocol` 로 추상화해 가짜를 꽂았다 —
리포지토리가 쿼리 인자로 무엇을 넘기는지 그대로 들여다보고 **원문이 없음을 테스트로 고정**했다.
스키마 리뷰만으로는 확인할 수 없던 부분이다.

### 7.3절이 이미 정해둔 규칙을 어댑터가 지킨다

> DB에는 `is_final: true`만 저장 — interim까지 저장하면 통화 1건에 수천 행이 쌓인다.

[V4 실측](/docs/05/)상 20초 발화에 interim 이 199건 온다. `record()` 는 interim 이면
**커넥션조차 열지 않고** 반환한다. 화면은 `segment_id` 로 교체해 보여주고 DB 는 확정본만 남긴다.

마스킹 구간은 다시 넣기 전에 지운다 — 같은 segment 를 재수신하면 이전 구간이 남아 새 마스킹과 섞인다.

### 로그 어댑터를 지우지 않았다

MySQL 설정이 없으면 로그 어댑터로 떨어진다. DB 없이 도는 경로가 있어야 로컬·CI 에서 파이프라인을
확인할 수 있고, **둘 다 마스킹 후 이벤트만 받으므로** 어느 쪽이든 SEC-1 은 깨지지 않는다.

### 의존성

`aiomysql==0.3.2` 를 `server/requirements.txt` 에 추가했다(포트가 `async` 라 async 드라이버).
`.importlinter` 계약 3 금지 목록에도 넣어 **adapter 밖에서 import 하면 실패**하게 했다.

**검증**: `cd server && pytest` 34개 통과(28→34) · `lint-imports` 계약 3종 KEPT ·
`pytest -m integration` 분리 확인.

**아직 `done` 이 아닌 이유**: 실제 MySQL 에 붙여본 적이 없다. `db/schema.sql` 마이그레이션이
미착수라(STATE 기준) 붙일 DB 가 없다. integration 테스트는 `skip` 으로 자리만 잡아뒀다.

### ⚠ 마이그레이션 때 확인할 것 — 계약과 스키마 불일치

[7.3절](/docs/07/) 전사 이벤트 예시는 `"segment_id": "seg_0031"` 로 **문자열**인데,
`transcript_segment.segment_id` 는 **BIGINT** 이고 `TranscriptIngestRequest.segment_id` 도 `int` 다.
코드와 DB 는 서로 맞고 **계약 예시만 어긋난다** — 예시를 고칠지 타입을 바꿀지 팀이 정해야 한다.
