/**
 * Authentication service and token management.
 *
 * TOKEN STORAGE ARCHITECTURE & SECURITY TRADEOFF:
 * ------------------------------------------------
 * In this initial implementation, the JWT access token is stored in `localStorage`.
 *
 * Tradeoff:
 * - `localStorage` is accessible to JavaScript running on the same origin, which makes
 *   it potentially susceptible to Cross-Site Scripting (XSS) attacks if malicious script
 *   injection is allowed.
 * - However, it enables simple cross-subdomain API access, stateless client routing,
 *   and straightforward Bearer token authentication without CSRF complications.
 *
 * Future Migration Path to HttpOnly Cookies:
 * - All token read/write logic is isolated within `getToken()`, `setToken()`, and `removeToken()`.
 * - When transitioning to production server-side HttpOnly cookies in a later stage,
 *   these client storage helpers can be updated to no-ops or delegate to cookie headers,
 *   requiring zero refactoring across application components or pages.
 */

import { TokenResponse, User } from "@/types";
import { apiFetch } from "./api";

const TOKEN_KEY = "ssc_prep_access_token";

/**
 * Retrieve the active access token from storage.
 */
export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

/**
 * Persist the access token to storage.
 */
export function setToken(token: string): void {
  try {
    localStorage.setItem(TOKEN_KEY, token);
  } catch (err) {
    console.error("Failed to persist token to storage", err);
  }
}

/**
 * Clear the stored access token.
 */
export function removeToken(): void {
  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch (err) {
    console.error("Failed to clear token from storage", err);
  }
}

export interface RegisterPayload {
  full_name: string;
  email: string;
  password: string;
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
