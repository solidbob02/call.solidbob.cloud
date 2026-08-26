import {
  useEffect,
  useRef,
  type ReactElement,
  type UIEvent,
} from "react";
import { MaskedText } from "./MaskedText";
import { formatOffsetMs } from "../lib/text/codepoints";
import { useCallStore } from "../store/callStore";

/** 이 거리 안이면 맨 아래에 있는 것으로 본다. */
const PIN_THRESHOLD_PX = 80;
const SMOOTH_LOCK_MS = 420;

export function TranscriptPanel(): ReactElement {
  const utterances = useCallStore((state) => state.utterances);
  const bodyRef = useRef<HTMLDivElement>(null);
  const pinnedRef = useRef(true);
  const autoScrollingRef = useRef(false);

  function onBodyScroll(event: UIEvent<HTMLDivElement>): void {
    if (autoScrollingRef.current) {
      return;
    }
    const el = event.currentTarget;
    const distance = el.scrollHeight - el.scrollTop - el.clientHeight;
    pinnedRef.current = distance <= PIN_THRESHOLD_PX;
  }

  useEffect(() => {
    if (utterances.length === 0) {
      pinnedRef.current = true;
      return;
    }
    if (!pinnedRef.current) {
      return;
    }
    const el = bodyRef.current;
    if (el === null) {
      return;
    }

    const last = utterances[utterances.length - 1];
    if (last === undefined) {
      return;
    }
    const smooth = last.is_final;
    autoScrollingRef.current = true;
    const frame = window.requestAnimationFrame(() => {
      el.scrollTo({
        top: el.scrollHeight,
        behavior: smooth ? "smooth" : "auto",
      });
    });

    const unlock = window.setTimeout(() => {
      autoScrollingRef.current = false;
      const distance = el.scrollHeight - el.scrollTop - el.clientHeight;
      if (distance <= PIN_THRESHOLD_PX) {
        pinnedRef.current = true;
      }
    }, smooth ? SMOOTH_LOCK_MS : 0);

    return () => {
      window.cancelAnimationFrame(frame);
      window.clearTimeout(unlock);
      autoScrollingRef.current = false;
    };
  }, [utterances]);

  return (
    <section className="panel" aria-labelledby="transcript-heading">
      <header className="panel-head">
        <h2 id="transcript-heading">실시간 자막</h2>
      </header>
      <div className="panel-body" ref={bodyRef} onScroll={onBodyScroll}>
        {utterances.length === 0 ? (
          <p className="empty">발화가 아직 없습니다.</p>
        ) : (
          <ol className="utterance-list">
            {utterances.map((item) => {
              const hasAlert = item.masked.length > 0;
              return (
                <li
                  key={item.segment_id}
                  className={`utterance ${item.speaker}${item.is_final ? "" : " interim"}`}
                >
                  <span className="bar" aria-hidden="true" />
                  <div className="utterance-body">
                    <div className="utterance-meta">
                      <span className="speaker">
                        {item.speaker === "customer" ? "고객" : "상담원"}
                      </span>
                      <time
                        className="ts"
                        dateTime={`+${item.utterance_end_ms}ms`}
                      >
                        {formatOffsetMs(item.utterance_end_ms)}
                      </time>
                    </div>
                    <div className="utterance-line">
                      <p className="utterance-text">
                        <MaskedText text={item.text} masked={item.masked} />
                      </p>
                      {hasAlert ? (
                        <span className="alert-pill">⚠ 경고</span>
                      ) : null}
                    </div>
                  </div>
                </li>
              );
            })}
          </ol>
        )}
      </div>
    </section>
  );
}
