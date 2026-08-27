import type {
  CallWrapUp,
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
  /**
   * §2.5 D-1~D-3. 요약·분류 모델이 아직 없어 손으로 적어둔 것이다.
   * 재생되는 transcripts 와 어긋나면 데모가 거짓말을 하게 되므로 같이 고친다.
   */
  wrapUp: Omit<CallWrapUp, "call_id">;
}
