---
title: "지식베이스 색인 — 고정 청킹 + 문서 ID 부여"
assignee: "류준·장민석"
role: "ai"
status: "in-progress"
sprint: 2
priority: 2
date: 2026-08-26
---

4개 도메인 지식베이스(`knowledge-base/{finance,dasan,shopping,health}/`)를 Elasticsearch 에 넣는다.
2주차는 **가장 단순한 형태**로 간다 — 고정 청킹, nori·dense_vector 없이 BM25 만.

## 할 것

- ~~고정 길이 청킹~~ → **1 조항 = 1 청크** (상한 400자, 넘을 때만 분할). 2026-08-26 실측 후 변경:
  조항 102개의 길이가 중앙값 101자 · 최대 332자 · **400자 초과 0개**라, 고정 길이(500자 등)로 자르면
  조항이 쪼개지는 게 아니라 **여러 조항이 한 청크로 뭉친다**. 그러면 아래 "청크마다 문서 ID 유지"가
  깨지고 골든셋 `expected_doc_ids`(조항 ID 기준)로 Recall@5 를 채점할 수 없다
- 청크마다 문서 ID 유지 — `FIN-TERM-3.2` 처럼 도메인 접두어 + 문서종류 + 조항.
  지식베이스 각 조항 앞에 `<!-- id: FIN-TERM-1.1 -->` 주석으로 이미 박혀 있으므로 그대로 읽는다
- 인덱스를 도메인별로 나눌지 하나로 두고 `domain` 필드로 필터할지 결정 — [도메인 라우팅](/backlog/w2-domain-routing/)은
  자동 분류로 확정됐으나(`_project/decisions/007`) **ES 인덱스 분할 여부는 여전히 미결**이다(`docs/domain.md` §3)
- 적재 후 chunk 목록 덤프 — 골든셋 라벨링이 이 목록을 본다

## 왜 단순하게 시작하나

4주차에 nori·dense_vector·RRF 를 넣고 **개선 폭을 수치로 보여주기 위해서**다.
처음부터 다 넣으면 무엇이 얼마나 기여했는지 말할 수 없다([평가 설계](/docs/06/)).

## 완료 조건

골든셋 라벨이 참조할 수 있는 chunk ID 목록이 나오고, 같은 명령으로 재적재가 재현된다.

## 2026-08-26 — 청킹·덤프 완료, ES 적재 남음

`fastapi/apps/retrieval/` 스포크를 만들고 청킹까지 붙였다. **첫 스포크**라
`.importlinter` 다섯 목록에 `retrieval` 을 등록했고 계약 5종 전부 통과한다.

| 계층 | 파일 | 역할 |
|---|---|---|
| `domain/value_objects/` | `chunk.py` | `Chunk` — `chunk_id` / `doc_id` 분리(분할 시에만 달라진다) |
| `domain/services/` | `chunking.py` | 조항 마커(`<!-- id: … -->`) 파싱 + 상한 초과 시 문단 경계 분할 |
| `adapter/outbound/` | `knowledge_base_loader.py` | 디렉토리 순회(파일 I/O 라 adapter) |
| — | `scripts/index_knowledge_base.py` | 덤프 명령 |

```
.venv/bin/python scripts/index_knowledge_base.py --out data/processed/kb-chunks.json
→ 청크 102개 (조항 102개) · finance 34 · shopping 27 · health 21 · dasan 20
  길이 최소 26 / 중앙 93 / 최대 318자 · 분할된 조항 0개
```

두 번 돌려 결과가 바이트 단위로 같음을 확인했다(재현성). 테스트 19건 추가 —
`pytest` 64개 통과. 골든셋 `expected_doc_ids` 가 전부 청크 목록 안에 있는지도
테스트로 고정했다(정답 문서가 색인에 없으면 Recall@5 를 영원히 못 맞힌다).

**아직 `done` 이 아닌 이유**: 완료 조건의 **재적재**(ES 적재)가 남았다. 인덱스를
도메인별로 나눌지 하나로 두고 `domain` 필드로 필터할지가 미결이라(`docs/domain.md` §3),
지금 인덱스를 만들면 결정 후 다시 만들어야 한다. 로컬에 ES 도 아직 안 떠 있다.

덤프 결과(`data/processed/`)는 `.gitignore` 대상이라 커밋되지 않는다 — 각자 위 명령으로
다시 만든다.
