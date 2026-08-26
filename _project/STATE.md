# STATE — 지금 어디까지 왔는가

> 세션 인수인계용 비공개 메모. 팀이 함께 보는 기록은 `jekyll/progress.markdown`, 미결은 `jekyll/open-items.markdown`.
> 여기에는 그쪽에 적기 애매한 내부 사정만 남긴다.

**최종 갱신**: 2026-08-26 (세션 #9)
**현재**: 1주차 / 8스프린트 (2026-08-20 ~ 2026-10-27)
**전체 상태**: 🟡 데모 도메인 전환 + 팀 개편 진행 중. 지식베이스·기획서는 4개 도메인
기준으로, 팀 문서는 4인 체제로 갱신 완료. 골든셋·DB 스키마·백엔드·AI 내부 세부 분담은
아직 미정(후속 작업 필요)

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

**다음 세션이 확인할 것**: 류준·장민석 사이 백엔드·AI 세부 분담(검색/생성/컴플라이언스/
F-2 등을 어떻게 나눌지) — 아직 팀 합의 전, `open-items.markdown`에 등록.

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
4. `services/core/eval/`의 골든셋 로더·지표 계산이 `domain` 필드를 다루도록 돼 있는지
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
5. **평가 하네스 CI 연결** — 하네스 골격은 류준이 완료(테스트 24개 통과). CI는 정성윤 담당.

---

## 내부 메모

- 이 저장소는 두 사람이 서로 모르고 같은 작업을 한 이력이 있다(사이트·ERD·골든셋 양식). **작업 전에 `jekyll/progress.markdown`을 먼저 읽는다.**
- backend의 `Gemfile.lock`은 macOS 기준이라 이 WSL에서는 `bundle install`을 한 번 돌려야 빌드된다(sass-embedded 버전 차이).
- 로컬 4000 포트는 다른 지킬 사이트가 점유 중이라 이 머신에서는 4001을 쓴다.
- 원격 인증: `gh` = SeongYuna (협업자, push 가능 / admin 아님). 저장소 설정 변경은 solidbob02만.
