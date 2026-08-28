---
title: "커스텀 도메인 docs.solidbob.cloud 연결 (배포 사이트 404 수정)"
assignee: "정성윤"
role: "infra"
status: "in-progress"
sprint: 2
priority: 3
date: 2026-08-28
paths:
  - "jekyll/_config.yml"
  - "jekyll/index.markdown"
  - "jekyll/CNAME"
  - ".github/workflows/pages.yml"
depends_on:
  - "w1-pages-deploy"
---

**무엇을** — 배포된 사이트에서 본문 링크(`/docs/09/`·`/toc/` …)가 전부 404 다.
프로젝트 페이지라 사이트가 `/call.solidbob.cloud/` 아래 놓이는데 링크 **405곳이 루트 절대경로**라
한 겹이 어긋난다. 상단 내비만 `relative_url` 을 써서 **내비는 되고 본문은 안 되는** 상태다.
커스텀 도메인을 붙여 사이트를 루트에 올리면 `baseurl` 이 `""` 가 되어 405곳이 그대로 맞는다.

**왜 이 방법인가** — 링크 405곳을 고치는 쪽은 네 브랜치 전부와 충돌하고, 새로 쓰는 링크마다
같은 실수가 재발한다. 클라우드플레어 경유는 네임서버를 통째로 옮겨야 하고 프록시가 GitHub 인증서
발급을 막아, 이 목적에는 얻는 게 없다. → `_project/decisions/102`

**한 것 (2026-08-28)**
- `jekyll/_config.yml` — `url` 설정 (baseurl 은 `""` 유지). ⚠ 오전엔 `call`, 오후에 **`https://docs.solidbob.cloud`** 로 확정(`decisions/104`)
- `jekyll/CNAME` 신규(`docs.solidbob.cloud`) — ⚠ Actions 배포는 이 파일을 읽지 않는다(표식·이관용)
- `jekyll/index.markdown` — 표지 「데모 사이트」를 「문서 사이트 `docs.solidbob.cloud`」 + 「데모 사이트 `solidbob.cloud`」 두 줄로
- `.github/workflows/pages.yml` — `--baseurl` 이 왜 자동으로 비워지는지 주석

**남은 것 — 사람이 해야 한다 (정성윤)**

⚠ 이름이 `call` → **`docs`** 로 바뀌었다(`_project/decisions/104` — `call` 은 프론트가 쓴다).
DNS 는 **클라우드플레어**다(`decisions/103`). 네임서버 전환은 2026-08-28 완료됐다.

1. 클라우드플레어 `DNS → Records → Add record`
   `CNAME` / `docs` / `solidbob02.github.io` / **DNS only(회색 구름)** / TTL Auto
2. GitHub Settings → Pages → Custom domain 에 `docs.solidbob.cloud` → Save
3. DNS check 통과 후 **Enforce HTTPS** (인증서 발급까지 몇 분~한 시간)

**완료 조건** — `https://docs.solidbob.cloud/docs/09/` 가 200 이고 HTTPS 가 강제된다.
표지의 「문서 사이트」 주소와 실제 주소가 같아진다.
