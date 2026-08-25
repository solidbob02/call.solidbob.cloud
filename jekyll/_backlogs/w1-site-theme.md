---
title: "사이트 비주얼 통일 — 홀로그램 표지 + 골드/네이비 테마"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 22
date: 2026-08-25
---

표지 시안(딥네이비 + 골드 + 모노 HUD)을 실제 지킬 사이트에 반영했다.

- 표지는 정적 이미지 대신 `jekyll/assets/js/hologram.js` 로 **실제로 회전하는** 와이어프레임 구체
  (캔버스, 노드/링크/궤도밴드/코어 글로우). 마이크를 연결하면 실음성 레벨에 반응하고,
  없으면 idle 호흡 패턴으로 움직인다
- `_layouts/cover.html`·`doc.html` 에 공통 디자인 토큰 — Syne(제목) · IBM Plex Mono(HUD·배지·표 헤더) ·
  Pretendard Variable(본문), 골드 `#F5A623`, 딥네이비 `#080B12`
- `doc.html` 은 무거운 캔버스 대신 CSS 방사형 글로우만 둬서 본문 많은 페이지도 가볍게 유지
- 칸반·마일스톤의 역할 배지(`role-infra/ai/app`)를 모노스페이스 HUD 톤으로 재배색

표지·목차·기능명세·칸반·ERD 페이지 렌더링과 홀로그램 회전을 브라우저로 확인, 콘솔 에러 없음.
