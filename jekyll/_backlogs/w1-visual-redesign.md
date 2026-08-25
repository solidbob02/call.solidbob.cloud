---
title: "지킬 사이트 비주얼 통일 — 홀로그램 테마"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 12
date: 2026-08-25
---

표지·본문 전체 페이지에 다크네이비+골드 "홀로그램" 톤을 통일 적용. Claude Design 시안(정적 이미지)을
참고 파일(`hologram-blog.html`)의 **움직이는** 효과로 재구현.

- `jekyll/assets/js/hologram.js`: 캔버스 기반 회전 와이어프레임 구체(피보나치 스피어) — 마이크 연결 시
  실음성 레벨 반응, 미연결 시 idle 호흡 패턴으로 계속 움직임(정적 이미지 아님)
- `_layouts/cover.html`·`_layouts/doc.html`에 공통 디자인 토큰(Syne·IBM Plex Mono·Pretendard, 골드
  `#F5A623`·딥네이비 `#080B12`) 적용. `doc.html`은 무거운 캔버스 대신 CSS 방사형 글로우만 사용해 본문
  페이지 성능 유지
- 칸반·마일스톤 역할 배지를 모노스페이스 HUD 톤으로 재배색
- 브라우저로 표지·목차·기능명세·칸반·ERD 페이지 렌더링 확인, 콘솔 에러 없음

기록: [진행상황 (9)](/progress/)
