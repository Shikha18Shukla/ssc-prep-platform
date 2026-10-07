/**
 * API client configuration and service functions.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "/api";

interface ApiOptions extends RequestInit {
  params?: Record<string, string>;
}

/**
 * Base fetch wrapper with common configuration.
 */
export async function apiFetch<T>(
  endpoint: string,
  options: ApiOptions = {},
): Promise<T> {
  const { params, ...fetchOptions } = options;

  const url = new URL(`${API_BASE_URL}${endpoint}`, window.location.origin);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, value);
    });
  }

  const response = await fetch(url.toString(), {
    ...fetchOptions,
    headers: {
      "Content-Type": "application/json",
      ...fetchOptions.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

/**
 * Health check — verify API connectivity.
 */
export async function checkHealth(): Promise<{
  status: string;
  service: string;
  version: string;
}> {
  return apiFetch("/health");
}
