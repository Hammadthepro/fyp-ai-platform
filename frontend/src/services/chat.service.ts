import { api } from "@/lib/api";
import type {
  ChatMessageCreate,
  ChatMessageResponse,
  ChatRoomCreate,
  ChatRoomResponse,
  UUID,
} from "@/types/api";

export const chatService = {
  createRoom: async (payload: ChatRoomCreate) =>
    (await api.post<ChatRoomResponse>("/chat/rooms", payload)).data,
  sendMessage: async (payload: ChatMessageCreate) =>
    (await api.post<ChatMessageResponse>("/chat/messages", payload)).data,
  getMessages: async (roomId: UUID) =>
    (await api.get<ChatMessageResponse[]>(`/chat/rooms/${roomId}/messages`)).data,
  updateMessage: async (messageId: UUID, message: string) =>
    (await api.put<ChatMessageResponse>(`/chat/messages/${messageId}`, { message })).data,
  deleteMessage: async (messageId: UUID) =>
    (await api.delete(`/chat/messages/${messageId}`)).data,
};
