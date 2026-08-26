import type { DemoDomain } from "../../types/contract";
import { dasanScenario } from "./dasan";
import { financeScenario } from "./finance";
import { healthScenario } from "./health";
import { shoppingScenario } from "./shopping";
import type { MockScenario } from "./types";

export type { MockScenario } from "./types";

export function getScenario(domain: DemoDomain): MockScenario {
  switch (domain) {
    case "finance":
      return financeScenario;
    case "shopping":
      return shoppingScenario;
    case "dasan":
      return dasanScenario;
    case "health":
      return healthScenario;
  }
}
