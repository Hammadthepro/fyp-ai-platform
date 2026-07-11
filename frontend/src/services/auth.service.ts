import { api } from "@/lib/api";
import type {
  ProfessorRegisterPayload,
  StudentRegisterPayload,
  TokenResponse,
  UserResponse,
} from "@/types/api";

export const authService = {
  async login(email: string, password: string): Promise<TokenResponse> {
    // Backend uses OAuth2PasswordRequestForm → application/x-www-form-urlencoded
    const body = new URLSearchParams();
    body.set("username", email);
    body.set("password", password);
    const { data } = await api.post<TokenResponse>("/auth/login", body, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return data;
  },

  async registerStudent(payload: StudentRegisterPayload): Promise<TokenResponse> {
    const { data } = await api.post<TokenResponse>("/auth/register/student", payload);
    return data;
  },

  async registerProfessor(payload: ProfessorRegisterPayload): Promise<TokenResponse> {
    const { data } = await api.post<TokenResponse>("/auth/register/professor", payload);
    return data;
  },

  async me(): Promise<UserResponse> {
    const { data } = await api.get<UserResponse>("/auth/me");
    return data;
  },
};
