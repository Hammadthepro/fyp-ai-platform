import { api } from "@/lib/api";
import type { NotificationResponse, UUID } from "@/types/api";

export const notificationsService = {
  list: async () => (await api.get<NotificationResponse[]>("/notifications/")).data,
  unread: async () => (await api.get<NotificationResponse[]>("/notifications/unread")).data,
  count: async () => (await api.get<{ unread: number } | number>("/notifications/count")).data,
  markRead: async (id: UUID) => (await api.patch(`/notifications/${id}/read`)).data,
  markAllRead: async () => (await api.patch("/notifications/read-all")).data,
  remove: async (id: UUID) => (await api.delete(`/notifications/${id}`)).data,
  removeAll: async () => (await api.delete("/notifications/")).data,
};
