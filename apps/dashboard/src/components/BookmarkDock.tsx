import { useEffect, useRef, type ReactElement } from "react";
import type { RecommendationCard } from "../types/contract";
import { useCallStore } from "../store/callStore";

function categoryFromDocId(docId: string): string {
  return docId.split("-")[0] ?? docId;
}

export function BookmarkDock(): ReactElement {
  const cards = useCallStore((state) => state.cards);
  const expandedIndex = useCallStore((state) => state.expandedIndex);
  const expandCard = useCallStore((state) => state.expandCard);
  const collapseCards = useCallStore((state) => state.collapseCards);
  const tabsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const root = tabsRef.current;
    if (root === null || cards.length === 0) {
      return;
    }
    root.scrollLeft = root.scrollWidth;
  }, [cards.length]);

  const expanded =
    expandedIndex === null ? undefined : cards[expandedIndex];
  const open = expanded !== undefined;

  return (
    <aside className="bookmark-dock" aria-label="추천 카드">
      <div className={`bookmark-sheet${open ? " open" : ""}`}>
        <div className="bookmark-sheet-inner">
          {expanded !== undefined ? (
            <ExpandedCard card={expanded} onCollapse={collapseCards} />
          ) : null}
        </div>
      </div>
      <div className="bookmark-tabs" role="tablist" ref={tabsRef}>
        {cards.length === 0 ? (
          <p className="bookmark-empty">관련 문서 없음</p>
        ) : (
          cards.map((card, index) => {
            const category = categoryFromDocId(card.source.doc_id);
            const selected = index === expandedIndex;
            return (
              <button
                key={`${card.source.doc_id}-${card.title}`}
                type="button"
                role="tab"
                aria-selected={selected}
                className={`bookmark-tab${selected ? " on" : ""}`}
                onClick={() => {
                  expandCard(index);
                }}
              >
                <span
                  className={`card-tab cat-${category.toLowerCase()}`}
                  aria-hidden="true"
                />
                <span className="bookmark-tab-label">{card.title}</span>
              </button>
            );
          })
        )}
      </div>
    </aside>
  );
}

function ExpandedCard({
  card,
  onCollapse,
}: {
  card: RecommendationCard;
  onCollapse: () => void;
}): ReactElement {
  const category = categoryFromDocId(card.source.doc_id);
  return (
    <article
      className="bookmark-card expanded"
      data-category={category}
      aria-labelledby="bookmark-card-title"
    >
      <span
        className={`card-tab cat-${category.toLowerCase()}`}
        aria-hidden="true"
      />
      <div className="bookmark-body">
        <div className="bookmark-card-head">
          <p className="card-category">{category}</p>
          <button
            type="button"
            className="bookmark-close"
            onClick={onCollapse}
            aria-label="닫기"
          >
            <CloseIcon />
          </button>
        </div>
        <h3 id="bookmark-card-title">{card.title}</h3>
        <p className="card-summary">{card.summary}</p>
        <p className="card-source">{card.source.title}</p>
      </div>
    </article>
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
