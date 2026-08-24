---
layout: post
title: "W1 — 저장소를 다중 프로젝트 구조로 분리 (jekyll/)"
date: 2026-08-24 18:10:19 +0900
categories: log
week: 1
track: [infra]
status: done
metrics_touched: false
---

## 한 일

- `flutter` 브랜치를 추가했다. 이제 역할 브랜치는 `PM` / `frontend` / `backend` / `flutter` 네 개다.
- 지킬 사이트 전체를 `jekyll/` 하위로 옮겼다 (`git mv` 로 이동해 이력이 rename 으로 남는다).
  - 이동: `_config.yml`, `Gemfile`, `Gemfile.lock`, `index.html`, `toc.md`, `log.md`, `open-items.md`, `progress.md`, `404.html`, `_docs/`, `_posts/`, `_data/`, `assets/`
  - 루트 유지: `CLAUDE.md`, `README.md`, `_project/`, `.gitignore`
- 경로 참조를 전부 갱신했다 — `CLAUDE.md` 3절 구조도·9절 실행 명령, `README.md`, `_project/STATE.md`, `3-guidelines` 저장소 구조, `5-appendix` 서식 경로, `milestones.yml` 의 `doc:` 항목.
- 미결 항목 OI-06(배포 방식) 등록.

## 판단과 근거

- **`_project/` 는 루트에 남겼다.** 지킬이 소비하지 않는 파일이고, 앞으로 Flutter 등 다른 코드가 들어오면 기획서·STATE·결정 기록은 저장소 전체에 걸리는 기록이 된다. 부수 효과로 이제 지킬 루트 밖이라 언더스코어 규칙과 무관하게 사이트에 게시되지 않는다.
- **`CLAUDE.md` 도 루트에 남겼다.** 세션 시작 시 가장 먼저 읽는 파일이고, 규칙의 적용 범위가 지킬 사이트에 한정되지 않는다.
- **`git mv` 를 썼다.** 파일을 지우고 새로 만들면 이력이 끊긴다. rename 으로 기록되어야 `git log --follow` 로 과거를 따라갈 수 있다.
- 버린 선택지: 사이트를 `docs/` 로 옮기기 — GitHub Pages 의 classic 빌드가 `/docs` 를 지원하므로 배포는 쉬워지지만, 저장소 안에 `docs/` 와 `jekyll/_docs/` 가 공존해 헷갈린다.

## 막힌 것

**GitHub Pages 배포 경로가 끊겼다.** Pages 의 "Deploy from a branch" 는 소스로 저장소 루트나 `/docs` 만 지원해서, `jekyll/` 하위는 인식하지 못한다. Actions 워크플로를 추가해야 한다. Pages 가 아직 켜져 있지 않아 실제 장애는 없고, 활성화 전에 정하면 된다. → OI-06

## 다음 세션 첫 작업

**AI Hub 데이터 신청** (사용자 직접 — 휴대폰 본인인증 필요). 신청 즉시 `jekyll/_data/milestones.yml` 의 `w1.aihub` 에 신청일을 기록한다.
