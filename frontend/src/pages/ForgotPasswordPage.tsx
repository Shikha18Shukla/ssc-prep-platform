/** Password setup/recovery request page. */

import React, { useState } from "react";
import { Link } from "react-router-dom";
import { ApiError } from "@/services/api";
import { requestPasswordReset } from "@/services/auth";

export const ForgotPasswordPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [fieldError, setFieldError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage(null);
    setError(null);
    if (isSubmitting) return;

    const normalized = email.trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalized)) {
      setFieldError("Please enter a valid email address");
      return;
    }
    setFieldError(null);
    setIsSubmitting(true);
    try {
      const response = await requestPasswordReset(normalized);
      setMessage(response.message);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? (typeof err.detail === "string" ? err.detail : err.message)
          : "Password setup could not be requested. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-[75vh] items-center justify-center py-6 px-4">
      <div className="w-full max-w-md rounded-xl bg-card p-8 shadow-sm border border-gray-100">
        <div className="mb-6 text-center">
          <h2 className="text-2xl font-bold text-content">Set or reset your password</h2>
          <p className="mt-2 text-sm text-gray-500">
            Enter your account email. We only send a link when email delivery is configured.
          </p>
        </div>

        {message && (
          <div className="mb-5 rounded-lg bg-blue-50 p-4 border border-primary/20 text-sm text-primary" role="status">
            {message}
          </div>
        )}
        {error && (
          <div className="mb-5 rounded-lg bg-red-50 p-4 border border-wrong/20 text-sm text-wrong" role="alert">
            {error}
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
                fieldError
                  ? "border-wrong focus:ring-wrong/20"
                  : "border-gray-300 focus:border-primary focus:ring-primary/20"
              }`}
              placeholder="name@example.com"
            />
            {fieldError && <p className="mt-1 text-xs text-wrong">{fieldError}</p>}
          </div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-lg bg-primary py-2.5 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:opacity-60 cursor-pointer"
          >
            {isSubmitting ? "Requesting..." : "Request password link"}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-500">
          <Link to="/login" className="font-semibold text-primary hover:underline">
            Back to sign in
          </Link>
        </div>
      </div>
    </div>
  );
};
