import React, { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";
import {
  createGenericInvitationBatch,
  CreatedGenericInvitation,
  GenericInvitationRecord,
  GenericInvitationStatus,
  InvitationState,
  getGenericInvitationSummary,
  listGenericInvitations,
  revokeInvitation,
} from "@/services/adminInvitations";

const STATES: InvitationState[] = ["available", "redeemed", "expired", "revoked"];

function errorText(error: unknown): string {
  if (error instanceof ApiError && error.status === 403) return "Administrator access is required.";
  if (error instanceof ApiError && error.status === 409) return "The beta capacity is full or this code has already changed state.";
  return "The invitation request failed. Please retry or sign in again.";
}

function csvCell(value: string): string {
  return `"${value.replace(/"/g, '""')}"`;
}

export const AdminInvitationsPage: React.FC = () => {
  const { user, token } = useAuth();
  const [summary, setSummary] = useState<GenericInvitationStatus | null>(null);
  const [records, setRecords] = useState<GenericInvitationRecord[]>([]);
  const [filter, setFilter] = useState<InvitationState>("available");
  const [created, setCreated] = useState<CreatedGenericInvitation[]>([]);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!token) return;
    const [nextSummary, nextRecords] = await Promise.all([
      getGenericInvitationSummary(token),
      listGenericInvitations(token, filter),
    ]);
    setSummary(nextSummary);
    setRecords(nextRecords);
  }, [filter, token]);

  useEffect(() => {
    if (!user?.is_admin || !token) return;
    refresh().catch((err: unknown) => setError(errorText(err)));
  }, [refresh, token, user?.is_admin]);

  const generate = async () => {
    if (!token) return;
    setBusy(true);
    setError(null);
    setMessage(null);
    setCreated([]);
    try {
      const response = await createGenericInvitationBatch(token);
      setCreated(response.invitations);
      setMessage("50 codes created. Copy or download them now; the plaintext codes cannot be retrieved again.");
      await refresh();
    } catch (err) {
      setError(errorText(err));
    } finally {
      setBusy(false);
    }
  };

  const copyCodes = async () => {
    try {
      await navigator.clipboard.writeText(created.map((item) => item.invitation_code).join("\n"));
      setMessage("Invitation codes copied to the clipboard.");
    } catch {
      setError("Clipboard access was unavailable. Select and copy the codes from the table or download the CSV.");
    }
  };

  const downloadCodes = () => {
    const rows = [
      ["invitation_id", "invitation_code", "expires_at"].join(","),
      ...created.map((item) => [item.id, item.invitation_code, item.expires_at].map(csvCell).join(",")),
    ];
    const blob = new Blob([rows.join("\r\n")], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "ssc-beta-invitation-codes.csv";
    anchor.click();
    URL.revokeObjectURL(url);
  };

  const revoke = async (item: GenericInvitationRecord) => {
    if (!token || !window.confirm("Revoke this unused invitation code? It cannot be redeemed afterward.")) return;
    setBusy(true);
    setError(null);
    try {
      await revokeInvitation(token, item.id);
      await refresh();
    } catch (err) {
      setError(errorText(err));
    } finally {
      setBusy(false);
    }
  };

  if (!user?.is_admin) {
    return <div className="rounded-xl border border-gray-200 bg-card p-8 text-center">Administrator access is required.</div>;
  }

  return (
    <section className="mx-auto max-w-5xl space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-content">Beta invitations</h1>
        <p className="mt-2 text-sm text-gray-600">Create 50 email-independent codes in one action. Each code is single-use and expires in 14 days.</p>
      </header>

      {error && <p role="alert" className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">{error}</p>}
      {message && <p role="status" className="rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-800">{message}</p>}

      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {STATES.map((state) => (
          <div key={state} className="rounded-xl border border-gray-200 bg-card p-4">
            <div className="text-sm capitalize text-gray-500">{state}</div>
            <div className="mt-1 text-2xl font-semibold text-content">{summary?.[state] ?? "—"}</div>
          </div>
        ))}
      </div>

      <div className="rounded-xl border border-gray-200 bg-card p-5">
        <p className="text-sm text-gray-600">Capacity is reserved when codes are created. A batch is rejected if 50 slots are not available.</p>
        <button
          type="button"
          onClick={generate}
          disabled={busy}
          className="mt-4 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white hover:bg-primary-600 disabled:opacity-60"
        >
          {busy ? "Working…" : "Generate 50 codes"}
        </button>
      </div>

      {created.length > 0 && (
        <div className="rounded-xl border border-amber-300 bg-amber-50 p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="font-semibold text-amber-950">Codes shown once</h2>
              <p className="mt-1 text-sm text-amber-900">Save this list now. Codes are not stored in plaintext and cannot be fetched after leaving this page.</p>
            </div>
            <div className="flex gap-2">
              <button type="button" onClick={copyCodes} className="rounded-lg border border-amber-500 px-3 py-2 text-sm font-semibold text-amber-950">Copy codes</button>
              <button type="button" onClick={downloadCodes} className="rounded-lg bg-amber-700 px-3 py-2 text-sm font-semibold text-white">Download CSV</button>
            </div>
          </div>
          <div className="mt-4 max-h-80 overflow-auto rounded-lg border border-amber-200 bg-white">
            <table className="w-full text-left text-xs">
              <thead className="sticky top-0 bg-amber-100 text-amber-950"><tr><th className="p-2">Invitation ID</th><th className="p-2">Code</th><th className="p-2">Expires</th></tr></thead>
              <tbody>{created.map((item) => <tr key={item.id} className="border-t border-amber-100"><td className="p-2 font-mono">{item.id}</td><td className="break-all p-2 font-mono">{item.invitation_code}</td><td className="p-2">{new Date(item.expires_at).toLocaleString()}</td></tr>)}</tbody>
            </table>
          </div>
        </div>
      )}

      <div className="rounded-xl border border-gray-200 bg-card p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="font-semibold text-content">Invitation records</h2>
          <select aria-label="Invitation status" value={filter} onChange={(event) => setFilter(event.target.value as InvitationState)} className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm capitalize">
            {STATES.map((state) => <option key={state} value={state}>{state}</option>)}
          </select>
        </div>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead><tr className="border-b text-gray-500"><th className="p-2">Invitation ID</th><th className="p-2">Status</th><th className="p-2">Expires</th><th className="p-2">Action</th></tr></thead>
            <tbody>
              {records.map((item) => (
                <tr key={item.id} className="border-b border-gray-100">
                  <td className="p-2 font-mono text-xs">{item.id}</td>
                  <td className="p-2 capitalize">{item.status}</td>
                  <td className="p-2">{new Date(item.expires_at).toLocaleString()}</td>
                  <td className="p-2">{item.status === "available" && <button type="button" disabled={busy} onClick={() => revoke(item)} className="text-sm font-semibold text-red-700 hover:underline disabled:opacity-50">Revoke</button>}</td>
                </tr>
              ))}
              {records.length === 0 && <tr><td colSpan={4} className="p-5 text-center text-gray-500">No {filter} codes.</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
};
