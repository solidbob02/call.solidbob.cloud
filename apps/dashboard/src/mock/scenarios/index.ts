import { accentKoScenario } from "./accentKo";
import { adminThScenario } from "./adminTh";
import { callGuardKoScenario } from "./callGuardKo";
import { covidZhScenario } from "./covidZh";
import { dasanScenario, maskingKoScenario } from "./dasan";
import { sewerJaScenario } from "./sewerJa";
import { transitEnScenario } from "./transitEn";
import type { MockScenario } from "./types";

export type { MockScenario } from "./types";

/** mock 재생용. 게이트웨이 계약이 아니다. */
export type MockScenarioId =
  | "vi-deungbon"
  | "en-transit"
  | "ja-sewer"
  | "zh-covid"
  | "th-admin"
  | "ko-masking"
  | "ko-callguard"
  | "ko-accent";

const BY_ID: Record<MockScenarioId, MockScenario> = {
  "vi-deungbon": dasanScenario,
  "en-transit": transitEnScenario,
  "ja-sewer": sewerJaScenario,
  "zh-covid": covidZhScenario,
  "th-admin": adminThScenario,
  "ko-masking": maskingKoScenario,
  "ko-callguard": callGuardKoScenario,
  "ko-accent": accentKoScenario,
};

let selectedId: MockScenarioId = "vi-deungbon";

export function setSelectedMockScenarioId(id: MockScenarioId): void {
  selectedId = id;
}

export function getScenario(): MockScenario {
  return BY_ID[selectedId];
}

export function getScenarioById(id: MockScenarioId): MockScenario {
  return BY_ID[id];
}

export const MOCK_SCENARIO_FLAG: Record<MockScenarioId, string> = {
  "vi-deungbon": "🇻🇳",
  "en-transit": "🇺🇸",
  "ja-sewer": "🇯🇵",
  "zh-covid": "🇨🇳",
  "th-admin": "🇹🇭",
  "ko-masking": "🇰🇷",
  "ko-callguard": "🇰🇷",
  "ko-accent": "🇰🇷",
};
