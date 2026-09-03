import type { ReactElement } from "react";

export function CTASection(): ReactElement {
  return (
    <section id="cta" className="bg-bg px-5 py-20">
      <div className="mx-auto grid max-w-[1120px] grid-cols-1 items-center gap-8 rounded-[16px] bg-linear-to-br from-brand-deep via-brand to-brand-bright px-8 py-10 text-white mid:grid-cols-2 mid:px-12">
        <div>
          <h2 className="m-0 text-[clamp(22px,3vw,30px)] font-semibold tracking-tight">
            통화가 끝난 뒤가 아니라, 통화 중에 문서를 엽니다.
          </h2>
          <p className="mt-4 m-0 text-[15px] leading-relaxed text-white/80">
            SOLIDBOB 4인이 8주 스프린트로 만드는 다산콜센터 상담사 어시스트입니다.
            기능과 흐름을 다시 보고 가실 수 있습니다.
          </p>
        </div>
        <div className="flex flex-wrap gap-3 mid:justify-end">
          <a
            href="#features"
            className="rounded-[10px] bg-white px-4 py-2.5 text-[14px] font-semibold text-brand-deep"
          >
            핵심 기능 다시 보기
          </a>
          <a
            href="#how"
            className="rounded-[10px] border border-white/35 px-4 py-2.5 text-[14px] font-semibold text-white"
          >
            작동 방식 다시 보기
          </a>
        </div>
      </div>
    </section>
  );
}
