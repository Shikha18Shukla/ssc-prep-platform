/**
 * User signup/registration page.
 */

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";

export const SignupPage: React.FC = () => {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Field-level validation errors
  const [fieldErrors, setFieldErrors] = useState<{
    fullName?: string;
    email?: string;
    password?: string;
    confirmPassword?: string;
  }>({});

  const validate = (): boolean => {
    const errors: {
      fullName?: string;
      email?: string;
      password?: string;
      confirmPassword?: string;
    } = {};

    if (!fullName.trim()) {
      errors.fullName = "Full name is required";
    }

    if (!email.trim()) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = "Please enter a valid email address";
    }

    if (!password) {
      errors.password = "Password is required";
    } else if (password.length < 8) {
      errors.password = "Password must be at least 8 characters long";
    } else if (!/[A-Za-z]/.test(password)) {
      errors.password = "Password must contain at least one letter";
    } else if (!/\d/.test(password)) {
      errors.password = "Password must contain at least one number";
    }

    if (!confirmPassword) {
      errors.confirmPassword = "Confirm password is required";
    } else if (confirmPassword !== password) {
      errors.confirmPassword = "Passwords do not match";
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
      await register({
        full_name: fullName.trim(),
        email: email.trim().toLowerCase(),
        password,
      });

      // Redirect immediately to dashboard upon successful registration & login
      navigate("/dashboard", { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMessage(typeof err.detail === "string" ? err.detail : err.message);
      } else {
        setErrorMessage("An unexpected error occurred during signup. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-[75vh] items-center justify-center py-6 px-4">
      <div className="w-full max-w-md rounded-xl bg-card p-8 shadow-sm border border-gray-100">
        <div className="mb-6 text-center">
          <h2 className="text-2xl font-bold text-content">Create an account</h2>
          <p className="mt-2 text-sm text-gray-500">
            Start your personalized SSC exam preparation journey.
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

        <form onSubmit={handleSubmit} className="space-y-4" noValidate>
          <div>
            <label htmlFor="fullName" className="block text-sm font-medium text-content mb-1">
              Full Name
            </label>
            <input
              id="fullName"
              type="text"
              autoComplete="name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className={`w-full rounded-lg border px-3.5 py-2.5 text-content text-sm transition focus:outline-none focus:ring-2 ${
                fieldErrors.fullName
                  ? "border-wrong focus:ring-wrong/20"
                  : "border-gray-300 focus:border-primary focus:ring-primary/20"
              }`}
              placeholder="e.g. Rahul Sharma"
            />
            {fieldErrors.fullName && (
              <p className="mt-1 text-xs text-wrong">{fieldErrors.fullName}</p>
            )}
          </div>

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
            <label htmlFor="password" className="block text-sm font-medium text-content mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={`w-full rounded-lg border px-3.5 py-2.5 text-content text-sm transition focus:outline-none focus:ring-2 ${
                fieldErrors.password
                  ? "border-wrong focus:ring-wrong/20"
                  : "border-gray-300 focus:border-primary focus:ring-primary/20"
              }`}
              placeholder="At least 8 characters (letters and numbers)"
            />
            {fieldErrors.password && (
              <p className="mt-1 text-xs text-wrong">{fieldErrors.password}</p>
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
              onChange={(e) => setConfirmPassword(e.target.value)}
              className={`w-full rounded-lg border px-3.5 py-2.5 text-content text-sm transition focus:outline-none focus:ring-2 ${
                fieldErrors.confirmPassword
                  ? "border-wrong focus:ring-wrong/20"
                  : "border-gray-300 focus:border-primary focus:ring-primary/20"
              }`}
              placeholder="Re-enter password"
            />
            {fieldErrors.confirmPassword && (
              <p className="mt-1 text-xs text-wrong">{fieldErrors.confirmPassword}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full mt-2 rounded-lg bg-primary py-2.5 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:opacity-60 cursor-pointer"
          >
            {isSubmitting ? "Creating account..." : "Sign Up"}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-500">
          Already have an account?{" "}
          <Link to="/login" className="font-semibold text-primary hover:underline">
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
};
