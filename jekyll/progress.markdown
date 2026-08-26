---
layout: doc
title: 진행상황
permalink: /progress/
---

### 2026-08-26 (43)
- **Jekyll CI 깨진 링크 수정** — `w1-dashboard-scaffold-seohee`가 이미 삭제된 `/backlog/w1-dashboard-scaffold/`를 가리켜 내부 링크 검사가 실패했다. 링크를 텍스트로 바꿨다.

### 2026-08-26 (42)
- **대시보드 시각 디테일** — 헤더 로고·연결 배지, 우측 카드 그림자·배지·출처 아이콘, 충족요건 진행률 링. 자막 패널은 그대로. `typecheck`·`build` 통과.

### 2026-08-26 (41)
- **칸반을 한 페이지 사이드바 전환으로 재구성** — 개인 permalink 4개를 지우고 `/kanban/`에서 왼쪽 담당자 목록·오른쪽 3열 보드만 JS로 전환. URL은 `/kanban/` 유지.

### 2026-08-26 (40)
- **칸반을 1인 1페이지로 분리** — `/kanban/`은 4명 링크 인덱스. 개인 보드는 `/kanban/seongyun/`·`ryujun/`·`minseok/`·`seohee/`. 공동 티켓(`류준·장민석`)은 두 사람 보드에 같이 표시.

### 2026-08-26 (39)
- **상담원 화면을 자막 | 이용약관·충족요건 2분할로 재설계** — 경고 패널·종결 모달 삭제. 마스킹된 자막 줄에만 「⚠ 경고」 태그. 카드와 F-2 체크리스트를 한 박스에 붙이고, 근거가 전부 충족되면 「종결 처리」. 하단은 진행중 탭만. `typecheck`·`build` 통과.

### 2026-08-26 (38)
- **자막 간격 2초 단축 + F-2 1/3을 모달 대신 경고 아래 실시간 표시** — 발화 사이 재생 간격을 2초 줄임. blocked 종결은 모달을 열지 않고 경고 패널 하단에 「근거 N건 중 M건 충족」 체크리스트로 갱신. approved만 종결 모달.

### 2026-08-26 (37)
- **mock 자막 재생을 utterance_end_ms 기준으로 통일** — 앞 8턴만 900ms 압축되던 것을 없애 후반(약 4초 간격)과 같은 호흡으로 맞춤.

### 2026-08-26 (36)
- **금융보험 mock을 blocked→approved 해지 완료 흐름으로 연장** — evidence를 `중도해지수수료_안내`·`약정혜택소멸_안내`·`고객확인_기록`(FIN-POLICY-CLOSE-1)로 통일. 첫 종결 후 약정 소멸 고지·고객 확인·기록 발화를 이어 붙이고 두 번째 종결은 3건 전부 충족. 모달은 blocked여도 X/닫기로 닫을 수 있음. `typecheck`·`build` 통과.

### 2026-08-26 (35)
- **F-2 종결 타입·evidence를 §2.7에 맞춤 + mock 4도메인 분리** — `ClosureType`을 상품해지/사고·보상/반품/교환으로 정정(명의변경·해지 제거). 금융보험 해지 evidence를 중도해지수수료_안내·약정혜택_소멸_고지·고지_확인_응답으로 교체. `mock/scenarios/{finance,shopping,dasan,health}` + 헤더 도메인 선택. 종결 모달은 「근거 N건 중 M건 충족」만 표시. 다산·헬스는 종결 이벤트 없음. `typecheck`·`build` 통과.

### 2026-08-26 (34)
- **책갈피 탭에 카드 제목 표시, 펼친 카드는 유지** — 탭 문구를 약관명 대신 「분실·도난 신고」 등 title 로. 6초 자동 접힘 제거, 접기는 버튼으로만.

### 2026-08-26 (33)
- **경고 패널 마스킹 유형을 한글로 표시** — P2→카드번호, P4→연락처. mock 연락처 발화는 P4로 구분.

### 2026-08-26 (32)
- **하단 책갈피 바를 뷰포트에 고정 + 수신 시 슬라이드업** — `app-shell` 마지막 행으로 고정해 자막이 길어져도 바가 화면 아래에 남음. 펼침은 `max-height` 전환(0fr 버그로 내용이 안 보이던 것 수정). mock에서 카드가 하단에서 펼쳐지는 것 확인.

### 2026-08-26 (31)
- **대시보드 mock 자막 마스킹 4자리 전부 + 통화 시나리오 연장** — `카드번호는 ****` span을 `[6,10)`으로 고쳐 네 자리 모두 표시. 분실 신고 대화 8턴·카드 4장(FIN-TERM-2.1/2.2/3.2/2.3)으로 mock을 늘림.

### 2026-08-26 (30)
- **상담원 화면을 상단 2분할(자막 2fr · 경고 1fr) + 하단 전체폭 책갈피로 고정** — `App.tsx` 레이아웃. 새 탭은 오른쪽 끝에 누적, 수신 시 슬라이드업 후 6초 접힘(임시). F-2 모달은 그대로. `apps/customer` 없음, `w1-customer-screen` cancelled(009). `typecheck`·`build` 통과.

### 2026-08-26 (29)
- **고객 화면 스코프 철회 + 상담원 하단 책갈피 카드** — `_project/decisions/014`(재배치 전 `009`). `apps/customer` 삭제. 티켓 `w1-customer-screen` cancelled. 대시보드 추천 카드는 사이드바 목록 대신 하단 고정 책갈피(수신 시 슬라이드업, 6초 후 접힘·탭은 유지). `typecheck`·`build` 통과.

### 2026-08-26 (28)
- **고객 팝업 mock을 데모 도메인 4종으로 맞춤** — 금융보험 · 다산콜센터 · 쇼핑 · 질병관리본부 각 1장(`FIN-TERM-2.1`, `DASAN-TERM-2.1`, `SHOP-TERM-4.1`, `HLT-TERM-2.1`). 7.3절 통신(요금제약관) 카드는 고객 mock에서 제거. 라벨은 한글 도메인명.

### 2026-08-26 (27)
- **고객 카드뉴스 팝업 재설계** — `CardNewsPopup.tsx`: 4px 책갈피 탭, 카드 바깥 원형 화살표, 하단 점 인디케이터, 우상단 X. 다크 서페이스(`#12141a`) 유지. 여러 장일 때만 화살표·점 표시, ←/→ 키, 180ms 전환. 출처는 source title 태그만.

### 2026-08-26 (26)
- **고객 화면에서 실시간 자막 제거** — `apps/customer`에 다시 들어가 있던 큰 자막(마스킹 박스 포함)을 삭제. 대기 문구 + 카드뉴스 팝업만 남김. 자막은 상담원 대시보드(`apps/dashboard`) 전용. 근거 `_project/decisions/013`(재배치 전 `008`)

### 2026-08-26 (25)
- **고객 화면 재스캐폴딩 (`apps/customer`)** — 대시보드와 같은 `contract.ts`·mock 타이밍(400/900/1600ms). 큰 자막(마스킹 유지) + 전체 화면 카드뉴스(왼쪽 컬러 탭, source만 하단, doc_id·유사도 비표시). e2e 3초 초과는 콘솔 경고만. 자동 접힘 8초는 임시(팀 컨펌). 티켓 [`w1-customer-screen`](/backlog/w1-customer-screen/) in-progress

### 2026-08-26 (24)
- 고객 화면 스코프 확정, apps/customer 착수

### 2026-08-26 (23)
- **고객 카드뉴스 mock 6장** — 지식베이스 조항을 옮김(`FIN-TERM-3.2`·`2.1`, `SHOP-TERM-4.1`·`4.2`, `DASAN-MANUAL-2.1`, `HLT-MANUAL-2.1`). 이전/다음으로 넘김. 유사도는 미측정이라 화면에 없음

### 2026-08-26 (22)
- **고객 화면은 카드뉴스 팝업만** — 대화·자막은 상담원 대시보드에만 두고, `apps/customer` 는 화면 중앙 카드뉴스 오버레이로 7.3절 카드를 띄운다. `_project/decisions/013`(재배치 전 `008`) 후속 확정, [2.1절](/docs/02/) 반영

### 2026-08-26 (21)
- **고객 화면 스코프 확정 + `apps/customer` 스캐폴딩** — 상담원 3분할과 같은 `call_id`·[7.3절](/docs/07/) `cards` 를 쓰되 표시는 자막 + 책갈피 카드뉴스 팝업(3초 내, 누적 없음). F-2·경고는 고객 화면에 두지 않음. 근거 `_project/decisions/013`(재배치 전 `008`). 티켓 [`w1-customer-scaffold-seohee`](/backlog/w1-customer-scaffold-seohee/). 검증: `typecheck`·`build` 통과, mock 시나리오 화면 확인

### 2026-08-26 (20)
- **React 대시보드 스캐폴딩 (`apps/dashboard`) — `frontend` 브랜치** — Vite + React 18 + TypeScript strict. 게이트웨이 클라이언트는 real/mock 동일 인터페이스, `.env`의 `VITE_GATEWAY_WS_URL` 유무로 전환. mock은 [7.3절](/docs/07/) v2 예시값(프로모션 할인 카드, 해지 종결 `blocked`)만 재생. 3분할(자막·추천 카드·마스킹 로그) + F-2 종결 모달. 상태관리 zustand는 팀 미정이라 컨펌 필요. 티켓 [`w1-dashboard-scaffold-seohee`](/backlog/w1-dashboard-scaffold-seohee/) (`w1-dashboard-scaffold` 장민석 티켓 대체). 검증: `typecheck`·`build` 통과, mock 시나리오 화면 확인
### 2026-08-26 (19)
- **`main` 병합 — `server/`·`ai/` 분리를 `backend` 브랜치로 받았다.** 충돌 2건은 번호 충돌이었다: `progress.markdown` 은 양쪽이 `(15)` 를 써서 장민석 님 항목을 `(18)` 로 옮겼고(**내용은 그대로** — 절대 원칙 8), `_project/STATE.md` 는 "현재 상태" 문서라 최신판(main)을 정본으로 두고 장민석 님 세션 #10 기록은 그 아래에 보존했다. 그 안의 "브랜치 통합 준비" 안내만 결정이 뒤집힌 사실(`decisions/011`)을 덧붙였다 — STATE 는 다음 세션이 그대로 따라가는 문서라 낡은 안내를 남기면 잘못 이어받는다
- **결정 기록 번호 충돌을 고쳤다 — `009` 가 둘이었다.** `009-생성모델-EXAONE-Ollama-확정.md`(내가 오전에 작성)와 `009-브랜치-정책과-main-보호.md`(정성윤, 오후)가 같은 번호였고, **`decisions/009` 로만 참조한 곳이 5군데**라 어느 문서인지 모호했다. §4 "나중에 시작한 쪽이 물러난다"에 따라 나중 것을 **`011`** 로 옮기고 참조 3곳(`CLAUDE.md`·`STATE.md`·이 로그)과 문서 자체 제목을 고쳤다. 진행 기록은 경로만 고치고 문장은 건드리지 않았다
- **담당 분리 확정 — 류준 `ai/` · 장민석 `server/`**(`_project/decisions/012`). `decisions/005` 의 "기능별 분할 없음"을 갱신한다. 나누지 않기로 했던 이유가 "경계가 없어서"였는데, `fastapi/` 분리로 디렉터리·의존 방향(`ai → server` 한쪽)·`.importlinter` 계약·영역별 `CLAUDE.md` 가 이미 경계를 정의하고 있다
- **⚠ 브랜치 이름과 디렉터리 이름이 엇갈린다** — 류준은 브랜치 `backend` 에서 `ai/` 를, 장민석은 브랜치 `ai` 에서 `server/` 를 고치게 된다. 브랜치는 넷을 유지하기로 해(`decisions/011`) 지금은 이름만 어긋난 상태다. **바꾸지 않고 남겨 뒀다** — 브랜치명을 바꾸면 `test.yml` 트리거와 **main 룰셋의 필수 통과 검사 이름**까지 함께 고쳐야 하고, 어긋나면 PR 이 없는 검사를 기다리며 영원히 머지되지 않는다(룰셋은 `solidbob02` admin 몫). 팀 확인 대상
- **미결 정리** — "브랜치 구조 통합 여부"를 결정됨으로 닫았다(통합하지 않음 + main 보호 적용 완료)
- **로컬 잔재 정리** — `fastapi/hub`·`fastapi/evaluation` 이 `.pyc` 캐시만 남은 채 떠 있었다(`fastapi/apps/` 재배치 때 git 은 추적 파일만 옮기고 gitignore 된 `__pycache__` 는 옛 경로에 버려진다). 저장소 전체를 `git clean -Xd --dry-run` 으로 훑어 캐시·빌드 산출물만 지웠다 — `.env`·`models/`·`data/raw/`·`logs/`·`.venv/` 는 gitignore 대상이지만 **"커밋하면 안 되는 것"이지 "지워도 되는 것"이 아니라** 그대로 뒀다
- 남은 것: ES 인덱스 분할 여부(2주차 진행을 막고 있다 — 이제 `ai/` 담당이라 내 쪽 결정). 브랜치명 정리 여부는 팀 확인

### 2026-08-26 (18)
- **브랜치 통합 준비 — `ai` 쪽 정리**. PR #22 머지로 `ai` 브랜치에 고유 커밋이 0건이 됐다(청킹·골든셋 50건·문서 정합성 전부 `main` 반영 확인). **지금 `ai` 를 정리해도 잃는 것이 없다**
- **합친 뒤에 고쳐야 할 곳 2군데를 찾아 기록** — `.github/workflows/test.yml:19`(`branches: [main, PM, backend, ai, frontend]`)와 [7절 브랜치 규칙](https://github.com/solidbob02/call.solidbob.cloud/blob/main/CLAUDE.md). **먼저 고치면 안 된다** — `ai` 가 살아 있는 동안 트리거에서 빼면 그 브랜치 푸시에 CI 가 돌지 않는다
- **`main` 에 브랜치 보호 설정이 없음을 확인**(API 404). `pages.yml` 은 `main` push 시 즉시 공개 배포이므로, 브랜치를 없애고 직접 커밋으로 가려면 **보호 설정을 먼저 켜는 것이 전제**다. 지금은 PR·CI 가 유일한 게이트다
- 네 브랜치가 실제로 만진 파일 영역을 세어보니 `jekyll/_backlogs`·`fastapi/apps/hub/app/*` 로 **전부 겹친다** — 브랜치가 격리를 제공하지 못하는 상태라는 것이 통합 논의의 근거가 된다
- 미결 2건 등록([미결 항목](/open-items/)) — **ES 인덱스 분할 여부**(2주차 진행을 막고 있음)와 **브랜치 구조 통합 여부**
- `w1-domain-routing` 에 `w2-domain-routing` 과의 관계 명시(결정 vs 구현) — 세션 종료 검사가 슬러그 중복으로 경고하지만 다른 작업이라 합치지 않았다. 전제였던 골든셋 50건은 확보됐고 남은 전제는 B-2 검색
- `_project/STATE.md` 를 세션 #10 기준으로 갱신
- 남은 것: 브랜치 통합 방식은 **팀 결정 사항** (`_project/decisions/` 대상). ES 인덱스 결정 후 `w2-naive-rag` 착수
- **브랜치 통합 건은 (16)에서 정성윤 님이 이미 확정했다** — 나도 같은 날 같은 결론(넷 유지)에 도달해 항목을 따로 썼으나, 그쪽이 `main` 보호 설정 **실제 적용**까지 마친 기록이라 내 중복 항목은 버리고 이 줄로 대신한다. `main` 보호 부재를 각자 독립적으로 확인(API 404)한 것도 같다
- **충돌 대응은 브랜치가 아니라 티켓 선점으로** — 오늘 `w2-db-schema-domain`·`w2-domain-routing` 중복은 13분 차이로 났다. 브랜치를 합쳐도 같은 시각에 같은 티켓을 고치면 똑같이 나므로, 착수할 때 `status: in-progress` 로 먼저 선점·푸시한다

### 2026-08-26 (17)
- **백엔드를 서브도메인 둘로 나눴다 — `fastapi/` → `server/` + `ai/`.** DNS 에 `server.solidbob.cloud`·`ai.solidbob.cloud` 가 잡혀 있어 코드 배치도 그에 맞췄다. **`server/` 는 요청이 흐르는 길**(계약 포트·DTO, 파이프라인 배선, 클린 아키텍처), **`ai/` 는 품질을 만들고 재는 쪽**(청킹·BM25·리랭크·임베딩·모델 학습·랭그래프·평가 하네스). `git mv` 로 옮겨 히스토리는 보존됐다(server 63파일 / ai 39파일)
- **경계는 짐작이 아니라 의존 방향을 조사해 정했다** — `retrieval`→`hub` 참조 **0건**(완전 독립), `evaluation`→`hub` **9건**(계약만), `hub`→스포크 **0건**. 이미 `hub` 가 포트를 정의하고 스포크가 구현하는 한쪽 방향이라, 그 선을 그대로 서브도메인 경계로 썼다. **의존은 `ai → server` 한쪽뿐**이고 `server/.importlinter` 계약 2 가 역방향을 막는다 — `torch`·`transformers`·`langchain`·`langgraph` 도 금지 목록에 넣었다. 서버 컨테이너에 그것들이 들어오면 방향이 이미 무너진 것이다
- **C-5 마스킹과 F-2 게이트는 `server/` 에 뒀다** — 지시받은 분류에 없어 판단이 필요했다. **둘 다 규칙 기반 판정이고 요청 경로에서 매번 실행된다.** 모델이 관여하지 않으므로 서버 쪽이다. "판정은 규칙이, 설명만 LLM이 한다"(절대 원칙 9)를 디렉터리 배치로 고정한 셈이다
- **영역 규칙 `CLAUDE.md` 를 각 루트에 뒀다** — 하는 일/하지 않는 일을 표로 못박고, 헷갈릴 때의 판단 기준("요청 하나를 처리하는 데 반드시 실행되는가?" → server / "품질을 만들거나 재는 코드인가?" → ai)을 넣었다. `ai/CLAUDE.md` 의 절대 규칙에 **"LLM 을 채점자로 쓰지 않는다"** 를 넣고, `.importlinter` 계약 3 이 `evaluation` 에서 모델 라이브러리 import 를 막아 **구조로 고정**했다. `docs/harness.md` 가 "영역 CLAUDE.md 는 규칙이 분화될 때 만든다"고 예고했던 그 시점이 왔다
- **의존성도 갈랐다** — `server/requirements.txt` 는 런타임(fastapi·uvicorn·pydantic·google-cloud-speech)만, `ai/requirements.txt` 는 모델(torch·transformers 등)만. 섞으면 서버 컨테이너가 torch 때문에 수 GB 커지고 CI 가 쓰지도 않는 것을 설치한다. 아직 안 쓰는 것(elasticsearch·rank-bm25·langchain·langgraph)은 주석으로만 적어 뒀다 — 미리 넣으면 CI 가 설치한다
- **CI 를 `server`·`ai` 두 job 으로 나눴다.** `ai` job 에 torch 를 설치하지 않는다 — 지금 테스트가 쓰지 않고 매번 수 GB 를 받게 된다. 모델이 실제로 필요한 테스트는 `@pytest.mark.slow`/`integration` 으로 빠진다
- **검증** — 이 머신에 `pip` 이 없어 pytest 를 못 돌렸다. 대신 정적으로 확인했다: 앱 간 import **78건 전부 새 경로에서 해석됨**, 전 파일 컴파일 문법 오류 0건, `server`→`ai` 참조 0건, 사이트 빌드 52페이지·링크 0건. **실제 테스트는 CI 가 돌린다**
- **문서 참조 49건 정리** — `CLAUDE.md`·`README.md`·`docs/harness.md`·`.claude/rules/rfp-harness.md`·`_project/STATE.md`·데이터 README 3종·사이트 문서 3종. 진행 로그·스프린트 로그·결정 기록의 `fastapi/` 언급은 **그 시점의 사실이라 고치지 않았다**(절대 원칙 8). 팀원 티켓 3건은 내가 옮겨서 깨진 **경로만** 고쳤고 상태·담당은 건드리지 않았다
- **남은 것 — 머지 전에 두 가지가 필요하다.** ① **CI job 이름이 `backend` → `server`+`ai` 로 바뀌어 main 룰셋의 필수 통과 검사도 함께 바꿔야 한다**(`[backend, jekyll]` → `[server, ai, jekyll]`). 안 바꾸면 없는 검사를 기다리며 PR 이 영원히 머지되지 않는다 — 어제 주석으로 경고해 둔 함정에 오늘 우리가 걸린다. 룰셋 변경은 `solidbob02` 계정(admin) 몫이다 ② **`backend`·`ai` 브랜치의 미머지 작업과 전면 충돌한다.** `fastapi/` 전체가 움직였으므로 류준·장민석 님과 합의가 필요하다


### 2026-08-26 (16)
- **브랜치 정책 확정 — 넷을 유지하고 합치지 않는다.** `ai` 를 `backend` 에 합치자는 안이 나왔으나 채택하지 않았다. **브랜치를 합쳐도 충돌은 줄지 않는다** — PR #22 의 충돌 3건(`w2-domain-routing`·`w2-db-schema-domain`·`progress.markdown`)은 브랜치 수가 아니라 **같은 티켓을 두 사람이 같은 시각에 다른 값으로 고친 것**이 원인이고, 합친 브랜치 안에서도 똑같이 일어난다. 실제 해결책은 [§4 티켓 선점 규칙](https://github.com/solidbob02/call.solidbob.cloud/blob/main/CLAUDE.md)("먼저 손댄 쪽이 산다")을 지키는 쪽이다. `CLAUDE.md` §7 을 브랜치 절과 main 절로 나눠 다시 썼다. 근거: `_project/decisions/011-브랜치-정책과-main-보호.md` *(작성 당시 009 였으나 번호가 겹쳐 011 로 옮겼다 — 아래 (18) 참고. 경로만 고쳤고 내용은 그대로다)*
- **main 에 보호 설정이 하나도 없다는 것을 확인했다** — `branches/main/protection` → **404**. `pages.yml` 이 main push 에 즉시 배포하므로, 누구든 실수로 main 에 직접 push 하면 **테스트 결과와 무관하게 이미 배포된 뒤**가 된다. CI 를 아무리 잘 만들어도 "배포 후에 빨간불을 보는" 구조였다. 설정 값을 `.github/branch-protection.json` 에 준비했다 — PR 필수(승인 1), 필수 통과 검사 `backend`·`jekyll`, force push·브랜치 삭제 금지
- **보호 설정 적용 완료** — 내 계정(`SeongYuna`)은 push 권한만 있고 `admin` 이 없어(`permissions.admin=false`) API 로 켤 수 없었다(PUT → 404. GitHub 은 권한 부족을 404 로 돌려준다). 소유자 `solidbob02` 계정이 **클래식 보호 대신 룰셋**으로 적용했다 — `enforcement: active`, 대상 `~DEFAULT_BRANCH`, 규칙 4종(`deletion`·`non_fast_forward`·`pull_request` 승인 1·`required_status_checks [backend, jekyll]` strict), 우회 허용 대상 없음. **중간에 한 번 헛돌았다** — 룰셋은 생성 직후 기본이 `enforcement: disabled` 이고 대상 브랜치도 비어 있어서, 규칙을 다 채웠는데도 아무것도 막지 않는 상태였다. `branches/main` 의 `protected: false` 로 알아냈다. 확인은 `rules/branches/main`(지금 적용 중인 규칙)으로 했다 — `branches/main/protection` 은 admin 없이는 404 라 못 쓴다. **이로써 "테스트가 빨간불이어도 main 에 들어가면 그대로 배포"되던 구멍이 막혔다**
- **워크플로에 안전장치 주석** — `test.yml` 의 job 이름 `backend`·`jekyll` 은 보호 설정의 **필수 통과 검사 이름**이 된다. 이름을 바꾸면 보호 설정이 존재하지 않는 검사를 기다리며 **조용히 무력화**되므로 그 사실을 job 정의 바로 위에 박아 뒀다. `pages.yml` 에는 "보호 설정 이후 이 push 는 PR 머지로만 발생한다"를 적었다. 트리거 목록 자체는 브랜치를 합치지 않기로 해서 바꿀 것이 없었다(`main, PM, backend, ai, frontend` + main 대상 PR)
- 남은 것: 이제 **모든 변경이 PR 로만 들어간다** — 커밋 대기분 16개도 PR 로 올려야 한다. `w1-domain-routing` ↔ `w2-domain-routing` 중복은 팀원 티켓이라 손대지 않았다

### 2026-08-26 (15)
- **1주차 마감** — [8절 마일스톤](/docs/08/) 체크리스트 6개를 전부 체크하고 근거 티켓을 링크했다. **목표 6개 전부 달성.** [Sprint 1 로그](/sprints/01/)에 마감 절을 추가 — 계획과 달라진 것 3가지(도메인 단일 시나리오→실측 4종, 팀 3인→4인, 백엔드 `services/core/`→`fastapi/`), 다음 주로 넘긴 것 2가지, **아직 측정하지 않은 것**(Recall@5·MRR·트리거 발동률·마스킹 재현율 전부 미측정 — 모듈이 없어 하네스가 "측정 불가"로 보고)을 명시했다
- **`w1-eval-ci` 완료 처리 + 기준선 게이트 분리** — 이 티켓은 1단계(회귀 방지: 하네스 테스트·구조 계약·사이트 빌드·링크 검사)까지로 닫았다. 2단계(기준선 미달 시 CI 실패)는 2주차 베이스라인이 나와야 붙일 수 있어 시점이 달라 계속 "안 끝난 일"로 보였다 → 신규 티켓 `w2-baseline-gate`(정성윤)로 떼어냈다. 그 티켓에 절대 원칙 4(최저치 고정)·5(절대 규칙은 1건 단위 실패)·"측정 불가는 그대로 통과"를 완료 조건으로 적었다
- **골든셋 50건 — 이미 만들어져 있었다.** 비율을 내가 정하려다 `ai` 브랜치를 먼저 확인했더니 장민석 님이 `golden-set/v1-50.json` 50건을 이미 작성해 두셨다(main 미반영, 커밋 4건). **내 티켓 편집을 되돌리고 그쪽을 정본으로 뒀다** — 데이터가 이미 있고 내 것은 글일 뿐이다. 실제 구성은 F-2 가중(금융보험 18·쇼핑 16·다산 9·질병관리 7). **P1~P7 개인정보 패턴이 전부 커버된 것이 큰 소득이다** — 1주차 10건에는 P3·P5·P6·P7 이 아예 없어 C-5 "누락 0건" 절대 규칙을 4개 패턴에 대해 측정할 방법 자체가 없었다
- **비율의 근거는 그 뒤 기록됐다**(`c9ff671`, 류준) — 내가 확인한 시점엔 티켓이 "(미정)" 상태라 근거 누락으로 봤으나, 같은 날 F-2 가중 이유가 티켓에 적혔다. 남은 것은 배분이 아니라 **이 표본으로 지표를 어떻게 읽을 것인가**라, [미결 항목](/open-items/)에 측정 관점 두 가지를 수치와 함께 올렸다: ① 도메인이 18/16/9/7 로 기울어 **B-0 도메인 분류 정확도의 기저율이 25%→36%** 로 올라간다(다수 도메인으로 찍기만 해도). [6.1절](/docs/06/)이 이 지표를 "도메인 내 검색 지표보다 엄격"하게 잡은 취지가 흐려진다 ② **B(검색) 14건은 2주차 베이스라인용으로 얇다** — 도메인당 2~4건이라 Recall@5·MRR 분산이 크고, "여러 번 실행한 값 중 최저치"로 고정할 때(절대 원칙 4) 그 최저치가 실력이 아니라 운을 반영할 수 있다. **데이터를 다시 만들자는 게 아니라 측정 방법에 반영할지를 정하자는 것**이다
- **`w2-stt-batch` 착수 — `scripts/transcribe_batch.py`** (in-progress). AI Hub 오디오를 파일 단위로 전사한다. 할당량을 태우지 않는 것이 핵심이라 ① **COST-1 애플리케이션 가드**(`data/processed/stt-usage.json` 에 날짜별 사용 초 누적, `STT_MAX_SECONDS_PER_DAY=600`/`_MONTH=3600` 을 넘길 파일은 **요청을 보내지 않고 건너뛰되 나머지는 계속 처리**) ② **내용 해시 캐시**(같은 오디오 재전사 안 함 — 검색·트리거·마스킹 실험에서 같은 전사를 반복해 쓰기 위한 것) ③ `--dry-run` 으로 쓰기 전에 소모 초 확인. 골든셋 스펙의 발화 종료 시각을 위해 단어별 `start_ms`/`end_ms` 를 저장한다. 합성 wav 로 네 경로 검증(대상 없음 exit 1 / dry-run 초 계산 / 900초 파일이 600초 한도에 걸려 건너뛰어짐 / 캐시 적중). **실제 API 호출 경로는 검증하지 못했다** — 이 머신에 `data/raw/` 오디오도 `google-cloud-speech` 도 없다. 오디오가 있는 머신에서 `--dry-run` 후 소량으로 실행해야 한다
- **2주차 병목 재판단** — 앞서 "kb-index→naive-rag→baseline 라인이 병목"이라고 봤으나, `ai` 브랜치를 보니 **이미 진행 중**이다: 지식베이스 조항 단위 청킹 스포크 스캐폴딩(`fastapi/apps/retrieval/`, 테스트 83줄), `scripts/index_knowledge_base.py`, 골든셋 50건. 병목은 그 라인이 아니라 **① `ai` 브랜치 커밋 4건이 main 에 없다는 것**(이번 주에 겪은 충돌이 그대로 반복될 조건) **② 프론트엔드** — `apps/dashboard/` 는 아직 존재하지 않고 담당자는 이번 주 신규 합류다. 백엔드가 앞서 나갈수록 계약 v2 를 구현할 화면이 없는 상태가 길어진다
- 남은 것: `ai` 브랜치 4건 머지 후 전 브랜치 재동기화(내일 아침). `transcribe_batch.py` 실제 실행 검증. 골든셋 비율 근거는 팀 확인 대기
### 2026-08-26 (14)
- **첫 스포크 `fastapi/apps/retrieval/` 착수 — 지식베이스 청킹**(`w2-kb-index`). `domain/services/chunking.py`(조항 마커 파싱 + 상한 초과 시 문단 경계 분할)·`domain/value_objects/chunk.py`·`adapter/outbound/knowledge_base_loader.py`·`scripts/index_knowledge_base.py`. **청크 102개**(finance 34·shopping 27·health 21·dasan 20), 두 번 돌려 바이트 단위로 동일함을 확인. `.importlinter` 다섯 목록에 `retrieval` 등록 — 계약 5종 KEPT, `pytest` **64개 통과**(45→64)
- **청킹 방식을 티켓의 "고정 길이"에서 "1 조항 = 1 청크"로 변경** — 조항 102개 길이를 실측하니 중앙값 101자·최대 332자로 **400자 초과가 0건**이라, 고정 길이(500자 등)로 자르면 조항이 쪼개지는 게 아니라 여러 조항이 한 청크로 뭉친다. 그러면 골든셋 `expected_doc_ids`(조항 ID 기준)로 Recall@5 를 채점할 수 없다. 상한 400자는 문서가 길어질 때를 위한 안전장치로만 남겼다
- **골든셋 재작성(오늘 11:20, 류준) 검증** — 도메인 분포(finance 4·shopping 3·dasan 2·health 1)와 참조 문서 ID 3건이 `knowledge-base/` 92개 안에 전부 실재함을 확인. 깨진 참조 0건
- **낡은 문서 정리** — `docs/domain.md`가 오늘 끝난 작업 3건(골든셋 재작성·DB 스키마 정리·도메인 라우팅 확정)을 여전히 "대기/미설계"로 적고 있어 갱신. `jekyll/docs/05`(⚠ 미반영)·`docs/14`(⚠ 재작성 필요)도 함께. 해소된 「한계」 항목은 지우지 않고 취소선 + 해소 근거를 붙였다. 아직 사실인 미결 2건(계약 `domain` 필드 v3, ES 인덱스 분할)은 그대로 뒀다
- 티켓 정합성 정정 — `w2-naive-rag` 가 `services/core/`·`RetrievalPredictor` Protocol(구 구조)을 가리키고 있어 `fastapi/apps/retrieval/`·`RetrievalPort` ABC(async)로 갱신. `w2-kb-index` 는 청킹 방식 변경 근거를 본문에 남기고 `in-progress` 로, `w2-golden-set-50` 은 "기존 10건 무효" 표현을 정정
- **`w2-db-schema-domain`·`w2-domain-routing` 은 내 수정을 물리고 류준 님 판(`origin/main`)을 채택** — 같은 티켓을 양쪽이 각각 고쳤고 류준 님이 13:03 으로 먼저였다. `CLAUDE.md` 칸반 규칙("나중에 시작한 쪽이 물러난다")을 따랐다. 두 티켓 모두 류준 님은 `done`, 나는 `in-progress` 로 봤는데 완료 조건의 팀 승인·계약 `domain` 필드 판단이 갈린 것이다. 계약 `domain` 필드 미결은 [7.3절](/docs/07/)에 그대로 남아 있다
- 로컬 개발 환경 구축 — `.venv`(Python 3.13.13) + `fastapi/requirements.txt`
- 남은 것: ES 적재(인덱스 분할 여부 미결로 막힘), `w2-naive-rag` BM25 검색 경로

### 2026-08-26 (13)
- **AI 모델 구성 전면 확정 — Opus 교차검증 반영** — 사용자가 별도로 Claude Opus에게 5개 역할(임베딩·생성·생성 대조군·NER·분류기) 전부 모델을 추천받아왔다. 그대로 받지 않고 검증 가능한 주장을 전부 직접 확인: ① `ko-sroberta-multitask`의 `sentence_bert_config.json`에 `max_seq_length: 128` 실제 확인(아키텍처는 512 지원하지만 SentenceTransformer로 쓰면 128에서 잘림), 지식베이스 조항 103건 직접 토크나이즈해 **8.7%가 128토큰 초과** 확인 → `KoE5`(512토큰, 1024차원, MIT)로 교체 확정. ② `EXAONE-4.0-1.2B`를 실제로 받아 `exaone3.5:2.4b`와 같은 방식으로 재측정 — **250토큰 2.01~2.14초로 3.5보다 1.7배 빠르고 크기는 절반**이라 다시 교체. 단 하이브리드 reasoning 모델이라 기본 상태로는 Qwen3와 같은 실패 모드(추론에 토큰 예산 전부 소진, 답 못 냄)가 실측으로 재현돼 **`/api/chat`+`think:false` 필수**임을 확인. NC 라이선스 원문도 확인(포트폴리오 프로젝트라 문제없음 판단). ③ 분류기(`KcELECTRA-base`)·NER(`koelectra-ner`)는 유지하되 `klue/roberta-base`를 분류기 대조군으로 추가(5주차 실측 비교) — 이건 파인튜닝 헤드가 없어 지금 실측 불가, 결정만 하고 측정은 미룸. `KoE5`·`klue/roberta-base` 로컬 다운로드 완료, `kanana-1.5-2.1b-instruct`(생성 대조군)는 Ollama에서 못 찾아 6주차로 미룸
- `scripts/download_models.py` TARGETS 갱신(KoE5·klue-roberta-base 추가, polyglot 제거는 이전 세션에서 이미 반영), [3.1절](/docs/03/)·[4.3절](/docs/04/) 갱신, 결정 기록 `_project/decisions/010-AI-모델-구성-확정.md`(`decisions/009`는 후속 갱신 절 추가로 연결)
- 남은 것: KoE5 vs 기존 임베딩 Recall@5 비교(4주차), 분류기 대조군 비교(5주차), 생성 대조군 환각 비교(6주차) — 전부 아직 미실측. NER P7(상세주소) 규칙 보강도 미착수

### 2026-08-26 (12)
- **생성 모델을 `polyglot-ko-1.3b`(HF Transformers)에서 `exaone3.5:2.4b`(Ollama 서빙)로 교체** — 4주차를 앞두고 실제로 로드해서 추론 속도를 쟀다. `polyglot-ko-1.3b`는 250토큰 생성에 7.6~7.7초로 목표(3~5초)를 크게 초과했고, instruction 튜닝이 안 된 베이스 모델이라 요약 지시를 무시하고 원문을 반복 출력(품질도 실패). Ollama로 대안을 실측(중국 출처 모델 제외 — Qwen3는 기본 "thinking" 모드가 250토큰 예산을 추론에 다 써버려 실제 답을 못 내는 문제까지 확인): `llama3.2:3b`(Meta) 2.75초지만 지시 이행 불완전 vs **`exaone3.5:2.4b`(LG AI Research) 3.63초, 지시 정확 이행, 예시까지 든 자연스러운 한국어** — 목표·품질 모두 충족해 확정. 재현: `scripts/test_generation_latency.py`(HF, 비교용), `scripts/test_ollama_latency.py`. [3.1절](/docs/03/)·[4.3절](/docs/04/) 갱신, 결정 기록 `_project/decisions/009-생성모델-EXAONE-Ollama-확정.md` — Ollama는 원래 투입자원 목록 밖 도구라 예외 사유도 함께 기록
- Ollama가 스택에 새로 들어오면서 [3.1절](/docs/03/) 도구 매핑 표·"목록 밖 도구 없음" 원칙 문구 갱신
- 남은 것: 컴플라이언스 분류기 베이스(`KcELECTRA-base`)·NER(`koelectra-ner`) 교체는 사용자가 "임베딩 제외 전부 교체 예정"이라 밝혀 추천안을 `open-items.markdown`에 남김 — 파인튜닝 헤드가 없어 이 둘은 생성 모델처럼 바로 실측할 수 없었음(결정은 아직 안 함)

### 2026-08-26 (11)
- **검수 방식을 "건건이" 대신 "체크포인트에 모아서"로 전환** — 사용자 지시: 아직 검수할 실물(실행되는 서비스, 실측 지표)이 부족하고 4인 전원이 각자 담당을 동시에 진행 중이라, 완료 건마다 즉시 검수를 기다리지 않고 계속 작업하다가 **4주차 말(5주차 오류 내성 실험 착수 직전)에 팀 전체가 모여 한 번에 검증**하기로 확정. 기존 6주차 코어 기준선·7주차 F-2 체크포인트는 유지, 그 사이에 하나 추가. 근거: `_project/decisions/008-검증-체크포인트-방식-전환.md`. [8절 마일스톤](/docs/08/)에 절 추가, [7.4절](/docs/07/) 원칙 추가, `w2-golden-set-50.md`의 완료 조건을 "체크포인트에서 교차검수"로 재정의. `w1-db-schema`는 아래 (9)에서 이미 팀원 확인으로 승인 처리돼 있어 그대로 둠
- 검수 없이 확정된 것처럼 기록하지는 않는다 — F-2 케이스 16건은 여전히 검수 대기로 표시

### 2026-08-26 (10)
- **골든셋 50건 작성** — `golden-set/v1-50.json` 신규(기존 10건 GS-001~010 포함). 도메인 분포: 금융보험 18(F-2 9)·쇼핑 16(F-2 7)·다산콜센터 9·질병관리본부 7 — 균등 대신 F-2 적용 도메인에 더 배정(`w2-golden-set-50.md`가 남긴 질문에 대한 답). 모듈 분포: B 14·C-1 3·C-2 3·C-3 4(신규 모듈 — 필수 안내 누락)·C-5 10(P1~P7 전 패턴)·F-2 16. 모든 문서 ID를 `knowledge-base/`의 실제 `<!-- id: -->` 주석과 대조해 검증(존재하지 않는 ID 0건), `fastapi/apps/evaluation/golden_set.py` 로더로 실제 파싱 확인(코드 변경 없음). `golden-set/README.md` 갱신
- 장민석이 `fastapi/apps/` 아키텍처 구조를 작업 중이라, 이번 작업은 의도적으로 `golden-set/`·`jekyll/_backlogs/` 등 fastapi/ 코드와 겹치지 않는 범위로만 진행
- 남은 것: F-2 케이스(16건) 검수 — 작성자(류준)가 아닌 사람이 확인. 아래 (9)에서 `w2-domain-routing`·`w2-db-schema-domain`도 이미 `done`으로 정정돼 있어 중복 반영하지 않음

### 2026-08-26 (9)
- **로그 백필 — 정성윤(PM) 작업 2일치** (08-25~08-26에 했으나 이 로그에 기록이 누락됐던 작업, 뒤늦게 기록). 08-26 기준 이 로그의 항목 8개가 전부 류준·장민석 작업이고 PM 세션 기록은 0건이었다. 원인은 세션 내용을 **PR 본문에만 쓰고 `progress.markdown`으로 옮기지 않은 것** — 내용을 빠뜨린 게 아니라 목적지를 틀렸다. PR은 머지되면 닫히고 팀이 보는 `/progress/`는 비어 있었다. 재발 방지는 이 항목 마지막에
  - **CI 워크플로 신설 (`.github/workflows/test.yml`)** — 하네스 테스트 job + 사이트 빌드 job. 범위를 좁게 잡았다: `requirements.txt` 전체가 아니라 테스트가 실제 import 하는 것만 설치(torch·transformers 제외). **기준선 미달 실패 게이트는 넣지 않았다** — 측정값이 없어 무조건 실패하거나 가짜 기준선을 적게 되므로(절대 원칙 2). 2주차 잠정 베이스라인이 나온 뒤 별도로 붙인다
  - **내부 링크 검사기 (`scripts/check_site_links.py`)** — 지킬 빌드는 깨진 내부 링크를 잡지 못한다(빌드는 통과하고 사람이 클릭할 때까지 아무도 모른다). 빌드 산출물 `_site`를 훑어 페이지·앵커 존재를 확인하고 깨지면 exit 1. 파일명이나 소제목을 바꿀 때 조용히 깨지는 링크가 대상
  - **`/CLAUDE.md` 링크 회귀 수정 (`128c3af`)** — 위 검사기가 도입 첫날 실제 회귀를 잡았다. [5절](/docs/05/)에서 절대 원칙 6을 인용하며 `/CLAUDE.md`로 링크했는데 `CLAUDE.md`는 저장소 루트(`jekyll/` 밖)라 사이트로 나가지 않아 404. GitHub blob 주소로 교체
  - **브랜치 개편 반영 `flutter` → `ai` (`5f50fe2`)** — 문서만 고치면 되는 변경이 아니었다. `test.yml`의 트리거 목록이 없어진 `flutter`를 가리키고 `ai`가 빠져 있어, 그대로 뒀으면 **류준·장민석의 `ai` 브랜치 푸시에 CI가 돌지 않았다.** `CLAUDE.md` 브랜치 규칙·`w1-eval-ci` 티켓·`_project/STATE.md` 동기화. 과거 시점을 기록한 문서(`decisions/005` 등)의 `flutter` 언급은 그대로 뒀다(절대 원칙 8)
  - **2주차 티켓 8건 생성 (`1aaf048`)** — 4인 전원 배분, 조서희 첫 티켓 포함. 팀 결정이 필요한 두 곳(도메인 라우팅 A/B, 골든셋 50건의 도메인별 비율)은 선택지와 판단 재료만 적고 결정은 비웠다. 이 중 도메인 라우팅은 같은 날 류준·장민석이 자동 분류(B안)로 확정했다((7))
  - **PR #15 충돌 분석** — `backend`→`main`이 CONFLICTING 이었다. 위험한 건 `services/core/eval/harness.py`의 modify/delete 였다: main은 `fastapi/`로 이사하며 삭제했고 backend는 같은 파일에 B-0을 추가했다. main의 삭제를 그대로 받으면 B-0 작업(메트릭·테스트·결정 기록 006·007)이 통째로 유실될 상황이라 임의로 머지하지 않고 넘겼다. 실제 해결은 (8)의 포팅
  - **대시보드 티켓 정정 → 되돌리기 (`017036f` → `19125ac`)** — 착수 전 todo 티켓의 담당이 장민석으로 남아 있어 삭제·통합했으나, 같은 문제를 류준이 `backend`에서 담당자 수정으로 고치는 중이었다. PM을 그대로 main에 올리면 PR #15 충돌이 "수정 vs 수정"에서 "수정 vs 삭제"로 커지므로 되돌렸다 — 나중에 시작한 쪽이 물러난다
  - **브랜치 동기화** — `ai`·`frontend`를 main(`0cf1b6c`)으로 fast-forward, PM에 main 병합(충돌 0건, CI 통과). `backend`는 푸시 권한 차단으로 미적용(main보다 1커밋 뒤, `git pull` 한 번이면 따라잡음)
- **칸반 대시보드 중복 티켓 정리** — `w1-dashboard-scaffold`(sprint 1)와 `w2-dashboard-scaffold`(sprint 2)가 같은 작업으로 보드에 둘 다 떠 있었다. w1은 착수 전 todo 인 데다 front matter(`assignee: 조서희`, 류준 수정)와 본문("assignee는 소급 수정하지 않는다", 내가 쓴 글)이 서로 모순된 상태였다. 실제 착수 시점이 2주차이므로 **w1을 지우고 w2 하나로 합쳤다.** 류준이 고친 내용(이 작업은 조서희 담당)은 w2가 그대로 담고 있어 유실 없음
- **재발 방지 — 규칙에 확인 장치를 붙였다.** 지금까지 지켜진 규칙(자격증명 금지·한글 파일명 금지 등)은 전부 어기면 즉시 드러나거나 CI가 잡는 것들이었고, 진행 기록만 **어겨도 아무 일이 없어서** 뚫렸다. ① `CLAUDE.md`에 §0 세션 시작 루틴과 짝이 되는 **세션 종료 루틴**을 바로 아래에 추가(시작 루틴을 읽을 때 같이 읽히게) ② CI 에 `scripts/check_progress_log.py` — 커밋이 있는 날짜에 로그 항목이 있는지 확인, **경고만**(로그 누락으로 코드 머지를 막는 건 과하다). 도입하자마자 2026-08-24 커밋 9건에 로그 항목이 없다는 실제 공백을 잡았다
- **세션 종료를 훅으로 강제** — 규칙과 스크립트만으로는 내가 안 부르면 안 돌아간다. `Stop` 훅에 `scripts/check_session_end.py --hook` 을 걸어 **파일을 고쳤는데 `progress.markdown` 을 건드리지 않았으면 exit 2 로 세션이 끝나지 않게** 했다(자격증명 훅과 같은 방식). 함께 도는 경고 2종: 티켓 `paths:` 소관 파일이 바뀌었는데 아직 todo 인 경우, 슬러그가 겹치는 중복 티켓. 절차는 `.claude/skills/session-log/` 스킬에 적었다 — 오늘 틀린 것들(기록을 PR 본문에만 씀, 남의 브랜치와 겹칠 때 처리, 중복 티켓 정리 기준)을 그대로 규칙화했다. 안전장치: 아무것도 안 고친 세션·병합 커밋만 있는 경우는 통과, `stop_hook_active` 로 무한 루프 방지, `CALLGUARD_SKIP_SESSION_CHECK=1` 탈출구. 네 경로 전부 실제로 돌려 확인했다. **만드는 중에 버그 2건을 테스트가 잡았다** — ⓐ "오늘 날짜 항목이 있는가"로 보면 팀원이 먼저 쓴 항목에 내 누락이 묻혀서(이번에 실제로 이렇게 뚫렸다) "내가 `progress.markdown` 을 건드렸는가"로 바꿨고, ⓑ `git status --porcelain` 이 미추적 디렉터리를 `apps/` 로 접어 `paths` 패턴에 안 걸려서 `-uall` 을 붙였다
- **티켓 상태 정정 (팀원 확인 반영)** — 보드의 status 가 실제 진행과 어긋나 "안 끝남"으로 보이던 것들을 팀원이 표로 짚어줘서 반영했다. `w1-db-schema` in-progress→done(도메인 정리까지 완료, `decisions/006`), `w2-db-schema-domain` todo→done(별도 진행 없이 1주차 w1 에서 끝남), `w2-domain-routing` todo→done(자동 분류로 결정 완료, `decisions/007`). **삭제하지 않고 상태만 옮기되**, 완료가 보드에서 두 번 세어지지 않도록 "실제 작업은 어느 티켓에서 끝났는지"를 각 본문에 적었다. 분류기 구현·학습은 `w1-domain-routing`(진행 중)에서 이어진다
- 남은 것: `w1-eval-ci` 가 아직 in-progress — CI 3종은 green 이지만 기준선 게이트가 빠져 있어 그대로 둔다(2주차 베이스라인 후 붙인다). `scripts/check_progress_log.py` 가 **2026-08-24 커밋 9건에 대한 로그 항목이 없다**고 잡아냈다. 그날 작업(`jekyll/` 하위 분리 등)은 08-25 항목에 섞여 기록된 것으로 보이나 날짜 항목 자체는 없다 — 소급 작성 여부는 미정

### 2026-08-26 (8)
- **`backend`·`main`(`ai` 브랜치 경유) 통합** — GitHub에서 `backend`→`main` PR에 충돌이 뜬 걸 확인. 원인: `ai` 브랜치(정성윤·장민석)가 내 이전 푸시 지점(`a0f95d3`, 도메인 4종 전환 직후)에서 갈라져 `fastapi/` 헥사고날 아키텍처를 독립적으로 구축했고, 그 이후의 내 작업(골든셋 재작성·DB 스키마 정리·B-0 도메인 라우팅)을 모른 채였다. 구조(`fastapi/`)는 저쪽이 더 진전됐고 내용(골든셋·DB 스키마·B-0)은 이쪽이 최신이라, **`fastapi/` 구조를 정본으로 채택하고 구 `services/core/eval/`의 작업물을 그 위로 포팅**했다: `domain_routing.py` 메트릭 이식, `hub/app/dtos/domain_classification_dto.py`+`hub/app/ports/output/domain_routing_port.py` 신규(기존 6개 포트와 같은 ABC 패턴), `harness.py`에 `DomainRoutingPort` 배선, 테스트 이식(`test_domain_routing_metrics.py` import 경로 수정, `test_harness.py`에 async 가짜 포트 배선 테스트 추가). golden-set·db/schema.sql은 main이 아직 구 버전이라 자동 병합됨(내 쪽 그대로 유지). `services/core/` 디렉토리 삭제. `.claude/rules/rfp-harness.md`·`jekyll/_backlogs/w1-db-schema.md`·`w1-dashboard-scaffold.md`·`knowledge-base/README.md`의 병렬 편집도 수동 병합
- 남은 것: `cd fastapi && pytest`·`lint-imports` 재확인 후 커밋·푸시

### 2026-08-26 (7)
- **지식베이스 팀 리뷰 완료** — 정성윤·장민석·조서희 팀 회의로 4개 도메인 지식베이스(`knowledge-base/`) 리뷰 마무리. `w1-knowledge-base.md` done 처리
- **도메인 라우팅 방식 확정 — 자동 분류** (수동 선택 안 함). 근거·설계: `_project/decisions/007-도메인-라우팅-자동분류-확정.md`. 상담원이 매번 도메인을 고르지 않고, 초반 발화를 KcELECTRA 계열 분류기(B-0)로 4클래스 분류하고 신뢰도가 낮으면 4개 인덱스 하이브리드 검색 폴백으로 판정하는 설계로 잡았다 — 새 도구 도입 없음
- **평가 하네스에 B-0 배선** — `services/core/eval/metrics/domain_routing.py`(정확도 + 오분류 행렬, 규칙 기반) 신규, `harness.py`에 `DomainPredictor` Protocol 추가(미구현 시 "측정 불가"로 정직 보고), 골든셋 `domain` 필드를 정답 라벨로 재사용. [6.1절](/docs/06/)에 목표(정확도 ≥0.95) 반영, [3.2절](/docs/03/)·[2.3절 B-0](/docs/02/) 문서화. 테스트 6건 추가 — `pytest services/core` 33개 전부 통과. 신규 티켓 `w1-domain-routing.md`(류준·장민석 공동). *(2026-08-26 (8)에서 `fastapi/evaluation/`으로 이식됨)*
- 남은 것: 실제 분류기 구현·학습은 미착수(골든셋 표본 부족, 2주차 확대 후 착수), 폴백에 필요한 B-2 하이브리드 검색도 아직 없음

### 2026-08-26 (6)
- **DB 스키마를 4개 도메인에 맞게 정리** — 통신 도메인 잔재였던 `plan`(요금제) 테이블 제거, `subscriber`를 `customer`로 정리(체납·분실신고 플래그 삭제 — 지금은 존재하지 않는 TERM-5.3(명의변경 제한)에만 쓰였던 필드), `call`에 `domain` ENUM('finance','dasan','shopping','health') 컬럼 신설(도메인 라우팅 정보가 스키마에 아예 없었던 공백을 메움), `closure.closure_type`/evidence 컬럼을 실제 F-2 적용 도메인(금융보험 상품해지·보상, 쇼핑 반품·교환) 기준으로 교체. `db/generate_schema_docs.py` 수정 후 재실행해 `schema.sql`·`erd.dot`·`ERD.png` 재생성 — 17개→16개 테이블. `db/docs/ERD.md`·[16절 ERD](/docs/16/)·[7.3절 인터페이스 계약](/docs/07/) 예시 전면 갱신, `test_closure_gate_metrics.py` 필드명 동기화 — `pytest services/core` 27개 계속 통과. 결정 기록: `_project/decisions/006-db-스키마-도메인-정리.md`
- 남은 것: `call.domain`을 실제로 언제·어떻게 채울지(도메인 라우팅 로직)는 여전히 미결([3.2절](/docs/03/)). `closure` evidence를 넓은 표로 둘지 EAV로 둘지도 기존 미결 그대로. 실제 MySQL 마이그레이션 적용은 미착수

### 2026-08-26 (5)
- **골든셋 10건 재작성** — 한별텔레콤 시나리오였던 기존 10건을 4개 도메인(금융보험·다산콜센터·쇼핑·질병관리본부) 기준으로 전면 재작성. 분포: 금융보험 4(B·C-1·F-2×2)·다산콜센터 2(B·C-5)·쇼핑 3(B·C-5·F-2)·질병관리본부 1(C-2). F-2 케이스는 F-2 적용 도메인(금융보험·쇼핑)에서만 작성. `services/core/eval/golden_set.py`에 `domain` 필드 파싱 추가, `test_golden_set.py`에 도메인 커버리지·F-2 도메인 제약 테스트 2건 추가 — `pytest services/core` 27개 전부 통과. `golden-set/README.md` 갱신
- `w1-dashboard-scaffold.md` 담당자를 장민석 → 조서희로 변경 (팀 개편 반영 — [7.1절](/docs/07/))
- 남은 것: 팀 리뷰(F-2 케이스는 규정 작성자 아닌 사람이 검수), 도메인별 Recall@5 집계를 `harness.py`에 배선

### 2026-08-26 (4)
- **백엔드 루트를 `fastapi/`로 확정하고 [Task 1] FastAPI 골격 스캐폴딩 — `ai` 브랜치** (`backend`에서 작업하던 것을 `ai`로 옮김). `services/core/eval`→`fastapi/evaluation`(내장 `eval` 가림 해소), `requirements.txt`·`pytest.ini`도 `fastapi/`로(Python 3.13). 신규: `main.py`(합성 루트, `/health` — 설정 *여부*만/SEC-2), `core/config.py`(`.env.example` 키 1:1, `os.environ` 읽는 유일한 곳), `hub/`(7.3절 v2 계약 DTO 3종 + 스포크 포트 6개 + `transcript_ingest`·`myself` 슬라이스를 schema→router→dto→input port→interactor→record port→log adapter→provider→test **프랙탈 단면**대로), `fastapi/.importlinter`(계약 5종 — 클린 계층·스포크 독립·프레임워크 격리·도메인 순수성·허브 격리). `POST /hub/transcripts`는 masking 스포크 미등록 시 **501** — 마스킹 없는 임시 통과 경로는 만들지 않음(SEC-1)
- **`docs/` 구조 하네스 문서 4종** — `harness.md`(요구사항/평가/구조 하네스 경계 + 검증 명령 + 문서 온톨로지), `architecture.md`(허브-스포크, 헥사고날, 수직 슬라이스 1:1, SOLID 대응, 4인 담당), `domain.md`(**도메인 4종 기준으로 재작성** — 스포크는 기능 축·도메인은 데이터 축, 도메인별 F-2 근거 필드 표, 골든셋 무효·라우팅 미설계 등 한계 명시), `plan-rev4.1.md`(사본). redoceanmap 프로젝트의 슬라이스 1:1·프랙탈 규칙을 크로스체크해 위반 4건(허브 슬라이스 누락·빈 포트·레이아웃·DTO 내 판정 로직) 정정, 평가 하네스는 hub 포트를 직접 소비(`Ports`)해 스포크당 계약 1개
- CI `test.yml`을 `fastapi/` 기준으로 갱신(Python 3.13, pytest + import-linter step, `ai` 브랜치 트리거). 검증: `cd fastapi && pytest` **37개 통과**, `lint-imports` 5종 통과. 남은 것: 7.3절 계약 `domain` 필드(v3), 도메인 라우팅 설계, 골든셋 재작성 후 `golden_set.py` 로더 갱신

### 2026-08-26 (3)
- **백엔드·AI(류준·장민석) 내부 분담 방식 확정** — 기능별로 쪼개 전담을 나누지 않고 **둘이 함께(공동 작업)** 하기로 확정. `jekyll/docs/07`·`open-items.markdown`·`.claude/rules/rfp-harness.md`·`14-이번주할일.markdown` 반영, `_project/decisions/005` 갱신

### 2026-08-26 (2)
- **팀을 3인 → 4인으로 개편** — 플러터(Flutter) 앱 개발을 중단하고, 장민석이 앱·프론트엔드에서 류준과 함께 백엔드·AI로 옮겼다. 조서희가 신규 합류해 프론트엔드(웹, `apps/dashboard`)를 전담한다. 정성윤은 AWS·인프라 그대로. [7.2절 부하 경고](/docs/07/)가 지적한 "류준 단독 백엔드·AI 과부하"가 이 개편으로 구조적으로 해소됨 — 기존 완화 조치(C-5·CI 운영→정성윤)는 유지. `CLAUDE.md`, `.claude/rules/rfp-harness.md`·`dashboard.md`, `jekyll/docs/07,14`, `jekyll/kanban.markdown`, `_project/rev4-보완지시서.md`(10번 항목) 반영. 근거: `_project/decisions/005-팀-개편-4인-체제.md`
- 기존 칸반 티켓의 `assignee`는 소급 수정하지 않음(작성 당시 실제 담당자 기록 원칙 유지). `origin/flutter` 브랜치는 삭제하지 않고 보존
- 남은 것: 류준·장민석 사이 백엔드·AI 세부 분담(검색/생성/컴플라이언스/F-2 등) 미정 — `open-items.markdown`에 등록

### 2026-08-26
- **데모 도메인을 가상 통신사 "한별텔레콤" 단일 시나리오에서 실제 확보 데이터 4종(금융보험·다산콜센터·쇼핑·질병관리본부)으로 전환** — 실제로 신청·확보한 데이터가 통신 도메인에는 없고, AI Hub 「민원(콜센터) 질의-응답」데이터셋(`data/raw/aihub-minwon-qa/`)이 이 4개 도메인의 실측 QA(화자·발화문·고객의도·상담사의도·개체명·지식베이스 참조 필드 포함)로만 구성돼 있다는 사실을 뒤늦게 재확인했다. 4개 도메인 전부 지원하는 쪽으로 결정(1개로 좁히지 않음) — 근거·선택지·되돌리는 법은 `_project/decisions/004-데모-도메인-4종-확정.md`
- **`knowledge-base/` 도메인별 4개 폴더로 재구성** — `finance/`(한별금융)·`dasan/`(한별시 통합민원콜센터)·`shopping/`(한별샵)·`health/`(한별헬스콜), 각각 terms/manual/policy 3종. 도메인 접두어 ID 체계(`FIN-`/`DASAN-`/`SHOP-`/`HLT-`) 적용. F-2(종결 요건 검증)는 종결형 처리가 있는 금융보험(상품해지·보상)·쇼핑(반품·교환)에만 적용, 안내형 업무인 다산콜센터·질병관리본부는 미적용으로 명시(대신 D-4 공백 리포트로 검증)
- **기획서·사이트 문서 동기화** — `CLAUDE.md`, `_project/rev4-보완지시서.md`(9번 항목 신규 추가), `jekyll/docs/01,02,04,05,06,07,09,14,15,16` 갱신. 특히 [5.1절](/docs/05/)에 그동안 "선택 사항"으로 취급되던 `aihub-minwon-qa` 데이터셋을 핵심 데이터로 재규정하고 `data/README.md`도 동기화
- **미반영 항목 기록** — `golden-set/v1-10.json`(한별텔레콤 시나리오라 재작성 필요, `w1-golden-set-10.md` 갱신)과 `db/schema.sql`·ERD의 `subscriber`/`plan` 등 통신 특화 테이블은 이번 세션에서 손대지 않았다. 후속 엔지니어링 티켓으로 남김

### 2026-08-25 (14)
- **정성윤의 GCP 쿼터·Pages 배포 개선 병합** — 병합 작업 중 `origin/backend`에 정성윤이 먼저 올린 커밋(STT 쿼터 하드 리밋 상세 기록, 예산 알림 설정, Pages 배포 워크플로를 "main에 머지되면 항상 배포"로 단순화, 완료 티켓 3건 상태 갱신)을 확인. `open-items.markdown`의 트리거 허용 창 항목에서 충돌 1건(내가 방금 갱신한 1,500ms 내용 vs 정성윤의 예전 800ms 줄 + 새 GCP 정리 할 일) — 미리보기 병합으로 확인 후 양쪽 내용을 모두 살려 수동 해결. 병합 후 테스트 25개·빌드 재확인 (`9eab5b1`)

### 2026-08-25 (13)
- **로그 백필 — Python 의존성 자동화** (세션 초반에 했으나 이 로그에 기록이 누락됐던 작업, 뒤늦게 기록). `requirements.txt`에 torch·transformers·huggingface_hub·sentencepiece·accelerate·pytest 고정, `scripts/check_requirements_updates.py` + 로컬 launchd(`com.callguard.requirements-check.plist`, 매주 월요일 09:00)로 PyPI 버전 자동 확인·갱신 체계 구축(클라우드 RemoteTrigger는 로컬 `.venv`에 못 닿아 로컬 예약 작업으로 결정). `scripts/download_models.py`로 오픈소스 모델 4종(~8.9GB) 다운로드 완료. 신규 티켓 `w1-visual-redesign`·`w1-repo-integration`·`w1-requirements-automation` 추가 — 지킬 비주얼 통일((9))·저장소 통합((7)(8))·이 항목이 지금까지 칸반 보드에 없었다

### 2026-08-25 (12)
- **인터페이스 스키마 v2 — 정성윤 조건부 컨펌 반영** ((11)의 "초안 그대로 확정"을 정정한다). 정성윤이 v1을 `db/schema.sql`·`golden-set/v1-10.json`과 필드 단위로 대조해 불일치 4건을 확인했고, 내(류준)가 코드로 직접 재검증 후 전부 사실로 확인했다: ① `verdict`는 `approved`/`blocked`(`allowed` 아님, DB ENUM·골든셋과 일치) ② `source`는 사람이 읽는 이름이 아니라 `doc_id`+`title` (DB FK·골든셋 `expected_doc_ids`가 ID 기준) ③ `evidence`는 `closure_type`별 부분집합(해지/명의변경/보상 컬럼이 다름), `missing`은 `false`인 키만 ④ 전사 이벤트에 `segment_id` 추가(interim 199건/20초를 구분할 식별자 필요). [7.3절](/docs/07/) v2로 갱신, 결정 기록 `_project/decisions/003-인터페이스-스키마-v2.md`
- **3주차 트리거 v1을 STT `is_final` 기반으로 설계 변경** — 자체 침묵 타이머를 따로 두면 STT 자체 엔드포인팅 지연(+346ms, V4 실측)과 이중으로 쌓인다는 정성윤 지적을 받아들여, `is_final` 도착을 발화 종료 신호로 쓰기로 했다. 1,500ms 허용 창의 근거도 "침묵 대기 최대 1,000ms"에서 "STT 엔드포인팅 +346ms 실측 + 판정·큐잉 여유 500ms"로 갱신([4.1절](/docs/04/))
- **평가 하네스에 트리거 지연 분포(p50/p95/p99) 배선 완료** — `services/core/eval/harness.py`의 `run_eval`이 트리거 delta를 모아 기존 `metrics/latency.py`(`summarize_latency`)로 계산, `report["trigger"]["latency_ms"]`에 싣는다. 가짜 predictor로 배선 테스트 추가(`test_harness.py`), 전체 25개 테스트 통과
- 티켓 갱신: `w1-interface-contract.md`·`w1-trigger-window.md` 모두 `done` 처리

### 2026-08-25 (11)
- **인터페이스 스키마 3종(전사·카드·종결) 팀 컨펌 완료** — [7.3절](/docs/07/) 초안 그대로 확정, 결정 기록 `_project/decisions/002-인터페이스-스키마-확정.md` 작성. 이제 각자 파트가 이 계약 기준으로 병렬 진행 가능
- **트리거 허용 창 800ms → 1,500ms로 확정** — 보완지시서 1번 안 A 채택(2026-08-25 팀 컨펌). 침묵 기반 트리거(700~1,000ms 대기) 특성상 800ms 창으로는 적절 발동률 0.85가 구조적으로 불가능했던 문제 해소. 안 B(침묵 임계값 실측 후 역산)는 검토했으나 보유 AI Hub 데이터가 발화 단위로 이미 분절돼 있어(세션 JSON에 타임스탬프 없음) 발화 간 침묵 길이를 잴 수 없어 기각. [4.1절](/docs/04/)·[6.1절](/docs/06/)(p50/p95 기록 항목 추가)·`services/core/eval/metrics/trigger.py`(`ON_TIME_WINDOW_MS`)·테스트 반영, `_backlogs/w1-trigger-window.md` done 처리

### 2026-08-25 (10)
- **Google STT 키 발급 + 연결 테스트 성공** — GCP 콘솔에서 서비스 계정 키(JSON) 발급, `.env`의 `GOOGLE_APPLICATION_CREDENTIALS`(경로만)·`GOOGLE_CLOUD_PROJECT` 설정. `scripts/test_stt.py`로 실제 오디오 1건 전사 성공 확인(키 파일 내용은 스크립트도 사람도 읽지 않음, 경로만 사용)
- **[5.6절](/docs/05/) V3·V4 실측 완료** — V3(한국어 숫자 출력 형태): 실제 AI Hub 오디오 3건으로 확인한 결과 완전 정규화/부분 정규화/오인식이 케이스마다 혼재, 자릿수 낭독형(인증코드류)은 저품질 통화 음성에서 오인식 위험 큼. V4(스트리밍 부분 결과 지연): 20.58초 실통화 음성 실시간 페이싱 전송 결과 첫 interim 962ms, 최종 결과는 발화 종료 후 +346ms. 재현 스크립트 `scripts/test_stt_v3.py`·`scripts/test_stt_v4_streaming.py`, 상세는 [5.6절](/docs/05/)·[미결 항목](/open-items/)에 반영
- `requirements.txt`에 `google-cloud-speech==2.40.0` 추가

### 2026-08-25 (9)
- **사이트 전체 비주얼 통일** — Claude Design으로 만든 표지 시안(딥네이비+골드+모노 HUD)을 실제 지킬 사이트에 반영. 표지는 정적 이미지 대신 `jekyll/assets/js/hologram.js`로 **실제로 회전하는** 와이어프레임 구체 홀로그램(캔버스, 노드/링크/궤도밴드/코어 글로우)으로 구현 — 마이크를 연결하면 실음성 레벨에 반응하고, 안 하면 idle 호흡 패턴으로 계속 움직임(정적 이미지 아님)
- `_layouts/cover.html`·`_layouts/doc.html`에 공통 디자인 토큰 적용: Syne(제목)·IBM Plex Mono(HUD·배지·표 헤더)·Pretendard Variable(본문), 골드 `#F5A623` 액센트, 딥네이비 `#080B12` 배경. `doc.html`은 무거운 캔버스 대신 헤더 브랜드 판 뒤 CSS 방사형 글로우만 둬서 본문 많은 페이지도 가볍게 유지
- 칸반(`kanban.markdown`)·마일스톤(`docs/08`)의 역할 배지(`role-infra/ai/app`)를 모노스페이스 HUD 톤으로 재배색
- 브라우저로 표지·목차·기능명세·칸반·ERD 페이지 렌더링과 홀로그램 회전(줌으로 두 시점 비교) 확인, 콘솔 에러 없음

### 2026-08-25 (8)
- **두 갈래로 갈려 있던 저장소를 하나로 통합** — `origin/main`(PM 브랜치 계열)과 `origin/backend`는 공통 조상이 없는 별개 히스토리였다. `integrate-backend` 브랜치에서 파일 단위로 비교해 정본을 정하고 합쳤다
- **지킬 사이트는 backend 쪽을 정본으로 채택** — 사업명(CallGuard)·팀명(SOLIDBOB)·개발기간 등 사실 정보가 정확하고, 기획서 16개 절을 1:1로 문서화했으며 자체 `cover`/`doc` 레이아웃과 빌드 성능 수정까지 반영돼 있다. PM 계열 사이트(표지+5개 절+`_posts`/`_data`)는 히스토리에만 남기고 트리에서 제거
- **ERD/스키마도 `db/`를 정본으로 확정** — 실행 가능한 DDL이고 이미 팀 교차검증(`db/docs/ERD.md`)을 거쳤다. PM 계열 `docs/erd/`(Mermaid + 정규화 문서)는 중복이라 제거
- **`CLAUDE.md`는 병합** — backend의 프로젝트 정체성·사이트 컨벤션(레이아웃/front matter/permalink/진행기록)에 PM 계열의 절대 원칙 10개, 수치 기록 규칙, 커밋 규칙, 공개/비공개 경계를 얹었다
- **`.gitignore`는 backend 것 채택**(Python·Node·macOS·자격증명 안전망) + `.claude/settings.local.json` 한 줄 추가. `.claude/`는 정리된 PM 계열에 backend 고유 규칙(`rules/rfp-harness.md`, `rules/dashboard.md`)만 흡수 — 외부 저장소에서 흘러든 파일(`memory/`, `rules/pci.md` 등)은 다시 들이지 않았다
- PM 계열에서 살린 것: `_project/`(기획서 rev.4 원본·보완지시서·결정 기록), `.github/workflows/pages.yml`(Pages 배포)
- **미결 2건 등록** — ① 사이트 문서는 5인 트랙 rev.4, `_project/plan.md`는 3인 실명 rev.4라 값이 갈린다(트리거 허용 창 800ms vs 1,500ms). 정본 확정 필요 ② Pages 활성화는 `solidbob02` 계정에서 Source를 "GitHub Actions"로 바꿔야 동작

### 2026-08-25 (7)
- 저장소 구조 조정 — 지킬 사이트를 저장소 루트에서 `jekyll/` 하위로 이동(`_config.yml`, `_layouts/`, `index/toc/progress/open-items.markdown`, `docs/`, `sprints/`, `404.html`, `Gemfile*`). 앞으로 생길 `services/`·`apps/`·`infra/`(코드)와 지킬 사이트를 분리하기 위함
- `origin/backend`에 이미 팀원이 독자적으로 만들어둔 별개 히스토리(공통 조상 없음, `jekyll/` 하위 구조 + 자체 ERD `docs/erd/`)를 확인. 팀 확인 후 **우리 쪽 ERD(`db/`)를 정본으로 채택**하고 구조는 팀원 컨벤션(`jekyll/` 하위)을 따르되 페이지 내용은 기존 형식(`docs/NN-슬러그.markdown` + `layout: doc`) 유지하기로 결정, `origin/backend`는 강제 업데이트로 교체
- ERD 이미지는 `db/generate_schema_docs.py` 실행 시 `jekyll/assets/erd/ERD.png`로 자동 복사되도록 파이프라인 확장 (dot 렌더링까지 한 번에)
- `CLAUDE.md`, `.claude/rules/rfp-harness.md` 등 경로 참조를 `jekyll/` 기준으로 갱신
- 개발 서버 실행 위치 변경: `cd jekyll && bundle exec jekyll serve --host 0.0.0.0 --port 4000`

### 2026-08-25 (6)
- MySQL 스키마·ERD 설계 완료 — 기획서엔 5개 테이블만 언급됐으나 실제 기능 명세 대조 결과 15개 필요 (가입자·요금제·문서·후속조치·공백리포트 등 추가, 1:N 관계는 분리해 1NF 준수, 2NF/3NF 검토, `closure`·`call`은 컬럼이 좁아지는 하위 테이블 대신 의도적으로 역정규화)
- `db/`(schema.sql, generate_schema_docs.py, docs/ERD.png·ERD.md·erd.dot) + 사이트에 `docs/16-ERD.markdown` 페이지 추가
- **팀 교차검증 완료** — 다른 팀원이 독립적으로 그린 ERD와 대조. 팀원 설계에서 `eval_run.error_rate`(4.2절 오류율 실험에 필수, 누락돼있던 것)·`compliance_rule`(C-4 권장 대체 표현 저장 위치)·`agent`(상담원 식별자) 3가지를 발견해 반영, 17개 테이블로 확장. 반대로 팀원 설계엔 `subscriber`/`plan`(F-3·TERM-5.3 구현 불가)·`follow_up_action`·`knowledge_gap`(D-3·D-4 누락)이 없다는 피드백을 전달. F-2 evidence를 넓은 표로 할지 팀원처럼 EAV+추적테이블로 할지는 미결 — F-2 구현 시 재검토
- 상세 기록: `db/docs/ERD.md` "팀 교차검증 기록" 섹션, 사이트: [/docs/16/](/docs/16/)
- ERD 관계선에 **실선(식별 관계)/점선(비식별 관계)** 표기 추가 — call→transcript_segment 등 "부모 없이 존재 의미 없는 약한 개체"는 실선, subscriber→plan 등 "참조·분류용, 자식이 독립 정체성 가짐"은 점선. 서로게이트 PK만 쓰는 스키마라 물리적 식별관계는 없고 개념적 표시임을 문서에 명시. FK 생성 순서 버그(document가 recommendation_card보다 뒤에 있어 실제 실행 시 에러 나던 것)도 발견해 수정

### 2026-08-25 (5)
- 평가 하네스 골격 설계 완료 — `services/core/eval/`(golden_set 로더 + metrics/retrieval·trigger·compliance·masking·closure_gate·latency + harness.py) + `services/core/tests/` 단위테스트 24개, 전부 통과
- 검색/트리거/컴플라이언스/마스킹/F-2 모듈은 Protocol로 추상화해두고 아직 `None`(미구현) — 실제 시스템 없이도 하네스가 크래시 없이 "측정 불가 — 모듈 미구현"으로 정직하게 보고하는 것까지 확인. 나중에 Predictor 구현체만 꽂으면 됨
- `pytest.ini` 추가(통합 테스트 마커 분리), `requirements.txt`에 pytest 추가, `_config.yml` exclude에 `services/` 추가
- 이걸로 서비스 코드베이스([Task 1](https://github.com/solidbob02/call.solidbob.cloud/blob/main/.claude/rules/rfp-harness.md))의 첫 조각(`services/core/eval/`)이 생김 — 나머지 스캐폴딩은 아직

### 2026-08-25 (4)
- 지식베이스 초안 작성 완료 — `knowledge-base/`에 요금제약관(TERM, 7장)·응대매뉴얼(MANUAL, 8장)·내부처리규정(POLICY) 3종, 가상 사업자 "한별텔레콤" 기준. 조항마다 ID(`TERM-3.2` 등) 부여
- 골든셋 10개 초안 작성 완료 — `golden-set/v1-10.json`, B(3)/C-1·C-2(2)/C-5(2)/F-2(3) 모듈 분포, 지식베이스 문서 ID를 그대로 참조
- **지킬 서버 장애 수정**: `data/`·`models/` 등 대용량 디렉토리를 지킬이 감시하면서 파일 감시 스레드가 죽어있던 문제(`Encoding::CompatibilityError`) 발견, `_config.yml` exclude에 `data/`·`models/`·`knowledge-base/`·`golden-set/`·`.venv/`·`logs/`·`scripts/` 추가. 빌드 시간 24.9초 → 0.05초로 단축
- 다음: 인터페이스 스키마 3종 팀 컨펌, 지식베이스·골든셋 팀 리뷰

### 2026-08-25 (3)
- AI Hub 4개 데이터셋(상담음성·고객응대음성·민원콜센터질의응답·저음질전화망음성) + 서울 열린데이터광장 행정민원상담음성까지 Validation 세트 전부 확보, `data/raw/` 구조 검증 완료 (총 ~9.8GB)
- **[V2] GPU 확인 완료** — 개발기(Apple M5 MacBook Air, 24GB)는 CUDA GPU 없음, PyTorch MPS 가속만 가능. 생성 모델은 `polyglot-ko-1.3b`급 소형부터 시작하기로 결정 ([3.1절](/docs/03/), [5.6절](/docs/05/) 반영)
- 다음: V1(채널 구성)·V3(STT 숫자 출력)·V4(부분 결과 지연) 확인, 인터페이스 스키마 3종 확정, 골든셋 10개 작성

### 2026-08-25 (2)
- STT 엔진 결정: Web Speech API(브라우저 내장, 무료) 대체안을 검토했으나 배치 파일 STT 불가·화자분리 미지원·비공식 API라 기각. **Google Cloud STT를 유지하되 무료 크레딧/무료 한도 내로만 쓰도록 이중 캡** 적용 — GCP 쿼터 하드 리밋(1차) + `services/gateway` 애플리케이션 가드(COST-1, `.env.example`의 `STT_MAX_SECONDS_PER_DAY`/`_MONTH`) 2차 방어. [리스크 및 대응](/docs/11/), [rfp-harness.md](https://github.com/solidbob02/call.solidbob.cloud/blob/main/.claude/rules/rfp-harness.md) 반영
- `.env.example`을 CallGuard 스택(MySQL·Elasticsearch·Google STT) 기준으로 재작성 — 이전 AdPass의 Aurora PostgreSQL(pgvector) 템플릿을 대체

### 2026-08-25
- 기획서 rev.4(`실시간-상담원-어시스트-RAG-기획서-rev4`) 기준으로 사이트 전체 마이그레이션 — 사업명 **CallGuard**(StreamRAG : CallGuard), 팀명 SOLIDBOB(3인: 정성윤·류준·장민석)로 전환
- 표지·개발목차·본문 15개 페이지(`docs/01`~`docs/15`) 재구성, 8주 마일스톤 체계로 일정 페이지 개편
- 깃허브 원격을 `github.com/solidbob02/call.solidbob.cloud`로 교체, 로컬 `backend` 브랜치 생성(추후 팀원 브랜치와 병합 예정)
- 다음: 1주차 목표인 AI Hub 데이터 신청, V1~V4 전제 확인, 인터페이스 스키마 확정, 골든셋 10개 작성 진행 후 결과를 이 페이지에 기록

### 2026-08-21
- 사업명 AdPass, 팀명 SOLIDBOB로 확정 — 이후 rev.4 기획서 반영으로 CallGuard 프로젝트로 대체됨
- 팀 킥오프 문서 기반으로 표지, 개발목차, 본문 페이지 구성

[← 표지로 돌아가기](/)
