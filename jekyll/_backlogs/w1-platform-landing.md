---
title: "플랫폼 홍보 랜딩 페이지"
assignee: "조서희"
role: "app"
status: "in-progress"
sprint: 1
priority: 15
date: 2026-08-27
paths:
  - "apps/platform"
---

`apps/platform` 신규. CallGuard 제품 소개용 마케팅 랜딩 페이지, `apps/dashboard`와
별개 배포 단위. 아직 팀 문서에 스펙이 없어 프론트가 처음 정의한다. 히어로에
라이브 자막+카드뉴스 데모 연출을 시그니처 요소로 둔다.

히어로 애니메이션에만 화려함을 몰아주고, 나머지 섹션은 차분하게 둔다.
데모에 쓰는 문장·카드는 `apps/dashboard/src/mock` 의 금융보험 시나리오 값을
옮긴다. 지어내지 않는다.

## 완료 조건

- Vite + React 18 + TypeScript strict, 개발 서버 포트 3000
- 히어로 자막이 반복 재생되고, 키워드 하이라이트 뒤 카드가 뜬다
- 섹션 순서: 헤더 · 히어로 · 문제 · 기능 3분할 · 도메인 4개 · 팀/CTA
