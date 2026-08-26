import { MockGatewayClient } from "../../mock/mockGateway";
import { RealGatewayClient } from "./realGatewayClient";
import { gatewayUrl, isLiveGatewayConfigured } from "./types";
import type { GatewayClient } from "./types";
import type { DemoDomain } from "../../types/contract";

export type { GatewayClient, GatewayListener, GatewayMode, GatewayStatus } from "./types";
export { gatewayUrl, isLiveGatewayConfigured } from "./types";

export function createGatewayClient(domain: DemoDomain = "finance"): GatewayClient {
  if (isLiveGatewayConfigured()) {
    return new RealGatewayClient(gatewayUrl());
  }
  return new MockGatewayClient(domain);
}
