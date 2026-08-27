---
title: "개발 로그를 작성자별 파일로 분리 (충돌 제거)"
assignee: "류준"
role: "ai"
status: "done"
sprint: 2
priority: 9
date: 2026-08-27
paths:
  - "jekyll/_logs/*"
  - "jekyll/progress.markdown"
  - "scripts/check_session_end.py"
  - "scripts/check_progress_log.py"
---

## 무엇을

`jekyll/progress.markdown` 한 파일에 모여 있던 개발 로그를 **항목 1건 = 파일 1개**
(`jekyll/_logs/`)로 가르고, `/progress/` 를 [칸반](/kanban/)과 같은 **작성자별 사이드바**로 바꾼다.

## 왜

**브랜치를 합칠 때마다 충돌했다.** 2026-08-25~26 이틀간 이 파일 커밋 37건 중 16건(43%)이
충돌 처리였고, 작성자는 4명이었다.

원인은 번호(`(44)`, `(45)`)가 아니라 **"같은 파일의 같은 위치"** 다. 빈 저장소에서 확인했다:

| 방식 | 결과 |
|---|---|
| 위에 삽입, 번호도 내용도 다름 | ❌ CONFLICT |
| 아래로 append | ❌ CONFLICT |
| 파일 분리 | ✅ 자동 병합 |

`CLAUDE.md` §4 가 칸반에 대해 이미 내린 진단("하나의 표를 같이 고치면 충돌")을
진행 기록에도 적용한 것이다. 같은 기간 `_backlogs/` 충돌은 0건이었다.

## 완료 조건

- [x] `_logs/` 컬렉션 추가 (`_config.yml`, `output: false`)
- [x] 옛 항목 66건 이관 — 본문 무수정, 불릿 193개 일치 확인
- [x] 작성자 배정 — `git log -S --reverse` 로 최초 커밋자 확인 (2건은 본문 근거로 지정)
- [x] `/progress/` 사이드바 렌더링 + 해시 딥링크(`#ryujun`)
- [x] 정렬을 파일 경로 기준으로 (Liquid `sort` 가 안정 정렬이 아님)
- [x] `check_session_end.py`(Stop 훅) · `check_progress_log.py`(CI) 경로 이전
- [x] `CLAUDE.md` §0·§0.5·§3·§4 · `session-log` 스킬 갱신
- [x] 결정 기록 `_project/decisions/016`
- [x] 지킬 빌드 + 내부 링크 검사 통과

## 남은 주의

이관 작성자는 git 이력에서 **찾은** 것이지 원래 기록에 있던 필드가 아니다.
틀린 것이 있으면 해당 로그 파일의 `author`/`person` 두 줄만 고치면 된다.
