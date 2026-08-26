import type { ReactElement } from "react";
import type { MaskType } from "../types/contract";
import { formatOffsetMs } from "../lib/text/codepoints";
import { useCallStore } from "../store/callStore";
import { ClosureStatus } from "./ClosureStatus";

const MASK_LABEL: Record<MaskType, string> = {
  P1: "주민등록번호",
  P2: "카드번호",
  P3: "계좌번호",
  P4: "연락처",
  P5: "인증번호",
  P6: "이름",
  P7: "주소",
};

export function MaskingLogPanel(): ReactElement {
  const entries = useCallStore((state) => state.maskingLog);

  return (
    <section className="panel" aria-labelledby="masking-heading">
      <header className="panel-head">
        <h2 id="masking-heading">경고</h2>
      </header>
      <div className="panel-body">
        {entries.length === 0 ? (
          <p className="empty">마스킹된 구간이 아직 없습니다.</p>
        ) : (
          <ul className="mask-log">
            {entries.map((entry) => (
              <li key={entry.id} className="mask-item">
                <div className="mask-meta">
                  <span className="mask-type">{MASK_LABEL[entry.type]}</span>
                  <time className="ts">{formatOffsetMs(entry.utterance_end_ms)}</time>
                </div>
                <p className="mask-excerpt">{entry.excerpt || "(빈 구간)"}</p>
                <p className="mask-span">
                  {entry.segment_id} · {entry.span[0]}–{entry.span[1]}
                </p>
              </li>
            ))}
          </ul>
        )}
        <ClosureStatus />
      </div>
    </section>
  );
}
