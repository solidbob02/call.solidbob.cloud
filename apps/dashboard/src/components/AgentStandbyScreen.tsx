import { useEffect, useState, type ReactElement } from "react";
import { BrandLockup } from "./AppHeader";
import { CallHistoryPanel } from "./CallHistoryPanel";
import { CallVolumeChart } from "./CallVolumeChart";
import { KpiCard } from "./KpiCard";
import {
  MOCK_HOURLY_VOLUME,
  MOCK_STANDBY_KPI,
} from "../mock/standbyKpi";

interface AgentStandbyScreenProps {
  agentName: string;
  onStartCall: () => void;
}

export function AgentStandbyScreen({
  agentName,
  onStartCall,
}: AgentStandbyScreenProps): ReactElement {
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const id = window.setInterval(() => {
      setNow(new Date());
    }, 30_000);
    return () => {
      window.clearInterval(id);
    };
  }, []);

  const initial = agentName.slice(0, 1);

  return (
    <main className="standby">
      <header className="standby-top">
        <div className="standby-hello">
          <BrandLockup />
          <div>
            <h1 className="standby-greeting">{`안녕하세요, ${agentName}님`}</h1>
            <p className="standby-clock">
              <time dateTime={now.toISOString()}>{formatStandbyNow(now)}</time>
            </p>
          </div>
        </div>
        <div className="standby-aside">
          <div className="standby-profile">
            <span className="standby-avatar" aria-hidden="true">
              {initial}
            </span>
            <span className="standby-agent">{agentName}</span>
          </div>
          <button
            type="button"
            className="btn-primary btn-start-call"
            onClick={onStartCall}
          >
            통화 시작
          </button>
        </div>
      </header>

      <section className="standby-kpi" aria-label="오늘 현황">
        {MOCK_STANDBY_KPI.map((item) => (
          <KpiCard
            key={item.label}
            label={item.label}
            value={item.value}
            variant={item.variant}
          />
        ))}
      </section>
      <p className="wrapup-note standby-kpi-note">
        위 숫자는 목업입니다. 실측이 아닙니다.
      </p>

      <CallVolumeChart points={MOCK_HOURLY_VOLUME} />

      <section className="standby-history wrapup-card">
        <CallHistoryPanel
          onReplay={onStartCall}
          variant="page"
          returnTo="standby"
        />
      </section>
    </main>
  );
}

function formatStandbyNow(date: Date): string {
  const weekdays = ["일", "월", "화", "수", "목", "금", "토"] as const;
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  const hh = String(date.getHours()).padStart(2, "0");
  const mm = String(date.getMinutes()).padStart(2, "0");
  return `${y}.${m}.${d} (${weekdays[date.getDay()]}) ${hh}:${mm}`;
}
