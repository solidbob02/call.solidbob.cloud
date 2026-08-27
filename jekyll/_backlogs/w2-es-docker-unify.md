---
title: "로컬 도커 환경 통합 — ES 구성 일원화"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 2
priority: 3
date: 2026-08-27
depends_on:
  - "w2-local-mysql"
requirement:
  - "B-2"
paths:
  - "infra/*"
---

> ⚠ **완료 시점에 만든 티켓이다.** `ai` 브랜치 병합 도중 문제가 드러나 그 자리에서 처리했고,
> 착수 시점에 티켓을 만들지 못했다. 담당·시점은 실제와 같다(장민석, 2026-08-27).

## 무엇을

`ai` 병합으로 **Elasticsearch 로컬 구성이 둘이 됐다.**

| | 루트 `docker-compose.yml` (류준) | `infra/docker-compose.yml` (장민석) |
|---|---|---|
| ES 버전 | 9.5.1 | 8.15.3 |
| nori | 기동 시 플러그인 설치 | `infra/elasticsearch/Dockerfile` 로 이미지에 굽기 |
| 포트 | `9200` | `127.0.0.1:9200` |
| 함께 뜨는 것 | ES 만 | PostgreSQL + ES |

**둘 다 9200 을 잡아 동시에 뜨지 않는다.**

## 왜

인프라 담당([7.1절](/docs/07/))은 정성윤 님이지만 부재 중이고, 이 상태로 두면 팀원이
어느 파일로 ES 를 띄워야 하는지 알 수 없다. 류준 님도 로그에 "`infra/` 가 아직 없어
루트에 뒀다, 생기면 옮기는 건 그쪽 판단"이라 남겼고 `infra/` 는 그 뒤에 생겼다.

## 완료 조건

- [x] compose 파일 하나 — `infra/docker-compose.yml` (루트 파일 삭제)
- [x] ES 버전을 `ai/requirements.txt` 클라이언트 핀과 맞춘다
- [x] `cd infra && docker compose up -d` 로 PostgreSQL + ES 가 함께 뜬다
- [x] 실제 지식베이스가 적재되고 `ai` 통합 테스트가 돈다
- [x] 결정 기록 — `_project/decisions/020-로컬-도커-환경-infra-단일화.md`

## 결과

**ES 9.5.1 · nori 는 이미지에 굽기 · `127.0.0.1` 바인딩.** 버전은 실측이 정했다 —
9.x 클라이언트는 8.x 서버에 접속 자체를 거부한다(`media_type_header_exception ... found 9`).

실기동 확인: ES 9.5.1 + `analysis-nori` / 지식베이스 **실적재 102건** · 재적재 재현 /
BM25 검색 동작 / **`ai` 통합 테스트 5건 skip → 통과**(`.venv` 에 클라이언트가 없어
그동안 건너뛰고 있었다) / `server` 155 · `ai` 68 통과 / 계약 4+3종 KEPT.

> ⚠ **정성윤 님 확인 대상** — `infra/` 는 인프라 담당 영역이다. 되돌리는 법은 `decisions/020` 에 있다.

## ⚠ 이 티켓에서 드러난 것 — RRF 가 basic 라이선스에서 막힌다

[3.1절](/docs/03/)이 지정한 `nori(BM25) + dense_vector + RRF` 중 **RRF 만 유료**다.
`retriever.rrf` 가 **8.15.3·9.5.1 양쪽 다** `403 non-compliant for [Reciprocal Rank Fusion (RRF)]`
로 거부된다. **버전으로 풀리지 않는다.** trial 은 되지만 만료가 2026-09-26 로 종료(10-27)를 못 넘긴다.

이 티켓 범위 밖이라 [미결](/open-items/)로 올렸다 — 순위 병합을 `ai/` 코드에서 계산하는
쪽을 권한다. [`w2-naive-rag`](/backlog/w2-naive-rag/) 담당인 류준 님 결정 사항이다.
