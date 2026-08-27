---
title: "브랜치 이름을 담당 디렉터리에 맞춘다 (backend→ai)"
assignee: "류준"
role: "ai"
status: "done"
sprint: 2
priority: 8
date: 2026-08-26
paths:
  - ".github/workflows/test.yml"
  - "_project/decisions/015-*"
---

## 무엇을

브랜치 `backend`(류준) → **`ai`**, `ai`(장민석) → **`server`** 로 개명한다.
브랜치 수는 넷 그대로다 — `PM` / `ai` / `server` / `frontend`.

## 왜

`_project/decisions/012` 로 담당을 디렉터리로 나눈 뒤 **브랜치 이름이 다른 사람을 가리키는**
상태가 남았다 — 장민석의 `ai` 브랜치에서 고치는 것이 `server/` 였다. 진행 기록·PR·티켓에서
`ai` 가 누구인지 매번 되짚어야 했다.

012 는 "브랜치명을 바꾸면 main 룰셋의 필수 통과 검사 이름까지 고쳐야 한다"며 미뤘는데,
**그게 사실이 아니었다.** 필수 통과 검사는 `test.yml` 의 **job 이름**(`server`·`ai`·`jekyll`)
이지 브랜치 이름이 아니다. 브랜치 이름이 걸린 곳은 push 트리거 목록 한 줄뿐이었다.

## 완료 조건

- [x] 삭제 전 `origin/backend`·구 `origin/ai` 가 `origin/main` 의 조상인지 확인 (미머지 0건)
- [x] `git branch -m backend ai` → `git push -u origin ai` → `git push origin --delete backend`
- [x] `test.yml` 트리거 `[main, PM, backend, ai, frontend]` → `[main, PM, ai, server, frontend]`
- [x] 룰셋·`branch-protection.json` 은 손대지 않음을 확인 (job 이름 기준)
- [x] `CLAUDE.md` §1·§7 · `.claude/rules/rfp-harness.md` §2 · [7절](/docs/07/) 갱신
- [x] 결정 기록 `_project/decisions/015`

## 남은 주의

**`ai` 라는 이름이 사람을 갈아탔다.** 2026-08-26 이전 기록의 `ai` 브랜치는 장민석,
그날 이후는 류준이다. 옛 기록은 그 시점의 사실이라 고치지 않는다(절대 원칙 8).
