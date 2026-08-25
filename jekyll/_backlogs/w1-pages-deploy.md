---
title: "GitHub Pages 배포 활성화"
assignee: "정성윤"
role: "infra"
status: "todo"
sprint: 1
priority: 11
date: 2026-08-25
---

지킬 사이트가 `jekyll/` 하위라 Pages 의 "Deploy from a branch"(루트 또는 /docs 만 지원)를 쓸 수 없다. Actions 워크플로로 빌드·배포한다.

**남은 것**: ① 워크플로 파일 커밋(토큰 `workflow` 스코프 필요) ② Settings → Pages → Source를 "GitHub Actions"로 변경(**solidbob02 계정 권한**) ③ 커스텀 도메인 DNS(CNAME → `solidbob02.github.io`)
