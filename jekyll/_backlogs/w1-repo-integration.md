---
title: "저장소 통합 및 jekyll/ 구조 정리"
assignee: "공동"
role: "infra"
status: "done"
sprint: 1
priority: 15
date: 2026-08-25
---

`origin/main`(PM 계열)과 `origin/backend`가 **공통 조상 없는 별개 히스토리**로 갈라져 있던 것을 하나로 통합했다.
두 사람이 각자 절반씩 했다.

## 류준

- 지킬 사이트를 저장소 루트에서 `jekyll/` 하위로 이동 — `services/`·`apps/`·`infra/`(코드)와 분리하기 위함
- 이후 `main` 에 추가된 내용(GCP 쿼터 하드 리밋, Pages 배포 트리거 단순화 등)을 재확인하며
  여러 차례 병합·충돌 해결 (커밋 `a8db209`, `9eab5b1`)
- 통합 과정에서 드러난 FK 생성 순서 버그, ERD 범례 렌더 실패(graphviz exit 138) 수정

## 정성윤

파일 단위로 정본을 정해 합쳤다 (PR #2). 기준은 **사실이 더 정확한 쪽**과 **이미 팀이 쓰고 있는 쪽**.

| 영역 | 채택 | 근거 |
|---|---|---|
| 지킬 사이트 | backend | 사업명·팀명·개발기간 등 사실 정보, 기획서 16개 절 1:1, 자체 레이아웃, 빌드 24.9s → 0.05s |
| ERD·스키마 | backend `db/` | 실행 가능한 DDL, 팀 교차검증 완료 |
| `CLAUDE.md` | 병합 | backend 사이트 컨벤션 + PM 계열 절대 원칙·기록·커밋 규칙 |
| `.gitignore` | backend | Python·Node·macOS·자격증명 안전망 |
| `.claude/` | PM 계열 + backend 고유 규칙 2개 | 외부 저장소에서 흘러든 파일은 제외 |
| `_project/`, Pages 워크플로 | PM 계열 | backend 에 없던 것 |

제거(히스토리에는 남음): PM 계열 지킬 사이트, `docs/erd/`(Mermaid ERD + 정규화 문서).
이후 모든 브랜치(`main`·`PM`·`frontend`·`flutter`·`backend`)를 같은 커밋으로 통일했다.

기록: [진행상황 (7)·(8)](/progress/)
