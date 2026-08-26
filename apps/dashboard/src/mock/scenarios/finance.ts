/**
 * 금융보험 mock. 분실 신고·해지 문의 후, 막힌 종결을 고지 보완으로 풀어 종결한다.
 * 카드 요약·출처는 knowledge-base/finance 조항을 옮긴 것이다.
 * similarity_score 0 은 미측정 — 화면에 강조하지 않는다.
 * 이어붙인 발화의 utterance_end_ms 는 실측이 아니다. 재생은 이 시각을 그대로 쓴다.
 */
import type { MockScenario } from "./types";
import { cardBatch, utterance } from "./helpers";

const CALL_ID = "c_001";
const DOMAIN = "finance" as const;
const CLOSE_SOURCE = {
  doc_id: "FIN-POLICY-CLOSE-1",
  title: "한별금융 내부 처리 규정 상품 해지",
};

export const financeScenario: MockScenario = {
  domain: DOMAIN,
  transcripts: [
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0001",
      "customer",
      "안녕하세요. 카드를 잃어버려서 분실 신고하려고 전화드렸어요.",
      4200,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0002",
      "agent",
      "네 한별금융입니다. 본인 확인을 위해 카드번호 뒷자리 네 자리를 말씀해 주시겠어요?",
      9100,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0003",
      "customer",
      "카드번호는 **** 입니다",
      12800,
      "P2",
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0004",
      "agent",
      "접수했습니다. 지금 시점부터 해당 카드는 사용 정지됩니다. 신고 이전 부정사용액은 보상 기준에 따라 따로 안내드리겠습니다.",
      17600,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0005",
      "customer",
      "그때 같이 든 적금도 오늘 해지하면 수수료가 얼마나 나오는지도 궁금해요. 연락처 뒷자리는 **** 이에요.",
      23100,
      "P4",
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0006",
      "agent",
      "중도해지수수료는 약정금리와 중도해지 적용금리 차액에 비례해 산정됩니다. 예상 금액은 해지 신청 시점에 고지해야 하고, 고지 없이 해지를 종결할 수는 없습니다.",
      28400,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0007",
      "customer",
      "재발급도 바로 되나요? 분실 신고만 하면 새 카드가 오는 거죠?",
      32100,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0008",
      "agent",
      "재발급은 본인확인 절차를 거친 뒤 신청할 수 있습니다. 새 카드는 기존 번호와 다른 카드번호로 발급됩니다.",
      36800,
      null,
    ),
    // 아래 시각은 실측이 아님. 첫 종결(blocked) 이후 약 3~5초 간격으로 이어붙인다.
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0009",
      "agent",
      "잔여 약정에 따라 우대금리 등 부가 혜택도 함께 소멸됩니다. 확인 되셨을까요?",
      40800,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0010",
      "customer",
      "네, 확인했습니다.",
      44800,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0011",
      "agent",
      "말씀하신 내용 확인 응답으로 기록하겠습니다. 해지 처리 도와드리겠습니다.",
      48800,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_0012",
      "agent",
      "해지 처리가 완료되었습니다. 오늘 상담은 여기까지 진행하겠습니다.",
      53800,
      null,
    ),
  ],
  cardBatches: [
    cardBatch(CALL_ID, DOMAIN, 13200, [
      {
        title: "분실·도난 신고",
        summary:
          "이용자가 카드 분실·도난을 신고하면 회사는 즉시 카드 사용을 정지한다. 신고 접수 시점 이전의 부정사용액은 보상 기준에 따라 처리한다.",
        source: { doc_id: "FIN-TERM-2.1", title: "한별금융 이용약관 제2조 1항" },
        similarity_score: 0,
      },
    ]),
    cardBatch(CALL_ID, DOMAIN, 18200, [
      {
        title: "부정사용 보상 기준",
        summary:
          "신고 접수 이전 부정사용액은 이용자의 고의·중과실이 없는 한 회사가 보상한다. 비밀번호를 타인에게 알려준 경우 등 이용자 귀책이 확인되면 보상이 제한될 수 있다. 조사 전 보상을 확정적으로 안내하지 않는다.",
        source: { doc_id: "FIN-TERM-2.2", title: "한별금융 이용약관 제2조 2항" },
        similarity_score: 0,
      },
    ]),
    cardBatch(CALL_ID, DOMAIN, 24100, [
      {
        title: "중도해지수수료 산정",
        summary:
          "약정 기간 중 적금·예치형 상품을 해지할 경우, 약정금리와 중도해지 적용금리의 차액에 비례한 중도해지수수료를 부과한다. 산정 기준과 예상 금액은 해지 신청 시점에 고지해야 하며, 고지 없이 해지를 종결할 수 없다.",
        source: { doc_id: "FIN-TERM-3.2", title: "한별금융 이용약관 제3조 2항" },
        similarity_score: 0,
      },
    ]),
    cardBatch(CALL_ID, DOMAIN, 33200, [
      {
        title: "재발급 절차",
        summary:
          "분실·도난 신고 후 카드 재발급은 본인확인 절차를 거쳐 신청할 수 있다. 재발급 카드는 기존 카드와 별개의 카드번호로 발급된다.",
        source: { doc_id: "FIN-TERM-2.3", title: "한별금융 이용약관 제2조 3항" },
        similarity_score: 0,
      },
    ]),
  ],
  closures: [
    {
      afterSegmentId: "seg_0006",
      event: {
        call_id: CALL_ID,
        closure_type: "상품해지",
        reason: "고지 완료",
        evidence: {
          중도해지수수료_안내: true,
          약정혜택소멸_안내: false,
          고객확인_기록: false,
        },
        verdict: "blocked",
        missing: ["약정혜택소멸_안내", "고객확인_기록"],
        source: CLOSE_SOURCE,
        domain: DOMAIN,
      },
    },
    {
      afterSegmentId: "seg_0009",
      event: {
        call_id: CALL_ID,
        closure_type: "상품해지",
        reason: "고지 완료",
        evidence: {
          중도해지수수료_안내: true,
          약정혜택소멸_안내: true,
          고객확인_기록: false,
        },
        verdict: "blocked",
        missing: ["고객확인_기록"],
        source: CLOSE_SOURCE,
        domain: DOMAIN,
      },
    },
    {
      afterSegmentId: "seg_0011",
      event: {
        call_id: CALL_ID,
        closure_type: "상품해지",
        reason: "고지 완료",
        evidence: {
          중도해지수수료_안내: true,
          약정혜택소멸_안내: true,
          고객확인_기록: true,
        },
        verdict: "approved",
        missing: [],
        source: CLOSE_SOURCE,
        domain: DOMAIN,
      },
    },
  ],
};
