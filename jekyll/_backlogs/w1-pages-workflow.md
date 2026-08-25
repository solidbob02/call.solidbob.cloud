---
title: "GitHub Pages 배포 워크플로 작성"
assignee: "정성윤"
role: "infra"
status: "done"
sprint: 1
priority: 23
date: 2026-08-25
---

지킬 사이트가 `jekyll/` 하위에 있어 Pages 의 "Deploy from a branch"(저장소 루트 또는 `/docs` 만 지원)를
쓸 수 없다. Actions 로 빌드해 산출물만 게시한다.

`.github/workflows/pages.yml`

- **build**: `ruby/setup-ruby`(jekyll/Gemfile.lock 기준) → `jekyll build` → 산출물 업로드
- **deploy**: `actions/deploy-pages`
- **트리거**: `main` push(머지 포함) + 수동 실행

처음에는 `paths: jekyll/**` 조건을 걸었으나 제거했다. 네 브랜치에서 각자 PR 을 올리는 구조라
`services/` 만 바뀐 머지에서 배포가 조용히 건너뛰어지면 "왜 반영이 안 되지"가 생긴다.
**머지 = 배포**로 규칙을 단순하게 유지한다.

토큰에 `workflow` 스코프가 없어 한 번 푸시가 거부됐다 — `gh auth refresh -h github.com -s workflow` 필요.

활성화(Settings → Pages → Source)는 [별도 티켓](/backlog/w1-pages-deploy/).
