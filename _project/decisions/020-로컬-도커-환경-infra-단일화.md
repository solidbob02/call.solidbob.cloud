# 020 — 로컬 도커 환경을 `infra/` 하나로 합치고 ES 를 9.5.1 로 맞춘다

**날짜**: 2026-08-27
**작성**: 장민석 (브랜치 `server`)
**관련**: `_project/decisions/017`(ES 인덱스 단일화) · `_project/decisions/018`(PostgreSQL 전환)

## 맥락

`ai` 브랜치를 병합하면서 **Elasticsearch 로컬 구성이 둘이 됐다.**

| | 저장소 루트 `docker-compose.yml` (류준) | `infra/docker-compose.yml` (장민석) |
|---|---|---|
| ES 버전 | 9.5.1 | 8.15.3 |
| nori | 기동 시 `elasticsearch-plugin install` | `infra/elasticsearch/Dockerfile` 로 이미지에 굽기 |
| 포트 | `9200` (0.0.0.0) | `127.0.0.1:9200` |
| 함께 뜨는 것 | ES 만 | PostgreSQL + ES |

둘 다 9200 을 잡아 **동시에 뜨지 않는다.** 류준 님도 로그에 "`infra/` 가 아직 없어 루트에
뒀다, 생기면 옮기는 건 그쪽 판단"이라고 남겼고, `infra/` 는 그 뒤에 생겼다.

## 선택지

1. **루트 compose 를 살리고 `infra/` 의 ES 를 뺀다** — DB 와 ES 를 따로 띄워야 한다. 명령이 둘이 되고,
   `infra/` 가 인프라 디렉터리라는 규칙(`.claude/rules/rfp-harness.md` §2)과 어긋난다
2. **`infra/` 로 합치고 ES 8.15.3 을 유지한다** — `ai/requirements.txt` 의 `elasticsearch==9.5.0` 을
   8.x 로 내려야 한다
3. **`infra/` 로 합치고 ES 9.5.1 로 올린다** ← 채택

## 결정

**`infra/docker-compose.yml` 하나. ES 는 9.5.1, nori 는 이미지에 굽는다, 포트는 `127.0.0.1` 바인딩.**
저장소 루트의 `docker-compose.yml` 은 삭제했다.

```bash
cd infra && docker compose up -d      # PostgreSQL 17 + ES 9.5.1(nori) 가 함께 뜬다
```

## 근거

**버전 — 클라이언트가 정했다. 실측이다.** `ai/requirements.txt` 가 `elasticsearch==9.5.0` 을
고정하고 있고, 9.x 클라이언트는 8.x 서버에 **접속 자체를 거부한다**:

```
BadRequestError(400, 'media_type_header_exception',
  'Accept version must be either version 8 or 7, but found 9')
```

같은 클라이언트로 9.5.1 서버에는 붙는다. 선택지 2(클라이언트를 8.x 로 내림)도 가능하지만,
**낮은 쪽으로 맞출 이유가 없었다** — 8.15.3 은 내가 고를 때 특별한 근거 없이 잡은 값이고,
9.5.1 에서 필요한 것이 전부 동작하는 것을 확인했다(아래).

**위치 — `infra/` 가 인프라 디렉터리다.** 로컬 환경을 한 명령으로 세우는 것이 이 폴더의 목적이고,
DB 와 ES 를 따로 띄우게 두면 "팀원 누구나 같은 상태를 만든다"가 깨진다.

**nori 설치 방식 — 이미지에 굽는다.** 기동 때마다 설치하면 컨테이너를 새로 만들 때마다
네트워크가 필요하고 기동이 느리다. 류준 님도 루트 compose 주석에 "오프라인이 잦아지면 그때
Dockerfile 로 빼서 굽는다"고 적어 두었다 — 같은 판단이다.

## 확인한 것 (실측, 2026-08-27)

- ES **9.5.1** + `analysis-nori` 9.5.1 기동, 라이선스 `basic active`
- `nori_tokenizer` + `dense_vector`(1024차원, cosine) 매핑이 한 인덱스에서 동작
- 지식베이스 실적재 **102건**(`callguard-kb-single`), 같은 명령 재실행 시 재현
- `ai` 통합 테스트 5건이 **skip → 통과** (`.venv` 에 `elasticsearch==9.5.0` 설치 후)
- BM25 검색 동작 (`"반품 배송비"` → `SHOP-TERM-4.2` 9.98)

## ⚠ 함께 드러난 것 — RRF 는 basic 라이선스에서 막힌다

기획서 3.1절이 지정한 `nori(BM25) + dense_vector + **RRF**` 중 **RRF 만 유료 기능**이다.
ES 의 `retriever.rrf` 는 **8.15.3·9.5.1 양쪽 모두** basic 에서 거부된다:

```
403 security_exception
current license is non-compliant for [Reciprocal Rank Fusion (RRF)]
```

30일 trial(`POST /_license/start_trial?acknowledge=true`)에서는 동작하는 것을 확인했지만
**만료가 2026-09-26 이라 프로젝트 종료(10-27)를 못 넘긴다.** 클러스터당 한 번만 켤 수 있다.

**이 결정으로 해결되지 않는다 — 버전을 올려도 마찬가지다.** 순위 병합은 ES 기능이 아니라
`ai/` 검색 코드에서 계산해야 한다(RRF 는 `1/(k+rank)` 합이라 구현 자체는 몇 줄이고,
평가 하네스 입장에서는 오히려 **재현 가능**해진다). `w2-naive-rag`(B-1~B-3) 담당인
류준 님 결정 사항이라 여기서는 미결로만 올렸다. **BM25·kNN·nori·`dense_vector` 는 basic 에서 전부 된다.**

## 되돌리는 법

- 버전만 되돌리려면: `infra/elasticsearch/Dockerfile` 의 `ARG ES_VERSION` 과
  `ai/requirements.txt` 의 클라이언트 핀을 **같이** 바꾼다. 한쪽만 바꾸면 붙지 않는다
- 파일을 다시 가르려면: `infra/docker-compose.yml` 의 `elasticsearch` 서비스를 잘라
  루트 `docker-compose.yml` 로 옮긴다. 포트가 겹치므로 한쪽은 `ELASTICSEARCH_PORT` 를 바꿔야 한다
