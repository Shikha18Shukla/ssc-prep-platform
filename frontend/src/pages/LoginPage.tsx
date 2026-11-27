/**
 * User login page.
 */

import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { GoogleButton } from "@/components/common";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";

interface FieldErrors {
  email?: string;
  password?: string;
}

function errorMessage(err: unknown): string {
  if (err instanceof ApiError) {
    return typeof err.detail === "string" ? err.detail : err.message;
  }
  return "An unexpected error occurred. Please try again.";
}

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, startGoogleSignIn } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGoogleStarting, setIsGoogleStarting] = useState(false);
  const [errorMessageText, setErrorMessage] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});

  const validate = (): boolean => {
    const errors: FieldErrors = {};
    if (!email.trim()) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = "Please enter a valid email address";
    }
    if (!password) errors.password = "Password is required";
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setErrorMessage(null);
    if (isSubmitting || isGoogleStarting || !validate()) return;

    setIsSubmitting(true);
    try {
      await login({ email: email.trim().toLowerCase(), password });
      const from = (location.state as { from?: { pathname: string } })?.from?.pathname || "/dashboard";
      navigate(from, { replace: true });
    } catch (err) {
      setErrorMessage(errorMessage(err));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGoogle = async () => {
    if (isSubmitting || isGoogleStarting) return;
    setIsGoogleStarting(true);
    setErrorMessage(null);
    try {
      const url = await startGoogleSignIn();
      window.location.assign(url);
    } catch (err) {
      setErrorMessage(errorMessage(err));
      setIsGoogleStarting(false);
    }
  };

  return (
    <div className="flex min-h-[75vh] items-center justify-center py-6 px-4">
      <div className="w-full max-w-md rounded-xl bg-card p-8 shadow-sm border border-gray-100">
        <div className="mb-6 text-center">
          <h2 className="text-2xl font-bold text-content">Sign in to your account</h2>
          <p className="mt-2 text-sm text-gray-500">
            Welcome back! Continue your SSC exam preparation.
          </p>
        </div>

        {errorMessageText && (
          <div className="mb-6 rounded-lg bg-red-50 p-4 border border-wrong/20 text-sm text-wrong" role="alert">
            {errorMessageText}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5" noValidate>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-content mb-1">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className={`w-full rounded-lg border px-3.5 py-2.5 text-content text-sm transition focus:outline-none focus:ring-2 ${
                fieldErrors.email
                  ? "border-wrong focus:ring-wrong/20"
                  : "border-gray-300 focus:border-primary focus:ring-primary/20"
              }`}
              placeholder="name@example.com"
            />
            {fieldErrors.email && (
              <p className="mt-1 text-xs text-wrong">{fieldErrors.email}</p>
            )}
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label htmlFor="password" className="block text-sm font-medium text-content">
                Password
              </label>
              <Link
                to="/forgot-password"
                className="text-xs font-medium text-primary hover:underline"
              >
                Forgot password?
              </Link>
            </div>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className={`w-full rounded-lg border px-3.5 py-2.5 text-content text-sm transition focus:outline-none focus:ring-2 ${
                fieldErrors.password
                  ? "border-wrong focus:ring-wrong/20"
                  : "border-gray-300 focus:border-primary focus:ring-primary/20"
              }`}
              placeholder="••••••••"
            />
            {fieldErrors.password && (
              <p className="mt-1 text-xs text-wrong">{fieldErrors.password}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting || isGoogleStarting}
            className="w-full rounded-lg bg-primary py-2.5 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:opacity-60 cursor-pointer"
          >
            {isSubmitting ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <div className="my-5 flex items-center gap-3 text-xs text-gray-400">
          <span className="h-px flex-1 bg-gray-200" />
          OR
          <span className="h-px flex-1 bg-gray-200" />
        </div>
        <GoogleButton
          onClick={handleGoogle}
          disabled={isSubmitting}
          busy={isGoogleStarting}
        />

        <div className="mt-6 text-center text-sm text-gray-500">
          Don't have an account?{" "}
          <Link to="/signup" className="font-semibold text-primary hover:underline">
            Create an account
          </Link>
        </div>
      </div>
    </div>
  );
};
