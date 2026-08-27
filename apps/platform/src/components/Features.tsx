import { useEffect, useState, type ReactElement } from "react";
import { CARD_LOSS, LINE_LOSS, MASKED_LINE, WRAP_UP_LINES } from "../demo/financeHero";

export function Features(): ReactElement {
  const [summaryIndex, setSummaryIndex] = useState(0);

  useEffect(() => {
    const id = window.setInterval(() => {
      setSummaryIndex((i) => (i + 1) % WRAP_UP_LINES.length);
    }, 2800);
    return () => {
      window.clearInterval(id);
    };
  }, []);

  return (
    <section className="section features" id="features">
      <div className="section-inner">
        <p className="eyebrow">하는 일</p>
        <h2>세 가지. 나머지는 나중에.</h2>
        <div className="feature-grid">
          <article className="feature-card">
            <span className="feature-icon feature-icon-teal" aria-hidden="true" />
            <h3>실시간요약</h3>
            <p className="feature-tech">생성 모델(EXAONE) 기반</p>
            <p className="feature-demo">{WRAP_UP_LINES[summaryIndex]}</p>
          </article>
          <article className="feature-card">
            <span className="feature-icon feature-icon-magenta" aria-hidden="true" />
            <h3>키워드팝업</h3>
            <p className="feature-tech">하이브리드 검색(BM25+임베딩) 기반</p>
            <p className="feature-demo">
              {LINE_LOSS.split("분실").map((part, index, parts) =>
                index < parts.length - 1 ? (
                  <span key={`kw-${index}`}>
                    {part}
                    <span className="kw-static" tabIndex={0}>
                      분실
                      <span className="kw-tip">
                        <strong>{CARD_LOSS.title}</strong>
                        {CARD_LOSS.source}
                      </span>
                    </span>
                  </span>
                ) : (
                  <span key="kw-end">{part}</span>
                ),
              )}
            </p>
          </article>
          <article className="feature-card">
            <span className="feature-icon feature-icon-red" aria-hidden="true" />
            <h3>PII암호화</h3>
            <p className="feature-tech">정규식+NER 기반</p>
            <PiiLine />
          </article>
        </div>
      </div>
    </section>
  );
}

function PiiLine(): ReactElement {
  const [before, after] = MASKED_LINE.split("****");
  return (
    <p className="feature-demo feature-demo-mono">
      {before}
      <span className="pii">****</span>
      {after}
    </p>
  );
}
