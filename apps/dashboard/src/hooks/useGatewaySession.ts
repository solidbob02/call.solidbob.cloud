import { useCallback, useEffect, useRef } from "react";
import { createGatewayClient } from "../lib/ws";
import type { GatewayClient } from "../lib/ws";
import type { TranscriptEvent } from "../types/contract";
import { useCallStore } from "../store/callStore";

/**
 * 같은 segment_id 의 interim 은 누적하지 않고 rAF 한 프레임에 최신 것만 반영.
 * 7.3절: requestAnimationFrame 또는 100ms 디바운스.
 */
export function useGatewaySession(): { replay: () => void } {
  const clientRef = useRef<GatewayClient | null>(null);
  const pendingRef = useRef<Map<string, TranscriptEvent>>(new Map());
  const rafRef = useRef<number>(0);

  const flushTranscripts = useCallback(() => {
    rafRef.current = 0;
    const batch = [...pendingRef.current.values()];
    pendingRef.current.clear();
    const apply = useCallStore.getState().applyTranscript;
    for (const event of batch) {
      apply(event);
    }
  }, []);

  const queueTranscript = useCallback(
    (event: TranscriptEvent) => {
      pendingRef.current.set(event.segment_id, event);
      if (rafRef.current !== 0) {
        return;
      }
      rafRef.current = window.requestAnimationFrame(flushTranscripts);
    },
    [flushTranscripts],
  );

  const attach = useCallback(
    (client: GatewayClient) => {
      useCallStore.getState().resetCall();
      client.connect({
        onTranscript: queueTranscript,
        onRecommendation: (batch) => {
          useCallStore.getState().applyRecommendation(batch.cards, batch.call_id);
        },
        onClosure: (event) => {
          useCallStore.getState().applyClosure(event);
        },
        onStatus: (status) => {
          useCallStore.getState().setStatus(status.mode, status.connected);
        },
        onError: (message) => {
          useCallStore.getState().setError(message);
        },
      });
    },
    [queueTranscript],
  );

  const demoDomain = useCallStore((state) => state.demoDomain);

  useEffect(() => {
    const client = createGatewayClient(demoDomain);
    clientRef.current = client;
    attach(client);
    return () => {
      if (rafRef.current !== 0) {
        window.cancelAnimationFrame(rafRef.current);
        rafRef.current = 0;
      }
      pendingRef.current.clear();
      client.disconnect();
      clientRef.current = null;
    };
  }, [attach, demoDomain]);

  const replay = useCallback(() => {
    const client = clientRef.current;
    if (client === null || client.mode !== "mock") {
      return;
    }
    attach(client);
  }, [attach]);

  return { replay };
}
