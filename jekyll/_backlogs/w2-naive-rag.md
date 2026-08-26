---
title: "가장 단순한 RAG — BM25 검색 경로 연결"
assignee: "류준·장민석"
role: "ai"
status: "todo"
sprint: 2
priority: 3
date: 2026-08-26
---

발화 → 검색 → 문서 ID 목록. 리랭킹·생성 없이 **검색만** 붙인다.

평가 하네스의 `RetrievalPredictor` 프로토콜을 구현하는 첫 실물이다.

```python
class RetrievalPredictor(Protocol):
    def retrieve(self, utterance: str) -> list[str]: ...
```

지금은 `Predictors(retrieval=None)` 이라 하네스가 "측정 불가 — 모듈 미구현"으로 보고한다.
이 티켓이 끝나면 **처음으로 실제 숫자가 나온다.**

## 범위 밖 (의도적으로 미룸)

리랭킹(4주차) · 생성(6주차) · 하이브리드 검색(4주차) · 트리거 판정(3주차)

## 완료 조건

`services/core/` 에 구현체가 있고, 하네스에 꽂으면 Recall@5·MRR 이 계산된다.
