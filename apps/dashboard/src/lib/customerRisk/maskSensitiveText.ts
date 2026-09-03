import type { CustomerRiskMatch } from "./detectCustomerRisk";

/**
 * PII 구간만 가린다. 주민번호는 하이픈 뒤를 • 로 바꾼다.
 * 원문 숫자는 화면에 남기지 않는다.
 */
export function maskSensitiveText(
  text: string,
  matches: readonly CustomerRiskMatch[],
): string {
  const pii = [...matches]
    .filter((item) => item.type === "pii")
    .sort((a, b) => b.startIndex - a.startIndex);
  let next = text;
  for (const hit of pii) {
    const slice = next.slice(hit.startIndex, hit.endIndex);
    const dash = slice.indexOf("-");
    const masked =
      dash === -1
        ? "•".repeat([...slice].length)
        : `${slice.slice(0, dash + 1)}${"•".repeat([...slice.slice(dash + 1)].length)}`;
    next = `${next.slice(0, hit.startIndex)}${masked}${next.slice(hit.endIndex)}`;
  }
  return next;
}
