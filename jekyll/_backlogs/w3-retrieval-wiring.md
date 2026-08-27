---
title: "검색 스포크를 요청 경로에 꽂는다 — /hub/search 가 실제로 검색한다"
assignee: "장민석"
role: "ai"
status: "done"
sprint: 3
priority: 2
date: 2026-08-27
depends_on:
  - "w2-naive-rag"
requirement:
  - "B-2"
paths:
  - "server/main.py"
---

## 무엇을

류준 님이 [`w2-naive-rag`](/backlog/w2-naive-rag/)에서 `EsBm25Retriever`(`RetrievalPort` 구현)를
만들었는데 **`server/` 요청 경로에서 쓸 방법이 정해져 있지 않아** `POST /hub/search` 가 계속 501 이었다.

`server/.importlinter` 계약 2 가 `hub`·`masking`·`closure_gate`·`core` → `ai` import 를 금지한다.

## 결정 — 같은 프로세스, `main.py` 가 꽂는다 (`_project/decisions/024`)

**설계가 이미 답을 갖고 있었다.**

1. **`ai/` 는 서비스가 아니라 라이브러리다** — `ai/requirements.txt` 주석이 *"의존성(fastapi·uvicorn)은
   `server/requirements.txt` 에 있다"* 고 적고 있다. HTTP 표면이 없다
2. **`main.py` 는 계약 대상이 아니다** — `.importlinter` 의 `root_packages` 넷에 없다. **합성 루트**다
3. **같은 패턴이 이미 돈다** — `scripts/run_eval.py` 가 평가 경로에서 하는 일이다.
   `main.py` docstring 도 애초에 *"스포크는 여기서 `dependency_overrides` 로 꽂는다"* 였다

## 결과 (실측)

```
GET  /health              spokes: ["masking","closure_gate","retrieval"]
POST /hub/search          501 → 200
   "반품 배송비는 누가 부담하나요"
   → SHOP-TERM-4.2  15.99   4.2 반품 배송비 부담
     SHOP-MANUAL-1.3 13.65  1.3 필수 안내 누락 금지
     SHOP-TERM-4.3    7.90  4.3 반품 처리 시 고지 의무
POST /hub/recommendations 501 (trigger B-1 미구현 — 3주차, ai/)
```

## 안전장치 셋

- **못 꽂으면 조용히 501** — `ELASTICSEARCH_URL` 이 없거나 `ai/`·`elasticsearch` 를 import 할 수
  없으면 주입하지 않는다. **임시 구현을 만들지 않는다**(빈 목록은 「관련 문서 없음」과 구분되지 않는다)
- **`server` CI 가 그대로 돈다** — `ai/` 의존성 없는 환경에서도 `main.py` 가 import 된다
- **기동 시 ping 하지 않는다** — ES 가 잠깐 내려갔다고 서버가 못 뜨면 **자막·마스킹까지 멈춘다**

## 곁들여 — `/health` 의 `spokes` 가 거짓말을 하고 있었다

`SPOKES` 리스트가 **비어 있었다.** 마스킹·F-2 는 프로바이더 기본값으로 이미 꽂혀 있는데
`/health` 는 «스포크 0개» 라고 답했다. 셋 다 실제로 보고하게 고치고,
**스포크 이름에 설정 값이 섞이지 않는지**(SEC-2) 테스트로 고정했다.

> ⚠ **정성윤 님 확인 대상** — `CLAUDE.md` 는 `server.solidbob.cloud`·`ai.solidbob.cloud` 두
> 도메인을 적어 뒀는데 같은 프로세스면 **한 컨테이너**다. [미결 항목](/open-items/) 참고.
