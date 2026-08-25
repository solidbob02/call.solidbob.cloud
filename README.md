# CallGuard — call.solidbob.cloud

**StreamRAG : CallGuard** — 통화를 실시간으로 들으면서 고객이 방금 물은 내용에 필요한 사내 문서를
상담원 화면에 자동으로 띄우고, 컴플라이언스 위반 표현과 개인정보를 실시간으로 탐지·마스킹하는 시스템.

- 팀: SOLIDBOB — 정성윤(AWS·인프라) · 류준(백엔드·AI) · 장민석(앱·프론트엔드)
- 개발기간: 2026-08-20 ~ 2026-10-27 (1주 1스프린트, 총 8스프린트)
- 사이트: https://call.solidbob.cloud

## 저장소 구조

| 경로 | 내용 |
|---|---|
| `CLAUDE.md` | 프로젝트 규칙. 작업 시작 전 필독 |
| `jekyll/` | **지킬 사이트 루트.** 표지 · 목차 · `docs/NN` 본문 · `sprints/` · 진행 기록 |
| `db/` | `schema.sql`(DDL) · ERD(`ERD.md` · `erd.dot` · `ERD.png`) · 생성 스크립트 |
| `services/` | 서비스 코드. 현재 `core/eval`(평가 하네스) + `core/tests` |
| `knowledge-base/` | 요금제약관 · 응대매뉴얼 · 내부처리규정 (가상 사업자 기준) |
| `golden-set/` | 골든셋 시나리오 |
| `scripts/`, `data/` | 유틸리티 / 데이터 (원본은 커밋하지 않는다) |
| `_project/` | 비공개 — 기획서 원본·보완지시서, 결정 기록, 세션 인수인계 상태 |
| `.github/workflows/` | GitHub Pages 배포 |

## 로컬 실행

```bash
cd jekyll
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

```bash
pytest                      # 평가 하네스 테스트
python db/generate_schema_docs.py   # ERD 재생성
```
