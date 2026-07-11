import { useEffect, useRef, useState } from "react";
import { config, AUTH_TOKEN_KEY } from "@/lib/config";
import type { WSChatMessage } from "@/types/api";

export type SocketStatus = "connecting" | "open" | "closed";

export function useChatSocket(roomId: string | null) {
  const [messages, setMessages] = useState<WSChatMessage[]>([]);
  const [status, setStatus] = useState<SocketStatus>("closed");
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimer = useRef<number | null>(null);

  useEffect(() => {
    if (!roomId) return;
    let closedByUs = false;

    function connect() {
      const token = localStorage.getItem(AUTH_TOKEN_KEY);
      if (!token) return;
      const url = `${config.wsBaseUrl}/chat/ws/${roomId}?token=${encodeURIComponent(token)}`;
      setStatus("connecting");
      const ws = new WebSocket(url);
      socketRef.current = ws;
      ws.onopen = () => setStatus("open");
      ws.onmessage = (evt) => {
        try {
          const msg = JSON.parse(evt.data) as WSChatMessage;
          setMessages((prev) => [...prev, msg]);
        } catch {
          /* ignore malformed */
        }
      };
      ws.onclose = () => {
        setStatus("closed");
        if (!closedByUs) {
          reconnectTimer.current = window.setTimeout(connect, 2000);
        }
      };
      ws.onerror = () => ws.close();
    }
    connect();
    return () => {
      closedByUs = true;
      if (reconnectTimer.current) window.clearTimeout(reconnectTimer.current);
      socketRef.current?.close();
      socketRef.current = null;
      setMessages([]);
    };
  }, [roomId]);

  function send(text: string) {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(text);
    }
  }

  return { messages, status, send, setMessages };
}
