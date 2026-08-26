import type {
  ClosureEvent,
  RecommendationBatch,
  TranscriptEvent,
} from "../../types/contract";

export interface GatewayListener {
  onTranscript: (event: TranscriptEvent) => void;
  onRecommendation: (event: RecommendationBatch) => void;
  onClosure: (event: ClosureEvent) => void;
  onStatus: (status: GatewayStatus) => void;
  onError: (message: string) => void;
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
}

export function gatewayUrl(): string {
  return (import.meta.env.VITE_GATEWAY_WS_URL ?? "").trim();
}

export function isLiveGatewayConfigured(): boolean {
  return gatewayUrl().length > 0;
}
