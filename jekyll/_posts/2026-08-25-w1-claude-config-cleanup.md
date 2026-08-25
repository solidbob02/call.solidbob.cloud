---
layout: post
title: "W1 — 외부에서 들여온 .claude 설정 정리"
date: 2026-08-25 10:53:30 +0900
categories: log
week: 1
track: [infra]
status: done
metrics_touched: false
---

## 한 일

다른 저장소에서 통째로 가져온 `.claude/` 14개 파일을 검증하고 3개만 남겼다.

**삭제 (11개)**

| 대상 | 사유 |
|---|---|
| `rules/typescript.md` (249줄) | 대상이 `**/*.ts` 인데 이 저장소에 `.ts` 파일 0개. 내용도 존재하지 않는 `nextjs/tsconfig.json`, `components/GeminiHeroChat.tsx` 등을 근거로 씀 |
| `rules/api-standards.md`, `rules/testing.md`, `rules/security/pci.md` | 셋 다 0바이트. PCI는 카드결제 규격이라 무관 |
| `projects/-home-messi-projects-watson-projects/memory/` (5개) | 남의 프로젝트 메모리. 경로가 달라 이 세션에서 로드되지 않으며, 타 저장소의 도메인·세션 ID가 포함돼 공개 저장소에 올릴 수 없다 |
| `agents/data-analyzer.md` | 본문 없음(frontmatter 예시만). 존재하지 않는 스킬 참조 |
| `skills/deploy/SKILL.md` | 본문 없음. `disable-model-invocation: true` + `user-invocable: false` 라 아무도 호출할 수 없음 |
| `skills/code-review/SKILL.md` | `code-reviewer` 에이전트 및 내장 `/code-review` 와 삼중 중복 |

**수정 (3개, 남긴 것)**

- `scripts/protect-files.sh` — `jq` 의존을 제거하고(미설치) python3 파싱으로 교체. 차단 대상에 `*service-account*.json`, `*.pem`, `id_rsa` 추가. 경로 전체가 아니라 파일명으로 판정해 오탐을 줄임
- `settings.json` — 동작하지 않던 `notify-send` 알림 훅 제거(이 환경에 미설치). 대신 위 스크립트를 `PreToolUse`(Write/Edit) 훅으로 연결해 실제로 동작하게 함
- `agents/code-reviewer.md` — 이 프로젝트 맥락으로 교체. 절대 원칙 기반 검토 항목(미측정 수치, LLM 채점 금지, 재현율 우선, 민감정보 마스킹, 약관 원문, 레이턴시 예산) 추가

## 판단과 근거

- **"동작하는가"를 먼저 확인했다.** 훅이 부르는 `notify-send` 와 `jq` 가 이 머신에 없고, `protect-files.sh` 는 `settings.json` 어디에서도 호출되지 않았다. 즉 보안 훅이 있는 것처럼 보였지만 실제로는 아무것도 막고 있지 않았다.
- **남의 메모리는 내용이 맞아도 위치가 틀렸다.** 자동 메모리는 `~/.claude/projects/<경로슬러그>/memory/` 에서 읽는다. 저장소 안의 남의 경로 슬러그 디렉터리는 영원히 로드되지 않는다.
- **교훈만 살렸다.** 지운 메모리 중 "붙여넣은 템플릿은 목차로만 쓰고 값은 저장소에서 검증한다"는 원칙은 정확히 이번 상황을 설명한다. 파일은 지우되 원칙은 리뷰 기준으로 적용했다.
- 삭제 전 스크래치패드에 원본 전체를 백업했다.
- 버린 선택지: `.claude/` 를 통째로 gitignore — 팀이 공유해야 할 리뷰 기준과 보안 훅까지 사라진다.

## 막힌 것

없음. 훅은 샘플 입력 5건으로 검증했다 — `.env`, `*.key`, `*service-account*.json` 차단(exit 2), `jekyll/_config.yml` 과 포스트는 통과(exit 0).

## 다음 세션 첫 작업

**AI Hub 데이터 신청** (사용자 직접 — 휴대폰 본인인증 필요). 신청 즉시 `jekyll/_data/milestones.yml` 의 `w1.aihub` 에 신청일을 기록한다.
