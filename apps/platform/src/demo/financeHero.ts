/**
 * 랜딩 데모에 쓰는 문장·카드.
 * 값을 지어내지 않는다. `apps/dashboard/src/mock/scenarios/` 에서 옮겼다.
 * 패키지가 갈라져 있어 import 하지 않고 필요한 필드만 복사한다.
 */

export interface DemoCard {
  title: string;
  summary: string;
  source: string;
}

export type HeroDomainId = "finance" | "shopping" | "dasan" | "health";

export interface HeroCycle {
  domain: HeroDomainId;
  keyword: string;
  cardTitle: string;
}

export const LINE_LOSS =
  "안녕하세요. 카드를 잃어버려서 분실 신고하려고 전화드렸어요.";

/** finance.ts cardBatches[0] FIN-TERM-2.1 */
export const CARD_LOSS: DemoCard = {
  title: "분실·도난 신고",
  summary:
    "이용자가 카드 분실·도난을 신고하면 회사는 즉시 카드 사용을 정지한다. 신고 접수 시점 이전의 부정사용액은 보상 기준에 따라 처리한다.",
  source: "한별금융 이용약관 제2조 1항",
};

/**
 * 히어로 음성 데모. 키워드·카드 제목만 쓴다.
 * finance.ts cardBatches[1] · shopping.ts · dasan.ts · health.ts
 */
export const HERO_CYCLES: readonly HeroCycle[] = [
  { domain: "finance", keyword: "보상", cardTitle: "부정사용 보상 기준" },
  { domain: "shopping", keyword: "반품", cardTitle: "반품 배송비 부담 기준" },
  { domain: "dasan", keyword: "환승", cardTitle: "노선·환승 안내 원칙" },
  { domain: "health", keyword: "증상", cardTitle: "증상 문의 응대 원칙" },
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

export const DOMAINS: readonly { id: HeroDomainId; label: string }[] = [
  { id: "finance", label: "금융보험" },
  { id: "dasan", label: "다산콜센터" },
  { id: "shopping", label: "쇼핑" },
  { id: "health", label: "질병관리본부" },
];
