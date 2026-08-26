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

export interface RecommendationCard {
  title: string;
  summary: string;
  source: DocumentSource;
  similarity_score: number;
}

export interface RecommendationBatch {
  call_id: string;
  trigger_at_ms: number;
  cards: RecommendationCard[];
  internal_latency_ms: number;
  e2e_latency_ms: number;
  domain?: DemoDomain;
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
