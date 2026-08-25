# STATE — 지금 어디까지 왔는가

> 세션 인수인계용 비공개 메모. 팀이 함께 보는 기록은 `jekyll/progress.markdown`, 미결은 `jekyll/open-items.markdown`.
> 여기에는 그쪽에 적기 애매한 내부 사정만 남긴다.

**최종 갱신**: 2026-08-25 (세션 #7)
**현재**: 1주차 / 8스프린트 (2026-08-20 ~ 2026-10-27)
**전체 상태**: 🟢 저장소 통합 완료. 지식베이스·골든셋·평가 하네스·DDL 초안까지 존재

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
