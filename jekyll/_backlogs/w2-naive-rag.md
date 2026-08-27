---
title: "가장 단순한 RAG — BM25 검색 경로 연결"
assignee: "류준·장민석"
role: "ai"
status: "done"
sprint: 2
priority: 3
date: 2026-08-26
requirement:
  - "B-2"
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

---

## 2026-08-27 완료 (류준)

**첫 실측치가 나왔다.** 이 프로젝트에서 처음으로 "측정 불가 — 모듈 미구현" 이 아닌 숫자다.

| 지표 | 값 | 목표([6.1절](/docs/06/)) |
|---|---|---|
| Recall@5 | **0.857** (12/14) | ≥0.70 (오류 없음) |
| MRR | **0.702** | ≥0.55 |

- **측정일** 2026-08-27 · **커밋** `670bc73` 기준 작업분 · **표본** 골든셋 `v1-50.json` 의 B 케이스 14건
- **재현 명령**
  ```bash
  cd infra && docker compose up -d elasticsearch && cd ..
  export ELASTICSEARCH_URL=http://localhost:9200
  .venv/bin/python scripts/index_knowledge_base.py --to-es --recreate
  .venv/bin/python scripts/run_eval.py --golden-set golden-set/v1-50.json --runs 3
  ```
- **3회 실행 최저치가 1회 값과 같다** — BM25 는 결정적이라 흔들리지 않는다(절대 원칙 4의
  "최저치 고정"이 여기서는 자명하게 성립한다). 임베딩이 들어가는 4주차부터는 다시 봐야 한다.

> ⚠ **이 값은 잠정이다.** 공식 기준선은 3주차 골든셋 150건 재측정이고, `db` 의
> `eval_run`/`eval_result` 기록과 [6.1절 지표 표](/docs/06/) 반영은
> [`w2-baseline`](/backlog/w2-baseline/) 의 몫이다.

### 만든 것

| 파일 | 역할 |
|---|---|
| `ai/apps/retrieval/adapter/outbound/es_bm25_retriever.py` | `RetrievalPort` 구현체. BM25(nori) 단독 |
| `scripts/run_eval.py` | **평가 쪽 합성 루트** — 스포크를 포트에 꽂는다 |
| `ai/tests/test_eval_wiring.py` | 배선 테스트 (`apps/` 밖) |

**`scripts/run_eval.py` 가 따로 있는 이유**: `evaluation` 이 `retrieval` 을 직접 import 하면
`.importlinter` 의 module-independence 계약이 깨진다. 두 모듈의 접점은 hub 포트(추상)뿐이고
구체 구현을 꽂는 일은 두 모듈 **밖에서** 해야 한다 — `server/main.py` 가 요청 경로에 대해
하는 일을 평가 경로에 대해 한다. **처음에 배선 테스트를 `retrieval/tests/` 에 뒀다가 계약이
깨져서** `ai/tests/` 로 옮겼다(`ai/pytest.ini` 의 `testpaths` 에 `tests` 추가).

### 못 맞힌 2건 — 원인이 보인다

```
MISS GS-001 정답 FIN-TERM-2.2  상위=['FIN-MANUAL-2.1', 'DASAN-MANUAL-4.1', 'HLT-MANUAL-1.4']
MISS GS-019 정답 SHOP-TERM-4.4 상위=['HLT-MANUAL-1.4', 'DASAN-MANUAL-1.4', 'SHOP-MANUAL-1.1']
```

**둘 다 정답이 `TERM` 인데 `MANUAL` 문서가 자리를 채웠다.** 그리고 금융·쇼핑 질의인데
`DASAN`·`HLT` 문서가 상위에 올라왔다 — **도메인 필터를 안 걸었기 때문**이다.
`RetrievalPort.retrieve(utterance, top_k)` 시그니처에 도메인이 없어 하네스가 넘겨줄 방법이 없다.

→ B-0 라우팅을 실제로 태우려면 **포트 시그니처를 바꿔야 하고 그건 `server/` 소관**이다.
어댑터 생성자에 `domain=` 을 임시 통로로 열어 뒀고, 필터가 실제로 듣는 것은 integration
테스트로 확인했다. [미결 항목](/open-items/)에 올렸다.

### 그 밖에 확인한 것

- **`collapse: doc_id`** 를 넣었다. 조항이 쪼개졌을 때 같은 조항의 청크들이 top-5 자리를
  나눠 먹으면 채점 후보가 줄어든다. 지금은 분할 0건이라 동작 차이가 없지만 조용히 손해가 나는 자리다
- **필드 가중치를 주지 않았다**(`title^2` 등). 4주차에 붙이고 그 차이를 재기 위해서다
- **⚠ nori 가 이미 베이스라인에 들어 있다.** [8주 로드맵](/docs/08/)의 "4주차 nori 인덱스"로는
  개선 폭을 못 잰다 — 재려면 `standard` 애널라이저 인덱스를 따로 적재해 비교해야 한다.
  [미결 항목](/open-items/) 참고
- **RRF 는 `ai/` 코드에서 계산하기로 정하고 함수까지 만들어 뒀다**(`_project/decisions/021`,
  `retrieval/domain/services/fusion.py`, 테스트 14건). 이 티켓(BM25 단독)에는 병합할 순위가
  하나뿐이라 **배선은 하지 않았다** — 4주차 하이브리드에서 쓴다. 미리 만든 이유는 알고리즘을
  테스트로 고정해 두면 그때 `k` 를 바꿔 가며 Recall@5 변화를 잴 수 있어서다

### 검증

`cd ai && pytest` **96개 통과**(53 → 68 → 82 → 96), `pytest -m integration` **9건 통과**(실제 ES 9.5.1),
구조 계약 3종 KEPT.
