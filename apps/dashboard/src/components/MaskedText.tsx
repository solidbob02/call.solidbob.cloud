import type { ReactElement } from "react";
import type { MaskedSpan } from "../types/contract";
import { sliceByCodepoints } from "../lib/text/codepoints";

interface MaskedTextProps {
  text: string;
  masked: MaskedSpan[];
}

export function MaskedText({ text, masked }: MaskedTextProps): ReactElement {
  const chars = Array.from(text);
  if (masked.length === 0) {
    return <span>{text}</span>;
  }

  const ranges = [...masked].sort((a, b) => a.span[0] - b.span[0]);
  const parts: ReactElement[] = [];
  let cursor = 0;

  ranges.forEach((mask, index) => {
    const start = Math.max(0, mask.span[0]);
    const end = Math.min(chars.length, mask.span[1]);
    if (start > cursor) {
      parts.push(
        <span key={`t-${index}`}>{sliceByCodepoints(text, cursor, start)}</span>,
      );
    }
    if (end > start) {
      parts.push(
        <mark key={`m-${index}`} className="masked-span">
          {sliceByCodepoints(text, start, end)}
        </mark>,
      );
    }
    cursor = Math.max(cursor, end);
  });

  if (cursor < chars.length) {
    parts.push(<span key="tail">{sliceByCodepoints(text, cursor, chars.length)}</span>);
  }

  return <>{parts}</>;
}
