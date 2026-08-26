import type { ReactElement } from "react";
import { MaskedText } from "./MaskedText";
import { formatOffsetMs } from "../lib/text/codepoints";
import { useCallStore } from "../store/callStore";

export function TranscriptPanel(): ReactElement {
  const utterances = useCallStore((state) => state.utterances);

  return (
    <section className="panel" aria-labelledby="transcript-heading">
      <header className="panel-head">
        <h2 id="transcript-heading">실시간 자막</h2>
      </header>
      <div className="panel-body">
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
