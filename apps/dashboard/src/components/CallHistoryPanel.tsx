import { useMemo, type ReactElement } from "react";
import { listCallHistoryRows } from "../mock/callHistory";
import {
  ResolutionStats,
  SHOW_RESOLUTION_STATS,
} from "./ResolutionStats";
import { setSelectedMockScenarioId } from "../mock/scenarios";
import { formatCallStartedAt } from "../lib/formatCallTime";
import { useCallStore } from "../store/callStore";
import { DEMO_DOMAIN_LABELS } from "../types/contract";

interface CallHistoryPanelProps {
  onReplay: () => void;
}

export function CallHistoryPanel({
  onReplay,
}: CallHistoryPanelProps): ReactElement {
  const rows = useMemo(() => listCallHistoryRows(), []);
  const openHistory = useCallStore((state) => state.openHistory);
  const historyCallId = useCallStore((state) => state.historyCallId);

  return (
    <div className="call-history">
      <p className="call-history-heading">상담기록</p>
      {SHOW_RESOLUTION_STATS ? <ResolutionStats /> : null}
      <ul className="call-history-list">
        {rows.map((row) => (
          <li key={row.item.call_id} className="call-history-item">
            <button
              type="button"
              className={`call-history-row${historyCallId === row.item.call_id ? " is-active" : ""}`}
              onClick={() => {
                openHistory(row.item);
              }}
            >
              <time dateTime={row.item.started_at}>
                {formatCallStartedAt(row.item.started_at)}
              </time>
              <span className="call-history-badge">
                <span className="call-history-flag" aria-hidden="true">
                  {row.langFlag}
                </span>
                {DEMO_DOMAIN_LABELS[row.item.domain]}
              </span>
              <span className="call-history-type">{row.item.inquiry_type}</span>
              <span className="call-history-ref">{row.item.customer_ref}</span>
            </button>
            <button
              type="button"
              className="call-history-replay"
              title="다시 재생"
              aria-label={`${row.item.inquiry_type} 다시 재생`}
              onClick={() => {
                setSelectedMockScenarioId(row.scenarioId);
                onReplay();
              }}
            >
              <ReplayIcon />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ReplayIcon(): ReactElement {
  return (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M6 4.75v14.5a.75.75 0 0 0 1.13.65l12.5-7.25a.75.75 0 0 0 0-1.3L7.13 4.1A.75.75 0 0 0 6 4.75z" />
    </svg>
  );
}
