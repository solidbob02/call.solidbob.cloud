import type { ReactElement } from "react";
import { useCallStore } from "../store/callStore";

export function ClosureModal(): ReactElement | null {
  const closure = useCallStore((state) => state.closure);
  const open = useCallStore((state) => state.closureOpen);
  const dismiss = useCallStore((state) => state.dismissClosure);

  if (!open || closure === null) {
    return null;
  }

  const missing = closure.missing;
  const canClose = missing.length === 0 && closure.verdict === "approved";
  const evidenceKeys = Object.keys(closure.evidence);
  const unmet = !canClose;

  return (
    <div className="modal-backdrop" role="presentation" onClick={dismiss}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="closure-title"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="modal-head">
          <button
            type="button"
            className="modal-close"
            onClick={dismiss}
            aria-label="닫기"
          >
            <CloseIcon />
          </button>
          <p className="modal-kicker">F-2 종결 요건</p>
          <h2 id="closure-title">{closure.closure_type}</h2>
          <p className="modal-reason">{closure.reason}</p>
        </header>

        <p className={`verdict ${unmet ? "verdict-blocked" : "verdict-approved"}`}>
          {unmet ? "종결 요건 미충족" : "종결 요건 충족"}
        </p>

        <ul className="evidence-list">
          {evidenceKeys.map((key) => {
            const met = closure.evidence[key];
            const isMissing = missing.includes(key);
            return (
              <li key={key} className={isMissing ? "missing" : met ? "met" : ""}>
                <span className="check" aria-hidden="true">
                  {met ? "☑" : "☐"}
                </span>
                <span>{key.replace(/_/g, " ")}</span>
              </li>
            );
          })}
        </ul>

        {missing.length > 0 ? (
          <p className="missing-note">미충족: {missing.join(", ")}</p>
        ) : null}

        <p className="card-source modal-source">
          <span className="doc-id">{closure.source.doc_id}</span>
          <span>{closure.source.title}</span>
        </p>

        <footer className="modal-actions">
          <button type="button" className="btn-ghost" onClick={dismiss}>
            닫기
          </button>
          <button
            type="button"
            className="btn-primary"
            disabled={!canClose}
            onClick={canClose ? dismiss : undefined}
          >
            {canClose ? "종결 처리" : "근거 미충족 — 종결 불가"}
          </button>
        </footer>
      </div>
    </div>
  );
}

function CloseIcon(): ReactElement {
  return (
    <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
      <path
        d="M6 6l12 12M18 6 6 18"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}
