# 011. 브랜치는 넷을 유지하고, main 을 보호한다

> 작성 당시 번호는 `009` 였으나 `009-생성모델-EXAONE-Ollama-확정.md` 와 겹쳐 `011` 로 옮겼다.
> `decisions/009` 로만 참조한 곳이 여럿이라 어느 문서인지 모호해지는 문제가 있었다.

- **날짜**: 2026-08-26
- **상태**: 채택 · **적용 완료** (2026-08-26, 룰셋 `main` id 21538648)
- **관련**: `CLAUDE.md` §4(티켓 선점)·§7(브랜치), `.github/workflows/test.yml`·`pages.yml`

## 맥락

2026-08-26 하루에 브랜치 간 충돌이 반복됐다.

| PR | 충돌 파일 | 원인 |
|---|---|---|
| #15 | `services/core/eval/harness.py` 외 6건 | `ai` 가 `fastapi/` 로 이사하는 동안 `backend` 가 옛 경로에서 B-0 을 추가 |
| #22 | `w2-domain-routing.md` · `w2-db-schema-domain.md` · `progress.markdown` | 같은 티켓의 `status` 를 `main`(정성윤 `0bd49eb`)은 `done`, `ai`(장민석)는 `in-progress` 로 동시에 변경 |

"브랜치가 너무 많아서 그런 것 아니냐"는 물음이 나왔다. 확인해 보니 **main 에 아무 보호 설정이
없다는 사실**도 함께 드러났다(`branches/main/protection` → 404). `pages.yml` 이 main push 에
즉시 배포하므로, 누구든 실수로 main 에 직접 push 하면 **테스트 결과와 무관하게 이미 배포된 뒤**가 된다.

## 선택지

| 안 | 장점 | 단점 |
|---|---|---|
| A. `ai` 를 `backend` 에 합쳐 공용 브랜치로 | 브랜치 수가 줄어 관리가 단순 | 충돌의 실제 원인을 건드리지 못한다. 한 브랜치 안에서 두 사람이 같은 파일을 고치는 상황은 그대로다 |
| **B. 넷을 유지 + main 보호** | 원인(동시 편집)에 직접 대응. 각자 브랜치가 남아 작업 경계가 보인다 | 브랜치 수는 그대로. 티켓 선점 규칙을 사람이 지켜야 한다 |
| C. 아무것도 안 함 | — | 충돌 반복. main 직접 push 사고에 무방비 |

## 결정

**B.** 브랜치는 `PM` / `backend` / `ai` / `frontend` 넷을 유지하고, **`ai` 와 `backend` 를 합치지 않는다.**
대신 main 에 보호 설정을 건다 — PR 필수, 승인 1건, CI(`backend`·`jekyll` job) 통과 필수, force push 금지.

## 근거

**브랜치를 합쳐도 충돌은 줄지 않는다.** #22 의 충돌 3건은 브랜치 수 때문이 아니라
**같은 티켓 파일을 두 사람이 같은 시각에 다른 값으로 고쳤기** 때문이다. 합친 브랜치 안에서도
똑같이 일어난다. 실제 해결책은 `CLAUDE.md` §4 의 티켓 선점 규칙("먼저 손댄 쪽이 산다")을
지키는 것이고, 브랜치 정리는 필요조건도 아니다.

한편 **보호 설정 부재는 브랜치 논의와 무관하게 그 자체로 위험**하다. main = 배포이므로,
막지 않으면 CI 를 아무리 잘 만들어도 "배포된 뒤에 빨간불을 보는" 구조다.

> 이 결정을 촉발한 위반은 이 저장소 안에 남아 있다. `0bd49eb` 은 §4 의 선점 규칙
> ("나중에 시작한 쪽이 물러난다")을 **CLAUDE.md 에 추가하면서 동시에 그 규칙을 어긴** 커밋이다.
> 규칙을 적어두는 것과 지키는 것이 다르다는 근거로 남긴다.

## 적용 결과 (2026-08-26)

`SeongYuna` 계정은 push 권한만 있고 `admin` 이 없어(`permissions.admin=false`) API 로 켤 수 없었다.
저장소 소유자 `solidbob02` 계정이 **클래식 브랜치 보호 대신 룰셋(Ruleset)** 으로 적용했다.

```
룰셋 main (id 21538648)   enforcement: active   대상: ~DEFAULT_BRANCH
  deletion · non_fast_forward
  pull_request              승인 1건, stale 승인 자동 해제
  required_status_checks    [backend, jekyll]  strict=true
  우회 허용 대상             없음
```

**중간에 한 번 걸렸던 것** — 룰셋은 생성 직후 기본이 `enforcement: disabled` 이고 대상 브랜치도
비어 있다(`ref_name.include: []`). 규칙을 다 채워도 이 둘을 손대지 않으면 **만들어졌는데 아무것도
막지 않는 상태**가 된다. `branches/main` 의 `protected` 가 `false` 로 남아 있는 것으로 알아냈다.

**권한 없이 확인하는 법** — `branches/main/protection` 은 admin 이 없으면 404 라 확인에 쓸 수 없다.
대신 이 셋은 push 권한만으로 읽힌다.

```bash
gh api repos/solidbob02/call.solidbob.cloud/branches/main --jq .protected
gh api repos/solidbob02/call.solidbob.cloud/rulesets
gh api repos/solidbob02/call.solidbob.cloud/rules/branches/main   # 지금 적용 중인 규칙
```

`.github/branch-protection.json` 은 클래식 보호용 설정값이다. 룰셋으로 적용했으므로 지금은 쓰이지
않지만, 룰셋을 걷어내고 클래식으로 돌아갈 때를 위해 남겨 둔다.

## 되돌리는 법

- 브랜치 합치기로 선회하려면: `ai` 를 `backend` 에 머지하고 `CLAUDE.md` §7 브랜치 목록과
  `test.yml` 트리거에서 `ai` 를 뺀다. 원격 `ai` 는 지우지 말고 남긴다(기록).
- 보호 설정 해제: `gh api -X DELETE repos/solidbob02/call.solidbob.cloud/branches/main/protection`
