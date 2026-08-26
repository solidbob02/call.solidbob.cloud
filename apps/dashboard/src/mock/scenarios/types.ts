import type {
  ClosureEvent,
  DemoDomain,
  RecommendationBatch,
  TranscriptEvent,
} from "../../types/contract";

export interface ScheduledClosure {
  /** 이 발화가 나간 뒤에 종결 이벤트를 재생한다. */
  afterSegmentId: string;
  event: ClosureEvent;
}

export interface MockScenario {
  domain: DemoDomain;
  transcripts: TranscriptEvent[];
  cardBatches: RecommendationBatch[];
  closures: ScheduledClosure[];
}
