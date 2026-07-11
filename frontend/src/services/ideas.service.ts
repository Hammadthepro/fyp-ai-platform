import { api } from "@/lib/api";
import type { IdeaCreate, IdeaListParams, IdeaResponse, IdeaUpdate, UUID } from "@/types/api";

export const ideasService = {
  list: async (params: IdeaListParams = {}) =>
    (await api.get<IdeaResponse[]>("/ideas", { params })).data,
  mine: async () => (await api.get<IdeaResponse[]>("/ideas/me")).data,
  get: async (id: UUID) => (await api.get<IdeaResponse>(`/ideas/${id}`)).data,
  create: async (payload: IdeaCreate) =>
    (await api.post<IdeaResponse>("/ideas", payload)).data,
  update: async (id: UUID, payload: IdeaUpdate) =>
    (await api.put<IdeaResponse>(`/ideas/${id}`, payload)).data,
  remove: async (id: UUID) => (await api.delete(`/ideas/${id}`)).data,
};
