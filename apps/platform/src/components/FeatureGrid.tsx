import type { ReactElement } from "react";

const FEATURES = [
  {
    wide: true,
    title: "실시간 문서 추천",
    body: "유사도 점수와 함께 카드를 자동으로 띄웁니다. 문서가 없으면 「관련 문서 없음」을 분명히 표시합니다.",
    tags: ["B-5", "B-6"],
    tone: "teal" as const,
  },
  {
    wide: false,
    title: "컴플라이언스 가드",
    body: "부적절 표현을 감지하면 경고와 권장 대체 표현을 같이 보여 줍니다.",
    tags: ["C-1~C-4"],
    tone: "amber" as const,
  },
  {
    wide: false,
    title: "5개 언어 동시 통번역",
    body: "외국인 민원인 발화를 상담사 화면에 한글로 같이 띄웁니다.",
    tags: ["A-5"],
    tone: "teal" as const,
  },
  {
    wide: false,
    title: "필요서류 체크리스트",
    body: "민원 유형별로 제출 서류를 빠짐없이 안내합니다. 하나라도 빠지면 완료 처리가 열리지 않습니다.",
    tags: ["F-2"],
    tone: "brand" as const,
  },
  {
    wide: true,
    title: "통화 후 자동 요약",
    body: "요약, 유형 분류, 후속 조치까지 정리합니다. 상담사가 확인하고 남깁니다.",
    tags: ["D-1~D-4", "G-2"],
    tone: "brand" as const,
  },
] as const;

export function FeatureGrid(): ReactElement {
  return (
    <section id="features" className="bg-bg px-5 pb-20">
      <div className="mx-auto max-w-[1120px]">
        <p className="mb-3 text-[13px] font-semibold text-brand">핵심 기능</p>
        <h2 className="m-0 max-w-[16em] text-[clamp(22px,3vw,32px)] font-semibold tracking-tight">
          통화가 이어지는 동안, 화면이 같이 일합니다
        </h2>
        <ul className="mt-10 grid list-none grid-cols-1 gap-4 p-0 mid:grid-cols-4">
          {FEATURES.map((item) => (
            <li
              key={item.title}
              className={`rounded-[16px] border border-line bg-card p-6 shadow-[0_8px_28px_rgba(22,27,46,0.06)] ${
                item.wide ? "mid:col-span-2" : "mid:col-span-1"
              }`}
            >
              <span
                className={`mb-4 flex h-[42px] w-[42px] items-center justify-center rounded-[10px] ${iconWrap[item.tone]}`}
                aria-hidden="true"
              >
                <FeatureMark tone={item.tone} />
              </span>
              <h3 className="m-0 text-[17px] font-semibold">{item.title}</h3>
              <p className="mt-2 mb-5 text-[14px] leading-relaxed text-ink-soft">
                {item.body}
              </p>
              <div className="flex flex-wrap gap-1.5">
                {item.tags.map((tag) => (
                  <span
                    key={tag}
                    className="rounded-full bg-bg px-2.5 py-1 text-[11px] font-semibold text-ink-soft"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

const iconWrap = {
  teal: "bg-teal-bg text-teal",
  amber: "bg-amber-bg text-amber",
  brand: "bg-bg text-brand",
} as const;

function FeatureMark({
  tone,
}: {
  tone: "teal" | "amber" | "brand";
}): ReactElement {
  if (tone === "amber") {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 9v4M12 17h.01M10.3 4.7 2.8 17.5A2 2 0 0 0 4.5 20.5h15a2 2 0 0 0 1.7-3L13.7 4.7a2 2 0 0 0-3.4 0Z" />
      </svg>
    );
  }
  if (tone === "brand") {
    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" />
      </svg>
    );
  }
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M4 19V5h10l6 6v8H4Z" />
      <path d="M14 5v6h6" />
    </svg>
  );
}
