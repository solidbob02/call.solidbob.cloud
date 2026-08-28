# CLAUDE.md — ai/

**품질을 만들고 재는 쪽.** 데이터셋으로 모델을 학습하고, 문서를 청킹하고, 검색·리랭킹을 하고,
그 결과를 규칙 기반으로 채점한다.
저장소 전체 규칙은 루트 `../CLAUDE.md` 가 우선하고, 이 파일은 그 아래에서 `ai/` 안의 일만 다룬다.

배포 대상: `ai.solidbob.cloud`

---

## 0. 이 디렉터리가 하는 일 / 하지 않는 일

| | |
|---|---|
| **한다** | 데이터셋 기반 모델 학습·평가 · 지식베이스 청킹 · BM25 · 임베딩 · 리랭킹 · 하이브리드 검색(RRF) · 랭그래프/랭체인 오케스트레이션 · 평가 하네스 |
| **하지 않는다** | HTTP 라우팅 · 요청 인증 · DB 저장 · 설정·비밀 관리 · C-5 마스킹 · F-2 종결 게이트 |

아래쪽은 `../server/` 다. **경계가 헷갈리면 이렇게 판단한다.**

```
"품질을 만들거나 재는 코드인가?"              → 예: ai/
"요청 하나를 처리하는 데 반드시 실행되는가?"   → 예: server/
```

C-5 마스킹과 F-2 게이트가 여기 없는 이유: **둘 다 규칙 기반 판정**이고 요청 경로에서 매번
실행된다. 모델이 관여하지 않으므로 `server/` 다(루트 절대 원칙 9).

---

## 1. 의존 방향 — 한쪽뿐이다

```
ai/  ──(hub 포트·DTO를 import)──▶  server/
server/  ──✗──▶  ai/            (금지)
```

`server/apps/hub` 가 포트(추상)를 정의하고 **여기서 그것을 구현한다.**
`pytest.ini` 와 `.importlinter` 가 `../server/apps` 를 경로에 올리는 이유가 이것이다 —
구조 문제가 아니라 경로 문제라서 경로만 이어 준다.

**포트 시그니처를 바꾸고 싶으면 `../server/` 를 고쳐야 한다.** 여기서 우회 정의를 만들지 않는다.
계약이 두 벌이 되는 순간 어느 쪽이 진짜인지 알 수 없게 된다.

---

## 2. 구조

```
ai/
  apps/
    retrieval/          B-1~B-3 검색
      domain/           청킹 규칙 · 랭킹 산식 — 순수 파이썬
      adapter/outbound/ 지식베이스 로더 · ES 색인(es_index.py) · (예정) 모델 로더
      tests/
    evaluation/         E-1~E-4 평가 하네스
      golden_set.py     골든셋 로더
      harness.py        hub 포트를 소비해 각 모듈을 채점
      metrics/          retrieval · trigger · masking · compliance · closure_gate · domain_routing · latency
      tests/
  provider.py           **합성 루트** — server/main.py 가 스포크를 꽂는 지점
  tests/                합성 루트 전용 (모듈끼리 못 보는 것을 여기서 교차 검증)
```

**`provider.py`·`tests/` 가 `apps/` 밖에 있는 이유**: `retrieval`·`evaluation` 은
서로를 import 할 수 없다(`.importlinter` 계약 2 — **테스트도 계약 대상이다**). 두 모듈을
동시에 아는 코드는 계약 밖에 둔다. `server/main.py`·`server/tests/` 와 같은 자리다.

**예정 모듈** — 실제로 만들 때 `.importlinter` 의 `root_packages` 와 계약 1·2 목록에 추가한다.

| 모듈 | 내용 | 요구 ID |
|---|---|---|
| `generation` | 근거 기반 카드 생성 · 출처 표시 | B-4~B-6 |
| `compliance` | 컴플라이언스 탐지 분류기 | C-1~C-4 |
| `orchestration` | 랭그래프 파이프라인 | — |

~~`training` 은 2026-08-27 에 만들어졌다(B-0 분류기).~~
**2026-08-28 삭제됐다** — 다산 단일 도메인이 되어 분류할 도메인이 없다(`_project/decisions/201`).
학습 코드·KcELECTRA 파인튜닝 어댑터·`scripts/train_domain_classifier.py` 가 함께 지워졌고
`.importlinter` 의 `root_packages` 에서도 빠졌다. 되돌리려면 git 이력에서 꺼낸다.

⚠ **모델 학습이 `ai/` 에서 완전히 사라진 것은 아니다.** A-3(동시 통번역)·C-6(콜 가드)·
D(감정분석)가 모델을 쓰므로, 새 학습 모듈이 필요해지면 그때 `root_packages` 에 다시 넣는다.

---

## 3. 절대 지킬 것

1. **LLM 을 채점자로 쓰지 않는다.** 모든 평가 지표는 규칙 기반으로 계산해 재현 가능해야 한다.
   `.importlinter` 계약 3 이 `evaluation` 에서 모델 라이브러리 import 를 금지해 이것을 구조로 고정한다.
2. **측정하지 않은 수치를 기록하지 않는다.** 미구현 모듈은 `"측정 불가 — 모듈 미구현"` 으로 보고한다.
   이 정직성을 우회하는 기본값·더미 점수를 넣지 않는다.
3. **기준선은 여러 번 실행한 값 중 최저치로 고정한다.** 평균이 아니다.
4. **알고리즘은 `domain/` 에, 라이브러리 호출은 `adapter/` 에.** 청킹 규칙과 랭킹 산식은 순수
   파이썬이어야 한다. Elasticsearch 를 다른 것으로 바꿔도 `domain/` 은 그대로여야 한다.
5. **모듈끼리 직접 import 하지 않는다.** 접점은 hub 포트(추상)뿐이다. 이게 깨지면 한 모듈 교체가
   전체 수정이 된다.
6. **자체 통화 녹음을 쓰지 않는다.** AI Hub 등 저작권·개인정보가 해결된 출처만 사용한다.

---

## 4. 검증

```bash
cd ai && pytest                                                        # 단위 테스트
cd ai && PYTHONPATH=apps:../server/apps lint-imports --config .importlinter   # 구조 계약 3종
```

CI(`.github/workflows/test.yml`)의 `ai` job 이 이 둘을 돌린다.
**job 이름은 main 브랜치 보호의 필수 통과 검사 이름이다** — 바꾸면 보호 설정이 조용히 무력화된다.

무거운 테스트는 마커로 분리한다 — `@pytest.mark.slow`(모델 로딩·학습),
`@pytest.mark.integration`(Elasticsearch·GPU·외부 LLM). 기본 실행에서는 둘 다 빠진다.
**CI 에 모델 다운로드를 넣지 않는다.** 수 GB 를 매번 받게 되고, 실패해도 원인이 코드인지
네트워크인지 알 수 없다.

---

## 5. 데이터

```
../knowledge-base/   dasan/ 하나 × terms/manual/policy (조항 20개 — 2026-08-28 `decisions/201`)
../golden-set/       골든셋 (v1-10 · v1-50 …). 도메인·발화 종료 시각·정답 문서 ID·P1~P7 패턴
../data/raw/         AI Hub 원본 (gitignore — 커밋하지 않는다)
../data/processed/   전사 결과 등 파생물 (gitignore)
```

**전사 원문과 원본 데이터에는 개인정보가 그대로 들어 있다.** 저장소에 커밋하지 않는다.
마스킹(C-5)은 `../server/` 의 책임이며, 여기서 다루는 것은 이미 처리된 데이터이거나
저작권·개인정보가 해결된 공개 데이터셋이다.

---

## 6. 담당 — 류준

`ai/` 는 **류준**이 맡는다. 브랜치도 같은 이름 `ai` 다(`_project/decisions/015`).
`../server/` 는 장민석(브랜치 `server`)이다. 근거: `_project/decisions/012`.

원래는 백엔드·AI 를 "둘이 함께"(`decisions/005`) 하기로 했으나, `fastapi/` 가 두
서브도메인으로 갈리면서 나눌 경계가 실제로 생겨 **디렉터리 경계를 담당 경계로** 삼았다.

**계약을 건드리면 양쪽이 함께 깨진다.** `../server/` 의 포트·DTO 가 바뀌면 여기가 깨지고,
여기서 포트 구현 시그니처를 임의로 바꾸면 `../server/` 의 배선이 깨진다.
그러니 계약을 손대기 전에 `../server/` 를 먼저 grep 해서 **무엇이 깨지는지 확인한다.**

합의를 절차로 요구하지는 않는다(2026-08-27, `_project/decisions/023`). 네 사람이 **같은 공간에서
일하므로 필요하면 그 자리에서 말로 맞춘다.** 규칙이 할 일은 "무엇이 깨지는지 먼저 보라"까지다.
