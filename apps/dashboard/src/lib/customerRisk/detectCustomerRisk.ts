/**
 * C-6 mock. 고객 발화 텍스트만 본다.
 * 키워드·정규식은 자리표시자다. 실제 모델이 오면 이 함수만 갈아끼운다.
 */
export type CustomerRiskType = "abuse" | "distress" | "pii";

export interface CustomerRiskMatch {
  type: CustomerRiskType;
  matchedText: string;
  startIndex: number;
  endIndex: number;
}

export type BannerRiskMatch = CustomerRiskMatch & {
  type: "abuse" | "distress";
};

const ABUSE = ["가만 안 둔다", "죽여버린다"] as const;
const DISTRESS = ["너무 힘들어요", "죽고 싶어요"] as const;
const PII_RRN = /\d{6}-\d{7}/g;

function collectPhrases(
  text: string,
  type: CustomerRiskType,
  phrases: readonly string[],
): CustomerRiskMatch[] {
  const found: CustomerRiskMatch[] = [];
  for (const phrase of phrases) {
    let from = 0;
    while (from <= text.length) {
      const startIndex = text.indexOf(phrase, from);
      if (startIndex === -1) {
        break;
      }
      found.push({
        type,
        matchedText: phrase,
        startIndex,
        endIndex: startIndex + phrase.length,
      });
      from = startIndex + phrase.length;
    }
  }
  return found;
}

export function detectCustomerRisk(text: string): CustomerRiskMatch[] {
  const pii: CustomerRiskMatch[] = [];
  for (const hit of text.matchAll(PII_RRN)) {
    const startIndex = hit.index ?? 0;
    const matchedText = hit[0];
    pii.push({
      type: "pii",
      matchedText,
      startIndex,
      endIndex: startIndex + matchedText.length,
    });
  }
  return [
    ...collectPhrases(text, "abuse", ABUSE),
    ...collectPhrases(text, "distress", DISTRESS),
    ...pii,
  ];
}
