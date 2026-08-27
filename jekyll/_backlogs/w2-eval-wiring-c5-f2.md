---
title: "평가 하네스에 C-5·F-2 배선 — 첫 통합 측정"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 2
priority: 1
date: 2026-08-27
depends_on:
  - "w2-naive-rag"
requirement:
  - "E-1"
  - "C-5"
  - "F-2"
paths:
  - "scripts/run_eval.py"
---

## 무엇을

`scripts/run_eval.py`(평가 쪽 합성 루트, 류준 님이 `w2-naive-rag` 에서 만듦)에
**C-5 마스킹·F-2 게이트를 꽂았다.** 구현은 2026-08-27 에 끝나 있었는데
**배선이 없어 하네스가 계속 「측정 불가 — 모듈 미구현」으로 보고**하고 있었다.

## 결과 — 세 지표가 한 화면에 나온다

```
[retrieval]     recall_at_k 0.857 · mrr 0.702 · n 14
[masking]       miss_count 0 · absolute_rule_passed True · n 12
[closure_gate]  accuracy 1.0 · absolute_rule_passed True · n 16
[domain_routing / trigger / compliance]  측정 불가 — 모듈 미구현
```

`--runs 3` 최저치도 같다(셋 다 결정적 계산이라 흔들리지 않는다, 절대 원칙 4).
골든셋 `v1-50` · ES 9.5.1 · `callguard-kb-single` 102건 기준.

> ⚠ **아직 기준선으로 고정하지 않았다.** 절대 원칙 5(기준선 미달 시 CI 실패)를 켜려면
> 미구현 4종 때문에 계속 빨간불이 된다 — 켜는 시점은 [미결](/open-items/)에 남겼다.

## 왜 여기서 꽂아도 되나

`masking`·`closure_gate` 는 `server/apps/` 에 있고 `evaluation` 은 `ai/apps/` 에 있다.
**`scripts/run_eval.py` 는 두 모듈 밖의 합성 루트**라 어느 쪽 계약에도 걸리지 않는다 —
의존 방향(`ai → server`)에도 맞고, `ai/.importlinter` 의 모듈 상호 독립 계약에도 걸리지 않는다.
`server/main.py` 가 요청 경로에 대해 하는 일을 여기서 평가 경로에 대해 한다.

**ES 가 없어도 마스킹·F-2 는 채점된다** — 둘 다 외부 의존이 없는 순수 규칙이다.
`ELASTICSEARCH_URL` 없이 돌리면 검색만 「측정 불가」로 남는다.

## 회귀를 테스트로 막았다

`ai/tests/test_eval_wiring.py` 에 3건 추가 — ① 합성 루트가 두 포트를 꽂는지
② ES 없이도 채점되는지 ③ 절대 규칙이 건 단위로 보고되는지.
**배선이 끊기면 하네스가 다시 「측정 불가」로 조용히 돌아가므로** 그 회귀를 잡는다.

> ⚠ `ai/tests/` 는 류준 님 영역이다. 그 파일 docstring 이 스스로 *"`scripts/run_eval.py` 소관"*
> 이라 적고 있고 이번 변경이 **배선 테스트**라 여기 뒀다. `decisions/022` ①(소유/배선 분리)이
> 아직 제안 단계이므로 사후 공유가 필요하다.
