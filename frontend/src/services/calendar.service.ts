import { api } from "@/lib/api";
import type {
  CalendarEventCreate,
  CalendarEventResponse,
  CalendarEventUpdate,
  UUID,
} from "@/types/api";

export const calendarService = {
  create: async (payload: CalendarEventCreate) =>
    (await api.post<CalendarEventResponse>("/calendar/events", payload)).data,
  list: async () => (await api.get<CalendarEventResponse[]>("/calendar/events")).data,
  upcoming: async () =>
    (await api.get<{ upcoming_events: CalendarEventResponse[] }>("/calendar/upcoming")).data,
  update: async (eventId: UUID, payload: CalendarEventUpdate) =>
    (await api.put<CalendarEventResponse>(`/calendar/events/${eventId}`, payload)).data,
  remove: async (eventId: UUID) =>
    (await api.delete(`/calendar/events/${eventId}`)).data,
  student: async () => (await api.get("/calendar/student")).data,
  professor: async () => (await api.get("/calendar/professor")).data,
  admin: async () => (await api.get("/calendar/admin")).data,
};
