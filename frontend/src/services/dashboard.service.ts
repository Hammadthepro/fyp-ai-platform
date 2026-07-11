import { api } from "@/lib/api";
import type {
  AdminAnalyticsResponse,
  AdminDashboardResponse,
  ProfessorDashboardResponse,
  StudentDashboardResponse,
} from "@/types/api";

export const dashboardService = {
  student: async () => (await api.get<StudentDashboardResponse>("/dashboard/student")).data,
  professor: async () => (await api.get<ProfessorDashboardResponse>("/dashboard/professor")).data,
  admin: async () => (await api.get<AdminDashboardResponse>("/dashboard/admin")).data,
  analytics: async () => (await api.get<AdminAnalyticsResponse>("/dashboard/analytics")).data,
};
