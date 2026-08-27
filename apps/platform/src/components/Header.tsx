import type { ReactElement } from "react";

export function Header(): ReactElement {
  return (
    <header className="site-header">
      <a className="logo" href="#hero">
        <span className="logo-mark" aria-hidden="true" />
        CallGuard
      </a>
      <nav className="nav" aria-label="바로가기">
        <a href="#hero">데모보기</a>
        <a className="nav-cta" href="#contact">
          문의
        </a>
      </nav>
    </header>
  );
}
