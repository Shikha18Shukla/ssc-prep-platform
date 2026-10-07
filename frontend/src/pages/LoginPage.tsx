/**
 * User login page.
 */

import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showForgotNotice, setShowForgotNotice] = useState(false);

  // Field validation errors
  const [fieldErrors, setFieldErrors] = useState<{
    email?: string;
    password?: string;
  }>({});

  const validate = (): boolean => {
    const errors: { email?: string; password?: string } = {};

    if (!email.trim()) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = "Please enter a valid email address";
    }

    if (!password) {
      errors.password = "Password is required";
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await login({
        email: email.trim().toLowerCase(),
        password,
      });

      // Redirect to the intended destination or default to /dashboard
      const from = (location.state as { from?: { pathname: string } })?.from?.pathname || "/dashboard";
      navigate(from, { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMessage(typeof err.detail === "string" ? err.detail : err.message);
      } else {
        setErrorMessage("An unexpected error occurred. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
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

        {errorMessage && (
          <div className="mb-6 rounded-lg bg-red-50 p-4 border border-wrong/20 text-sm text-wrong">
            <div className="flex items-center gap-2">
              <svg className="h-5 w-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <span>{errorMessage}</span>
            </div>
          </div>
        )}

        {showForgotNotice && (
          <div className="mb-6 rounded-lg bg-blue-50 p-3 border border-primary/20 text-xs text-primary flex items-center justify-between">
            <span>Password reset functionality is Coming Soon.</span>
            <button
              type="button"
              onClick={() => setShowForgotNotice(false)}
              className="text-gray-400 hover:text-gray-600 font-bold ml-2"
            >
              &times;
            </button>
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
              onChange={(e) => setEmail(e.target.value)}
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
              <button
                type="button"
                onClick={() => setShowForgotNotice(true)}
                className="text-xs font-medium text-primary hover:underline"
              >
                Forgot password?
              </button>
            </div>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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
            disabled={isSubmitting}
            className="w-full rounded-lg bg-primary py-2.5 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:opacity-60 cursor-pointer"
          >
            {isSubmitting ? "Signing in..." : "Sign In"}
          </button>
        </form>

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
