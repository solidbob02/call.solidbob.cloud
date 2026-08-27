/**
 * 7.3절 인터페이스 계약 v2.
 * 정본: jekyll/docs/07-역할분담.markdown
 * domain 은 v3 보류 — optional 만 둔다.
 */

export type Speaker = "customer" | "agent";

export type MaskType = "P1" | "P2" | "P3" | "P4" | "P5" | "P6" | "P7";

/** 문자(코드포인트) 오프셋. span 은 [start, end) 반열린 구간. */
export interface MaskedSpan {
  type: MaskType;
  span: [number, number];
}

export type DemoDomain = "finance" | "dasan" | "shopping" | "health";

export const DEMO_DOMAINS: readonly DemoDomain[] = [
  "finance",
  "dasan",
  "shopping",
  "health",
];

export const DEMO_DOMAIN_LABELS: Record<DemoDomain, string> = {
  finance: "금융보험",
  dasan: "다산콜센터",
  shopping: "쇼핑",
  health: "질병관리본부",
};

/** §2.7 처리 유형. 다산콜센터·질병관리본부는 F-2 미적용이라 이 값이 오지 않는다. */
export type ClosureType = "상품해지" | "사고·보상" | "반품" | "교환";

export interface TranscriptEvent {
  call_id: string;
  segment_id: string;
  speaker: Speaker;
  text: string;
  masked: MaskedSpan[];
  is_final: boolean;
  utterance_end_ms: number;
  domain?: DemoDomain;
}

export interface DocumentSource {
  doc_id: string;
  title: string;
}

/** 자동 트리거(B-1)로 뜬 카드인지, 상담원이 직접 찾은 카드인지. */
export type CardSourceType = "auto" | "manual";

export interface RecommendationCard {
  title: string;
  summary: string;
  source: DocumentSource;
  similarity_score: number;
  /**
   * 7.3절 계약에는 아직 없다 — 수동 검색(B-6 보완 경로)을 화면에서 구분하려고
   * 프론트가 먼저 정의했다. 서버가 안 보내면 "auto" 로 본다.
   */
  source_type?: CardSourceType;
}

/**
 * 수동 검색 요청 — §2.3 B-6 으로 "관련 문서 없음"이 떴을 때 상담원이 직접 찾는 경로.
 * 서버 메시지 형식이 정해지면 7.3절로 올린다.
 */
export interface ManualSearchRequest {
  call_id: string;
  query: string;
}

export interface RecommendationBatch {
  call_id: string;
  trigger_at_ms: number;
  cards: RecommendationCard[];
  internal_latency_ms: number;
  e2e_latency_ms: number;
  domain?: DemoDomain;
}

/**
 * §2.5 D. 통화 후 처리 결과. 7.3절 계약에 아직 없다 — 프론트가 먼저 정의했다.
 * D-4(지식베이스 공백)는 이 통화에서 화면이 직접 관찰한 것이라 서버가 주지 않는다.
 */
export interface CallWrapUp {
  call_id: string;
  /** D-1 상담 요약. 한 줄씩. */
  summary: string[];
  /** D-2 문의 유형. */
  category: string;
  /** D-3 후속조치 항목. */
  follow_ups: string[];
}

export type ClosureVerdict = "approved" | "blocked";

export interface ClosureEvent {
  call_id: string;
  closure_type: ClosureType;
  reason: string;
  evidence: Record<string, boolean>;
  verdict: ClosureVerdict;
  missing: string[];
  source: DocumentSource;
  domain?: DemoDomain;
}

export function hasCardSource(card: RecommendationCard): boolean {
  return card.source.doc_id.length > 0 && card.source.title.length > 0;
}

export function cardSourceType(card: RecommendationCard): CardSourceType {
  return card.source_type === "manual" ? "manual" : "auto";
}
