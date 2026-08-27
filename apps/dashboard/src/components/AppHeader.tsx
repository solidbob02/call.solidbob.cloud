import type { ChangeEvent, ReactElement } from "react";
import { isCoreApiConfigured } from "../lib/api/coreClient";
import { useCallStore } from "../store/callStore";
import { DEMO_DOMAIN_LABELS, DEMO_DOMAINS } from "../types/contract";
import type { DemoDomain } from "../types/contract";

interface AppHeaderProps {
  onReplay: () => void;
  onEndCall: () => void;
}

export function AppHeader({ onReplay, onEndCall }: AppHeaderProps): ReactElement {
  const mode = useCallStore((state) => state.mode);
  const connected = useCallStore((state) => state.connected);
  const callId = useCallStore((state) => state.callId);
  const error = useCallStore((state) => state.error);
  const demoDomain = useCallStore((state) => state.demoDomain);
  const setDemoDomain = useCallStore((state) => state.setDemoDomain);
  const phase = useCallStore((state) => state.phase);
  const hasCall = useCallStore((state) => state.utterances.length > 0);

  function onDomainChange(event: ChangeEvent<HTMLSelectElement>): void {
    setDemoDomain(event.target.value as DemoDomain);
  }

  return (
    <header className="app-header">
      <div className="brand">
        <span className="brand-logo" aria-hidden="true" />
        <span className="brand-mark">CallGuard</span>
        <span className="brand-sub">상담원 어시스트</span>
      </div>
      <div className="header-meta">
        {mode === "mock" ? (
          <label className="domain-picker">
            <span className="domain-picker-label">도메인</span>
            <select
              className="domain-select"
              value={demoDomain}
              onChange={onDomainChange}
              aria-label="도메인"
            >
              {DEMO_DOMAINS.map((domain) => (
                <option key={domain} value={domain}>
                  {DEMO_DOMAIN_LABELS[domain]}
                </option>
              ))}
            </select>
          </label>
        ) : null}
        {phase === "live" ? (
          <button
            type="button"
            className="btn-outline"
            onClick={onEndCall}
            disabled={!hasCall}
            title={hasCall ? undefined : "아직 통화 내용이 없습니다"}
          >
            <svg
              className="btn-outline-icon"
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <rect x="6.25" y="6.25" width="11.5" height="11.5" rx="1.5" />
            </svg>
            통화 종료
          </button>
        ) : null}
        <span className="call-id">{callId ?? "대기"}</span>
        <span className={`conn-badge ${connected ? "on" : "off"}`}>
          {connected ? <span className="conn-dot" aria-hidden="true" /> : null}
          {connected ? "연결됨" : "끊김"}
        </span>
        {isCoreApiConfigured() ? <span className="status">REST</span> : null}
        {mode === "mock" && phase === "live" ? (
          <button type="button" className="btn-replay" onClick={onReplay}>
            <svg
              className="btn-replay-icon"
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M6 4.75v14.5a.75.75 0 0 0 1.13.65l12.5-7.25a.75.75 0 0 0 0-1.3L7.13 4.1A.75.75 0 0 0 6 4.75z" />
            </svg>
            다시 재생
          </button>
        ) : null}
      </div>
      {error !== null ? <p className="header-error">{error}</p> : null}
    </header>
  );
}
