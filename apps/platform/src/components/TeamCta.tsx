import type { ReactElement } from "react";

const TEAM = ["정성윤", "류준", "장민석", "조서희"] as const;

export function TeamCta(): ReactElement {
  return (
    <section className="quiet contact" id="contact">
      <p className="eyebrow">SOLIDBOB</p>
      <h2>문의</h2>
      <p className="team-line">{TEAM.join(" · ")}</p>
      <a
        className="hero-cta"
        href="https://github.com/solidbob02/call.solidbob.cloud"
      >
        저장소에서 문의
      </a>
    </section>
  );
}
