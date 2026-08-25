---
title: "저장소 통합 및 jekyll/ 구조 정리"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 15
date: 2026-08-25
---

`origin/main`(PM 계열)과 `origin/backend`가 공통 조상 없는 별개 히스토리로 갈라져 있던 것을 하나로 통합.

- 지킬 사이트를 저장소 루트에서 `jekyll/` 하위로 이동 — `services/`·`apps/`·`infra/`(코드)와 분리하기 위함
- 파일 단위 비교로 정본 확정: 지킬 사이트·ERD/스키마는 backend 계열, `_project/`·Pages 배포 워크플로는 PM
  계열에서 채택. `CLAUDE.md`는 양쪽 내용을 병합
- 이후 팀원이 `main`에 추가로 병합한 내용(GCP 쿼터 하드 리밋, Pages 배포 트리거 단순화 등)을
  재확인하며 여러 차례 병합·충돌 해결 (커밋 `a8db209`, `9eab5b1` 등)
- FK 생성 순서 버그, ERD 범례 렌더 실패(graphviz exit 138) 등 통합 과정에서 드러난 문제 함께 수정

기록: [진행상황 (7)·(8)](/progress/)
