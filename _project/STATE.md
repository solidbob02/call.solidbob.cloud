# STATE — 지금 어디까지 왔는가

> 세션 인수인계용 비공개 메모. 팀이 함께 보는 기록은 `jekyll/progress.markdown`, 미결은 `jekyll/open-items.markdown`.
> 여기에는 그쪽에 적기 애매한 내부 사정만 남긴다.

**최종 갱신**: 2026-08-26 (브랜치 개명 `backend`→`ai` 완료 · 담당 분리 문서 전면 반영 / frontend 토스식 레이아웃)
**현재**: 1주차 **마감 완료** / 8스프린트 (2026-08-20 ~ 2026-10-27) → 2주차 진행 중
**전체 상태**: 🟢 1주차 목표 6개 전부 달성. 데모 도메인 4종·팀 4인 체제·골든셋 50건·
DB 스키마 도메인 정리·B-0 도메인 라우팅 설계·CI 3종·main 브랜치 보호까지 끝났다.
실제 모듈 구현(검색·마스킹·컴플라이언스·F-2)은 2주차 진행 중.
프론트: `apps/dashboard` 떠있는 흰 카드 셸. 자막 | 이용약관·충족요건. 고객 화면은 009로 철회.

**백엔드 디렉터리가 바뀌었다 (2026-08-26)** — `fastapi/` 를 둘로 나눴다.

```
server/   요청이 흐르는 길   계약(포트·DTO)·파이프라인 배선·클린 아키텍처   → server.solidbob.cloud
ai/       품질을 만들고 재는 쪽   청킹·BM25·리랭크·모델 학습·평가 하네스     → ai.solidbob.cloud
```

의존 방향은 **ai → server 한쪽뿐**이다(evaluation 이 hub 계약을 import). 역방향은
`server/.importlinter` 계약 2 가 막는다. 각 디렉터리에 영역 규칙 `CLAUDE.md` 가 있다.
아래 이전 세션 기록의 `fastapi/` 경로는 **그 시점의 사실**이므로 고치지 않았다.

> ✅ **해결됨.** CI job 이름 `backend` → `server` + `ai` 에 맞춰 main 룰셋도 이미
> `[server, ai, jekyll]` 로 바뀌어 있다(2026-08-26 확인).
> `gh api repos/solidbob02/call.solidbob.cloud/rules/branches/main` 으로 확인 가능.

**브랜치 이름도 담당 디렉터리에 맞췄다 — 양쪽 다 완료 (2026-08-26).**
장민석 님이 `ai`→`server`(PR #28)를 먼저, 류준이 `backend`→`ai`(PR #31, `decisions/015`)를 이어서.

```
류준    브랜치 ai      ←  디렉터리 ai/       (구 브랜치 backend, 삭제됨)
장민석   브랜치 server  ←  디렉터리 server/   (구 브랜치 ai)
정성윤   브랜치 PM      조서희  브랜치 frontend
```

> ⚠ **`ai` 라는 이름이 사람을 갈아탔다.** 아래 2026-08-26 이전 세션 기록에 나오는
> `ai` 브랜치는 **장민석**, `backend` 는 **류준**이다. 그날 이후의 `ai` 는 류준이다.
> 옛 기록은 그 시점의 사실이라 고치지 않았다(절대 원칙 8).

> 필수 통과 검사 이름은 `test.yml` 의 **job 이름**이지 브랜치 이름이 아니다 —
> 브랜치를 개명해도 룰셋은 손댈 필요가 없었다. `decisions/012` 가 반대로 적어 두어
> 이 정리를 하루 미뤘던 것을 `decisions/015` 에 기록해 뒀다.

## 2026-08-26 세션 (류준, 브랜치 ai) — main 동기화 + 브랜치 개명 + 담당 분리 반영

**끝낸 것**
1. `main`(`3c518de`) fast-forward — 조서희 님 대시보드 스캐폴딩 전체 + `decisions/014`(고객 화면 철회) 흡수. 충돌 0건
2. **브랜치 개명** `backend`→`ai`. 장민석 님이 `ai`→`server` 를 먼저 마쳐 이름이 비어 있었다
3. 아직 "류준·장민석 공동"으로 남아 있던 문서를 `decisions/012` 기준으로 전부 갱신

**개명에서 배운 것 — `decisions/012` 의 미룬 이유가 틀렸다.** "브랜치명을 바꾸면 main 룰셋의
필수 통과 검사 이름까지 고쳐야 한다(admin 몫)"고 적혀 있었지만, 그 검사 이름은 `test.yml` 의
**job 이름**이다. 브랜치 이름이 걸린 곳은 push 트리거 목록 한 줄뿐이었다. 룰셋·
`branch-protection.json` 은 손대지 않았고 admin 권한도 필요 없었다.

**지우기 전에 확인한 것**: `origin/backend` 와 구 `origin/ai` 둘 다 `origin/main` 의 조상
(`git merge-base --is-ancestor`) — 미머지 0건. 되돌리려면 `git push origin main:backend`.

**곁가지로 찾은 모순 — 아직 열려 있다.** `.claude/rules/rfp-harness.md §3.1` 이
`generation`(B-4~B-6)·`compliance`(C-1~C-4)를 `server/apps/` 로 적어 뒀는데, 둘 다 모델을
로드하므로 **`server/.importlinter` 계약 2**(`torch`·`transformers`·`langchain`·`langgraph`
금지)에 걸려 거기서는 만들 수 없다. `ai/apps/` 로 정정하고 `docs/architecture.md §1` 에 근거를
남겼으나 **담당이 장민석 → 류준으로 옮겨가는 변경**이라 확인이 필요하다. `open-items` 에 올렸다.

**다음 세션이 이어받을 것**: `ai/` 2주차 B-1~B-3(트리거 판정·하이브리드 검색·리랭킹).
ES 인덱스 분리 여부 미결이 적재를 막고 있는 상태는 그대로다.

## 2026-08-26 세션 #10 (ai) — 첫 스포크 청킹 — 첫 스포크 청킹 + 브랜치 통합 준비

**끝낸 것**: `fastapi/apps/retrieval/` 스캐폴딩(chunking domain + KB loader adapter +
`scripts/index_knowledge_base.py`), `.importlinter` 다섯 목록에 `retrieval` 등록(계약 5종 KEPT),
테스트 19건 추가(pytest 45→64). 청크 102개, 두 번 돌려 바이트 단위 동일. PR #22 로 `main` 머지 완료.

**티켓 문구와 다르게 간 것**: 청킹을 "고정 길이"에서 **1 조항 = 1 청크**로 바꿨다. 조항 102개
길이 실측(중앙값 101자·최대 332자·400자 초과 0건) 결과 고정 길이로 자르면 조항이 쪼개지는 게
아니라 여러 조항이 한 청크로 뭉쳐서, 골든셋 `expected_doc_ids` 로 Recall@5 를 채점할 수 없다.

**충돌 처리 — 물러난 기록**: `w2-db-schema-domain`·`w2-domain-routing` 을 류준(13:03)과
나(13:16)가 각각 고쳤다. `CLAUDE.md` 칸반 규칙("나중에 시작한 쪽이 물러난다")에 따라 내 수정을
물리고 류준 판을 채택했다. 갈린 지점은 완료 조건이었다 — 류준 `done` / 나 `in-progress`(팀 승인·
계약 `domain` 필드를 남은 조건으로 봄). 계약 `domain` 필드 미결은 7.3절에 그대로 있다.
`main` 이 작업 중 두 번 앞서서 머지도 두 번 했다.

**모델 선정**: 사용자가 5개 역할 모델 추천을 요청해 웹 조사로 답했고(임베딩 KoE5 교체 근거는
`ko-sroberta` 의 `max_seq_length=128` — 우리 청크의 15~28% 가 잘린다), 류준이 이를 독립 검증해
`_project/decisions/010-AI-모델-구성-확정.md` 로 확정했다. 내 세션에서 문서를 쓰지는 않았다.

**브랜치 통합 준비 (→ 통합하지 않기로 결정됨, 2026-08-26)**: 당시 `ai` 브랜치에 고유
커밋이 0건이라 지워도 잃을 것이 없는 상태였고 통합을 준비했으나, 팀은 **네 브랜치를 그대로
유지**하기로 정했다 — 충돌 원인은 브랜치 수가 아니라 같은 티켓 동시 수정이라는 판단.
근거: `_project/decisions/011-브랜치-정책과-main-보호.md`. `main` 보호 설정은 별도로 적용됐다.

**다음 세션이 확인할 것**: 브랜치 통합 방식 확정(팀 결정 사항, `_project/decisions/` 대상).
그리고 `w2-naive-rag` 는 ES 인덱스 분할 결정이 나야 착수할 수 있다.

## 2026-08-26 (이어서) — 상담원 대시보드 (`frontend`)

`apps/dashboard` 떠있는 흰 카드 셸(웜그레이 그라데이션). 자막 자동 스크롤 | 이용약관·충족요건. F-2는 카드 안 체크리스트, approved만 「종결 처리」.
칸반은 `/kanban/` 사이드바 전환. 고객 화면은 009로 철회.

## 2026-08-26 세션 (이어서 5) — backend·main(ai 경유) 통합

GitHub에서 `backend`→`main` PR이 충돌났다(사용자가 스크린샷으로 확인 요청). 원인 파악:
`ai` 브랜치(정성윤·장민석)가 내 이전 푸시 지점(`a0f95d3`)에서 갈라져 `fastapi/` 헥사고날
아키텍처(hub-스포크, import-linter 계약 5종, DTO/포트/유스케이스)를 독자적으로 구축했고
`docs/architecture.md`·`domain.md`·`harness.md`를 새로 썼다. `docs/domain.md`는 내
`_project/decisions/004`를 근거로 삼고 있어 이어받은 작업이 맞지만, 갈라진 시점 이후의
내 작업(골든셋 재작성·DB 스키마 정리·B-0 도메인 라우팅)은 전혀 모른 상태였다.

**AskUserQuestion으로 확인**: fastapi/ 구조를 정본으로 채택하고 내 작업물을 그 위에
포팅하기로 확정(사용자 승인).

**실제로 한 일**: `git merge origin/main` 실행 후 충돌 5건(rfp-harness.md, w1-dashboard
-scaffold.md, w1-db-schema.md, progress.markdown, knowledge-base/README.md) 수동 해결
+ 파일 위치 충돌 2건(domain_routing.py 관련) + modify/delete 충돌 2건(harness.py,
test_harness.py — main에서 ai/apps/evaluation/으로 이미 이동됨). golden-set/v1-10.json과
db/schema.sql 계열은 main이 그 시점 이후 안 건드려서 3-way 병합이 자동으로 내 버전을
채택함(충돌 없음) — 확인 완료.

포팅 작업: `fastapi/hub/app/dtos/domain_classification_dto.py` +
`fastapi/hub/app/ports/output/domain_routing_port.py`(기존 6개 포트와 같은 ABC 패턴,
async — 컴플라이언스 포트와 동급) 신규 작성, `harness.py`에 `DomainRoutingPort` 배선,
`domain_routing.py` 메트릭 그대로 이식, 테스트 이식(import 경로 수정 + async 가짜 포트
배선 테스트 추가). `services/core/` 디렉토리 완전 삭제(`__pycache__`만 남아있었음).

**검증**: `cd server && pytest` 45개 전부 통과(main 37개 + 내 도메인 라우팅 8개),
`lint-imports --config .importlinter` 5개 계약 전부 KEPT(내 새 포트가 아키텍처 경계를
위반하지 않음 확인), 지킬 빌드 + 링크 검사(52페이지, 깨진 링크 0) 통과.

**그 밖에 정리한 것**: `jekyll/docs/03-아키텍처.markdown`·`data/README.md`·
`golden-set/README.md`의 남은 `services/core` 참조를 `fastapi/`로 갱신(현재 상태를
설명하는 살아있는 문서만 — `progress.markdown`·`decisions/`·과거 티켓의 역사적 기록은
그 시점 사실이므로 안 건드림).

**다음 세션이 확인할 것**: 커밋·푸시 여부(사용자 확인 대기 중). 이후 실제 스포크 구현
(검색·마스킹·컴플라이언스·F-2·게이트웨이·대시보드)이 2주차 본작업.

## 2026-08-26 (이어서) — 브랜치 개편: flutter → ai

사용자가 원격 `flutter` 를 지우고 **`ai`** 브랜치를 만들었다. 백엔드·AI 를 류준·장민석이
공동으로 맡는 4인 체제와 맞물린 변경이다.

```
현재 원격:  main · PM · backend · ai · frontend
```

- `ai` 는 `main`(a0f95d3) 과 동일한 지점에서 출발
- **CI 트리거에 `ai` 가 빠져 있어 추가했다** — `test.yml` 의 `branches` 목록이
  아직 `flutter` 를 가리키고 있어서, 그대로 뒀으면 `ai` 푸시에 테스트가 돌지 않았다
- `CLAUDE.md` 브랜치 규칙, `pages.yml` 주석, `w1-eval-ci` 티켓도 함께 갱신
- 과거 기록(`progress.markdown`, `decisions/005`, `rev4-보완지시서`, `w1-repo-integration`)의
  `flutter` 언급은 **그 시점의 사실이므로 고치지 않았다**

## 2026-08-26 세션 (이어서) — 팀 개편 4인 체제

같은 세션에서 사용자가 팀 변경도 통보: 플러터 앱 중단, 장민석이 류준과 함께 백엔드·AI로
합류, 조서희 신규 합류(프론트엔드 전담), 정성윤은 그대로 AWS·인프라.

**끝낸 것**: `CLAUDE.md`(팀 섹션, 커밋 브랜치 컨벤션, 칸반 티켓 예시), `.claude/rules/
rfp-harness.md`(R&R 표), `.claude/rules/dashboard.md`(담당자), `.claude/agents/
code-reviewer.md`(스택 목록에서 Flutter 제거), `jekyll/docs/07-역할분담.markdown`(7.1·7.2
전면 수정), `jekyll/docs/14-이번주할일.markdown`, `jekyll/kanban.markdown`(범례·역할
라벨), `.github/workflows/pages.yml`(주석), `_project/rev4-보완지시서.md`(10번 항목),
`_project/decisions/005-팀-개편-4인-체제.md`, `progress.markdown`·`open-items.markdown`.

**의도적으로 건드리지 않은 것**: 기존 칸반 티켓의 `assignee`(작성 당시 실제 담당자
기록이므로 소급 수정 안 함), `origin/flutter` 원격 브랜치(삭제는 사용자 확인 필요 —
히스토리 보존 목적으로 남겨둠), `jekyll/sprints/01-sprint1.markdown` 등 과거 진행 로그
(그 시점 사실 그대로 유지).

**다음 세션이 확인할 것**: 류준·장민석 사이 백엔드·AI 세부 분담 — 2026-08-26 같은 날
사용자가 "기능별로 나누지 않고 둘이 함께 한다"고 확정해 해소됨(아래 참고).

## 2026-08-26 세션 (이어서 2) — 골든셋 재작성 + 대시보드 티켓 정정

사용자가 "백엔드·AI는 둘이 같이 한다"고 확정(세부 분담 논의 불필요) → `open-items.markdown`
반영. 이어서 "오늘 할 일" 질문에 답하며 파악한 두 가지를 실행: `w1-dashboard-scaffold.md`
담당자를 장민석 → 조서희로 정정(팀 개편 반영), `golden-set/v1-10.json`을 4개 도메인
기준으로 전면 재작성(`services/core/eval/golden_set.py`에 `domain` 필드 파싱 추가, 테스트
2건 추가, `pytest services/core` 27개 통과). 커밋 `d6e2061` → 푸시 중 정성윤의 CI 워크플로
커밋(`w1-eval-ci.md` 완료 반영)과 충돌해 병합(`0935d1b`) 후 재푸시.

## 2026-08-26 세션 (이어서 3) — DB 스키마 도메인 정리

사용자 요청: "DB 스키마가 4개 도메인에 맞게 잘 됐는지 확인하고, 남은 다른 도메인
내용은 정리해달라." 실제로 확인해보니 `plan`(요금제)·`subscriber`의 체납·분실신고
플래그·`closure`의 evidence 7컬럼이 전부 통신 도메인 가정(TERM-5.3 등 지금은 없는
문서 ID 참조)이었다.

**끝낸 것**: `db/generate_schema_docs.py`(TABLES 정의 — `plan` 제거, `subscriber`→
`customer`로 정리, `call`에 `domain` ENUM 컬럼 추가, `closure.closure_type`/evidence
컬럼을 금융보험(상품해지·보상)·쇼핑(반품·교환) 기준으로 교체) 수정 후 재실행해
`schema.sql`·`erd.dot`·`ERD.png` 재생성(17→16개 테이블). `db/docs/ERD.md`·`jekyll/docs/16`
프로즈 전면 갱신, `jekyll/docs/07` 인터페이스 계약 JSON 예시도 새 스키마 값으로 교체,
`services/core/tests/test_closure_gate_metrics.py` 필드명 동기화 — `pytest services/core`
27개 계속 통과. 결정 기록 `_project/decisions/006-db-스키마-도메인-정리.md`.

**의도적으로 남겨둔 것**: `call.domain`을 실제로 언제·어떻게 채울지(도메인 라우팅
로직)는 여전히 미결 — [3.2절](/docs/03/), `open-items.markdown`. `closure` evidence를
넓은 표로 둘지 EAV로 둘지도 기존부터 있던 미결 항목으로 이번에 해소되지 않음. 실제
MySQL 마이그레이션 적용은 아직 착수 전(설계 문서 단계).

**다음 세션이 확인할 것**: 커밋·푸시 여부(사용자가 아직 명시적으로 요청하지 않았다면
대기).

## 2026-08-26 세션 (이어서 4) — 지식베이스 팀 리뷰 완료 + 도메인 라우팅 자동 분류 확정

사용자 통보: "지식베이스 팀 회의로 리뷰 마무리, 도메인 라우팅은 자동 분류로 간다,
진행해줘." `w1-knowledge-base.md` done 처리. 도메인 라우팅은 설계(KcELECTRA 분류기 +
하이브리드 검색 폴백, 새 도구 없음)를 확정하고 **평가 하네스에 실제로 배선**했다 —
`services/core/eval/metrics/domain_routing.py`(정확도+오분류행렬), `harness.py`에
`DomainPredictor` Protocol(B-0) 추가, 골든셋 `domain` 필드를 그대로 재사용. 테스트
6건 추가, `pytest services/core` 33개 통과. `jekyll/docs/01,02,03,06`·`open-items.markdown`
반영, 결정 기록 `_project/decisions/007`, 신규 티켓 `w1-domain-routing.md`.

**의도적으로 안 한 것**: 실제 분류기 학습(데이터 부족), B-2 하이브리드 검색 자체(아직
없음 — 폴백의 전제 조건).

**다음 세션이 확인할 것**: 커밋·푸시 여부.

## 2026-08-26 세션 — 데모 도메인 4종 전환

사용자가 "실제 구할 수 있는 데이터가 금융보험·다산콜센터·쇼핑·질병관리본부로 한정돼
있으니 이 도메인으로만 한정하라"고 지시. 조사해보니 가상 통신사 "한별텔레콤" 지식베이스는
**대조할 실제 데이터가 아예 없었던** 반면, AI Hub 「민원(콜센터) 질의-응답」데이터셋은
정확히 이 4개 도메인으로 실측 라벨링돼 있었음(`data/raw/aihub-minwon-qa/`).

`AskUserQuestion`으로 "4개 전부 지원 vs 1개만 선택 vs 1개+나머지 시연용" 중 확인 →
**4개 전부 지원**으로 확정.

**이번 세션에서 끝낸 것**: `knowledge-base/` 도메인별 4폴더 재구성(각 terms/manual/
policy, 도메인 접두어 ID), `CLAUDE.md`·`rev4-보완지시서.md`(9번 항목)·`jekyll/docs/
01,02,04,05,06,07,09,14,15,16`·`data/README.md`·`knowledge-base/README.md` 갱신,
결정 기록 `_project/decisions/004`, 칸반 티켓 2건(`w1-knowledge-base.md`,
`w1-golden-set-10.md`) 갱신, `progress.markdown`·`open-items.markdown` 반영.

**다음 세션이 이어받아야 할 것**:
1. **골든셋 재작성** — 기존 10개는 무효(구 문서 ID 참조). 4개 도메인 비율 팀 컨펌 필요
2. **DB 스키마·ERD 재검토** — `subscriber`/`plan`, `closure` evidence 컬럼이 아직 통신
   도메인 가정. 스키마 변경이 필요한 엔지니어링 작업이라 이번 세션에서 의도적으로
   미룸([16절 ERD](/docs/16/)의 경고 박스 참고)
3. `jekyll/docs/03-아키텍처.markdown`은 이번 세션에서 확인/수정하지 못했다 — 도메인
   라우팅 로직이 들어갈 자리인지 다음 세션에서 점검할 것
4. `ai/apps/evaluation/`의 골든셋 로더·지표 계산이 `domain` 필드를 다루도록 돼 있는지
   미확인 — 코드베이스 자체는 아직 확인 전

---

## 저장소 통합 결과 (2026-08-25)

`origin/main`(PM 계열)과 `origin/backend`(류준)는 **공통 조상이 없는 별개 히스토리**였다.
`integrate-backend` 브랜치에서 파일별로 정본을 정해 합쳤다.

| 영역 | 정본 | 이유 |
|---|---|---|
| 지킬 사이트 | **backend** | 사업명·팀명·기간 등 사실 정보 정확, 기획서 16개 절 1:1, 자체 레이아웃, 빌드 성능 수정 |
| ERD·스키마 | **backend `db/`** | 실행 가능한 DDL, 팀 교차검증 완료 |
| `CLAUDE.md` | **병합** | backend 사이트 컨벤션 + PM 계열 절대 원칙·기록·커밋 규칙 |
| `.gitignore` | **backend** + 개인 설정 한 줄 | Python·Node·macOS·자격증명 안전망 |
| `.claude/` | **PM 계열** + backend 고유 규칙 2개 | 외부 저장소 유래 파일은 다시 들이지 않음 |
| `_project/`, `.github/` | **PM 계열** | backend에 없던 것 |

버려진 것(히스토리에는 남음): PM 계열 지킬 사이트(표지+5개 절+`_posts`/`_data`),
`docs/erd/`(Mermaid ERD + 정규화 문서), `docs/kb-ingest.md`, `docs/golden-set/` 양식.

---

## 확인된 전제 (backend 기록에서)

| # | 결과 |
|---|---|
| V1 채널 구성 | **모노** — diarization 필수, 데모는 물리 2채널(브라우저 2대)로 우회 |
| V2 GPU | **Apple M5 MacBook Air 24GB, CUDA 없음(MPS)** — 소형 모델(polyglot-ko-1.3b 등)로 대응 |
| V3·V4 | 미확인 — Google STT 결제 계정 연결 필요, **팀 카드 결정 대기** |

---

## 다음 작업

1. **기획서 정본 확정** ⚠ — 사이트 문서(`jekyll/docs/01~16`)는 **5인 트랙 rev.4**, `_project/plan.md`는 **3인 실명 rev.4**다.
   트리거 허용 창(800ms vs 1,500ms), 팀 분업표가 서로 다르다. 어느 판을 정본으로 할지 정한 뒤 한쪽으로 맞춘다.
2. **GitHub Pages 활성화** — Settings → Pages → Source: GitHub Actions. `solidbob02` 계정 권한이라 사용자가 직접 해야 한다.
3. **AI Hub 데이터 신청** — `open-items.markdown` 기준 아직 미완료. 팀원 한 명이 진행 중이라고 들었으므로 현황 확인 필요.
4. **인터페이스 스키마 3종 확정** — 초안은 기획서 7.3절. 팀 컨펌 대기.
5. **평가 하네스 CI 연결** — 하네스 골격은 류준이 완료(테스트 24개 통과). CI는 정성윤 담당. `.github/workflows/test.yml`은 2026-08-26에 `fastapi/` 기준(working-directory, Python 3.13, import-linter step, `ai` 브랜치 추가)으로 갱신됨.
6. **백엔드 루트 `fastapi/` + 허브-스포크 (2026-08-26, `ai` 브랜치)** — `services/core/eval`→`fastapi/evaluation`, `hub/`에 `transcript_ingest`·`myself` 슬라이스(프랙탈 단면), 계약 5종 `server/.importlinter` 통과, 테스트 37개. `backend` 브랜치의 stash는 `ai`에 복원 후 삭제. 스포크 0개 — `POST /hub/transcripts`는 masking 스포크가 꽂히기 전까지 501.
7. **첫 스포크 착수 순서** — `masking`(정성윤, P1~P5) → `retrieval`(류준·장민석, B-1 트리거 is_final 기반 + B-2 + **도메인 라우팅**). 각 스포크는 `docs/architecture.md §3` 단면대로, `apps/hub/app/ports/output/<이름>_port.py` 구현, `main.py` `dependency_overrides`와 `evaluation.harness.Ports(...)` 양쪽에 꽂고 `.importlinter` 다섯 목록에 이름 추가.
8. **도메인 4종이 백엔드에 미친 것** — `ClosureType`은 `str`(도메인별 처리유형), `docs/domain.md` 재작성 완료. 아직 안 된 것: 7.3절 계약에 `domain` 필드(v3), `golden_set.py` 로더 `domain` 필드, 도메인 라우팅 설계, `closure` DDL. F-2 규칙(verdict/missing ↔ evidence)은 `closure_gate/domain/services` 몫.

---

## 내부 메모

- 이 저장소는 두 사람이 서로 모르고 같은 작업을 한 이력이 있다(사이트·ERD·골든셋 양식). **작업 전에 `jekyll/progress.markdown`을 먼저 읽는다.**
- backend의 `Gemfile.lock`은 macOS 기준이라 이 WSL에서는 `bundle install`을 한 번 돌려야 빌드된다(sass-embedded 버전 차이).
- 로컬 지킬 포트 (2026-08-26 정리): **이 저장소 = 4000**, `com.minseok.callguard/jekyll`(같은 프로젝트의 다른 클론) = 4200, `com.redoceanmap/blog` = 4100. 셋 다 `--detach`로 떠 있음 — `lsof -nP -iTCP:4000 -sTCP:LISTEN`으로 확인.
- 원격 인증: `gh` = SeongYuna (협업자, push 가능 / admin 아님). 저장소 설정 변경은 solidbob02만.
