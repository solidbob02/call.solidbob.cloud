import type { ReactElement } from "react";

const LINKS = [
  { href: "#problem", label: "문제 상황" },
  { href: "#features", label: "핵심 기능" },
  { href: "#how", label: "작동 방식" },
  { href: "#project", label: "프로젝트 정보" },
] as const;

export function Nav(): ReactElement {
  return (
    <header className="sticky top-0 z-50 border-b border-line/80 bg-bg/80 backdrop-blur-md">
      <div className="mx-auto flex h-[68px] max-w-[1120px] items-center justify-between gap-6 px-5">
        <a href="#hero" className="flex items-center gap-2.5 text-ink">
          <span
            className="block h-7 w-7 rounded-[7px] bg-linear-to-br from-brand-deep via-brand to-brand-bright"
            aria-hidden="true"
          />
          <span className="text-[17px] font-semibold tracking-tight">
            CallGuard
          </span>
        </a>
        <nav className="hidden items-center gap-7 text-[14px] text-ink-soft mid:flex" aria-label="바로가기">
          {LINKS.map((link) => (
            <a key={link.href} href={link.href} className="hover:text-ink">
              {link.label}
            </a>
          ))}
        </nav>
        <a
          href="#cta"
          className="rounded-[10px] bg-brand px-3.5 py-2 text-[13px] font-semibold text-white"
        >
          문의
        </a>
      </div>
    </header>
  );
}
