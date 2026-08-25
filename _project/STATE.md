# STATE — 지금 어디까지 왔는가

> 이 파일이 프로젝트의 현재 상태다. 매 세션 종료 시 갱신한다.
> 다음 세션의 Claude 는 사람의 기억이 아니라 이 파일을 믿는다.

**최종 갱신**: 2026-08-25 (세션 #5)
**현재 주차**: 1주차 (기반 + 평가셋) — D+0 / 8주 (2026-08-24 ~ 2026-10-18)
**전체 상태**: 🟡 착수. 기획서 rev.4(3인) 반영 완료. 팀·도메인·LLM 확정, V1~V4 전제 미확인

---

## 지금 진행 중

없음. 사이트를 개발 제안서 형식(표지 → 목차 → 5개 절)으로 재구성하고 기록 체계를 붙이는 데까지 완료.
실제 개발(코드)은 아직 한 줄도 시작하지 않았다.

---

## 기준 문서

`_project/plan.md` = 기획서 **rev.4 (3인 팀)**. 그 위에 `rev4-보완지시서.md` 가 얹힌다 (충돌 시 보완지시서 우선).
채택 근거: `decisions/001-기획서-rev4-채택.md`. 팀: 정성윤(인프라) / 류준(백엔드·AI) / 장민석(앱·프론트).

## 다음 작업 (우선순위 순 — 위에서부터 집는다)

1. **AI Hub 데이터 신청** ⚠ 최우선·사용자 직접 수행
   회원가입 → 휴대폰 본인인증 → 「상담 음성」「고객 응대 음성」 신청.
   승인에 시간이 걸리고, 늦어지면 5주차 핵심 실험이 통째로 밀린다.
   → 신청일을 `jekyll/_data/milestones.yml` 의 `w1.aihub.note` 에 기록할 것.

2. **V1·V2 전제 확인** — AI Hub 데이터 채널 구성(2채널/모노), GPU 가용 여부.
   V2 결과에 따라 생성 폴백 모드 전환이 결정된다. V3·V4도 1주차 안에.

3. **문서 수집 + 청킹 + ID 부여 → 골든셋 10건 시범 작성**
   문서 ID 가 있어야 정답 라벨을 붙일 수 있다. 여기서 막히면 지식베이스 구성을 바꿔야 한다.
   골든셋 스펙에 **발화 종료 시각**과 **개인정보 패턴 삽입 여부**를 반드시 포함한다.
   → 결과를 `jekyll/_docs/golden-set.md` 에 반영.

4. **인터페이스 스키마 3종 확정**(전사·카드·종결) — `jekyll/_docs/interface-contract.md` 를 `draft` → `agreed` 로.
   병렬 작업의 전제 조건이므로 1주차 안에 끝낸다.

5. **평가 하네스 골격 + CI 연결** — 골든셋 로드 → 검색 호출 → Recall@5·MRR 계산 → 기준선 미달 시 exit 1.

---

## 블로커

없음.

---

## 미결 질문

공개 항목은 `jekyll/_data/open_items.yml` 이 정본이다 (사이트 `/open-items/`). 현재 OI-01 ~ OI-05 가 열려 있다.
그중 **OI-01 인원 구성**과 **OI-02 지식베이스 도메인**은 1주차 안에 답이 나와야 8주 일정이 유지된다.

내부 메모:
- 표지의 개발팀 칸이 "미정"으로 나가 있다. 인원이 확정되면 `jekyll/index.html` 의 `cover__meta` 를 채운다.
- 표지 제목의 수치는 목표치다. 실측이 나오면 표기를 "목표"에서 "달성"으로 바꿀지 결정해야 한다 —
  단, 실측 없이 달성 표기를 하는 일은 절대 없어야 한다 (CLAUDE.md 절대 원칙 2).

---

## 환경 상태

| 항목 | 상태 |
|---|---|
| Ruby | 3.3.12 (rbenv, `~/.rbenv/versions/3.3.12`) |
| Jekyll | 4.4.1 + minima 2.5.2, jekyll-feed |
| 미리보기 | `cd jekyll && bundle exec jekyll serve --host 0.0.0.0 --port 4001` (4000 은 다른 사이트가 점유) |
| 원격 | github.com/solidbob02/call.solidbob.cloud (PUBLIC). main + PM/frontend/backend 푸시 완료 |
| 브랜치 | main / PM / frontend / backend / flutter — 전부 원격에 있고 ec598eb 로 동일. 사용자는 PM 담당 |
| 인증 | gh CLI = SeongYuna (협업자, push 권한 있음). 저장소 설정 변경은 solidbob02 만 가능 |
| .claude | 외부 저장소에서 들여온 14개 중 11개 삭제, 3개(code-reviewer 에이전트 · protect-files 훅 · settings) 유지 |
| 저장소 구조 | 지킬 사이트는 `jekyll/` 하위. 루트에는 CLAUDE.md, README.md, _project/ |
| 배포 | GitHub Pages 미활성. jekyll/ 하위라 classic 빌드 불가 → Actions 필요 (OI-06) |
| apt 빌드 의존성 | 미설치 (gcc 없음). 현재 gem 은 전부 미리 컴파일된 바이너리라 문제 없음. 소스 빌드가 필요한 gem 추가 시 설치 필요 |
| 미착수 | Python/FastAPI, Node.js, Elasticsearch, MySQL, Docker — 아직 아무것도 세팅 안 됨 |
