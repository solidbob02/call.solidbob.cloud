---
title: "평가 결과를 DB 에 남긴다 — eval_run / eval_result"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 2
priority: 1
date: 2026-08-27
depends_on:
  - "w2-eval-wiring-c5-f2"
requirement:
  - "E-1"
  - "E-4"
  - "QUA-2"
paths:
  - "server/apps/hub/adapter/outbound/postgres/eval_run_repository.py"
  - "scripts/run_eval.py"
---

## 무엇을

`db/schema.sql` 에 `eval_run`·`eval_result` 테이블이 **있는데 쓰는 코드가 0줄**이었다.
수치는 터미널에만 찍히고 **다음 실행에 덮여 사라졌다.**

[`CLAUDE.md` §5](https://github.com/solidbob02/call.solidbob.cloud/blob/main/CLAUDE.md):

> 값 하나에는 **언제·어느 커밋으로·어떤 명령으로·표본 몇 건**인지가 함께 남아야 한다.
> 넷 중 하나라도 채울 수 없으면 그 숫자는 아직 기록할 준비가 되지 않은 것이다.

```bash
cd infra && docker compose up -d && cd ..
export ELASTICSEARCH_URL=http://localhost:9200
.venv/bin/python scripts/run_eval.py --golden-set golden-set/v1-50.json --runs 3 --record
```

## 첫 기록 (`run_id = 2`)

```
eval_run     v1-50 · 커밋 253ad25 · error_rate 0 · 2026-08-27 · jangminseok
eval_result  B-2  recall_at_k 0.857 · mrr 0.702 · n 14
             C-5  miss_count 0 · n 12          passed_absolute_rule = true
             F-2  accuracy 1.0 · n 16          passed_absolute_rule = true
```

`--runs N` 이면 **최저치**를 남긴다(절대 원칙 4). 기준선은 평균이 아니다.

## 판단한 것

- **미구현·NaN 은 기록하지 않는다.** 미측정을 `0.0` 으로 적으면 «0점을 받았다» 와
  구분되지 않는다(절대 원칙 2·10). 과잉 마스킹률이 NaN 인 것도 그래서 빠진다
- **불리언을 지표값으로 넣지 않는다.** `absolute_rule_passed` 는 판정이지 측정값이 아니다 —
  `1.0` 으로 섞이면 지표가 오염된다. 전용 컬럼(`passed_absolute_rule`)으로 간다
- **기록하는 쪽이 판정하지 않는다.** 기준선 미달 여부는 하네스가 정하고 여기서는 그대로 옮긴다
- **지표가 하나도 없으면 실행 자체를 남기지 않는다.** 빈 실행 기록은
  «돌렸는데 아무것도 못 쟀다» 를 «돌린 적 있다» 로 보이게 한다

## ⚠ 실제 DB 가 결함을 잡았다

첫 시도가 `StringDataRightTruncation: value too long for type character varying(10)` 로 깨졌다.
`eval_result.module` 이 `VARCHAR(10)` 이고 스키마 주석이 **`'B/C/C-5/F-2 등'`** —
**하네스 섹션명이 아니라 기능 ID 를 넣으라는 설계**였다(`closure_gate` 는 12자).

→ 섹션명 → 기능 ID 매핑을 넣었다(`retrieval`→`B-2` · `masking`→`C-5` · `closure_gate`→`F-2`).
[rfp-harness §1](https://github.com/solidbob02/call.solidbob.cloud/blob/main/.claude/rules/rfp-harness.md)
의 «기획서 기능 ID 를 그대로 쓴다» 와도 맞는다.
**가짜 커서였으면 통과했을 결함**이라 integration 테스트로 고정했다.

트랜잭션도 확인했다 — 실패한 실행은 롤백돼 **유령 행이 남지 않았다**(IDENTITY 시퀀스만 1 소모).

## 남은 것

[`w2-baseline`](/backlog/w2-baseline/)의 기록 위치 조건이 이걸로 채워졌다.
다만 그 티켓은 «3주차 150건 재측정값이 공식 기준선» 이라 **지금 값은 잠정**이다.
[6.1절](/docs/06/) 지표 표 반영은 팀과 함께 본다.
