import { create } from "zustand";
import { hasCardSource } from "../types/contract";
import type {
  ClosureEvent,
  DemoDomain,
  MaskType,
  RecommendationCard,
  Speaker,
  TranscriptEvent,
  MaskedSpan,
} from "../types/contract";
import type { GatewayMode } from "../lib/ws";
import { sliceByCodepoints } from "../lib/text/codepoints";

export interface Utterance {
  segment_id: string;
  speaker: Speaker;
  text: string;
  masked: MaskedSpan[];
  is_final: boolean;
  utterance_end_ms: number;
}

export interface MaskingLogEntry {
  id: string;
  segment_id: string;
  type: MaskType;
  span: [number, number];
  excerpt: string;
  utterance_end_ms: number;
}

export interface PanelCard {
  card: RecommendationCard;
  trigger_at_ms: number;
  closure: ClosureEvent | null;
  settled: boolean;
}

export interface CallState {
  mode: GatewayMode;
  connected: boolean;
  error: string | null;
  demoDomain: DemoDomain;
  callId: string | null;
  utterances: Utterance[];
  cards: PanelCard[];
  maskingLog: MaskingLogEntry[];
  closure: ClosureEvent | null;
  applyTranscript: (event: TranscriptEvent) => void;
  applyRecommendation: (
    cards: RecommendationCard[],
    callId: string,
    triggerAtMs: number,
  ) => void;
  applyClosure: (event: ClosureEvent) => void;
  settleClosure: (closureType: ClosureEvent["closure_type"]) => void;
  setStatus: (mode: GatewayMode, connected: boolean) => void;
  setError: (message: string) => void;
  setDemoDomain: (domain: DemoDomain) => void;
  resetCall: () => void;
}

const emptyCall = {
  callId: null as string | null,
  utterances: [] as Utterance[],
  cards: [] as PanelCard[],
  maskingLog: [] as MaskingLogEntry[],
  closure: null as ClosureEvent | null,
};

function attachIndex(cards: PanelCard[], event: ClosureEvent): number {
  const sameType = cards.findIndex(
    (item) => item.closure?.closure_type === event.closure_type,
  );
  if (sameType !== -1) {
    return sameType;
  }
  for (let i = cards.length - 1; i >= 0; i -= 1) {
    if (cards[i].closure === null) {
      return i;
    }
  }
  return cards.length - 1;
}

function withClosure(
  cards: PanelCard[],
  event: ClosureEvent,
): PanelCard[] {
  if (cards.length === 0) {
    return cards;
  }
  const index = attachIndex(cards, event);
  return cards.map((item, i) =>
    i === index ? { ...item, closure: event, settled: false } : item,
  );
}

export function evidenceTally(closure: ClosureEvent): {
  met: number;
  total: number;
} {
  const keys = Object.keys(closure.evidence);
  return {
    total: keys.length,
    met: keys.filter((key) => closure.evidence[key] === true).length,
  };
}

export const useCallStore = create<CallState>((set) => ({
  mode: "mock",
  connected: false,
  error: null,
  demoDomain: "finance",
  ...emptyCall,

  applyTranscript: (event) => {
    set((state) => {
      const next: Utterance = {
        segment_id: event.segment_id,
        speaker: event.speaker,
        text: event.text,
        masked: event.masked,
        is_final: event.is_final,
        utterance_end_ms: event.utterance_end_ms,
      };
      const index = state.utterances.findIndex(
        (item) => item.segment_id === event.segment_id,
      );
      const utterances =
        index === -1
          ? [...state.utterances, next]
          : state.utterances.map((item, i) => (i === index ? next : item));

      const remaining = state.maskingLog.filter(
        (item) => item.segment_id !== event.segment_id,
      );
      const added = event.masked.map((mask, maskIndex) => ({
        id: `${event.segment_id}-${maskIndex}`,
        segment_id: event.segment_id,
        type: mask.type,
        span: mask.span,
        excerpt: sliceByCodepoints(event.text, mask.span[0], mask.span[1]),
        utterance_end_ms: event.utterance_end_ms,
      }));

      return {
        callId: event.call_id,
        utterances,
        maskingLog: [...remaining, ...added],
      };
    });
  },

  applyRecommendation: (incoming, callId, triggerAtMs) => {
    set((state) => {
      const withSource = incoming.filter(hasCardSource);
      const seen = new Set(
        state.cards.map((item) => `${item.card.source.doc_id}\0${item.card.title}`),
      );
      const added = withSource.filter(
        (card) => !seen.has(`${card.source.doc_id}\0${card.title}`),
      );
      if (added.length === 0) {
        return { callId };
      }
      let cards: PanelCard[] = [
        ...state.cards,
        ...added.map((card) => ({
          card,
          trigger_at_ms: triggerAtMs,
          closure: null,
          settled: false,
        })),
      ];
      if (state.closure !== null) {
        const attached = cards.some(
          (item) => item.closure?.closure_type === state.closure?.closure_type,
        );
        if (!attached) {
          cards = withClosure(cards, state.closure);
        }
      }
      return { callId, cards };
    });
  },

  applyClosure: (event) => {
    set((state) => ({
      callId: event.call_id,
      closure: event,
      cards: withClosure(state.cards, event),
    }));
  },

  settleClosure: (closureType) => {
    set((state) => ({
      cards: state.cards.map((item) =>
        item.closure?.closure_type === closureType
          ? { ...item, settled: true }
          : item,
      ),
    }));
  },

  setStatus: (mode, connected) => {
    set({ mode, connected, error: null });
  },

  setError: (message) => {
    set({ error: message, connected: false });
  },

  setDemoDomain: (demoDomain) => {
    set({ demoDomain });
  },

  resetCall: () => {
    set({ ...emptyCall, error: null });
  },
}));
