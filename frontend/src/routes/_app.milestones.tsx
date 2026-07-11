import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Plus, Target, Trash2 } from "lucide-react";
import { format } from "date-fns";
import toast from "react-hot-toast";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { EmptyState } from "@/components/common/EmptyState";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { milestonesService } from "@/services/milestones.service";
import { useAuth } from "@/contexts/AuthContext";
import { extractApiError } from "@/lib/api";

export const Route = createFileRoute("/_app/milestones")({ component: MilestonesPage });

const STATUSES = ["pending", "in_progress", "completed", "delayed"];

function MilestonesPage() {
  const { role } = useAuth();
  const qc = useQueryClient();
  const [groupId, setGroupId] = useState("");
  const [open, setOpen] = useState(false);

  const { data } = useQuery({
    queryKey: ["milestones", groupId],
    queryFn: () => milestonesService.listByGroup(groupId),
    enabled: !!groupId,
  });

  const removeMut = useMutation({
    mutationFn: (id: string) => milestonesService.remove(id),
    onSuccess: () => {
      toast.success("Deleted");
      qc.invalidateQueries({ queryKey: ["milestones", groupId] });
    },
    onError: (e) => toast.error(extractApiError(e)),
  });

  const statusMut = useMutation({
    mutationFn: ({ id, status }: { id: string; status: string }) => milestonesService.update(id, { status }),
    onSuccess: () => {
      toast.success("Status updated");
      qc.invalidateQueries({ queryKey: ["milestones", groupId] });
    },
    onError: (e) => toast.error(extractApiError(e)),
  });

  return (
    <div>
      <PageHeader
        title="Milestones"
        description="Track project milestones by group."
        actions={
          role === "professor" && groupId ? (
            <Dialog open={open} onOpenChange={setOpen}>
              <DialogTrigger asChild><Button><Plus className="mr-2 h-4 w-4" /> New milestone</Button></DialogTrigger>
              <CreateMilestoneDialog groupId={groupId} onDone={() => setOpen(false)} />
            </Dialog>
          ) : null
        }
      />

      <Card className="mb-4 max-w-md border-border/60">
        <CardHeader><CardTitle className="text-sm">Load group</CardTitle></CardHeader>
        <CardContent>
          <Label className="text-xs">Group ID</Label>
          <Input value={groupId} onChange={(e) => setGroupId(e.target.value)} />
        </CardContent>
      </Card>

      {!groupId ? (
        <EmptyState icon={Target} title="Enter a group ID to view milestones" />
      ) : !data || data.length === 0 ? (
        <EmptyState icon={Target} title="No milestones for this group" />
      ) : (
        <div className="grid gap-3">
          {data.map((m) => (
            <Card key={m.id} className="border-border/60">
              <CardHeader className="flex flex-row items-start justify-between gap-3">
                <div className="flex-1">
                  <CardTitle className="text-base">{m.title}</CardTitle>
                  <p className="mt-1 text-xs text-muted-foreground">{m.description}</p>
                  <p className="mt-1 text-xs">Due: {format(new Date(m.due_date), "PPP")}</p>
                  {m.feedback && <p className="mt-2 rounded-md bg-muted px-2 py-1 text-xs">Feedback: {m.feedback}</p>}
                </div>
                <div className="flex items-center gap-2">
                  {role === "professor" ? (
                    <>
                      <Select value={m.status} onValueChange={(v) => statusMut.mutate({ id: m.id, status: v })}>
                        <SelectTrigger className="h-8 w-36"><SelectValue /></SelectTrigger>
                        <SelectContent>
                          {STATUSES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                        </SelectContent>
                      </Select>
                      <Button size="icon" variant="ghost" onClick={() => removeMut.mutate(m.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </>
                  ) : (
                    <Badge variant="secondary">{m.status}</Badge>
                  )}
                </div>
              </CardHeader>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

function CreateMilestoneDialog({ groupId, onDone }: { groupId: string; onDone: () => void }) {
  const qc = useQueryClient();
  const form = useForm<{ title: string; description: string; due_date: string }>();
  const mut = useMutation({
    mutationFn: (v: { title: string; description: string; due_date: string }) =>
      milestonesService.create(groupId, { ...v, due_date: new Date(v.due_date).toISOString() }),
    onSuccess: () => {
      toast.success("Milestone created");
      qc.invalidateQueries({ queryKey: ["milestones", groupId] });
      onDone();
    },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <DialogContent>
      <DialogHeader><DialogTitle>New milestone</DialogTitle></DialogHeader>
      <form onSubmit={form.handleSubmit((v) => mut.mutate(v))} className="space-y-3">
        <div className="space-y-1.5"><Label>Title</Label><Input {...form.register("title", { required: true })} /></div>
        <div className="space-y-1.5"><Label>Description</Label><Textarea rows={3} {...form.register("description", { required: true })} /></div>
        <div className="space-y-1.5"><Label>Due date</Label><Input type="datetime-local" {...form.register("due_date", { required: true })} /></div>
        <DialogFooter><Button type="submit" disabled={mut.isPending}>Create</Button></DialogFooter>
      </form>
    </DialogContent>
  );
}
