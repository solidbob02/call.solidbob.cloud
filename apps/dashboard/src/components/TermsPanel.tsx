import { useRef, type ReactElement } from "react";
import type { ClosureEvent } from "../types/contract";
import { evidenceTally, useCallStore } from "../store/callStore";
import type { PanelCard } from "../store/callStore";
import { BookmarkDock } from "./BookmarkDock";

function categoryFromDocId(docId: string): string {
  return docId.split("-")[0] ?? docId;
}

function cardDomId(index: number): string {
  return `term-card-${index}`;
}

export function TermsPanel(): ReactElement {
  const cards = useCallStore((state) => state.cards);
  const pending = cards.find((item) => item.closure !== null && !item.settled);
  const tally =
    pending?.closure !== undefined && pending.closure !== null
      ? evidenceTally(pending.closure)
      : null;

  const bodyRef = useRef<HTMLDivElement>(null);

  function jumpTo(index: number): void {
    const node = bodyRef.current?.querySelector(`#${cardDomId(index)}`);
    node?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  return (
    <section className="panel terms-panel" aria-labelledby="terms-heading">
      <header className="panel-head terms-head">
        <h2 id="terms-heading">이용약관 · 충족요건</h2>
        {tally !== null ? (
          <div className="tally-chip">
            <ProgressRing met={tally.met} total={tally.total} />
            <span>{`근거 ${tally.met}/${tally.total} 충족`}</span>
          </div>
        ) : null}
      </header>
      <div className="panel-body terms-body" ref={bodyRef}>
        {cards.length === 0 ? (
          <p className="empty">관련 문서가 아직 없습니다.</p>
        ) : (
          <ul className="term-card-list">
            {cards.map((item, index) => (
              <li key={`${item.card.source.doc_id}-${item.card.title}`}>
                <TermCard item={item} index={index} />
              </li>
            ))}
          </ul>
        )}
      </div>
      <BookmarkDock onJump={jumpTo} />
    </section>
  );
}

function TermCard({
  item,
  index,
}: {
  item: PanelCard;
  index: number;
}): ReactElement {
  const settleClosure = useCallStore((state) => state.settleClosure);
  const category = categoryFromDocId(item.card.source.doc_id);
  const closure = item.closure;
  const canSettle =
    closure !== null && closure.missing.length === 0 && !item.settled;

  return (
    <article
      id={cardDomId(index)}
      className="term-card"
      data-category={category}
    >
      <span
        className={`card-tab cat-${category.toLowerCase()}`}
        aria-hidden="true"
      />
      <div className="term-card-body">
        <p className={`card-category cat-${category.toLowerCase()}`}>{category}</p>
        <h3>{item.card.title}</h3>
        <p className="card-summary">{item.card.summary}</p>
        <p className="card-source">
          <FileTextIcon />
          <span>{item.card.source.title}</span>
        </p>
        {closure !== null ? (
          <ClosureBlock
            closure={closure}
            canSettle={canSettle}
            category={category}
            onSettle={() => {
              settleClosure(closure.closure_type);
            }}
          />
        ) : null}
      </div>
    </article>
  );
}

function ClosureBlock({
  closure,
  canSettle,
  category,
  onSettle,
}: {
  closure: ClosureEvent;
  canSettle: boolean;
  category: string;
  onSettle: () => void;
}): ReactElement {
  const keys = Object.keys(closure.evidence);
  const tally = evidenceTally(closure);

  return (
    <div className="closure-block">
      <hr className="closure-split" />
      <h4 className="closure-subhead">종결 충족요건</h4>
      <div className={`tally-row cat-${category.toLowerCase()}`}>
        <ProgressRing met={tally.met} total={tally.total} />
        <p className="evidence-tally">{`근거 ${tally.total}건 중 ${tally.met}건 충족`}</p>
      </div>
      <ul className="evidence-list">
        {keys.map((key) => {
          const met = closure.evidence[key] === true;
          return (
            <li key={key} className={met ? "met" : "missing"}>
              <span className={`evidence-icon-wrap ${met ? "met" : "missing"}`}>
                {met ? <CheckIcon /> : <CrossIcon />}
              </span>
              <span>{key.replace(/_/g, " ")}</span>
            </li>
          );
        })}
      </ul>
      {canSettle ? (
        <button type="button" className="btn-primary" onClick={onSettle}>
          종결 처리
        </button>
      ) : null}
    </div>
  );
}

function ProgressRing({
  met,
  total,
}: {
  met: number;
  total: number;
}): ReactElement {
  const size = 38;
  const stroke = 3;
  const radius = (size - stroke) / 2;
  const center = size / 2;
  const circumference = 2 * Math.PI * radius;
  const ratio = total === 0 ? 0 : met / total;
  const offset = circumference * (1 - ratio);

  return (
    <svg
      className="progress-ring"
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      aria-hidden="true"
    >
      <circle
        cx={center}
        cy={center}
        r={radius}
        fill="none"
        stroke="#ecece7"
        strokeWidth={stroke}
      />
      <circle
        className="progress-ring-arc"
        cx={center}
        cy={center}
        r={radius}
        fill="none"
        stroke="currentColor"
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${center} ${center})`}
      />
      <text
        x={center}
        y={center}
        textAnchor="middle"
        dominantBaseline="central"
        className="progress-ring-label"
      >
        {`${met}/${total}`}
      </text>
    </svg>
  );
}

function FileTextIcon(): ReactElement {
  return (
    <svg
      className="source-icon"
      viewBox="0 0 16 16"
      width="14"
      height="14"
      aria-hidden="true"
    >
      <path
        d="M4.2 1.75h5.1L12.3 4.8v9.45H4.2V1.75Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.2"
        strokeLinejoin="round"
      />
      <path
        d="M9.2 1.75V4.9h3.1M6 8.2h4.2M6 10.6h4.2"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function CheckIcon(): ReactElement {
  return (
    <svg
      className="evidence-icon"
      viewBox="0 0 16 16"
      width="11"
      height="11"
      aria-hidden="true"
    >
      <path
        d="M3.4 8.2 6.5 11.1 12.6 4.8"
        fill="none"
        stroke="#1F7A43"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function CrossIcon(): ReactElement {
  return (
    <svg
      className="evidence-icon"
      viewBox="0 0 16 16"
      width="11"
      height="11"
      aria-hidden="true"
    >
      <path
        d="M4.6 4.6l6.8 6.8M11.4 4.6l-6.8 6.8"
        fill="none"
        stroke="#8F2A29"
        strokeWidth="1.8"
        strokeLinecap="round"
      />
    </svg>
  );
}
