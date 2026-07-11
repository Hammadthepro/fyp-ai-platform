import { api } from "@/lib/api";
import type { MilestoneCreate, MilestoneResponse, MilestoneUpdate, UUID } from "@/types/api";

export const milestonesService = {
  create: async (groupId: UUID, payload: MilestoneCreate) =>
    (await api.post<MilestoneResponse>(`/milestones/group/${groupId}`, payload)).data,
  listByGroup: async (groupId: UUID) =>
    (await api.get<MilestoneResponse[]>(`/milestones/group/${groupId}`)).data,
  update: async (milestoneId: UUID, payload: MilestoneUpdate) =>
    (await api.put<MilestoneResponse>(`/milestones/${milestoneId}`, payload)).data,
  remove: async (milestoneId: UUID) =>
    (await api.delete(`/milestones/${milestoneId}`)).data,
};
