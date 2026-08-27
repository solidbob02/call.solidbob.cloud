import type { ReactElement } from "react";
import { DOMAINS } from "../demo/financeHero";

export function Domains(): ReactElement {
  return (
    <section className="quiet domains" id="domains">
      <p className="eyebrow">데모 도메인</p>
      <h2>확보한 데이터 네 곳만 다룬다.</h2>
      <ul className="domain-grid">
        {DOMAINS.map((domain) => (
          <li key={domain.id}>
            <span className={`domain-icon domain-${domain.id}`} aria-hidden="true" />
            <span className="domain-label">{domain.label}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
