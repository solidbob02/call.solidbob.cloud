/**
 * 쇼핑 mock. 반품 문의 + SHOP-TERM-4.2 카드.
 * F-2 반품: 근거 2건 중 1건 충족 → blocked.
 */
import type { MockScenario } from "./types";
import { cardBatch, utterance } from "./helpers";

const CALL_ID = "c_shopping_001";
const DOMAIN = "shopping" as const;

export const shoppingScenario: MockScenario = {
  domain: DOMAIN,
  transcripts: [
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_s001",
      "customer",
      "어제 받은 옷이 사이즈가 안 맞아서 반품하려고요.",
      4200,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_s002",
      "agent",
      "한별샵입니다. 단순 변심 반품은 왕복 배송비를 이용자가 부담합니다. 상품 하자·오배송이면 회사가 부담합니다.",
      9100,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_s003",
      "customer",
      "그냥 안 맞아서요. 환불은 얼마가 되고 언제쯤 들어오나요?",
      12800,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_s004",
      "agent",
      "반품 접수 시 환불 예정 금액과 소요 기간을 고지합니다. 상품 상태 확인이 끝나기 전에는 반품을 종결하지 않습니다.",
      17600,
      null,
    ),
  ],
  cardBatches: [
    cardBatch(CALL_ID, DOMAIN, 9600, [
      {
        title: "반품 배송비 부담 기준",
        summary:
          "단순 변심 반품의 왕복 배송비는 이용자가 부담하고, 상품 하자·오배송의 경우 회사가 부담한다. 반품 신청 시 사유에 따른 배송비 부담 주체를 고지해야 한다.",
        source: { doc_id: "SHOP-TERM-4.2", title: "한별샵 이용약관 제4조 2항" },
        similarity_score: 0,
      },
    ]),
  ],
  closures: [
    {
      afterSegmentId: "seg_s004",
      event: {
        call_id: CALL_ID,
        closure_type: "반품",
        reason: "고지 완료",
        evidence: {
          환불금액_기간_고지: true,
          상품상태_확인: false,
        },
        verdict: "blocked",
        missing: ["상품상태_확인"],
        source: {
          doc_id: "SHOP-POLICY-RETURN-1",
          title: "한별샵 내부 처리 규정 반품",
        },
        domain: DOMAIN,
      },
    },
  ],
};
