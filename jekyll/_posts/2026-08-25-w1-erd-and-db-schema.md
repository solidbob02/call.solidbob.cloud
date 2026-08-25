---
layout: post
title: "W1 — ERD 작성과 docs/ 신설, DB 스키마 확정을 1주차에 배치"
date: 2026-08-25 11:37:18 +0900
categories: log
week: 1
track: [infra, data]
status: done
metrics_touched: false
---

## 한 일

- 저장소 루트에 **`docs/`** 를 신설했다. 지킬 사이트(`jekyll/`)와 분리된 구현자용 기술 문서 자리다.
  - `docs/erd/schema.mmd` — MySQL 5개 테이블 ERD의 **Mermaid 소스(정본)**
  - `docs/erd/schema.png` — 렌더 산출물 (1784×580)
  - `docs/erd/mmd-config.json` — 렌더 설정
  - `docs/architecture.md` — 아키텍처 + 데이터 모델 + ERD 재생성 절차
- 사이트의 `architecture.md` 에서는 ERD 상세를 걷어내고 테이블 5종 요약과 `docs/erd/` 포인터만 남겼다.
- `CLAUDE.md` 3절에 **`docs/` 와 `jekyll/_docs/` 구분 표**를 넣었다. 이름이 비슷해 반드시 헷갈린다.
- 마일스톤에 **`w1.db_schema`(MySQL 스키마 확정, 정성윤)** 를 추가했다. 지금까지 1주차에 인터페이스 계약 3종(`w1.schema`)만 있었고 DB 스키마 항목이 없었다.
- 미결 항목 **OI-13** 등록 — 컴플라이언스 경고(C-1~C-4)를 어느 테이블에 저장할지.

## 판단과 근거

- **ERD는 확정 스키마가 아니라 회의 출발점이다.** 기획서 rev.4에 있는 것은 테이블 이름 5개와 한 줄 설명이 전부다(3절 397~402행). 컬럼 중 계약에서 유도한 것(`utterance_end_ms`, `masked_spans`, `verdict`, `internal_latency_ms` 등)과 내가 추론한 것(대리 키, 타임스탬프, 카디널리티, 타입)이 섞여 있다. 그래서 문서와 마일스톤 note에 "확정 필요"를 명시했다.
- **`eval_result` 컬럼은 기획서가 아니라 이 저장소의 규칙에서 왔다.** `CLAUDE.md` 4.4가 측정값 한 건에 value/measured_at/commit/command/n을 강제하므로 그 구조를 그대로 테이블로 옮겼다. 하네스가 쓰는 형식과 DB 형식이 어긋나면 기록이 두 벌이 된다.
- **소스와 산출물을 한 폴더에 두되 역할을 명시했다.** `.mmd`가 정본이고 `.png`는 생성물이다. PNG만 고치는 일이 없도록 문서 첫 줄에 적었다.
- **DB 스키마 담당은 정성윤**으로 잡았다. rev.4 7.1절이 MySQL 스키마를 인프라 담당 범위로 두고 있다. 다만 계약 3종(류준)과 같은 회의에서 함께 정해야 필드가 어긋나지 않는다.
- 버린 선택지: ERD를 `jekyll/_docs/` 안에 두기 — 처음엔 그렇게 만들었는데, 지킬 컬렉션은 front matter 없는 파일을 출력하지 않아 사이트에서 보이지도 않고 소스 파일이 문서 목록에 섞인다. 프로젝트 문서는 프로젝트 루트에 두는 것이 맞다.

## 막힌 것

없음. 첫 렌더에서 **한글이 전부 네모(두부)로 나왔다.** mermaid-cli가 쓰는 헤드리스 Chromium에 한글 글꼴이 없어서다. WSL의 Windows 폰트(맑은 고딕)를 `~/.local/share/fonts/`에 복사하고 `fc-cache -f` 후 재렌더해 해결했고, 이미지를 직접 열어 확인했다. 다음 사람이 그대로 밟을 함정이라 `docs/architecture.md`와 `.mmd` 주석에 절차를 남겼다.

## 다음 세션 첫 작업

**AI Hub 데이터 신청**과 **V1·V2 확인**(채널 구성 / GPU 가용 여부). V2 결과에 따라 생성 폴백 모드 전환이 갈린다. 확인 즉시 `jekyll/_data/milestones.yml`의 해당 항목에 기록한다.
