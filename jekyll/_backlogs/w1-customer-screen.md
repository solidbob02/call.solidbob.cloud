---
title: "고객용 화면 (키워드 카드뉴스 팝업)"
assignee: "조서희"
role: "app"
status: "cancelled"
sprint: 1
priority: 14
date: 2026-08-26
---

**009로 철회.** 고객 화면(`apps/customer`)은 음성 통화 서비스에 필요 없다.
근거: `_project/decisions/014-고객화면-스코프-재철회.md`.

원래 범위: 상담원 대시보드와 같은 `call_id` 세션을 WebSocket으로 공유,
`cards` 이벤트 수신 시 카드뉴스 팝업 렌더링. 근거였던 `_project/decisions/013` 은
009가 철회했다.
