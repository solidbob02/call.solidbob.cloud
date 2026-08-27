import type { ReactElement } from "react";

const TEAM = ["정성윤", "류준", "장민석", "조서희"] as const;

export function TeamCta(): ReactElement {
  return (
    <footer className="section contact" id="contact">
      <div className="section-inner">
        <p className="eyebrow">SOLIDBOB</p>
        <h2>문의</h2>
        <p className="team-line">{TEAM.join(" · ")}</p>
        <p className="cta-lead">도입 검토 중이신가요? 실제 데모로 확인하세요.</p>
        <a
          className="nav-cta"
          href="https://github.com/solidbob02/call.solidbob.cloud"
        >
          상담 신청
        </a>
      </div>
    </footer>
  );
}
