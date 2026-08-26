export function coreApiUrl(): string {
  return (import.meta.env.VITE_CORE_API_URL ?? "").trim();
}

export function isCoreApiConfigured(): boolean {
  return coreApiUrl().length > 0;
}
