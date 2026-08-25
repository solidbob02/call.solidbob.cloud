---
title: "GitHub Pages 배포 활성화"
assignee: "정성윤"
role: "infra"
status: "done"
sprint: 1
priority: 11
date: 2026-08-25
---

**완료 (2026-08-25)** — Settings → Pages → Source 를 "GitHub Actions" 로 변경, 배포 워크플로 정상 동작 확인.
공개 주소: `https://solidbob02.github.io/call.solidbob.cloud/`

워크플로(`.github/workflows/pages.yml`)는 `main` 에 push/머지되면 브랜치·변경 내용과 무관하게 실행된다.

**남은 것**: 커스텀 도메인(`call.solidbob.cloud`) CNAME 연결 — Sprint 7(배포) 단계로 미룸.
