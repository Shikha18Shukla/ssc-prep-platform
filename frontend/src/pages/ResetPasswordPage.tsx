/** Single-use password setup/recovery confirmation page. */

import React, { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";

interface FieldErrors {
  newPassword?: string;
  confirmPassword?: string;
}

export const ResetPasswordPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { completePasswordReset } = useAuth();
  const token = searchParams.get("token") ?? "";

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = (): boolean => {
    const errors: FieldErrors = {};
    if (newPassword.length < 8) {
      errors.newPassword = "Password must be at least 8 characters long";
    } else if (!/[A-Za-z]/.test(newPassword)) {
      errors.newPassword = "Password must contain at least one letter";
    } else if (!/\d/.test(newPassword)) {
      errors.newPassword = "Password must contain at least one number";
    }
    if (!confirmPassword) {
      errors.confirmPassword = "Confirm password is required";
    } else if (confirmPassword !== newPassword) {
      errors.confirmPassword = "Passwords do not match";
    }
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    if (isSubmitting || !token || !validate()) return;

    setIsSubmitting(true);
    try {
      await completePasswordReset(token, newPassword, confirmPassword);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(
        err instanceof ApiError
          ? (typeof err.detail === "string" ? err.detail : err.message)
          : "Password setup could not be completed. Please request a new link.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-[75vh] items-center justify-center py-6 px-4">
      <div className="w-full max-w-md rounded-xl bg-card p-8 shadow-sm border border-gray-100">
        <div className="mb-6 text-center">
          <h2 className="text-2xl font-bold text-content">Choose a new password</h2>
          <p className="mt-2 text-sm text-gray-500">
            This link is single-use and expires soon.
          </p>
        </div>

        {!token && (
          <div className="mb-5 rounded-lg bg-red-50 p-4 border border-wrong/20 text-sm text-wrong" role="alert">
            This password setup link is missing its token. Request a fresh link from the sign-in page.
          </div>
        )}
        {error && (
          <div className="mb-5 rounded-lg bg-red-50 p-4 border border-wrong/20 text-sm text-wrong" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5" noValidate>
          <div>
            <label htmlFor="newPassword" className="block text-sm font-medium text-content mb-1">
              New Password
            </label>
            <input
              id="newPassword"
              type="password"
              autoComplete="new-password"
              value={newPassword}
              onChange={(event) => setNewPassword(event.target.value)}
              className={`w-full rounded-lg border px-3.5 py-2.5 text-content text-sm transition focus:outline-none focus:ring-2 ${
                fieldErrors.newPassword
                  ? "border-wrong focus:ring-wrong/20"
                  : "border-gray-300 focus:border-primary focus:ring-primary/20"
              }`}
              placeholder="At least 8 characters (letters and numbers)"
            />
            {fieldErrors.newPassword && (
              <p className="mt-1 text-xs text-wrong">{fieldErrors.newPassword}</p>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-content mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              className={`w-full rounded-lg border px-3.5 py-2.5 text-content text-sm transition focus:outline-none focus:ring-2 ${
                fieldErrors.confirmPassword
                  ? "border-wrong focus:ring-wrong/20"
                  : "border-gray-300 focus:border-primary focus:ring-primary/20"
              }`}
              placeholder="Re-enter new password"
            />
            {fieldErrors.confirmPassword && (
              <p className="mt-1 text-xs text-wrong">{fieldErrors.confirmPassword}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting || !token}
            className="w-full rounded-lg bg-primary py-2.5 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:opacity-60 cursor-pointer"
          >
            {isSubmitting ? "Saving password..." : "Set password"}
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
