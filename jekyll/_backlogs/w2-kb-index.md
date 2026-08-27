---
title: "지식베이스 색인 — 고정 청킹 + 문서 ID 부여"
assignee: "류준·장민석"
role: "ai"
status: "done"
sprint: 2
priority: 2
date: 2026-08-26
requirement:
  - "B-2"
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

`ai/apps/retrieval/` 스포크를 만들고 청킹까지 붙였다. **첫 스포크**라
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

## 2026-08-27 — ES 적재 붙임 (류준). 남은 것은 레이아웃 확정뿐

**막고 있던 미결을 풀었다 — `single`(인덱스 하나 + `domain` 필터)로 확정했다**
(`_project/decisions/017`). 조항이 102개뿐이라 도메인별로 나누면 인덱스당 20~34건이 되어
BM25 IDF 가 불안정해지고, 얻는 이점(독립 재적재)은 전체 재적재가 1초도 안 걸리는 지금
있으나 마나다. **`per-domain` 코드 경로는 지우지 않았다** — 도메인이 크게 늘면 그쪽으로
전환한다(전환 조건은 결정 기록 참고).

| 계층 | 파일 | 역할 |
|---|---|---|
| `adapter/outbound/` | `es_index.py` | 인덱스 이름·설정(nori)·매핑, 생성, bulk 적재 |
| — | `scripts/index_knowledge_base.py` | `--to-es --layout single\|per-domain --recreate` 추가 |
| — | `infra/docker-compose.yml` | 로컬 ES 9.5.1 + `analysis-nori`(이미지에 굽는다) |

```
single      callguard-kb-single                            ← 현재 쓰는 것
per-domain  callguard-kb-{finance,dasan,shopping,health}   ← 전환 대비로 남겨둔 경로
```

**공정 비교를 위해 고정한 것** — 문서 본문·매핑·애널라이저가 두 레이아웃에서 동일하고
(`per-domain` 에도 `domain` 필드를 남긴다), `number_of_shards` 를 1로 못박았다.
BM25 term statistics 가 샤드 단위라 샤드 수가 다르면 그 자체가 교란 변수가 된다.

**재적재 재현** — `_id` 를 `chunk_id` 로 고정한 upsert 라 같은 명령을 몇 번 돌려도 문서 수와
`_id` 집합이 같다. 완료 조건의 그 항목이다. `@pytest.mark.integration` 테스트로 고정했다.

테스트 15건 추가(`ai` 53 → 68개 통과). 그중 ES 없이 도는 것이 대부분이라 **CI 는 그대로
초록불**이다 — `elasticsearch` 패키지를 설치하지 않는 CI 에서도 `es_index.py` 가 import 되도록
클라이언트를 주입받게 했고, `bulk` 도 `helpers` 대신 클라이언트 메서드를 쓴다.

곁가지로 `test_골든셋이_참조하는_문서_ID가_전부_실린다` 가 `v1-10.json` 만 보고 있어서
`v1-50.json` 을 추가했다. 지금은 14개 ID 전부 실려 있지만 테스트가 지켜주고 있진 않았다.

**아직 `done` 이 아닌 이유**: 완료 조건은 채워졌지만 **실제 ES 를 띄워 확인하지 않았다.**
`pytest -m integration` 과 아래 명령을 돌려 102건이 들어가는 것을 본 뒤 `done` 으로 옮긴다.

```bash
cd infra && docker compose up -d elasticsearch && cd ..
export ELASTICSEARCH_URL=http://localhost:9200
.venv/bin/python scripts/index_knowledge_base.py --to-es --recreate
.venv/bin/python scripts/index_knowledge_base.py --to-es            # 재적재 재현 확인
cd ai && pytest -m integration
```

> ⚠ `assignee` 는 `류준·장민석` 공동 그대로 두었다. 2026-08-26 담당 분리(`decisions/012`)로
> `ai/` 는 류준 몫이 됐지만, 이 티켓은 그 전에 이미 `in-progress` 였다 — 진행 중 티켓의
> 수행자는 소급 수정하지 않는다(CLAUDE.md §4). 이번 작업은 류준이 했다.

---

## ✅ 완료 확인 (2026-08-27, 장민석)

위 "아직 `done` 이 아닌 이유"에 적힌 **실제 ES 기동 확인을 마쳐 `done` 으로 옮겼다.**
공동 티켓(`assignee: 류준·장민석`)이라 상태를 옮겼고, 본문은 고치지 않았다.

- ES **9.5.1** + `analysis-nori` 9.5.1 기동 (`cd infra && docker compose up -d`)
- `--to-es --recreate` → `callguard-kb-single` **102건** 적재
- `--to-es` 재실행 → **재적재 재현** (문서 수 동일)
- `cd ai && pytest -m integration` → **5건 통과** (그동안 `.venv` 에 `elasticsearch` 가
  없어 `importorskip` 으로 skip 되고 있었다. `elasticsearch==9.5.0` 설치 후 통과)
- BM25 검색 동작 확인 — `"반품 배송비"` → `SHOP-TERM-4.2` (9.98)

**도커 구성이 바뀌었다** — 루트 `docker-compose.yml` 을 `infra/` 로 합치고 ES 를 **9.5.1** 로
맞췄다(`_project/decisions/020`). 9.x 클라이언트가 8.x 서버에 붙지 않는 것이 실측으로 확인돼
버전을 클라이언트 핀에 맞췄다. 명령이 `cd infra && docker compose up -d` 로 바뀐 것이 차이다.

> ⚠ **후속 — RRF 는 basic 라이선스에서 막힌다.** `retriever.rrf` 가 8.15.3·9.5.1 양쪽 다
> `403 non-compliant for [Reciprocal Rank Fusion (RRF)]` 다. 이 티켓(적재)에는 영향이 없지만
> [`w2-naive-rag`](/backlog/w2-naive-rag/)에 걸린다 — 순위 병합을 `ai/` 코드에서 계산해야 한다.
> [미결 항목](/open-items/) 참고.
