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

허브 아웃바운드 포트 `RetrievalPort` 를 구현하는 **첫 스포크**다.

```python
# apps/hub/app/ports/output/retrieval_port.py
class RetrievalPort(ABC):
    @abstractmethod
    async def retrieve(self, utterance: str, top_k: int = 5) -> list[RetrievedDoc]: ...
```

> 2026-08-26 정정: 이 티켓은 원래 `RetrievalPredictor` Protocol(`def` · `list[str]` 반환)을
> 적고 있었으나, `fastapi/` 아키텍처 통합으로 접점이 **hub 아웃바운드 포트 하나**로 바뀌었다
> (ABC · `async` · `list[RetrievedDoc]` 반환). 스포크당 계약 1개 — `docs/architecture.md` §1.

지금은 `Ports(retrieval=None)` 이라 하네스가 "측정 불가 — 모듈 미구현"으로 보고한다.
이 티켓이 끝나면 **처음으로 실제 숫자가 나온다.**

## 범위 밖 (의도적으로 미룸)

리랭킹(4주차) · 생성(6주차) · 하이브리드 검색(4주차) · 트리거 판정(3주차)

## 완료 조건

`ai/apps/retrieval/` 에 구현체가 있고, `evaluation.harness.Ports(retrieval=...)` 에
꽂으면 Recall@5·MRR 이 계산된다. `.importlinter` 다섯 목록에 `retrieval` 등록 + 계약 5종 통과.
