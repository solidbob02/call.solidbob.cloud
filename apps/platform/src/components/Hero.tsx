import { useCallback, useEffect, useRef, useState, type ReactElement } from "react";
import {
  HERO_BEATS,
  type DemoCard,
  type HeroBeat,
} from "../demo/financeHero";

const CHAR_MS = 38;
const AFTER_KEYWORD_MS = 280;
const AFTER_LINE_MS = 1100;
const AFTER_CARD_MS = 1600;
const LOOP_GAP_MS = 1800;

interface LineState {
  speaker: HeroBeat["speaker"];
  text: string;
  keyword: string | null;
  glow: boolean;
}

export function Hero(): ReactElement {
  const [lines, setLines] = useState<LineState[]>([]);
  const [typed, setTyped] = useState(0);
  const [card, setCard] = useState<DemoCard | null>(null);
  const [loop, setLoop] = useState(0);
  const timers = useRef<number[]>([]);

  const clearTimers = useCallback(() => {
    for (const id of timers.current) {
      window.clearTimeout(id);
    }
    timers.current = [];
  }, []);

  const wait = useCallback((ms: number): Promise<void> => {
    return new Promise((resolve) => {
      const id = window.setTimeout(resolve, ms);
      timers.current.push(id);
    });
  }, []);

  useEffect(() => {
    let cancelled = false;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const lastWithCard = [...HERO_BEATS].reverse().find((beat) => beat.card !== null);
      setLines(
        HERO_BEATS.map((beat) => ({
          speaker: beat.speaker,
          text: beat.text,
          keyword: beat.keyword,
          glow: beat.keyword !== null,
        })),
      );
      const last = HERO_BEATS[HERO_BEATS.length - 1];
      setTyped(last?.text.length ?? 0);
      setCard(lastWithCard?.card ?? null);
      return;
    }

    async function play(): Promise<void> {
      setLines([]);
      setTyped(0);
      setCard(null);

      for (const beat of HERO_BEATS) {
        if (cancelled) {
          return;
        }
        const line: LineState = {
          speaker: beat.speaker,
          text: beat.text,
          keyword: beat.keyword,
          glow: false,
        };
        setLines((prev) => [...prev, line].slice(-4));
        setTyped(0);

        const keywordAt =
          beat.keyword === null ? -1 : beat.text.indexOf(beat.keyword);
        const keywordEnd =
          keywordAt === -1 || beat.keyword === null
            ? -1
            : keywordAt + beat.keyword.length;

        for (let i = 1; i <= beat.text.length; i += 1) {
          if (cancelled) {
            return;
          }
          setTyped(i);
          if (keywordEnd !== -1 && i === keywordEnd) {
            setLines((prev) =>
              prev.map((item, idx) =>
                idx === prev.length - 1 ? { ...item, glow: true } : item,
              ),
            );
            await wait(AFTER_KEYWORD_MS);
            if (cancelled) {
              return;
            }
            if (beat.card !== null) {
              setCard(beat.card);
            }
          }
          await wait(CHAR_MS);
        }
        await wait(beat.card !== null ? AFTER_CARD_MS : AFTER_LINE_MS);
      }

      await wait(LOOP_GAP_MS);
      if (!cancelled) {
        setLoop((n) => n + 1);
      }
    }

    void play();
    return () => {
      cancelled = true;
      clearTimers();
    };
  }, [loop, wait, clearTimers]);

  const current = lines[lines.length - 1];

  return (
    <section id="hero" className="hero" aria-label="라이브 데모">
      <div className="hero-bundle">
        <div className="hero-stage" aria-hidden="true">
        <div className="hero-feed">
          {lines.map((line, index) => {
            const isCurrent = index === lines.length - 1;
            return (
              <p
                key={`${loop}-${index}-${line.text.slice(0, 8)}`}
                className={`hero-line ${line.speaker}${isCurrent ? " is-live" : ""}`}
              >
                <span className="hero-speaker">
                  {line.speaker === "customer" ? "고객" : "상담원"}
                </span>
                <span className="hero-text">
                  {renderTyped(
                    line.text,
                    isCurrent ? typed : line.text.length,
                    line.keyword,
                    line.glow,
                    isCurrent,
                  )}
                </span>
              </p>
            );
          })}
        </div>
        {card !== null ? (
          <article className="hero-card">
            <p className="hero-card-kicker">추천 문서</p>
            <h3>{card.title}</h3>
            <p>{card.summary}</p>
            <p className="hero-card-source">{card.source}</p>
          </article>
        ) : null}
        </div>
        <div className="hero-copy">
          <p className="hero-eyebrow">CallGuard</p>
          <h1>묻는 순간, 문서가 뜬다.</h1>
          <a className="hero-cta" href="#contact">
            문의
          </a>
        </div>
      </div>
      {current === undefined ? <span className="sr-only">데모 준비 중</span> : null}
    </section>
  );
}

function renderTyped(
  text: string,
  typed: number,
  keyword: string | null,
  glow: boolean,
  live: boolean,
): ReactElement {
  const shown = text.slice(0, typed);
  const caret = live && typed < text.length ? <span className="caret" /> : null;
  if (keyword === null || !glow) {
    return (
      <>
        {shown}
        {caret}
      </>
    );
  }
  const start = text.indexOf(keyword);
  if (start === -1 || typed <= start) {
    return (
      <>
        {shown}
        {caret}
      </>
    );
  }
  const end = Math.min(typed, start + keyword.length);
  return (
    <>
      {text.slice(0, start)}
      <mark className="kw">{text.slice(start, end)}</mark>
      {text.slice(end, typed)}
      {caret}
    </>
  );
}
