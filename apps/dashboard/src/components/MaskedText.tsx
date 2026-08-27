import type { ReactElement } from "react";
import type { MaskedSpan } from "../types/contract";
import { buildTextRuns, type CharRange } from "../lib/text/highlight";

interface MaskedTextProps {
  text: string;
  masked: MaskedSpan[];
  hits?: CharRange[];
  activeHit?: CharRange | null;
}

export function MaskedText({
  text,
  masked,
  hits = [],
  activeHit = null,
}: MaskedTextProps): ReactElement {
  if (masked.length === 0 && hits.length === 0) {
    return <span>{text}</span>;
  }

  const runs = buildTextRuns(text, masked, hits, activeHit);

  return (
    <>
      {runs.map((run, index) => {
        if (!run.masked && !run.hit) {
          return <span key={index}>{run.text}</span>;
        }
        const classes = [
          run.masked ? "masked-span" : "",
          run.hit ? "search-hit" : "",
          run.active ? "is-active" : "",
        ]
          .filter((name) => name.length > 0)
          .join(" ");
        return (
          <mark key={index} className={classes}>
            {run.text}
          </mark>
        );
      })}
    </>
  );
}
