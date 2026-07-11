export const config = {
  apiBaseUrl:
    (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
    "http://localhost:8000",
  wsBaseUrl:
    (import.meta.env.VITE_WS_BASE_URL as string | undefined) ??
    "ws://localhost:8000",
};

export const AUTH_TOKEN_KEY = "fyp_access_token";
