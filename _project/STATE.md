# STATE — 지금 어디까지 왔는가

> 세션 인수인계용 비공개 메모. 팀이 함께 보는 기록은 `jekyll/progress.markdown`, 미결은 `jekyll/open-items.markdown`.
> 여기에는 그쪽에 적기 애매한 내부 사정만 남긴다.

**최종 갱신**: 2026-08-26 (세션 #9 fastapi 통합 + frontend 대시보드)
**현재**: 1주차 / 8스프린트 (2026-08-20 ~ 2026-10-27), 사실상 마무리 → 2주차 전환 직전
**전체 상태**: 🟢 1주차 핵심 항목 거의 완료. 데모 도메인 4종·팀 4인 체제·골든셋 재작성·
DB 스키마 도메인 정리·B-0 도메인 라우팅 설계까지 끝났고, `ai` 브랜치가 구축한
`fastapi/` 헥사고날 아키텍처로 전부 통합 완료. 실제 스포크 구현(검색·마스킹·컴플라이언스
·F-2)은 2주차부터 착수.
프론트: `apps/dashboard` mock 4도메인 + F-2 실시간 패널. 고객 화면은 009로 철회.

## 2026-08-26 (이어서) — 상담원 대시보드 (`frontend`)

`apps/dashboard` 스캐폴딩 완료(자막 2fr | 경고 1fr + 하단 책갈피). F-2 evidence는
§2.7 필드명. blocked는 경고 아래 실시간 표시, approved만 모달. 티켓
`w1-dashboard-scaffold-seohee` done. 고객 화면 006/007 번호는 팀 ADR과 겹쳐
008(확정 후 철회)·009(재철회)로 옮김.

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
test_harness.py — main에서 fastapi/evaluation/으로 이미 이동됨). golden-set/v1-10.json과
db/schema.sql 계열은 main이 그 시점 이후 안 건드려서 3-way 병합이 자동으로 내 버전을
채택함(충돌 없음) — 확인 완료.

포팅 작업: `fastapi/hub/app/dtos/domain_classification_dto.py` +
`fastapi/hub/app/ports/output/domain_routing_port.py`(기존 6개 포트와 같은 ABC 패턴,
async — 컴플라이언스 포트와 동급) 신규 작성, `harness.py`에 `DomainRoutingPort` 배선,
`domain_routing.py` 메트릭 그대로 이식, 테스트 이식(import 경로 수정 + async 가짜 포트
배선 테스트 추가). `services/core/` 디렉토리 완전 삭제(`__pycache__`만 남아있었음).

**검증**: `cd fastapi && pytest` 45개 전부 통과(main 37개 + 내 도메인 라우팅 8개),
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
4. `fastapi/apps/evaluation/`의 골든셋 로더·지표 계산이 `domain` 필드를 다루도록 돼 있는지
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
6. **백엔드 루트 `fastapi/` + 허브-스포크 (2026-08-26, `ai` 브랜치)** — `services/core/eval`→`fastapi/evaluation`, `hub/`에 `transcript_ingest`·`myself` 슬라이스(프랙탈 단면), 계약 5종 `fastapi/.importlinter` 통과, 테스트 37개. `backend` 브랜치의 stash는 `ai`에 복원 후 삭제. 스포크 0개 — `POST /hub/transcripts`는 masking 스포크가 꽂히기 전까지 501.
7. **첫 스포크 착수 순서** — `masking`(정성윤, P1~P5) → `retrieval`(류준·장민석, B-1 트리거 is_final 기반 + B-2 + **도메인 라우팅**). 각 스포크는 `docs/architecture.md §3` 단면대로, `apps/hub/app/ports/output/<이름>_port.py` 구현, `main.py` `dependency_overrides`와 `evaluation.harness.Ports(...)` 양쪽에 꽂고 `.importlinter` 다섯 목록에 이름 추가.
8. **도메인 4종이 백엔드에 미친 것** — `ClosureType`은 `str`(도메인별 처리유형), `docs/domain.md` 재작성 완료. 아직 안 된 것: 7.3절 계약에 `domain` 필드(v3), `golden_set.py` 로더 `domain` 필드, 도메인 라우팅 설계, `closure` DDL. F-2 규칙(verdict/missing ↔ evidence)은 `closure_gate/domain/services` 몫.

---

## 내부 메모

- 이 저장소는 두 사람이 서로 모르고 같은 작업을 한 이력이 있다(사이트·ERD·골든셋 양식). **작업 전에 `jekyll/progress.markdown`을 먼저 읽는다.**
- backend의 `Gemfile.lock`은 macOS 기준이라 이 WSL에서는 `bundle install`을 한 번 돌려야 빌드된다(sass-embedded 버전 차이).
- 로컬 지킬 포트 (2026-08-26 정리): **이 저장소 = 4000**, `com.minseok.callguard/jekyll`(같은 프로젝트의 다른 클론) = 4200, `com.redoceanmap/blog` = 4100. 셋 다 `--detach`로 떠 있음 — `lsof -nP -iTCP:4000 -sTCP:LISTEN`으로 확인.
- 원격 인증: `gh` = SeongYuna (협업자, push 가능 / admin 아님). 저장소 설정 변경은 solidbob02만.
