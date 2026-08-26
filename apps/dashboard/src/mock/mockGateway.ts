import type { DemoDomain, TranscriptEvent } from "../types/contract";
import type { GatewayClient, GatewayListener } from "../lib/ws/types";
import { getScenario } from "./scenarios";

/** 발화 직후 종결 상태를 보내는 간격. 실측이 아님. */
const CLOSURE_AFTER_UTTERANCE_MS = 800;
/** 발화 사이 간격을 이만큼 줄인다. 실측이 아님. */
const GAP_SHAVE_MS = 2000;
const MIN_GAP_MS = 1500;

/**
 * domain 으로 시나리오 하나를 골라 재생한다.
 * 발화 시각은 utterance_end_ms 를 쓰되, 발화 사이 간격만 2초 줄여 재생한다.
 */
export class MockGatewayClient implements GatewayClient {
  readonly mode = "mock" as const;
  private timers: number[] = [];
  private aborted = false;

  constructor(private readonly domain: DemoDomain) {}

  connect(listeners: GatewayListener): void {
    this.disconnect();
    this.aborted = false;
    listeners.onStatus({ mode: "mock", connected: true });

    const scenario = getScenario(this.domain);
    const playAt = playbackClock(scenario.transcripts);

    for (const event of scenario.transcripts) {
      this.schedule(playAt(event.utterance_end_ms), () => {
        listeners.onTranscript(event);
      });
    }

    for (const batch of scenario.cardBatches) {
      this.schedule(playAt(batch.trigger_at_ms), () => {
        listeners.onRecommendation(batch);
      });
    }

    for (const item of scenario.closures) {
      const after = scenario.transcripts.find(
        (event) => event.segment_id === item.afterSegmentId,
      );
      const atMs = (after?.utterance_end_ms ?? 0) + CLOSURE_AFTER_UTTERANCE_MS;
      this.schedule(playAt(atMs), () => {
        listeners.onClosure(item.event);
      });
    }
  }

  disconnect(): void {
    this.aborted = true;
    for (const id of this.timers) {
      window.clearTimeout(id);
    }
    this.timers = [];
  }

  private schedule(delayMs: number, fn: () => void): void {
    const id = window.setTimeout(() => {
      if (!this.aborted) {
        fn();
      }
    }, delayMs);
    this.timers.push(id);
  }
}

function playbackClock(
  transcripts: TranscriptEvent[],
): (originalMs: number) => number {
  const anchors = transcripts.map((event) => event.utterance_end_ms);
  if (anchors.length === 0) {
    return (ms) => Math.max(0, ms);
  }

  const compressed = [anchors[0]];
  for (let i = 1; i < anchors.length; i += 1) {
    const gap = anchors[i] - anchors[i - 1];
    compressed.push(compressed[i - 1] + Math.max(gap - GAP_SHAVE_MS, MIN_GAP_MS));
  }

  return (originalMs: number) => {
    if (originalMs <= anchors[0]) {
      return Math.max(0, compressed[0] - (anchors[0] - originalMs));
    }
    for (let i = 1; i < anchors.length; i += 1) {
      if (originalMs <= anchors[i]) {
        const span = anchors[i] - anchors[i - 1];
        const ratio = span === 0 ? 1 : (originalMs - anchors[i - 1]) / span;
        return compressed[i - 1] + ratio * (compressed[i] - compressed[i - 1]);
      }
    }
    const last = anchors.length - 1;
    return compressed[last] + (originalMs - anchors[last]);
  };
}
