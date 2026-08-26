/**
 * 질병관리본부 mock. 안내형 업무라 F-2 종결 이벤트 없음.
 * 근거: knowledge-base/health/policy/POLICY.md
 */
import type { MockScenario } from "./types";
import { cardBatch, utterance } from "./helpers";

const CALL_ID = "c_health_001";
const DOMAIN = "health" as const;

export const healthScenario: MockScenario = {
  domain: DOMAIN,
  transcripts: [
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_h001",
      "customer",
      "기침이 며칠째 안 나아요. 무슨 병일까요?",
      4200,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_h002",
      "agent",
      "한별헬스콜입니다. 증상만으로 특정 질병이라고 단정하지 않습니다. 공식 자료 기준의 일반 정보만 안내합니다.",
      9100,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_h003",
      "customer",
      "그래도 집에서 그냥 있어도 되나요?",
      12800,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_h004",
      "agent",
      "지속되거나 악화되는 증상은 의료기관 방문을 권합니다. 진단·처방은 의료기관의 역할입니다.",
      17600,
      null,
    ),
  ],
  cardBatches: [
    cardBatch(CALL_ID, DOMAIN, 9600, [
      {
        title: "증상 문의 응대 원칙",
        summary:
          "증상 문의는 공식 자료를 근거로 일반 정보를 제공하되, 특정 질병으로 단정하지 않는다. 지속·악화되는 증상은 의료기관 방문을 권장한다.",
        source: { doc_id: "HLT-TERM-2.1", title: "한별헬스콜 이용안내 2.1" },
        similarity_score: 0,
      },
    ]),
  ],
  closures: [],
};
