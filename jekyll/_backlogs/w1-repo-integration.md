---
title: "두 갈래 저장소 통합 — 파일별 정본 확정"
assignee: "정성윤"
role: "infra"
status: "done"
sprint: 1
priority: 20
date: 2026-08-25
---

`origin/main`(PM 계열)과 `origin/backend`(류준)가 **공통 조상이 없는 별개 히스토리**였다.
같은 프로젝트를 두 벌 만든 상태라 일반 머지가 불가능해, 파일 단위로 정본을 정해 합쳤다.

채택 기준은 **사실이 더 정확한 쪽**과 **이미 팀이 쓰고 있는 쪽**이다.

| 영역 | 채택 | 근거 |
|---|---|---|
| 지킬 사이트 | backend | 사업명·팀명·개발기간 등 사실 정보, 기획서 16개 절 1:1 문서화, 자체 레이아웃, 빌드 성능 수정(24.9s → 0.05s) |
| ERD·스키마 | backend `db/` | 실행 가능한 DDL, 팀 교차검증 완료 |
| `CLAUDE.md` | 병합 | backend 사이트 컨벤션 + PM 계열 절대 원칙·기록·커밋 규칙 |
| `.gitignore` | backend | Python·Node·macOS·자격증명 안전망 |
| `.claude/` | PM 계열 + backend 고유 규칙 2개 | 외부 저장소에서 흘러든 파일은 제외 |
| `_project/` | PM 계열 | backend 에 없던 기획서 원본·보완지시서·결정 기록 |

제거(히스토리에는 남음): PM 계열 지킬 사이트, `docs/erd/`(Mermaid ERD + 정규화 문서).

이후 모든 브랜치(`main`·`PM`·`frontend`·`flutter`·`backend`)를 같은 커밋으로 통일했다.
