# CallGuard — call.solidbob.cloud

**StreamRAG : CallGuard** — 통화를 실시간으로 들으면서 고객이 방금 물은 내용에 필요한 사내 문서를
상담원 화면에 자동으로 띄우고, 컴플라이언스 위반 표현과 개인정보를 실시간으로 탐지·마스킹하는 시스템.

- 팀: SOLIDBOB (4인) — 정성윤(AWS·인프라) · 류준·장민석(백엔드·AI, 공동) · 조서희(프론트엔드)
- 개발기간: 2026-08-20 ~ 2026-10-27 (1주 1스프린트, 총 8스프린트)
- **기획서 사이트: <https://solidbob02.github.io/call.solidbob.cloud/>**
  — [개발목차](https://solidbob02.github.io/call.solidbob.cloud/toc/) ·
  [진행 기록](https://solidbob02.github.io/call.solidbob.cloud/progress/) ·
  [칸반 보드](https://solidbob02.github.io/call.solidbob.cloud/kanban/) ·
  [미결 항목](https://solidbob02.github.io/call.solidbob.cloud/open-items/)
  `main` 에 머지되면 `.github/workflows/pages.yml` 이 `jekyll/` 을 빌드해 자동 배포한다.
  데모 도메인 `call.solidbob.cloud` 는 Sprint 7(배포) 전까지 연결되지 않는다.

## 저장소 구조

| 경로 | 내용 |
|---|---|
| `CLAUDE.md` | 프로젝트 규칙. 작업 시작 전 필독 |
| `jekyll/` | **지킬 사이트 루트.** 표지 · 목차 · `docs/NN` 본문 · `sprints/` · 진행 기록 |
| `db/` | `schema.sql`(DDL) · ERD(`ERD.md` · `erd.dot` · `ERD.png`) · 생성 스크립트 |
| `server/` | **요청이 흐르는 길**(Python 3.13). 계약(포트·DTO)·파이프라인 배선·클린 아키텍처. `apps/hub` · `core/config.py` · `.importlinter`. → `server.solidbob.cloud` |
| `ai/` | **품질을 만들고 재는 쪽**(Python 3.13). 청킹·BM25·리랭크·모델 학습·평가 하네스. `apps/retrieval` · `apps/evaluation`. → `ai.solidbob.cloud` |
| `knowledge-base/` | 도메인 4종(`finance`·`dasan`·`shopping`·`health`) × terms / manual / policy |
| `golden-set/` | 골든셋 시나리오 (`v1-10.json` — 도메인 4종 기준) |
| `scripts/`, `data/` | 유틸리티 / 데이터 (원본은 커밋하지 않는다) |
| `_project/` | 비공개 — 기획서 원본·보완지시서, 결정 기록, 세션 인수인계 상태 |
| `.github/workflows/` | `pages.yml`(사이트 배포) · `test.yml`(CI — 하네스 테스트 · 구조 계약 · 사이트 빌드·링크 검사) |

## 로컬 실행

```bash
cd jekyll
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

```bash
cd server && pytest && PYTHONPATH=apps lint-imports --config .importlinter        # 파이프라인·계약 (4종)
cd ai     && pytest && PYTHONPATH=apps:../server/apps lint-imports --config .importlinter  # 검색·평가 (3종)
python3 scripts/check_site_links.py jekyll/_site   # 내부 링크 (빌드 후)
python3 scripts/check_session_end.py               # 진행 기록·티켓 상태·중복 티켓
python db/generate_schema_docs.py                  # ERD 재생성
```
