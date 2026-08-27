---
title: "자막 화자 라벨을 본문 폰트로"
assignee: "조서희"
role: "app"
status: "done"
sprint: 2
priority: 8
date: 2026-08-27
paths:
  - "apps/dashboard/src/index.css"
---

화자 라벨(「고객」/「상담원」)에 모노스페이스를 쓰면 한글 글리프가 없어 브라우저가 다른 폰트로 대체하고, letter-spacing과 크기가 안 맞아 글자가 깨져 보인다.

## 완료 조건

- `.speaker` 는 본문 폰트(`--font`, Inter)
- letter-spacing 없음
- font-size 11px, font-weight 600
- 타임스탬프(`.ts`)는 모노스페이스 유지
