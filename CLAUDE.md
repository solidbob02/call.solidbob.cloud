# CLAUDE.md — CallGuard

이 저장소는 **CallGuard 모노레포**다. 지킬 사이트는 블로그가 아니라 **개발 제안서를 문서화하는 사이트**이며,
`services/`·`apps/`·`infra/`(코드)와 섞이지 않게 **`jekyll/` 하위에 격리**돼 있다.
`data/`·`models/`·`knowledge-base/`·`golden-set/`·`db/`·`services/`는 지킬 사이트가 아니라 저장소 루트의 프로젝트 산출물이다.

---

## 0. 세션 시작 루틴 (모든 세션의 첫 3분, 예외 없음)

```
1. CLAUDE.md                  ← 지금 이 파일 (규칙)
2. jekyll/progress.markdown   ← 팀 전체가 보는 진행 기록. 최신 항목이 맨 위
3. _project/STATE.md          ← 세션 인수인계용 현재 상태 (비공개)
4. jekyll/open-items.markdown ← 아직 정하지 못한 것
```

이 4개를 읽기 전에 코드를 건드리지 않는다. 사용자가 다른 지시를 하면 그것이 우선하고, 대신 위 문서를 그에 맞게 고친다.
코드를 건드릴 때는 `docs/harness.md`(검증 장치)·`docs/architecture.md`(계층·슬라이스 규칙)를 추가로 먼저 읽고,
**그 디렉터리의 `CLAUDE.md` 를 함께 읽는다** — `server/CLAUDE.md`(요청이 흐르는 길) · `ai/CLAUDE.md`(품질을 만들고 재는 쪽).
프론트엔드 작업은 `.claude/rules/dashboard.md`도 함께 본다.

---

## 0.5. 세션 종료 루틴 (작업이 있었던 모든 세션, 예외 없음)

```
1. jekyll/progress.markdown   ← 오늘 한 일을 항목으로 남겼는가?
2. jekyll/_backlogs/          ← 손댄 티켓의 status 를 옮겼는가? 새로 시작한 일의 티켓을 만들었는가?
3. _project/STATE.md          ← 다음 세션이 이어받을 상태를 갱신했는가?
4. jekyll/open-items.markdown ← 이번에 정하지 못하고 남긴 것을 적었는가?
```

**커밋·푸시·PR 로 세션이 끝나지 않는다. 위 4개를 확인해야 끝난다.**

- 기록을 PR 본문이나 커밋 메시지에만 쓰지 않는다. PR 은 머지되면 닫히고, 팀이 보는 것은 `/progress/` 페이지다.
  같은 내용을 두 곳에 쓰는 게 아까우면 **`progress.markdown` 을 먼저 쓰고 PR 본문에 옮긴다** — 반대 방향은 유실된다.
- 확인만 하고 아무것도 바꾸지 않은 세션(질문 답변·조사)은 기록하지 않아도 된다. 파일을 하나라도 고쳤으면 남긴다.
- **`Stop` 훅이 이 루틴을 강제한다.** 파일을 고쳤는데 `progress.markdown` 을 건드리지 않았으면
  세션이 끝나지 않는다(`scripts/check_session_end.py --hook`, exit 2). 같이 도는 경고 2종:
  티켓 status 정합성(②)·중복 티켓(③). 판정이 틀렸다면 `CALLGUARD_SKIP_SESSION_CHECK=1` 로 통과시킨다.
- **`session-log` 스킬**(`.claude/skills/session-log/`)이 절차를 안내한다. 훅이 막았을 때 이걸 따른다.
- CI 는 `scripts/check_progress_log.py` 로 커밋이 있는 날짜에 로그 항목이 있는지 본다(경고만, 실패시키지 않는다).

> 이 루틴이 §0 바로 아래에 있는 이유: 진행 기록 규칙(§4)은 지금까지 가장 자주 뚫린 규칙이다.
> 다른 규칙(자격증명 금지·한글 파일명 금지)은 어기면 즉시 드러나거나 CI 가 잡지만, 기록 누락은
> 어겨도 아무 일이 일어나지 않아서 조용히 밀렸다. 시작 루틴과 같이 읽히도록 붙여 둔다.

---

## 1. 프로젝트 개요

- **사업명**: CallGuard (StreamRAG : CallGuard) — 실시간 상담원 어시스트 RAG 시스템
- **팀명**: SOLIDBOB
- **팀 (2026-08-26 개편)**: 정성윤(AWS·인프라) · 류준(백엔드·AI 중 `ai/`) · 장민석(백엔드·AI 중 `server/`) · 조서희(프론트엔드, 신규 합류)
  — 백엔드·AI 는 원래 "둘이 함께"였으나, `fastapi/` 가 `server/`·`ai/` 로 갈리면서
  **디렉터리 경계를 담당 경계로** 삼았다(`_project/decisions/012`). ⚠ 브랜치 이름과
  엇갈린다 — 류준은 브랜치 `backend`에서 `ai/`를, 장민석은 브랜치 `ai`에서 `server/`를 고친다
  — 원래 3인 체제(정성윤·류준·장민석)에서 플러터 앱 개발을 접고, 장민석이 프론트엔드에서
  류준과 함께 백엔드·AI로 옮기고, 조서희가 새로 합류해 프론트엔드를 전담한다. 근거:
  `_project/decisions/005-팀-개편-4인-체제.md`
- **개발기간**: 2026-08-20 ~ 2026-10-27, 애자일 스크럼 (1주 1스프린트, 총 8스프린트)
- **한 줄**: 통화를 실시간으로 들으면서, 고객이 방금 물은 내용에 필요한 사내 문서를 상담원 화면에 자동으로 띄우고,
  컴플라이언스 위반 표현과 개인정보를 실시간으로 탐지·마스킹한다.
- 2026-08-21~24에는 같은 저장소가 AdPass(AI 광고 규제 사전검수) 기획서를 다루었고, 08-25 rev.4 반영으로 CallGuard로 전환됐다.
- **데모 도메인 (2026-08-26 확정)**: 가상 통신사 "한별텔레콤" 단일 시나리오 대신, 실제로 확보한 AI Hub
  「민원(콜센터) 질의-응답」데이터셋 기준 4개 도메인 — **금융보험 · 다산콜센터 · 쇼핑 · 질병관리본부** — 를
  전부 지원한다. 이 4개 밖의 도메인(통신 등)은 예시로도 새로 만들지 않는다. 근거·되돌리는 법:
  `_project/decisions/004-데모-도메인-4종-확정.md`.

### 기준 문서

| 문서 | 위치 |
|---|---|
| 기획서 rev.4 (3인 팀 버전) 사본 | `_project/plan.md` |
| rev.4 보완지시서 — 위에 얹히는 패치. **충돌 시 보완지시서가 우선** | `_project/rev4-보완지시서.md` |
| rev.4.1 — rev.4 + 보완지시서 병합본 (공개 사본, 도메인 4종 전환 이전 판) | `docs/plan-rev4.1.md` |
| rev.4 대안(5인 트랙 버전) | `_project/plan-rev4-alt-5인안.md` |
| 이전 판 | `_project/plan-rev1-initial.md` |
| 결정 기록 | `_project/decisions/` |

> ⚠ **확인 필요**: 사이트 문서(`jekyll/docs/01~16`)는 5인 트랙 버전(`plan-rev4-alt-5인안.md`)을 바탕으로 작성됐고,
> `_project/plan.md`는 3인 실명 버전이다. 두 판은 트리거 허용 창(800ms vs 1,500ms) 등에서 값이 다르다.
> 어느 판을 정본으로 할지 팀이 확정한 뒤 한쪽으로 맞춘다.

### 기능 블록

| 블록 | 내용 | 우선순위 |
|---|---|---|
| A | 실시간 STT (스트리밍·화자분리·발화구간 검출) | 필수 |
| **B** | **자동 문서 추천 = RAG 핵심** | **사수** |
| C | 실시간 컴플라이언스 감지 | 필수 |
| **C-5** | **개인정보 실시간 마스킹** (자막·저장 양쪽 앞단) | **사수 — 코어** |
| D | 통화 후 처리 (요약·유형분류·지식베이스 공백 리포트) | 필수 |
| **E** | **평가 하네스** (골든셋·자동채점·CI) | **사수** |
| F-2 | 종결 요건 검증 게이트 | 조건부 (7주차 체크포인트) |
| F-1·F-3·F-4 / G-2 / H·I | 확장 모듈 | 여유 시 |

코어 기준선을 통과하지 못했다면 F·G·H·I를 착수하지 않는다. C-5만 예외로 코어에 포함된다.
성공 조건은 F-2가 아니라 **STT 오류 내성 실험 + 검색 품질 개선 수치**다.

---

## 2. 절대 원칙 (사용자의 명시적 지시 없이는 위반 금지)

1. **LLM을 채점자로 쓰지 않는다.** 모든 평가 지표는 규칙 기반으로 계산해 재현 가능해야 한다.
2. **측정하지 않은 수치를 기록하지 않는다.** 기획서의 성능 표는 형식 예시다. 미측정은 "측정 불가 / 미측정"으로 적고 숫자를 지어내지 않는다.
3. **컴플라이언스 감지와 마스킹은 재현율 우선.** C-5는 **누락 0건 > 과잉 마스킹 억제** 순서를 고정한다 — 애매하면 가린다.
4. **기준선은 여러 번 실행한 값 중 최저치로 고정한다.**
5. **기준선 미달은 CI 실패.** 절대 규칙(C-5 누락 0건, F-2 판정 정확도)은 평균이 아니라 **1건이라도 뚫리면 실패**로 처리한다.
6. **약관 원문을 사이트에 전재하지 않는다.** 요약·해석 + 출처(문서명·조항)만 싣는다.
7. **자체 통화 녹음은 하지 않는다.** AI Hub 등 저작권·개인정보가 해결된 출처만 사용한다.
8. **실패를 지운 기록은 기록이 아니다.** 안 된 실험, 미달한 지표, 틀린 가설은 그대로 남긴다.
9. **판정은 규칙이, 설명만 LLM이 한다.** 종결 가능 여부·요건 충족·마스킹 대상 판정을 생성 모델에 맡기지 않는다.
10. **측정할 수 없는 것을 측정한 것처럼 쓰지 않는다.** F-1·G-1 탐지 성능은 측정 불가이고, F-2의 100%는 "팀이 만든 규정 안에서의 100%"다.

---

## 3. 저장소 구조

```
CLAUDE.md                이 파일. 규칙과 프로젝트 정의
_project/                ⚠ 비공개. 지킬 루트 밖이라 사이트에 올라가지 않음
  plan.md                기획서 rev.4 사본 (수정하지 않는다)
  rev4-보완지시서.md      rev.4 위에 얹히는 패치
  STATE.md               세션 인수인계용 현재 상태
  decisions/             결정 기록 (ADR)
db/                      schema.sql(DDL) · ERD.md · erd.dot · generate_schema_docs.py
knowledge-base/          도메인별(finance/dasan/shopping/health) terms / manual / policy
golden-set/              골든셋 (v1-10.json …)
docs/                    구조 하네스(harness.md) · 아키텍처(architecture.md) · 도메인(domain.md) · 기획서 rev.4.1 사본. 공개, 지킬 밖
server/                  요청이 흐르는 길 (Python 3.13). 계약(포트·DTO)·파이프라인 배선·클린 아키텍처.
                         main.py(합성 루트) · core/config.py · apps/hub/(7.3절 계약 DTO+포트, 슬라이스 transcript_ingest·myself)
                         · .importlinter(계약 4종) · requirements.txt · pytest.ini · CLAUDE.md(영역 규칙). 배포: server.solidbob.cloud
                         실행: cd server && uvicorn main:app --reload --env-file ../.env
                         검증: cd server && pytest && PYTHONPATH=apps lint-imports --config .importlinter
ai/                      품질을 만들고 재는 쪽 (Python 3.13). 청킹·BM25·리랭크·임베딩·모델 학습·랭그래프.
                         apps/retrieval/(검색) · apps/evaluation/(평가 하네스) · .importlinter(계약 3종)
                         · requirements.txt · pytest.ini · CLAUDE.md(영역 규칙). 배포: ai.solidbob.cloud
                         검증: cd ai && pytest && PYTHONPATH=apps:../server/apps lint-imports --config .importlinter
                         의존 방향은 ai → server 한쪽뿐이다 (evaluation 이 hub 계약을 import). 역방향은 계약이 막는다
apps/                    dashboard(상담원). 고객 화면은 `_project/decisions/014` 로 철회(013 철회)
scripts/ data/           유틸리티 / 데이터 (원본은 .gitignore)
.github/workflows/       Pages 배포(pages.yml) · CI(test.yml — server · ai · jekyll job) · branch-protection.json
jekyll/                  지킬 사이트 루트 — 지킬 명령은 전부 이 안에서 실행
  index.markdown         표지 (layout: cover)
  toc.markdown           목차
  progress.markdown      진행 기록 (팀 공개)
  open-items.markdown    미결 항목
  docs/NN-슬러그.markdown 본문 페이지 (permalink /docs/NN/)
  sprints/NN-슬러그.markdown 스프린트 로그 (permalink /sprints/NN/)
  _layouts/              cover.html · doc.html
```

---

## 4. 사이트 작성 규칙

### Front Matter

```yaml
---
layout: doc
title: <페이지 제목>
permalink: /<경로>/
---
```

- `layout: home`, `layout: page`(minima 기본)는 쓰지 않는다. **표지만 `layout: cover`**, 나머지는 전부 `layout: doc`이다.
- 표지는 front matter의 `eyebrow`/`title_lines`/`subtitle`/`meta`/`footer_*` 필드로 내용을 채운다.
- `permalink`은 항상 명시한다 (파일명에 의존하지 않는다).
- `doc.html`·`cover.html`이 상단 내비를 하드코딩하므로, 새 최상위 섹션이 필요하면 **두 레이아웃의 `<nav>`를 둘 다** 고친다.
- `_posts/`, `about.markdown` 등 지킬 기본 스캐폴딩은 만들지 않는다. 생기면 지운다 — 이 사이트는 블로그가 아니다.
- 그림 등 정적 자산은 `jekyll/assets/` 아래에 둔다 (ERD 이미지는 `db/generate_schema_docs.py`가 자동 복사).

### 진행 기록

`jekyll/progress.markdown`에 **최신 항목이 위로** 오도록 누적한다. 날짜는 `YYYY-MM-DD`.

```markdown
### 2026-08-25
- 무엇을 했는지 한 줄 요약
- 다음에 할 일
```

작업이 있었던 세션은 여기에 반드시 한 항목을 남긴다. 한 번 쓴 항목은 고치지 않는다.

### 백로그 · 칸반 (충돌 방지)

**티켓 1건 = 파일 1개.** `jekyll/_backlogs/` 아래 개별 마크다운으로 만든다.
세 사람이 하나의 표를 같이 고치면 병합 충돌이 나므로, 보드를 페이지에 직접 그리지 않는다.
`/kanban/` 페이지가 컬렉션을 읽어 담당자 사이드바와 3열(할 일 / 진행 중 / 완료) 보드를 한 페이지에서 전환한다.

```yaml
---
title: "카카오 로그인 API 연동"
assignee: "류준"          # 정성윤 | 류준 | 장민석 | 조서희
                          # 백엔드·AI 공동 작업은 "류준·장민석", 팀 전체는 "공동"
role: "ai"                # infra | ai | app  (배지 — ai: 류준·장민석, app: 조서희)
status: "in-progress"     # todo | in-progress | done
sprint: 1
priority: 5               # 같은 칸 안의 정렬 순서
date: 2026-08-25
paths:                    # (선택) 이 티켓 소관 파일. 세션 종료 검사가 status 정합성을 본다
  - "services/gateway/stt/*"
---
```

- **티켓은 작업을 시작할 때 만든다.** 끝난 뒤 몰아서 소급 생성하면 담당자와 시점이 실제와 어긋난다.
- **`assignee` 는 실제로 손대는 사람**이다. 기획서 7.1절 역할표가 아니라 실제 수행자를 적는다.
  역할표와 다르면 티켓 본문에 그 사실을 적는다.
- **담당이 바뀌면 착수 여부로 갈린다.** 이미 진행·완료된 티켓은 그 시점의 수행자를 보존한다(소급 수정 금지).
  아직 `todo` 인 티켓은 **보존할 수행 기록이 없으므로** 새 담당자로 옮기거나 다른 티켓에 합치고 옛 티켓은 지운다 —
  아무도 손대지 않은 일을 남의 이름으로 보드에 띄워두면 "지금 누가 무엇을 하는가"가 거짓이 된다.
- **남의 브랜치에서 진행 중인 작업과 겹치면 나중에 시작한 쪽이 물러난다.** 같은 티켓을 두 사람이 다르게
  고치고 있으면 먼저 손댄 쪽을 살리고 자기 변경을 되돌린다. 조용히 덮어쓰면 머지 충돌이 커진다.
- **티켓 하나에 두 사람의 작업을 담지 않는다.** 담당이 갈리면 티켓을 쪼갠다.
- 파일명은 `w{주차}-{영문-슬러그}.md`. **한글 파일명은 URL이 깨진다**(permalink는 `:name` 기반).
- **`paths:` 는 선택이지만 붙여두면 잊는 걸 막아준다.** 그 경로의 파일을 고쳤는데 티켓이 아직
  `todo` 면 세션 종료 검사가 경고한다. 슬러그가 겹치는 티켓(`w1-db-schema` ↔ `w2-db-schema-domain`)도 함께 경고한다.
- 단계를 일부러 나눈 티켓(예: `w2-baseline` 측정 → `w2-baseline-gate` CI 게이트)은 뒤 티켓에
  `depends_on: ["w2-baseline"]` 을 적는다. 중복 경고에서 빠지고, 무엇이 무엇을 기다리는지도 남는다.
- 상태를 옮길 때는 **자기 티켓의 `status` 한 줄만** 고친다. 남의 티켓 파일은 건드리지 않는다.
- 본문에는 무엇을 / 왜 / 완료 조건을 적는다. 근거가 있으면 문서 링크를 건다.
- 주차별 목표는 `jekyll/docs/08-마일스톤.markdown`, 일자별 기록은 `progress.markdown`이 담당한다. 같은 내용을 세 곳에 적지 않는다.

### 미결 항목

정하지 못한 것은 `jekyll/open-items.markdown`에 남긴다. 비워두면 다음 세션이 같은 질문을 다시 하게 된다.
되돌리기 어려운 선택은 `_project/decisions/NNN-제목.md`에 **맥락 / 선택지 / 결정 / 근거 / 되돌리는 법** 형식으로 남긴다.

---

## 5. 수치를 다루는 규칙

성능 수치는 **평가 하네스(`ai/apps/evaluation/`)가 낸 값만** 쓴다. 손으로 적은 숫자를 문서에 넣지 않는다.
값 하나에는 언제·어느 커밋으로·어떤 명령으로·표본 몇 건인지가 함께 남아야 한다(`db` 스키마의 `eval_run`/`eval_result`).
넷 중 하나라도 채울 수 없으면 그 숫자는 아직 기록할 준비가 되지 않은 것이다.

미구현 모듈에 대해 하네스는 **"측정 불가 — 모듈 미구현"**으로 보고한다. 이 정직성을 우회하지 않는다.

---

## 6. 개발 서버

```bash
cd jekyll
bundle exec jekyll serve --host 0.0.0.0 --port 4000    # 포트가 점유돼 있으면 4001
bundle exec jekyll build                                # 기록 커밋 전 검증
```

- 파일 저장 시 자동 재빌드된다. `_config.yml`을 고쳤을 때만 서버를 재시작한다.
- 루비는 rbenv로 관리한다 (3.3 이상, Jekyll 4.4.1).

---

## 7. 커밋 규칙

```
log(w3): 스트리밍 STT 파이프라인 연결
docs(search): 인터페이스 계약 v2 확정
data(metrics): 오류율 10% 구간 Recall@5 실측 반영
code(eval): 마스킹 재현율 계산 추가
```

타입: `log` | `docs` | `data` | `code` | `rule` | `chore`
**커밋과 푸시는 사용자가 명시적으로 요청할 때만 한다.**

### 브랜치

역할별로 넷을 유지한다 — `PM`(정성윤) / `backend`(류준) / `ai`(장민석) / `frontend`(조서희).
`flutter` 는 앱 개발 중단(2026-08-26)으로 `ai` 에 대체됐다.

**`ai` 와 `backend` 를 합치지 않는다** (2026-08-26 결정). 류준·장민석이 백엔드·AI 를 공동으로
맡지만 브랜치는 따로 둔다. 근거·되돌리는 법: `_project/decisions/011-브랜치-정책과-main-보호.md`.

> 브랜치를 합쳐도 충돌은 줄지 않는다. 이번 주 충돌 3건(`w2-domain-routing`·`w2-db-schema-domain`·
> `progress.markdown`)의 원인은 브랜치 수가 아니라 **같은 티켓을 두 사람이 동시에 고친 것**이었다.
> 해결책은 §4 의 티켓 선점 규칙("먼저 손댄 쪽이 산다")을 실제로 지키는 쪽이다.

### main 에는 직접 push 하지 않는다

**모든 변경은 PR 로 들어간다.** main 은 push 즉시 배포되므로(`pages.yml`), 직접 push 하면
테스트가 끝나기 전에 이미 배포된 뒤가 된다.

| | 설정 |
|---|---|
| PR 필수 | 승인 1건 이상 |
| 필수 통과 검사 | `backend`(하네스 테스트 + 구조 계약) · `jekyll`(사이트 빌드 + 링크 검사) |
| force push · 브랜치 삭제 | 금지 |

CI(`test.yml`)는 위 네 브랜치 push 와 main 대상 PR 양쪽에서 돈다. 배포(`pages.yml`)는
main push 에서만 도는데, 보호 설정 이후 그 push 는 **PR 머지로만 발생한다.**

---

## 8. 공개 / 비공개 경계 ⚠

이 저장소는 GitHub Pages로 **공개 게시**된다. 커밋이 곧 발행이다.

| | 위치 |
|---|---|
| 공개해도 되는 것 | 아키텍처, 스키마, 실험 방법과 결과, 실패 분석, 진행 기록 |
| 공개하면 안 되는 것 | 약관 원문, API 키·자격증명, 개인정보 포함 데이터 샘플, 내부 서사 |

내부 성격의 글은 `_project/` 아래에 둔다 (지킬 루트 밖이라 게시되지 않는다).
**어떤 경우에도 자격증명을 커밋하지 않는다.** 키는 `.env`(gitignore)로 관리한다.

---

## 9. Claude 작업 방식

- 기획서에 이미 답이 있는 것을 다시 묻지 않는다. `_project/plan.md`를 먼저 본다.
- 판단이 갈리면 선택지를 나열하지 말고 **권고안 하나 + 이유**를 제시하고 진행한다. 되돌리기 어려운 것만 사전에 확인한다.
- 측정으로 결론 낼 수 있는 논쟁은 측정한다.
- 안 된 것을 됐다고 보고하지 않는다. 미달 지표는 숫자 그대로 쓰고 원인 가설을 붙인다.
