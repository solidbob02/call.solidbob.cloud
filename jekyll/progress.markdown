---
layout: doc
title: 진행상황
permalink: /progress/
---

### 2026-08-26 (13)
- **첫 스포크 `fastapi/apps/retrieval/` 착수 — 지식베이스 청킹**(`w2-kb-index`). `domain/services/chunking.py`(조항 마커 파싱 + 상한 초과 시 문단 경계 분할)·`domain/value_objects/chunk.py`·`adapter/outbound/knowledge_base_loader.py`·`scripts/index_knowledge_base.py`. **청크 102개**(finance 34·shopping 27·health 21·dasan 20), 두 번 돌려 바이트 단위로 동일함을 확인. `.importlinter` 다섯 목록에 `retrieval` 등록 — 계약 5종 KEPT, `pytest` **64개 통과**(45→64)
- **청킹 방식을 티켓의 "고정 길이"에서 "1 조항 = 1 청크"로 변경** — 조항 102개 길이를 실측하니 중앙값 101자·최대 332자로 **400자 초과가 0건**이라, 고정 길이(500자 등)로 자르면 조항이 쪼개지는 게 아니라 여러 조항이 한 청크로 뭉친다. 그러면 골든셋 `expected_doc_ids`(조항 ID 기준)로 Recall@5 를 채점할 수 없다. 상한 400자는 문서가 길어질 때를 위한 안전장치로만 남겼다
- **골든셋 재작성(오늘 11:20, 류준) 검증** — 도메인 분포(finance 4·shopping 3·dasan 2·health 1)와 참조 문서 ID 3건이 `knowledge-base/` 92개 안에 전부 실재함을 확인. 깨진 참조 0건
- **낡은 문서 정리** — `docs/domain.md`가 오늘 끝난 작업 3건(골든셋 재작성·DB 스키마 정리·도메인 라우팅 확정)을 여전히 "대기/미설계"로 적고 있어 갱신. `jekyll/docs/05`(⚠ 미반영)·`docs/14`(⚠ 재작성 필요)도 함께. 해소된 「한계」 항목은 지우지 않고 취소선 + 해소 근거를 붙였다. 아직 사실인 미결 2건(계약 `domain` 필드 v3, ES 인덱스 분할)은 그대로 뒀다
- 티켓 정합성 정정 — `w2-naive-rag` 가 `services/core/`·`RetrievalPredictor` Protocol(구 구조)을 가리키고 있어 `fastapi/apps/retrieval/`·`RetrievalPort` ABC(async)로 갱신. `w2-kb-index` 는 청킹 방식 변경 근거를 본문에 남기고 `in-progress` 로, `w2-golden-set-50` 은 "기존 10건 무효" 표현을 정정
- **`w2-db-schema-domain`·`w2-domain-routing` 은 내 수정을 물리고 류준 님 판(`origin/main`)을 채택** — 같은 티켓을 양쪽이 각각 고쳤고 류준 님이 13:03 으로 먼저였다. `CLAUDE.md` 칸반 규칙("나중에 시작한 쪽이 물러난다")을 따랐다. 두 티켓 모두 류준 님은 `done`, 나는 `in-progress` 로 봤는데 완료 조건의 팀 승인·계약 `domain` 필드 판단이 갈린 것이다. 계약 `domain` 필드 미결은 [7.3절](/docs/07/)에 그대로 남아 있다
- 로컬 개발 환경 구축 — `.venv`(Python 3.13.13) + `fastapi/requirements.txt`
- 남은 것: ES 적재(인덱스 분할 여부 미결로 막힘), `w2-naive-rag` BM25 검색 경로
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
