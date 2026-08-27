/**
 * 히어로 데모에 쓰는 문장·카드.
 * 값을 지어내지 않는다. `apps/dashboard/src/mock/scenarios/finance.ts` 에서 옮겼다.
 * 패키지가 갈라져 있어 import 하지 않고 필요한 필드만 복사한다.
 */

export interface DemoCard {
  title: string;
  summary: string;
  source: string;
}

export interface HeroBeat {
  speaker: "customer" | "agent";
  text: string;
  /** 원문에 실제로 들어 있는 단어. 이 단어가 타이핑되는 순간 카드가 뜬다. */
  keyword: string | null;
  card: DemoCard | null;
}

export const LINE_LOSS =
  "안녕하세요. 카드를 잃어버려서 분실 신고하려고 전화드렸어요.";

/** finance.ts transcripts seg_0004 — 「보상」이 원문에 들어 있다. */
const LINE_HOLD =
  "접수했습니다. 지금 시점부터 해당 카드는 사용 정지됩니다. 신고 이전 부정사용액은 보상 기준에 따라 따로 안내드리겠습니다.";

/** finance.ts transcripts seg_0005 — 마스킹 구간은 히어로에서 빼 문장만 쓴다. */
const LINE_FEE =
  "그때 같이 든 적금도 오늘 해지하면 수수료가 얼마나 나오는지도 궁금해요.";

/** finance.ts cardBatches[0] FIN-TERM-2.1 */
export const CARD_LOSS: DemoCard = {
  title: "분실·도난 신고",
  summary:
    "이용자가 카드 분실·도난을 신고하면 회사는 즉시 카드 사용을 정지한다. 신고 접수 시점 이전의 부정사용액은 보상 기준에 따라 처리한다.",
  source: "한별금융 이용약관 제2조 1항",
};

/** finance.ts cardBatches[1] FIN-TERM-2.2 */
export const CARD_COMPENSATION: DemoCard = {
  title: "부정사용 보상 기준",
  summary:
    "신고 접수 이전 부정사용액은 이용자의 고의·중과실이 없는 한 회사가 보상한다. 비밀번호를 타인에게 알려준 경우 등 이용자 귀책이 확인되면 보상이 제한될 수 있다. 조사 전 보상을 확정적으로 안내하지 않는다.",
  source: "한별금융 이용약관 제2조 2항",
};

/** finance.ts cardBatches[2] FIN-TERM-3.2 */
export const CARD_FEE: DemoCard = {
  title: "중도해지수수료 산정",
  summary:
    "약정 기간 중 적금·예치형 상품을 해지할 경우, 약정금리와 중도해지 적용금리의 차액에 비례한 중도해지수수료를 부과한다. 산정 기준과 예상 금액은 해지 신청 시점에 고지해야 하며, 고지 없이 해지를 종결할 수 없다.",
  source: "한별금융 이용약관 제3조 2항",
};

export const HERO_BEATS: readonly HeroBeat[] = [
  {
    speaker: "customer",
    text: LINE_LOSS,
    keyword: null,
    card: null,
  },
  {
    speaker: "agent",
    text: LINE_HOLD,
    keyword: "보상",
    card: CARD_COMPENSATION,
  },
  {
    speaker: "customer",
    text: LINE_FEE,
    keyword: "수수료",
    card: CARD_FEE,
  },
];

/** finance.ts wrapUp.summary */
export const WRAP_UP_LINES: readonly string[] = [
  "고객이 카드 분실을 신고해 접수하고, 해당 카드를 즉시 사용 정지했습니다.",
  "신고 접수 이전의 부정사용액은 보상 기준에 따라 별도 안내하기로 했습니다.",
  "함께 가입한 적금의 중도해지수수료 산정 기준과 약정혜택 소멸을 고지하고 고객 확인 응답을 기록했습니다.",
  "상품 해지 처리를 완료했고, 재발급은 본인확인 절차 후 신청 가능하다고 안내했습니다.",
];

/** finance.ts transcripts seg_0003 — 이미 마스킹된 문장. 원 숫자는 쓰지 않는다. */
export const MASKED_LINE = "카드번호는 **** 입니다";

export const DOMAINS: readonly { id: string; label: string }[] = [
  { id: "finance", label: "금융보험" },
  { id: "dasan", label: "다산콜센터" },
  { id: "shopping", label: "쇼핑" },
  { id: "health", label: "질병관리본부" },
];
