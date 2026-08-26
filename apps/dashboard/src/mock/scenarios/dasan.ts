/**
 * 다산콜센터 mock. 안내형 업무라 F-2 종결 이벤트 없음.
 * 근거: knowledge-base/dasan/policy/POLICY.md
 */
import type { MockScenario } from "./types";
import { cardBatch, utterance } from "./helpers";

const CALL_ID = "c_dasan_001";
const DOMAIN = "dasan" as const;

export const dasanScenario: MockScenario = {
  domain: DOMAIN,
  transcripts: [
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_d001",
      "customer",
      "2호선에서 버스로 갈아탈 때 환승 할인이 되나요?",
      4200,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_d002",
      "agent",
      "한별시 통합민원콜센터입니다. 환승 할인 기준은 교통공사·운수업체 공개 자료를 근거로 안내합니다. 실시간 배차는 변동될 수 있습니다.",
      9100,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_d003",
      "customer",
      "지금 오는 버스가 몇 분 남았는지도 알 수 있어요?",
      12800,
      null,
    ),
    utterance(
      CALL_ID,
      DOMAIN,
      "seg_d004",
      "agent",
      "실시간 배차 정보는 변동될 수 있어 확정 시각을 안내하지 않습니다. 노선과 배차 간격은 공개 자료를 기준으로 말씀드립니다.",
      17600,
      null,
    ),
  ],
  cardBatches: [
    cardBatch(CALL_ID, DOMAIN, 9600, [
      {
        title: "노선·환승 안내 원칙",
        summary:
          "버스·지하철 노선, 배차 간격, 환승 할인 기준은 교통공사·운수업체 공개 자료를 근거로 안내한다. 실시간 배차 정보는 변동될 수 있음을 함께 고지한다.",
        source: {
          doc_id: "DASAN-TERM-2.1",
          title: "한별시 통합민원콜센터 이용안내 2.1",
        },
        similarity_score: 0,
      },
    ]),
  ],
  closures: [],
};
