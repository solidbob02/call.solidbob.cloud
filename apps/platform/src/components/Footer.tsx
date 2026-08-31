import type { ReactElement } from "react";

export function Footer(): ReactElement {
  return (
    <footer className="border-t border-line bg-bg px-5 py-8">
      <div className="mx-auto flex max-w-[1120px] flex-col gap-3 text-[13px] text-ink-soft mid:flex-row mid:items-center mid:justify-between">
        <p className="m-0">© 2026 SOLIDBOB · CallGuard</p>
        <p className="m-0">다산콜센터 상담 시나리오 기반 포트폴리오 프로젝트</p>
      </div>
    </footer>
  );
}
