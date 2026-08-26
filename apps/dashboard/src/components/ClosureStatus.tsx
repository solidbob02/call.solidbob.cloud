import type { ReactElement } from "react";
import { useCallStore } from "../store/callStore";

export function ClosureStatus(): ReactElement | null {
  const closure = useCallStore((state) => state.closure);

  if (closure === null) {
    return null;
  }

  const evidenceKeys = Object.keys(closure.evidence);
  const total = evidenceKeys.length;
  const met = evidenceKeys.filter((key) => closure.evidence[key] === true).length;
  const unmet = closure.verdict !== "approved" || met < total;

  return (
    <div className="closure-live" aria-live="polite">
      <p className="closure-live-kicker">F-2 종결 요건</p>
      <p className="evidence-tally">{`근거 ${total}건 중 ${met}건 충족`}</p>
      <p className={`verdict ${unmet ? "verdict-blocked" : "verdict-approved"}`}>
        {unmet ? "종결 요건 미충족" : "종결 요건 충족"}
      </p>
      <ul className="evidence-list">
        {evidenceKeys.map((key) => {
          const done = closure.evidence[key] === true;
          return (
            <li key={key} className={done ? "met" : "missing"}>
              <span className="check" aria-hidden="true">
                {done ? "☑" : "☐"}
              </span>
              <span>{key.replace(/_/g, " ")}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
