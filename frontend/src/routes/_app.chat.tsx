import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useMemo, useRef, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { MessageSquare, Plus, Send, Wifi, WifiOff } from "lucide-react";
import { format } from "date-fns";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { EmptyState } from "@/components/common/EmptyState";
import { chatService } from "@/services/chat.service";
import { useChatSocket } from "@/hooks/useChatSocket";
import { useAuth } from "@/contexts/AuthContext";
import { extractApiError } from "@/lib/api";
import type { WSChatMessage } from "@/types/api";

export const Route = createFileRoute("/_app/chat")({ component: ChatPage });

function ChatPage() {
  const { user } = useAuth();
  const [roomId, setRoomId] = useState<string>("");
  const [activeRoom, setActiveRoom] = useState<string | null>(null);
  const [draft, setDraft] = useState("");
  const [createOpen, setCreateOpen] = useState(false);
  const listRef = useRef<HTMLDivElement>(null);

  const { data: history } = useQuery({
    queryKey: ["chat", "messages", activeRoom],
    queryFn: () => chatService.getMessages(activeRoom!),
    enabled: !!activeRoom,
  });

  const { messages: live, status, send } = useChatSocket(activeRoom);

  const all = useMemo<WSChatMessage[]>(() => {
    const historyMapped: WSChatMessage[] = (history ?? []).map((m) => ({
      id: m.id,
      room_id: m.room_id,
      sender_id: m.sender_id,
      sender_name: m.sender_id === user?.id ? user.full_name : "Member",
      message: m.message,
      created_at: m.created_at,
    }));
    const seen = new Set<string>();
    return [...historyMapped, ...live].filter((m) => {
      if (seen.has(m.id)) return false;
      seen.add(m.id);
      return true;
    });
  }, [history, live, user]);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [all.length]);

  function handleSend(e: React.FormEvent) {
    e.preventDefault();
    const text = draft.trim();
    if (!text) return;
    send(text);
    setDraft("");
  }

  return (
    <div>
      <PageHeader
        title="Team Chat"
        description="Realtime chat for your project group."
        actions={
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              {status === "open" ? <Wifi className="h-4 w-4 text-green-500" /> : <WifiOff className="h-4 w-4" />}
              {status}
            </div>
            <Dialog open={createOpen} onOpenChange={setCreateOpen}>
              <DialogTrigger asChild>
                <Button size="sm"><Plus className="mr-2 h-4 w-4" /> New room</Button>
              </DialogTrigger>
              <CreateRoomDialog onDone={(id) => { setCreateOpen(false); setRoomId(id); setActiveRoom(id); }} />
            </Dialog>
          </div>
        }
      />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[280px_1fr]">
        <Card className="border-border/60">
          <CardContent className="space-y-2 p-3">
            <Label className="text-xs">Room ID</Label>
            <Input value={roomId} onChange={(e) => setRoomId(e.target.value)} placeholder="UUID" />
            <Button size="sm" className="w-full" disabled={!roomId} onClick={() => setActiveRoom(roomId)}>Join room</Button>
          </CardContent>
        </Card>

        <Card className="flex h-[calc(100vh-14rem)] flex-col border-border/60">
          {!activeRoom ? (
            <div className="flex flex-1 items-center justify-center">
              <EmptyState icon={MessageSquare} title="Join a chat room" description="Enter a room ID or create a new one." />
            </div>
          ) : (
            <>
              <div ref={listRef} className="flex-1 space-y-3 overflow-y-auto p-4">
                {all.length === 0 && <p className="text-center text-xs text-muted-foreground">No messages yet.</p>}
                {all.map((m) => {
                  const mine = m.sender_id === user?.id;
                  return (
                    <div key={m.id} className={"flex " + (mine ? "justify-end" : "justify-start")}>
                      <div className={"max-w-[70%] rounded-lg px-3 py-2 text-sm " + (mine ? "bg-primary text-primary-foreground" : "bg-muted")}>
                        {!mine && <p className="mb-0.5 text-[10px] font-semibold opacity-70">{m.sender_name}</p>}
                        <p className="whitespace-pre-wrap">{m.message}</p>
                        <p className="mt-1 text-[10px] opacity-60">{format(new Date(m.created_at), "p")}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
              <form onSubmit={handleSend} className="flex gap-2 border-t border-border/60 p-3">
                <Input value={draft} onChange={(e) => setDraft(e.target.value)}
                  placeholder={status === "open" ? "Type a message" : "Connecting…"}
                  disabled={status !== "open"} />
                <Button type="submit" disabled={status !== "open" || !draft.trim()}><Send className="h-4 w-4" /></Button>
              </form>
            </>
          )}
        </Card>
      </div>
    </div>
  );
}

function CreateRoomDialog({ onDone }: { onDone: (roomId: string) => void }) {
  const form = useForm<{ group_id: string; name: string }>();
  const mut = useMutation({
    mutationFn: (v: { group_id: string; name: string }) => chatService.createRoom({ group_id: v.group_id, name: v.name }),
    onSuccess: (room) => { toast.success("Room created"); onDone(room.id); },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <DialogContent>
      <DialogHeader><DialogTitle>New chat room</DialogTitle></DialogHeader>
      <form onSubmit={form.handleSubmit((v) => mut.mutate(v))} className="space-y-3">
        <div className="space-y-1.5"><Label>Group ID (UUID)</Label><Input {...form.register("group_id", { required: true })} /></div>
        <div className="space-y-1.5"><Label>Room name</Label><Input {...form.register("name", { required: true })} /></div>
        <DialogFooter><Button type="submit" disabled={mut.isPending}>Create</Button></DialogFooter>
      </form>
    </DialogContent>
  );
}
