/**
 * Authentication service and token management.
 *
 * TOKEN STORAGE ARCHITECTURE & SECURITY TRADEOFF:
 * ------------------------------------------------
 * The short-lived JWT access token is stored in `sessionStorage`.
 *
 * Tradeoff:
 * - It remains accessible to JavaScript in this origin, so CSP and XSS prevention matter.
 * - It is cleared when the browser tab session ends. Bearer headers avoid cookie CSRF.
 *
 * No refresh token is issued. Expired access tokens require a fresh login.
 */

import { TokenResponse, User } from "@/types";
import { apiFetch } from "./api";

const TOKEN_KEY = "ssc_prep_access_token";
const USER_KEY = "ssc_prep_session_user";

export function getCachedUser(): User | null {
  try {
    const value = sessionStorage.getItem(USER_KEY);
    if (!value) return null;
    const user = JSON.parse(value) as User;
    return user && typeof user.id === "string" && typeof user.email === "string" ? user : null;
  } catch {
    return null;
  }
}

function cacheUser(user: User): void {
  try { sessionStorage.setItem(USER_KEY, JSON.stringify(user)); } catch { /* Cache is optional. */ }
}

/**
 * Retrieve the active access token from storage.
 */
export function getToken(): string | null {
  try {
    const sessionToken = sessionStorage.getItem(TOKEN_KEY);
    if (sessionToken) return sessionToken;
    const legacyToken = localStorage.getItem(TOKEN_KEY);
    if (legacyToken) {
      sessionStorage.setItem(TOKEN_KEY, legacyToken);
      localStorage.removeItem(TOKEN_KEY);
      return legacyToken;
    }
    return null;
  } catch {
    return null;
  }
}

/**
 * Persist the access token to storage.
 */
export function setToken(token: string): void {
  try {
    sessionStorage.setItem(TOKEN_KEY, token);
  } catch {
    console.warn("The sign-in session could not be stored in this browser tab.");
  }
}

/**
 * Clear the stored access token.
 */
export function removeToken(): void {
  try {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
    localStorage.removeItem(TOKEN_KEY);
  } catch {
    // Storage may be blocked by browser policy.
  }
}

export interface RegisterPayload {
  full_name: string;
  email: string;
  password: string;
  invitation_code?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

/**
 * Register a new user account.
 * Endpoint: POST /api/auth/register
 */
export async function register(payload: RegisterPayload): Promise<User> {
  return apiFetch<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * Authenticate existing user and obtain access token.
 * Endpoint: POST /api/auth/login
 */
export async function login(payload: LoginPayload): Promise<TokenResponse> {
  const response = await apiFetch<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  setToken(response.access_token);
  cacheUser(response.user);
  return response;
}

/**
 * Fetch authenticated user profile.
 * Endpoint: GET /api/auth/me
 */
export async function getCurrentUser(): Promise<User> {
  const token = getToken();
  if (!token) {
    throw new Error("No authentication token present");
  }
  return apiFetch<User>("/auth/me", {
    method: "GET",
    token,
  });
}

/**
 * Log out user by removing token from storage.
 */
export function logout(): void {
  removeToken();
}
