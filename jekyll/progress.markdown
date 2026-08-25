---
layout: doc
title: 진행상황
permalink: /progress/
---

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
