---
title: "평가 하네스 골격"
assignee: "류준"
role: "ai"
status: "done"
sprint: 1
priority: 9
date: 2026-08-25
---

`services/core/eval/` — 골든셋 로더 + metrics(retrieval·trigger·compliance·masking·closure_gate·latency) + `harness.py`. 단위테스트 24개 통과.

검색·트리거·마스킹·F-2 모듈은 Protocol로 추상화해 두고 미구현 상태에서는 **"측정 불가 — 모듈 미구현"**으로 정직하게 보고한다.
