---
paths:
  - "apps/dashboard/**/*.tsx"
  - "apps/dashboard/**/*.ts"
---

# 프론트엔드 규칙 (apps/dashboard)

CallGuard 상담원 대시보드는 React(웹)다 ([팀 분업](/docs/07/): 조서희 담당 — 2026-08-26
팀 개편 이전에는 장민석 담당이었으나, 장민석이 백엔드·AI로 옮기고 조서희가 신규 합류해
프론트엔드를 전담한다. `_project/decisions/005`). 앱(Flutter)은 개발하지 않는다.
`apps/dashboard`는 상담원 화면이다. 자막·경고 패널 + 하단 책갈피 카드.
고객 화면(`apps/customer`)은 `_project/decisions/009` 로 철회했다.

---

## 1. 기본

- TypeScript strict 모드. `any` 남용 금지 — WebSocket으로 받는 이벤트(전사/카드/종결)는
  [7.3절 인터페이스 계약](/docs/07/)의 스키마 타입으로 파싱해서 쓴다.
- 상태관리는 팀 내 합의된 단일 방식으로 통일한다 — 화면마다 다른 방식을 섞지 않는다.
  아직 미정이면 새로 도입하기 전에 팀에 먼저 확인한다.

## 2. 화면 구조 — 상단 2분할 + 하단 책갈피

[2.1절](/docs/02/) 화면 구성(실시간 자막 / 경고, 추천 카드는 하단 책갈피, F-2 게이트는 모달)을
그대로 반영하는 컴포넌트를 기준으로 한다.

```tsx
// Requirement: B-5
interface RecommendationCard {
  title: string;
  summary: string;
  source: { doc: string; clause: string };  // 출처는 항상 존재해야 함
  score: number;                            // 유사도
}
```

- `source` 필드는 항상 표시해야 한다 — 근거 없는 카드를 렌더링하지 않는다 ([B-6](/docs/02/)).
- 추천 카드는 사이드바 목록이 아니라 **하단 책갈피 팝업**이다 (`_project/decisions/009`).
- 화면 어디에도 위험도 점수나 "안전합니다" 류 표현을 하드코딩하지 않는다 ([부록 A-1](/docs/12/)).
- F-2 종결 모달은 근거 필드 체크리스트(예: 중도해지수수료 안내 ☑ / 약정혜택소멸 안내 ☐)를
  그대로 노출하고, 근거 미충족 시 종결 버튼을 비활성화한다. 카피는 「종결 요건 미충족」
  「근거 N건 중 M건」처럼 관찰만 하고, 시스템이 종결을 막았다는 식의 표현은 쓰지 않는다
  ([2.7절 주장 범위](/docs/02/), [2.8절 단방향 경고](/docs/02/)).

## 3. API·WebSocket 통신

- `services/gateway`(WebSocket)와 `fastapi`(REST) 호출은 각각 단일 클라이언트
  모듈(`lib/ws/gatewayClient.ts`, `lib/api/coreClient.ts`)로 모으고, 컴포넌트에서 직접
  소켓/HTTP 호출을 흩뿌리지 않는다.
- 에러 메시지는 한국어로, 사용자에게 서버 내부 정보(스택트레이스 등)를 노출하지 않는다.

## 4. 테스트

- `apps/dashboard/test/`에 컴포넌트 테스트 — 상세 규칙은 `.claude/rules/testing.md` 참고.
