/** Finalizes a Google sign-in after the backend-validated OAuth callback. */

import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";

export const GoogleCallbackPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { completeGoogleSignIn } = useAuth();
  const started = useRef(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (started.current) return;
    started.current = true;

    const code = searchParams.get("code");
    if (!code) {
      setError("Google sign-in was not completed. Please try again.");
      return;
    }

    void (async () => {
      try {
        await completeGoogleSignIn(code);
        navigate("/dashboard", { replace: true });
      } catch (err) {
        setError(
          err instanceof ApiError
            ? (typeof err.detail === "string" ? err.detail : err.message)
            : "Google sign-in could not be completed. Please try again.",
        );
      }
    })();
  }, [searchParams, completeGoogleSignIn, navigate]);

  return (
    <div className="flex min-h-[75vh] items-center justify-center py-6 px-4">
      <div className="w-full max-w-md rounded-xl bg-card p-8 text-center shadow-sm border border-gray-100">
        {error ? (
          <>
            <h2 className="text-xl font-bold text-content">Sign-in incomplete</h2>
            <p className="mt-3 text-sm text-wrong" role="alert">{error}</p>
            <Link
              to="/login"
              className="mt-6 inline-block font-semibold text-primary hover:underline"
            >
              Back to sign in
            </Link>
          </>
        ) : (
          <>
            <div className="mx-auto h-9 w-9 animate-spin rounded-full border-4 border-primary border-t-transparent" />
            <h2 className="mt-5 text-xl font-bold text-content">Finishing Google sign-in</h2>
            <p className="mt-2 text-sm text-gray-500">Do not close this tab.</p>
          </>
        )}
      </div>
    </div>
  );
};
