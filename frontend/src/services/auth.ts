/**
 * Authentication service and token management.
 *
 * TOKEN STORAGE ARCHITECTURE & SECURITY TRADEOFF:
 * ------------------------------------------------
 * The short-lived JWT access token is stored in `sessionStorage`.
 *
 * Tradeoff:
 * - It remains accessible to JavaScript in this origin, so CSP and XSS prevention matter.
 * - It is cleared when the browser tab session ends. Bearer headers avoid CSRF for API calls.
 *
 * No refresh token is issued. Expired access tokens require a fresh sign-in.
 * The Google state cookie is HttpOnly and used only for the OAuth callback.
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
  try {
    sessionStorage.setItem(USER_KEY, JSON.stringify(user));
  } catch {
    /* Cache is optional. */
  }
}

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

export function setToken(token: string): void {
  try {
    sessionStorage.setItem(TOKEN_KEY, token);
  } catch {
    console.warn("The sign-in session could not be stored in this browser tab.");
  }
}

export function removeToken(): void {
  try {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
    localStorage.removeItem(TOKEN_KEY);
  } catch {
    // Storage may be blocked by browser policy.
  }
}

function storeSession(response: TokenResponse): TokenResponse {
  setToken(response.access_token);
  cacheUser(response.user);
  return response;
}

export interface RegisterPayload {
  full_name: string;
  email: string;
  password: string;
  confirm_password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface GoogleStartResponse {
  authorization_url: string;
}

export interface MessageResponse {
  message: string;
}

export async function register(payload: RegisterPayload): Promise<TokenResponse> {
  return storeSession(await apiFetch<TokenResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  }));
}

export async function login(payload: LoginPayload): Promise<TokenResponse> {
  return storeSession(await apiFetch<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  }));
}

export async function getCurrentUser(): Promise<User> {
  const token = getToken();
  if (!token) {
    throw new Error("No authentication token present");
  }
  return apiFetch<User>("/auth/me", { method: "GET", token });
}

export async function logout(): Promise<void> {
  const token = getToken();
  removeToken();
  if (!token) return;
  try {
    await apiFetch<MessageResponse>("/auth/logout", {
      method: "POST",
      token,
    });
  } catch {
    // Local sign-out must always succeed even when the server is unreachable.
  }
}

export async function startGoogleSignIn(): Promise<string> {
  const response = await apiFetch<GoogleStartResponse>("/auth/google/start", {
    method: "GET",
    credentials: "include",
  });
  return response.authorization_url;
}

export async function exchangeGoogleCode(code: string): Promise<TokenResponse> {
  return storeSession(await apiFetch<TokenResponse>("/auth/google/exchange", {
    method: "POST",
    credentials: "include",
    body: JSON.stringify({ code }),
  }));
}

export async function requestPasswordReset(email: string): Promise<MessageResponse> {
  return apiFetch<MessageResponse>("/auth/password-reset/request", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function confirmPasswordReset(
  token: string,
  new_password: string,
  confirm_password: string,
): Promise<TokenResponse> {
  return storeSession(await apiFetch<TokenResponse>("/auth/password-reset/confirm", {
    method: "POST",
    body: JSON.stringify({ token, new_password, confirm_password }),
  }));
}
