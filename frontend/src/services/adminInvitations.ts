import { apiFetch } from "./api";

export type InvitationState = "available" | "redeemed" | "expired" | "revoked";

export interface GenericInvitationStatus {
  available: number;
  redeemed: number;
  expired: number;
  revoked: number;
}

export interface GenericInvitationRecord {
  id: string;
  status: InvitationState;
  expires_at: string;
  redeemed_at: string | null;
  revoked_at: string | null;
  created_at: string;
}

export interface CreatedGenericInvitation {
  id: string;
  invitation_code: string;
  expires_at: string;
}

export async function createGenericInvitationBatch(token: string) {
  return apiFetch<{
    invitations: CreatedGenericInvitation[];
    expires_at: string;
    total_accounts: number;
    pending_invitations: number;
    remaining_slots: number;
  }>("/admin/invitations/bulk", {
    method: "POST",
    token,
    body: JSON.stringify({ count: 50, expires_in_days: 14 }),
  });
}

export async function getGenericInvitationSummary(token: string) {
  return apiFetch<GenericInvitationStatus>("/admin/invitations/generic/summary", { token });
}

export async function listGenericInvitations(token: string, state: InvitationState) {
  return apiFetch<GenericInvitationRecord[]>("/admin/invitations/generic", {
    token,
    params: { status: state, limit: "200", offset: "0" },
  });
}

export async function revokeInvitation(token: string, id: string) {
  return apiFetch<{ revoked: boolean }>(`/admin/invitations/${encodeURIComponent(id)}`, {
    method: "DELETE",
    token,
  });
}
