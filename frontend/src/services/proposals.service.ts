import { api } from "@/lib/api";
import type { ProposalCreate, ProposalResponse, UUID } from "@/types/api";

export const proposalsService = {
  create: async (groupId: UUID, payload: ProposalCreate) =>
    (await api.post<ProposalResponse>(`/proposals/groups/${groupId}`, payload)).data,
  pending: async () =>
    (await api.get<ProposalResponse[]>("/proposals/pending")).data,
  approve: async (proposalId: UUID) =>
    (await api.post<ProposalResponse>(`/proposals/${proposalId}/approve`)).data,
  reject: async (proposalId: UUID, feedback?: string) =>
    (await api.post<ProposalResponse>(`/proposals/${proposalId}/reject`, { action: "reject", feedback })).data,
};
