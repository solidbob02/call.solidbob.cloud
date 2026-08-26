---
title: "MySQL 영속성 계층 — 로그 어댑터를 리포지토리로 교체"
assignee: "장민석"
role: "ai"
status: "todo"
sprint: 2
priority: 1
date: 2026-08-26
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
