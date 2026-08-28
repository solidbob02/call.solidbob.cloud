import { useEffect, useRef, useState, type ReactElement } from "react";
import { DOMAINS, HERO_CYCLES, type HeroCycle } from "../demo/financeHero";

const CYCLE_MS = 2800;
const FADE_MS = 700;

export function Hero(): ReactElement {
  const [index, setIndex] = useState(0);
  const [outgoing, setOutgoing] = useState<number | null>(null);
  const reduceMotion = useRef(
    typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  );
  const skipFirstFade = useRef(true);

  useEffect(() => {
    const id = window.setInterval(() => {
      setIndex((current) => (current + 1) % HERO_CYCLES.length);
    }, CYCLE_MS);
    return () => {
      window.clearInterval(id);
    };
  }, []);

  useEffect(() => {
    if (skipFirstFade.current) {
      skipFirstFade.current = false;
      return;
    }
    if (reduceMotion.current) {
      return;
    }
    const leaving = (index - 1 + HERO_CYCLES.length) % HERO_CYCLES.length;
    setOutgoing(leaving);
    const fade = window.setTimeout(() => {
      setOutgoing(null);
    }, FADE_MS);
    return () => {
      window.clearTimeout(fade);
    };
  }, [index]);

  const current = HERO_CYCLES[index];
  const leaving = outgoing === null ? null : HERO_CYCLES[outgoing];

  return (
    <section id="hero" className="hero" aria-label="라이브 데모">
      <div className="blob teal" aria-hidden="true" />
      <div className="blob magenta" aria-hidden="true" />
      <div className="hero-grid">
        <div className="hero-copy">
          <p className="hero-eyebrow">CallGuard</p>
          <h1>묻는 순간, 문서가 뜬다.</h1>
          <a className="nav-cta" href="#contact">
            문의
          </a>
          <ul className="hero-badges">
            {DOMAINS.map((domain) => (
              <li key={domain.id}>
                <span className={`domain-dot domain-${domain.id}`} aria-hidden="true" />
                {domain.label}
              </li>
            ))}
          </ul>
        </div>
        <article className="demo-card">
          <div className="hero-wave" aria-hidden="true">
            <span />
            <span />
            <span />
            <span />
            <span />
          </div>
          <div className="demo-live">
            {leaving !== undefined && leaving !== null ? (
              <BeatLayer key={`out-${outgoing}`} beat={leaving} state="out" />
            ) : null}
            {current !== undefined ? (
              <BeatLayer key={`in-${index}`} beat={current} state="in" />
            ) : null}
          </div>
        </article>
      </div>
    </section>
  );
}

function BeatLayer({
  beat,
  state,
}: {
  beat: HeroCycle;
  state: "in" | "out";
}): ReactElement {
  return (
    <div className={`demo-beat demo-beat--${beat.domain} is-${state}`}>
      <p className="hero-keyword">{beat.keyword}</p>
      <div className="demo-doc">
        <p className="demo-doc-kicker">추천 문서</p>
        <h3>{beat.cardTitle}</h3>
      </div>
    </div>
  );
}
