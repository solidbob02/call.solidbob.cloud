# call.solidbob.cloud

**실시간 상담원 어시스트 RAG** — 통화를 실시간으로 들으면서, 고객이 방금 물은 내용에 필요한
사내 문서를 상담원 화면에 자동으로 띄워주는 시스템. 8주 프로젝트의 설계·실험·측정 기록.

사이트: https://call.solidbob.cloud

## 이 저장소의 구조

| 경로 | 내용 |
|---|---|
| `CLAUDE.md` | 프로젝트 헌법 + 기록 규칙. 작업 시작 전 필독 |
| `jekyll/` | **지킬 사이트 루트.** 지킬 명령은 전부 이 안에서 실행 |
| `jekyll/index.html` · `jekyll/toc.md` | 제안서 표지 · 목차 |
| `jekyll/_docs/1~5-*.md` | 제안서 본문 5개 절. `architecture` 등은 세부 문서 |
| `jekyll/_posts/` | 개발 로그 (과거, 수정하지 않음) |
| `jekyll/_data/` | `milestones.yml` 진행률 · `metrics.yml` 수치 단일 출처 · `open_items.yml` 미결 항목 |
| `_project/` | 비공개 — 기획서 원본, `STATE.md`, 결정 기록. 사이트에 게시되지 않음 |

## 로컬 미리보기

```bash
cd jekyll                                              # 저장소 루트가 아니라 jekyll/ 안에서
bundle exec jekyll serve --host 0.0.0.0 --port 4001
bundle exec jekyll build                               # 기록 커밋 전 검증
```

Ruby 3.3.12 (rbenv) / Jekyll 4.4.1.
