import {
  useEffect,
  useRef,
  useState,
  type FormEvent,
  type ReactElement,
} from "react";
import { cardSourceType, type ClosureEvent } from "../types/contract";
import { cardId, evidenceTally, useCallStore } from "../store/callStore";
import type { PanelCard } from "../store/callStore";
import type { ManualSearchOutcome } from "../hooks/useGatewaySession";
import { BookmarkDock } from "./BookmarkDock";

function categoryFromDocId(docId: string): string {
  return docId.split("-")[0] ?? docId;
}

function cardDomId(index: number): string {
  return `term-card-${index}`;
}

interface TermsPanelProps {
  onManualSearch: (query: string) => Promise<ManualSearchOutcome>;
}

export function TermsPanel({ onManualSearch }: TermsPanelProps): ReactElement {
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
      <ManualSearchBar onSearch={onManualSearch} />
      <BookmarkDock onJump={jumpTo} />
    </section>
  );
}

function noticeFor(outcome: ManualSearchOutcome, query: string): string {
  switch (outcome.kind) {
    case "added":
      return `「${query}」 결과 ${outcome.count}건을 아래에 추가했어요.`;
    case "empty":
      return `「${query}」 관련 문서 없음. 검색어를 바꿔 다시 찾아보세요.`;
    case "duplicate":
      return `「${query}」 결과는 이미 패널에 올라와 있어요.`;
    case "error":
      return outcome.message;
  }
}

/**
 * §2.3 B-6 으로 "관련 문서 없음"이 떴을 때 상담원이 직접 찾는 경로.
 * 카드가 있든 없든 항상 열려 있어야 한다 — 자동 추천이 맞았는지는 상담원이 판단한다.
 */
function ManualSearchBar({
  onSearch,
}: {
  onSearch: (query: string) => Promise<ManualSearchOutcome>;
}): ReactElement {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      inputRef.current?.focus();
    }
  }, [open]);

  async function submit(event: FormEvent<HTMLFormElement>): Promise<void> {
    event.preventDefault();
    const trimmed = query.trim();
    if (trimmed.length === 0 || busy) {
      return;
    }
    setBusy(true);
    setNotice(null);
    const outcome = await onSearch(trimmed);
    setBusy(false);
    setNotice(noticeFor(outcome, trimmed));
  }

  if (!open) {
    return (
      <div className="manual-search">
        <button
          type="button"
          className="manual-search-open"
          onClick={() => {
            setOpen(true);
          }}
        >
          <SearchIcon />
          관련 문서를 못 찾으셨나요?
        </button>
      </div>
    );
  }

  return (
    <div className="manual-search">
      <form
        className="manual-search-form"
        onSubmit={(event) => {
          void submit(event);
        }}
      >
        <SearchIcon />
        <input
          ref={inputRef}
          type="text"
          className="manual-search-input"
          placeholder="직접 검색해보세요"
          aria-label="문서 직접 검색"
          value={query}
          disabled={busy}
          onChange={(event) => {
            setQuery(event.target.value);
          }}
        />
        <button
          type="submit"
          className="manual-search-submit"
          disabled={busy || query.trim().length === 0}
        >
          검색
        </button>
        <button
          type="button"
          className="search-clear"
          aria-label="직접 검색 닫기"
          onClick={() => {
            setOpen(false);
            setQuery("");
            setNotice(null);
          }}
        >
          <svg
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.6"
            strokeLinecap="round"
            aria-hidden="true"
          >
            <path d="M6 6 18 18M18 6 6 18" />
          </svg>
        </button>
      </form>
      {busy ? (
        <p className="manual-search-note">
          <span className="spinner" aria-hidden="true" />
          검색 중...
        </p>
      ) : notice !== null ? (
        <p className="manual-search-note" role="status">
          {notice}
        </p>
      ) : null}
    </div>
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
  const toggleAdoption = useCallStore((state) => state.toggleAdoption);
  const adopted = useCallStore(
    (state) => state.adoptions[cardId(item.card)]?.adopted === true,
  );
  const category = categoryFromDocId(item.card.source.doc_id);
  const closure = item.closure;
  const manual = cardSourceType(item.card) === "manual";
  const canSettle =
    closure !== null && closure.missing.length === 0 && !item.settled;

  function onAdopt(): void {
    toggleAdoption(item.card);
  }

  return (
    <article
      id={cardDomId(index)}
      className={`term-card${manual ? " manual" : ""}${adopted ? " adopted" : ""}`}
      data-category={category}
    >
      <div className="term-card-body">
        <div className="card-head">
          <p className={`card-category cat-${category.toLowerCase()}`}>
            {category}
          </p>
          {manual ? <span className="card-flag">수동 검색</span> : null}
          {/* 종결 카드는 하단이 이미 꽉 차 있어 토글을 배지 옆에 둔다. */}
          {closure !== null ? (
            <AdoptToggle compact adopted={adopted} onToggle={onAdopt} />
          ) : adopted ? (
            <span className="adopt-mark" title="이 카드를 사용했습니다">
              <TickIcon />
            </span>
          ) : null}
        </div>
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
        ) : (
          <AdoptToggle adopted={adopted} onToggle={onAdopt} />
        )}
      </div>
    </article>
  );
}

/**
 * 어떤 문서가 실제로 쓰였는지 남기는 기록. 지식베이스 보강용이지 상담원 평가가 아니라서
 * 누르지 않은 것을 문제처럼 보이게 하지 않는다 — 기본 상태는 조용한 회색이다.
 */
function AdoptToggle({
  adopted,
  onToggle,
  compact = false,
}: {
  adopted: boolean;
  onToggle: () => void;
  compact?: boolean;
}): ReactElement {
  return (
    <button
      type="button"
      className={`adopt-toggle${adopted ? " on" : ""}${compact ? " compact" : ""}`}
      aria-pressed={adopted}
      aria-label={adopted ? "사용함" : "사용 표시"}
      title={adopted ? "사용함" : "사용 표시"}
      onClick={onToggle}
    >
      <span className="adopt-box" aria-hidden="true">
        <TickIcon />
      </span>
      {compact ? null : <span>{adopted ? "사용함" : "사용 표시"}</span>}
    </button>
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

function SearchIcon(): ReactElement {
  return (
    <svg
      className="search-icon"
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.2"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="M15.5 15.5 21 21" />
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

function TickIcon(): ReactElement {
  return (
    <svg
      viewBox="0 0 16 16"
      width="11"
      height="11"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M3.4 8.2 6.5 11.1 12.6 4.8" />
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
