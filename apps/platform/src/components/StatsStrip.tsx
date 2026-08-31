import type { ReactElement } from "react";

const STATS = [
  { value: "4인", label: "SOLIDBOB 팀 구성" },
  { value: "8주", label: "스프린트 개발 기간" },
  { value: "5개", label: "동시 지원 통역 언어" },
  { value: "RAG", label: "문서 검색·추천 구조" },
] as const;

export function StatsStrip(): ReactElement {
  return (
    <section id="project" className="border-y border-line bg-card px-5 py-14">
      <div className="mx-auto grid max-w-[1120px] grid-cols-2 gap-8 mid:grid-cols-4">
        {STATS.map((item) => (
          <div key={item.label}>
            <p className="m-0 text-[32px] font-semibold tracking-tight text-brand">
              {item.value}
            </p>
            <p className="mt-1.5 text-[14px] text-ink-soft">{item.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
