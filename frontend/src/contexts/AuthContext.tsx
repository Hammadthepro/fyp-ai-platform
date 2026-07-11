import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { authService } from "@/services/auth.service";
import { getStoredToken, setStoredToken, setUnauthenticatedHandler } from "@/lib/api";
import type { UserResponse, UserRole } from "@/types/api";

interface AuthContextValue {
  user: UserResponse | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  role: UserRole | null;
  setToken: (token: string) => Promise<void>;
  logout: () => void;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(null);
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const logout = useCallback(() => {
    setStoredToken(null);
    setTokenState(null);
    setUser(null);
  }, []);

  const refresh = useCallback(async () => {
    const stored = getStoredToken();
    if (!stored) {
      setUser(null);
      setTokenState(null);
      setIsLoading(false);
      return;
    }
    setTokenState(stored);
    try {
      const me = await authService.me();
      setUser(me);
    } catch {
      logout();
    } finally {
      setIsLoading(false);
    }
  }, [logout]);

  const setToken = useCallback(async (newToken: string) => {
    setStoredToken(newToken);
    setTokenState(newToken);
    setIsLoading(true);
    try {
      const me = await authService.me();
      setUser(me);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    setUnauthenticatedHandler(() => {
      setTokenState(null);
      setUser(null);
    });
    void refresh();
  }, [refresh]);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      isLoading,
      isAuthenticated: !!user && !!token,
      role: user?.role ?? null,
      setToken,
      logout,
      refresh,
    }),
    [user, token, isLoading, setToken, logout, refresh],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
