/**
 * Authenticated dashboard placeholder page.
 * Full analytics, question bank, and exam selection logic will be added in later stages.
 */

import React from "react";
import { useAuth } from "@/hooks";

export const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <div className="flex flex-col items-center justify-center py-8">
      <div className="w-full max-w-card rounded-xl bg-card p-8 shadow-sm border border-gray-100">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-gray-100 pb-6 gap-4">
          <div>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-correct mb-2">
              <span className="h-1.5 w-1.5 rounded-full bg-correct"></span>
              Authenticated Session
            </span>
            <h2 className="text-2xl font-bold text-content">
              Welcome back, {user?.full_name || user?.email}!
            </h2>
            <p className="text-sm text-gray-500 mt-1">{user?.email}</p>
          </div>
          <button
            type="button"
            onClick={logout}
            className="self-start sm:self-center rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-content hover:bg-gray-50 transition cursor-pointer"
          >
            Sign Out
          </button>
        </div>

        <div className="mt-6 space-y-4">
          <div className="rounded-lg bg-primary-50 p-4 border border-primary/20">
            <h3 className="font-semibold text-primary text-sm mb-1">
              Stage 3 — Authentication Active
            </h3>
            <p className="text-sm text-content leading-relaxed">
              You are currently logged in through secure JWT authentication with Argon2id password hashing.
              This dashboard will host full mock tests, subject selections, test timers, and score reports in upcoming stages.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
            <div className="rounded-lg border border-gray-100 p-4 bg-gray-50/50">
              <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Account ID</span>
              <p className="font-mono text-xs text-gray-700 mt-1 truncate">{user?.id}</p>
            </div>
            <div className="rounded-lg border border-gray-100 p-4 bg-gray-50/50">
              <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Status</span>
              <p className="text-sm font-medium text-correct mt-1">
                {user?.is_active ? "Active Aspirant" : "Inactive"}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
