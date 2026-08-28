import type {
  CallWrapUp,
  ClosureEvent,
  ManualSearchRequest,
  RecommendationBatch,
  TranscriptEvent,
  TranslatedUtterance,
  AgentTtsStatus,
} from "../../types/contract";

export interface GatewayListener {
  onTranscript: (event: TranscriptEvent) => void;
  onRecommendation: (event: RecommendationBatch) => void;
  onClosure: (event: ClosureEvent) => void;
  onStatus: (status: GatewayStatus) => void;
  onError: (message: string) => void;
  /** A-5. §7.3 미정 — mock만 보낸다. 키는 자막 segment_id. */
  onTranslation?: (
    transcriptSegmentId: string,
    event: TranslatedUtterance,
  ) => void;
  onAgentTts?: (transcriptSegmentId: string, event: AgentTtsStatus) => void;
}

export type GatewayMode = "mock" | "live";

export interface GatewayStatus {
  mode: GatewayMode;
  connected: boolean;
}

export interface GatewayClient {
  readonly mode: GatewayMode;
  connect(listeners: GatewayListener): void;
  disconnect(): void;
  /**
   * 상담원이 직접 검색한다(B-6 보완 경로). 자동 추천과 달리 요청·응답이 1:1 이라
   * 리스너가 아니라 Promise 로 돌려준다. 결과가 없으면 cards 가 빈 배열이다 —
   * 없는 것을 채워 보내지 않는다.
   */
  manualSearch(request: ManualSearchRequest): Promise<RecommendationBatch>;
  /** §2.5 D-1~D-3 통화 후 처리. 계약 미정 — manualSearch 와 같은 이유로 Promise 다. */
  wrapUp(callId: string): Promise<CallWrapUp>;
}

export function gatewayUrl(): string {
  return (import.meta.env.VITE_GATEWAY_WS_URL ?? "").trim();
}

export function isLiveGatewayConfigured(): boolean {
  return gatewayUrl().length > 0;
}
