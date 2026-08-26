import type {
  ClosureEvent,
  ClosureType,
  ClosureVerdict,
  DemoDomain,
  DocumentSource,
  MaskedSpan,
  MaskType,
  RecommendationBatch,
  RecommendationCard,
  Speaker,
  TranscriptEvent,
} from "../../types/contract";
import type { GatewayClient, GatewayListener } from "./types";

type ParsedMessage =
  | { kind: "transcript"; payload: TranscriptEvent }
  | { kind: "recommendation"; payload: RecommendationBatch }
  | { kind: "closure"; payload: ClosureEvent };

export class RealGatewayClient implements GatewayClient {
  readonly mode = "live" as const;
  private socket: WebSocket | null = null;
  private listeners: GatewayListener | null = null;

  constructor(private readonly url: string) {}

  connect(listeners: GatewayListener): void {
    this.disconnect();
    this.listeners = listeners;
    listeners.onStatus({ mode: "live", connected: false });

    try {
      this.socket = new WebSocket(this.url);
    } catch {
      listeners.onError("게이트웨이에 연결하지 못했습니다.");
      return;
    }

    this.socket.addEventListener("open", () => {
      this.listeners?.onStatus({ mode: "live", connected: true });
    });

    this.socket.addEventListener("message", (event: MessageEvent<string>) => {
      this.handleMessage(event.data);
    });

    this.socket.addEventListener("error", () => {
      this.listeners?.onError("게이트웨이 연결에 문제가 생겼습니다.");
    });

    this.socket.addEventListener("close", () => {
      this.listeners?.onStatus({ mode: "live", connected: false });
    });
  }

  disconnect(): void {
    if (this.socket !== null) {
      this.socket.close();
      this.socket = null;
    }
    this.listeners = null;
  }

  private handleMessage(raw: string): void {
    const listeners = this.listeners;
    if (listeners === null) {
      return;
    }

    let parsed: unknown;
    try {
      parsed = JSON.parse(raw) as unknown;
    } catch {
      listeners.onError("게이트웨이 메시지를 읽지 못했습니다.");
      return;
    }

    const message = parseGatewayMessage(parsed);
    if (message === null) {
      listeners.onError("알 수 없는 게이트웨이 메시지입니다.");
      return;
    }

    if (message.kind === "transcript") {
      listeners.onTranscript(message.payload);
      return;
    }
    if (message.kind === "recommendation") {
      listeners.onRecommendation(message.payload);
      return;
    }
    listeners.onClosure(message.payload);
  }
}

export function parseGatewayMessage(value: unknown): ParsedMessage | null {
  const body = unwrapPayload(value);
  if (body === null) {
    return null;
  }

  const tagged = readString(body, "type");
  if (tagged === "transcript" || tagged === "recommendation" || tagged === "closure") {
    const inner = isRecord(body.payload) ? body.payload : body;
    return parseByKind(tagged, inner);
  }

  if (hasKeys(body, ["segment_id", "speaker", "text"])) {
    return parseByKind("transcript", body);
  }
  if (hasKeys(body, ["cards", "trigger_at_ms"])) {
    return parseByKind("recommendation", body);
  }
  if (hasKeys(body, ["verdict", "evidence", "missing"])) {
    return parseByKind("closure", body);
  }
  return null;
}

function parseByKind(
  kind: "transcript" | "recommendation" | "closure",
  body: Record<string, unknown>,
): ParsedMessage | null {
  if (kind === "transcript") {
    const payload = parseTranscript(body);
    return payload === null ? null : { kind, payload };
  }
  if (kind === "recommendation") {
    const payload = parseRecommendation(body);
    return payload === null ? null : { kind, payload };
  }
  const payload = parseClosure(body);
  return payload === null ? null : { kind, payload };
}

function unwrapPayload(value: unknown): Record<string, unknown> | null {
  if (!isRecord(value)) {
    return null;
  }
  return value;
}

function parseTranscript(body: Record<string, unknown>): TranscriptEvent | null {
  const call_id = readString(body, "call_id");
  const segment_id = readString(body, "segment_id");
  const speaker = readSpeaker(body.speaker);
  const text = readString(body, "text");
  const is_final = readBoolean(body, "is_final");
  const utterance_end_ms = readNumber(body, "utterance_end_ms");
  const masked = parseMaskedList(body.masked);
  if (
    call_id === null ||
    segment_id === null ||
    speaker === null ||
    text === null ||
    is_final === null ||
    utterance_end_ms === null ||
    masked === null
  ) {
    return null;
  }
  const event: TranscriptEvent = {
    call_id,
    segment_id,
    speaker,
    text,
    masked,
    is_final,
    utterance_end_ms,
  };
  const domain = readDomain(body.domain);
  if (domain !== undefined) {
    event.domain = domain;
  }
  return event;
}

function parseRecommendation(body: Record<string, unknown>): RecommendationBatch | null {
  const call_id = readString(body, "call_id");
  const trigger_at_ms = readNumber(body, "trigger_at_ms");
  const internal_latency_ms = readNumber(body, "internal_latency_ms");
  const e2e_latency_ms = readNumber(body, "e2e_latency_ms");
  if (
    call_id === null ||
    trigger_at_ms === null ||
    internal_latency_ms === null ||
    e2e_latency_ms === null ||
    !Array.isArray(body.cards)
  ) {
    return null;
  }
  const cards: RecommendationCard[] = [];
  for (const item of body.cards) {
    if (!isRecord(item)) {
      return null;
    }
    const card = parseCard(item);
    if (card === null) {
      return null;
    }
    cards.push(card);
  }
  const batch: RecommendationBatch = {
    call_id,
    trigger_at_ms,
    cards,
    internal_latency_ms,
    e2e_latency_ms,
  };
  const domain = readDomain(body.domain);
  if (domain !== undefined) {
    batch.domain = domain;
  }
  return batch;
}

function parseCard(body: Record<string, unknown>): RecommendationCard | null {
  const title = readString(body, "title");
  const summary = readString(body, "summary");
  const similarity_score = readNumber(body, "similarity_score");
  const source = parseSource(body.source);
  if (title === null || summary === null || similarity_score === null || source === null) {
    return null;
  }
  return { title, summary, source, similarity_score };
}

function parseClosure(body: Record<string, unknown>): ClosureEvent | null {
  const call_id = readString(body, "call_id");
  const closure_type = readClosureType(body.closure_type);
  const reason = readString(body, "reason");
  const verdict = readVerdict(body.verdict);
  const source = parseSource(body.source);
  const missing = parseStringList(body.missing);
  const evidence = parseEvidence(body.evidence);
  if (
    call_id === null ||
    closure_type === null ||
    reason === null ||
    verdict === null ||
    source === null ||
    missing === null ||
    evidence === null
  ) {
    return null;
  }
  const event: ClosureEvent = {
    call_id,
    closure_type,
    reason,
    evidence,
    verdict,
    missing,
    source,
  };
  const domain = readDomain(body.domain);
  if (domain !== undefined) {
    event.domain = domain;
  }
  return event;
}

function parseSource(value: unknown): DocumentSource | null {
  if (!isRecord(value)) {
    return null;
  }
  const doc_id = readString(value, "doc_id");
  const title = readString(value, "title");
  if (doc_id === null || title === null) {
    return null;
  }
  return { doc_id, title };
}

function parseMaskedList(value: unknown): MaskedSpan[] | null {
  if (!Array.isArray(value)) {
    return null;
  }
  const spans: MaskedSpan[] = [];
  for (const item of value) {
    if (!isRecord(item)) {
      return null;
    }
    const type = readMaskType(item.type);
    const span = parseSpan(item.span);
    if (type === null || span === null) {
      return null;
    }
    spans.push({ type, span });
  }
  return spans;
}

function parseSpan(value: unknown): [number, number] | null {
  if (!Array.isArray(value) || value.length !== 2) {
    return null;
  }
  const start = value[0];
  const end = value[1];
  if (typeof start !== "number" || typeof end !== "number") {
    return null;
  }
  return [start, end];
}

function parseStringList(value: unknown): string[] | null {
  if (!Array.isArray(value)) {
    return null;
  }
  const items: string[] = [];
  for (const item of value) {
    if (typeof item !== "string") {
      return null;
    }
    items.push(item);
  }
  return items;
}

function parseEvidence(value: unknown): Record<string, boolean> | null {
  if (!isRecord(value)) {
    return null;
  }
  const evidence: Record<string, boolean> = {};
  for (const [key, flag] of Object.entries(value)) {
    if (typeof flag !== "boolean") {
      return null;
    }
    evidence[key] = flag;
  }
  return evidence;
}

function readSpeaker(value: unknown): Speaker | null {
  if (value === "customer" || value === "agent") {
    return value;
  }
  return null;
}

function readClosureType(value: unknown): ClosureType | null {
  if (
    value === "상품해지" ||
    value === "사고·보상" ||
    value === "반품" ||
    value === "교환"
  ) {
    return value;
  }
  return null;
}

function readVerdict(value: unknown): ClosureVerdict | null {
  if (value === "approved" || value === "blocked") {
    return value;
  }
  return null;
}

function readMaskType(value: unknown): MaskType | null {
  if (
    value === "P1" ||
    value === "P2" ||
    value === "P3" ||
    value === "P4" ||
    value === "P5" ||
    value === "P6" ||
    value === "P7"
  ) {
    return value;
  }
  return null;
}

function readDomain(value: unknown): DemoDomain | undefined {
  if (
    value === "finance" ||
    value === "dasan" ||
    value === "shopping" ||
    value === "health"
  ) {
    return value;
  }
  return undefined;
}

function readString(body: Record<string, unknown>, key: string): string | null {
  const value = body[key];
  return typeof value === "string" ? value : null;
}

function readNumber(body: Record<string, unknown>, key: string): number | null {
  const value = body[key];
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function readBoolean(body: Record<string, unknown>, key: string): boolean | null {
  const value = body[key];
  return typeof value === "boolean" ? value : null;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function hasKeys(body: Record<string, unknown>, keys: readonly string[]): boolean {
  return keys.every((key) => key in body);
}
