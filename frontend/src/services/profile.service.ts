import { api } from "@/lib/api";
import type {
  ProfessorProfileResponse,
  ProfessorProfileUpdate,
  StudentProfileResponse,
  StudentProfileUpdate,
} from "@/types/api";

export const profileService = {
  async getStudent(): Promise<StudentProfileResponse> {
    const { data } = await api.get<StudentProfileResponse>("/profile/student");
    return data;
  },
  async updateStudent(payload: StudentProfileUpdate): Promise<StudentProfileResponse> {
    const { data } = await api.put<StudentProfileResponse>("/profile/student", payload);
    return data;
  },
  async getProfessor(): Promise<ProfessorProfileResponse> {
    const { data } = await api.get<ProfessorProfileResponse>("/profile/professor");
    return data;
  },
  async updateProfessor(payload: ProfessorProfileUpdate): Promise<ProfessorProfileResponse> {
    const { data } = await api.put<ProfessorProfileResponse>("/profile/professor", payload);
    return data;
  },
};
