import { api } from "@/lib/api";
import type { SubmissionCreate, SubmissionResponse, SubmissionUpdate, UUID } from "@/types/api";

export const submissionsService = {
  create: async (payload: SubmissionCreate) =>
    (await api.post<SubmissionResponse>("/submissions", payload)).data,
  listByMilestone: async (milestoneId: UUID) =>
    (await api.get<SubmissionResponse[]>(`/submissions/milestone/${milestoneId}`)).data,
  update: async (submissionId: UUID, payload: SubmissionUpdate) =>
    (await api.patch<SubmissionResponse>(`/submissions/${submissionId}`, payload)).data,
};
