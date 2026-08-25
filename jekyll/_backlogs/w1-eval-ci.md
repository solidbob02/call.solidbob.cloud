---
title: "평가 하네스 CI 연결"
assignee: "정성윤"
role: "infra"
status: "in-progress"
sprint: 1
priority: 10
date: 2026-08-25
---

하네스 설계는 류준이 끝냈다. 운영·유지는 인프라 담당이 이관받는다([7.2절](/docs/07/) 부하 완화).

**완료 조건**: 푸시마다 `pytest`가 돌고, 기준선 미달 시 CI가 실패한다.

## 1단계 — 테스트 자동 실행 (2026-08-26)

`.github/workflows/test.yml` 추가. `main`·`PM`·`backend`·`frontend`·`flutter` 푸시와
`main` 대상 PR 에서 실행된다.

**범위를 좁게 잡은 이유**

- **`pytest` 만 설치한다.** `requirements.txt` 의 torch·transformers 는 테스트가 쓰지 않는다
  (`services/core/tests` 는 표준 라이브러리와 프로젝트 모듈만 import). 전체 설치하면
  매 실행이 몇 분씩 걸리고 실패 지점만 늘어난다
- **기준선 게이트는 넣지 않았다.** 측정값이 없어서 지금 켜면 무조건 실패하거나
  가짜 기준선을 넣게 된다 — 절대 원칙 2번 위반이다.
  **빨간불에 익숙해지는 것이 CI 가 죽는 가장 흔한 경로**라 통과 가능한 것만 넣는다
- 실제 DB·ES·외부 API 가 필요한 테스트는 `pytest.ini` 의 `-m "not integration"` 로 빠진다

## 1단계-b — 사이트 빌드 검사 (2026-08-26)

같은 워크플로에 `jekyll` job 추가. 사이트가 곧 산출물이라 `main` 에 머지되는 순간 배포되는데,
기존에는 배포 워크플로가 **머지 후에야** 빌드해서 깨진 사이트가 들어가도 그때서야 알았다.

- `bundle exec jekyll build` — 리퀴드 오류·front matter 오류를 잡는다
- `scripts/check_site_links.py` — **내부 링크 검사**. 파일 이름이나 소제목을 바꾸면
  링크가 조용히 깨지는데 빌드는 통과하므로 사람이 클릭해 보기 전까지 모른다.
  실제로 이 프로젝트에서 파일 재배치 때 20건이 한 번에 깨진 적이 있다

링크 검사기는 로컬에서도 같은 명령으로 쓸 수 있다.

```bash
cd jekyll && bundle exec jekyll build && cd ..
python3 scripts/check_site_links.py
```

역테스트로 "페이지 없음"·"앵커 없음" 두 종류를 모두 잡고 종료 코드 1을 반환하는 것을 확인했다.

## 2단계 — 기준선 게이트 (2주차 이후)

2주차 잠정 베이스라인(골든셋 50건)이 나온 뒤에 붙인다. 기획서 6.2절 요구사항이다.
기준선은 **여러 번 실행한 값 중 최저치**로 고정한다.
