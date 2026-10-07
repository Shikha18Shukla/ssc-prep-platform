/**
 * API client configuration and base service functions.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL ?? "/api";

export class ApiError extends Error {
  public status: number;
  public detail: string | unknown;

  constructor(status: number, message: string, detail: string | unknown = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

interface ApiOptions extends RequestInit {
  params?: Record<string, string>;
  token?: string | null;
}

/**
 * Base fetch wrapper with error parsing, token injection, and JSON serialization.
 */
export async function apiFetch<T>(
  endpoint: string,
  options: ApiOptions = {},
): Promise<T> {
  const { params, token, ...fetchOptions } = options;

  const url = new URL(`${API_BASE_URL}${endpoint}`, window.location.origin);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, value);
    });
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((fetchOptions.headers as Record<string, string>) || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let response: Response;
  try {
    response = await fetch(url.toString(), {
      ...fetchOptions,
      headers,
    });
  } catch (error) {
    throw new ApiError(
      0,
      "Unable to connect to the server. Please check your internet connection.",
      error,
    );
  }

  if (!response.ok) {
    let errorDetail = "";
    try {
      const errJson = await response.json();
      if (typeof errJson.detail === "string") {
        errorDetail = errJson.detail;
      } else if (Array.isArray(errJson.detail)) {
        // Pydantic 422 validation errors
        errorDetail = errJson.detail.map((d: { msg: string }) => d.msg).join(", ");
      } else if (errJson.message) {
        errorDetail = errJson.message;
      }
    } catch {
      errorDetail = `${response.status} ${response.statusText}`;
    }

    throw new ApiError(
      response.status,
      errorDetail || `Request failed with status ${response.status}`,
    );
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
