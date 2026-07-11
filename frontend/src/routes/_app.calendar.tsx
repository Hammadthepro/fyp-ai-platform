import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { format } from "date-fns";
import { Calendar as CalendarIcon, Plus, Trash2 } from "lucide-react";
import toast from "react-hot-toast";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { EmptyState } from "@/components/common/EmptyState";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { calendarService } from "@/services/calendar.service";
import { extractApiError } from "@/lib/api";

export const Route = createFileRoute("/_app/calendar")({ component: CalendarPage });

const EVENT_TYPES = ["general", "meeting", "deadline", "presentation", "viva"];

function CalendarPage() {
  const qc = useQueryClient();
  const [open, setOpen] = useState(false);
  const { data, isLoading } = useQuery({ queryKey: ["calendar"], queryFn: calendarService.list });
  const { data: upcoming } = useQuery({ queryKey: ["calendar", "upcoming"], queryFn: calendarService.upcoming });

  const removeMut = useMutation({
    mutationFn: (id: string) => calendarService.remove(id),
    onSuccess: () => {
      toast.success("Deleted");
      qc.invalidateQueries({ queryKey: ["calendar"] });
      qc.invalidateQueries({ queryKey: ["calendar", "upcoming"] });
    },
    onError: (e) => toast.error(extractApiError(e)),
  });

  return (
    <div>
      <PageHeader
        title="Calendar"
        description="Upcoming events and deadlines."
        actions={
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild><Button><Plus className="mr-2 h-4 w-4" /> New event</Button></DialogTrigger>
            <CreateEventDialog onDone={() => setOpen(false)} />
          </Dialog>
        }
      />
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {isLoading ? (
            <Skeleton className="h-40" />
          ) : !data || data.length === 0 ? (
            <EmptyState icon={CalendarIcon} title="No events" />
          ) : (
            <div className="grid gap-3">
              {data.map((e) => (
                <Card key={e.id} className="border-border/60">
                  <CardHeader className="flex flex-row items-start justify-between gap-2">
                    <div>
                      <CardTitle className="text-base">{e.title}</CardTitle>
                      <p className="mt-1 text-xs text-muted-foreground">{format(new Date(e.start_date), "PPP p")}</p>
                    </div>
                    <div className="flex items-center gap-1">
                      <Badge variant="secondary">{e.event_type}</Badge>
                      <Button size="icon" variant="ghost" onClick={() => removeMut.mutate(e.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardHeader>
                  {e.description && <CardContent><p className="text-sm text-muted-foreground">{e.description}</p></CardContent>}
                </Card>
              ))}
            </div>
          )}
        </div>
        <Card className="border-border/60">
          <CardHeader><CardTitle className="text-sm">Upcoming</CardTitle></CardHeader>
          <CardContent className="space-y-2">
            {(upcoming?.upcoming_events ?? []).slice(0, 5).map((e) => (
              <div key={e.id} className="rounded-md border border-border/60 p-2">
                <p className="text-sm font-medium">{e.title}</p>
                <p className="text-xs text-muted-foreground">{format(new Date(e.start_date), "PPP")}</p>
              </div>
            ))}
            {(upcoming?.upcoming_events ?? []).length === 0 && (
              <p className="text-xs text-muted-foreground">Nothing upcoming.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function CreateEventDialog({ onDone }: { onDone: () => void }) {
  const qc = useQueryClient();
  const form = useForm<{ title: string; description: string; event_type: string; start_date: string; end_date: string; group_id: string }>({
    defaultValues: { event_type: "general" },
  });
  const mut = useMutation({
    mutationFn: (v: { title: string; description: string; event_type: string; start_date: string; end_date: string; group_id: string }) =>
      calendarService.create({
        title: v.title,
        description: v.description || null,
        event_type: v.event_type,
        start_date: new Date(v.start_date).toISOString(),
        end_date: v.end_date ? new Date(v.end_date).toISOString() : null,
        group_id: v.group_id || null,
        is_all_day: false,
      }),
    onSuccess: () => {
      toast.success("Event created");
      qc.invalidateQueries({ queryKey: ["calendar"] });
      qc.invalidateQueries({ queryKey: ["calendar", "upcoming"] });
      onDone();
    },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <DialogContent>
      <DialogHeader><DialogTitle>New event</DialogTitle></DialogHeader>
      <form onSubmit={form.handleSubmit((v) => mut.mutate(v))} className="space-y-3">
        <div className="space-y-1.5"><Label>Title</Label><Input {...form.register("title", { required: true })} /></div>
        <div className="space-y-1.5"><Label>Description</Label><Textarea rows={2} {...form.register("description")} /></div>
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1.5">
            <Label>Type</Label>
            <Select defaultValue="general" onValueChange={(v) => form.setValue("event_type", v)}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>{EVENT_TYPES.map((t) => <SelectItem key={t} value={t}>{t}</SelectItem>)}</SelectContent>
            </Select>
          </div>
          <div className="space-y-1.5"><Label>Group ID (optional)</Label><Input {...form.register("group_id")} /></div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1.5"><Label>Start</Label><Input type="datetime-local" {...form.register("start_date", { required: true })} /></div>
          <div className="space-y-1.5"><Label>End</Label><Input type="datetime-local" {...form.register("end_date")} /></div>
        </div>
        <DialogFooter><Button type="submit" disabled={mut.isPending}>Create</Button></DialogFooter>
      </form>
    </DialogContent>
  );
}
