import { api } from "@/lib/api";
import type { GroupResponse, InvitationResponse, UUID } from "@/types/api";

export const groupsService = {
  create: async (name: string) =>
    (await api.post<GroupResponse>("/groups", { name })).data,
  invite: async (groupId: UUID, studentId: UUID) =>
    (await api.post<InvitationResponse>(`/groups/${groupId}/invite`, { student_id: studentId })).data,
  respond: async (invitationId: UUID, action: "accept" | "reject") =>
    (await api.post<InvitationResponse>(`/groups/invitations/${invitationId}`, { action })).data,
};
