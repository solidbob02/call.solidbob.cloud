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

export interface CallState {
  mode: GatewayMode;
  connected: boolean;
  error: string | null;
  demoDomain: DemoDomain;
  callId: string | null;
  utterances: Utterance[];
  cards: RecommendationCard[];
  maskingLog: MaskingLogEntry[];
  closure: ClosureEvent | null;
  closureOpen: boolean;
  expandedIndex: number | null;
  dockEpoch: number;
  applyTranscript: (event: TranscriptEvent) => void;
  applyRecommendation: (cards: RecommendationCard[], callId: string) => void;
  expandCard: (index: number) => void;
  collapseCards: () => void;
  applyClosure: (event: ClosureEvent) => void;
  dismissClosure: () => void;
  setStatus: (mode: GatewayMode, connected: boolean) => void;
  setError: (message: string) => void;
  setDemoDomain: (domain: DemoDomain) => void;
  resetCall: () => void;
}

const emptyCall = {
  callId: null as string | null,
  utterances: [] as Utterance[],
  cards: [] as RecommendationCard[],
  maskingLog: [] as MaskingLogEntry[],
  closure: null as ClosureEvent | null,
  closureOpen: false,
  expandedIndex: null as number | null,
  dockEpoch: 0,
};

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

  applyRecommendation: (incoming, callId) => {
    set((state) => {
      const withSource = incoming.filter(hasCardSource);
      const seen = new Set(
        state.cards.map((card) => `${card.source.doc_id}\0${card.title}`),
      );
      const added = withSource.filter(
        (card) => !seen.has(`${card.source.doc_id}\0${card.title}`),
      );
      if (added.length === 0) {
        return { callId };
      }
      return {
        callId,
        cards: [...state.cards, ...added],
        expandedIndex: state.cards.length + added.length - 1,
        dockEpoch: state.dockEpoch + 1,
      };
    });
  },

  expandCard: (index) => {
    set((state) => {
      if (index < 0 || index >= state.cards.length) {
        return state;
      }
      return {
        expandedIndex: index,
        dockEpoch: state.dockEpoch + 1,
      };
    });
  },

  collapseCards: () => {
    set({ expandedIndex: null });
  },

  applyClosure: (event) => {
    set({
      callId: event.call_id,
      closure: event,
      closureOpen: event.verdict === "approved",
    });
  },

  dismissClosure: () => {
    set({ closureOpen: false });
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
