import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { ClipboardList, Plus, Pencil } from "lucide-react";

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
import { submissionsService } from "@/services/submissions.service";
import { useAuth } from "@/contexts/AuthContext";
import { extractApiError } from "@/lib/api";
import type { SubmissionResponse } from "@/types/api";

export const Route = createFileRoute("/_app/submissions")({ component: SubmissionsPage });

const STATUSES = ["submitted", "approved", "rejected", "revision_requested"];

function SubmissionsPage() {
  const { role } = useAuth();
  const [milestoneId, setMilestoneId] = useState("");
  const [createOpen, setCreateOpen] = useState(false);

  const { data } = useQuery({
    queryKey: ["submissions", milestoneId],
    queryFn: () => submissionsService.listByMilestone(milestoneId),
    enabled: !!milestoneId,
  });

  return (
    <div>
      <PageHeader
        title="Submissions"
        description="Submit deliverables and review feedback."
        actions={
          role === "student" && milestoneId ? (
            <Dialog open={createOpen} onOpenChange={setCreateOpen}>
              <DialogTrigger asChild><Button><Plus className="mr-2 h-4 w-4" /> New submission</Button></DialogTrigger>
              <CreateSubmissionDialog milestoneId={milestoneId} onDone={() => setCreateOpen(false)} />
            </Dialog>
          ) : null
        }
      />
      <Card className="mb-4 max-w-md border-border/60">
        <CardHeader><CardTitle className="text-sm">Load milestone</CardTitle></CardHeader>
        <CardContent>
          <Label className="text-xs">Milestone ID</Label>
          <Input value={milestoneId} onChange={(e) => setMilestoneId(e.target.value)} />
        </CardContent>
      </Card>
      {!milestoneId ? (
        <EmptyState icon={ClipboardList} title="Enter a milestone ID" />
      ) : !data || data.length === 0 ? (
        <EmptyState icon={ClipboardList} title="No submissions" />
      ) : (
        <div className="grid gap-3">
          {data.map((s) => <SubmissionCard key={s.id} submission={s} canReview={role === "professor"} />)}
        </div>
      )}
    </div>
  );
}

function SubmissionCard({ submission: s, canReview }: { submission: SubmissionResponse; canReview: boolean }) {
  const [open, setOpen] = useState(false);
  return (
    <Card className="border-border/60">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <div className="flex-1">
          <CardTitle className="text-base">Submission {s.id.slice(0, 8)}</CardTitle>
          {s.github_link && <p className="text-xs text-muted-foreground">GitHub: {s.github_link}</p>}
          {s.drive_link && <p className="text-xs text-muted-foreground">Drive: {s.drive_link}</p>}
          {s.notes && <p className="mt-1 text-xs">{s.notes}</p>}
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="secondary">{s.status}</Badge>
          {canReview && (
            <Dialog open={open} onOpenChange={setOpen}>
              <DialogTrigger asChild><Button size="icon" variant="ghost"><Pencil className="h-4 w-4" /></Button></DialogTrigger>
              <ReviewSubmissionDialog submission={s} onDone={() => setOpen(false)} />
            </Dialog>
          )}
        </div>
      </CardHeader>
      {(s.feedback || s.marks != null) && (
        <CardContent>
          {s.marks != null && <p className="text-xs">Marks: {s.marks}</p>}
          {s.feedback && <p className="text-xs text-muted-foreground">{s.feedback}</p>}
        </CardContent>
      )}
    </Card>
  );
}

function CreateSubmissionDialog({ milestoneId, onDone }: { milestoneId: string; onDone: () => void }) {
  const qc = useQueryClient();
  const form = useForm<{ github_link: string; drive_link: string; notes: string }>();
  const mut = useMutation({
    mutationFn: (v: { github_link: string; drive_link: string; notes: string }) =>
      submissionsService.create({
        milestone_id: milestoneId,
        github_link: v.github_link || null,
        drive_link: v.drive_link || null,
        notes: v.notes || null,
      }),
    onSuccess: () => {
      toast.success("Submitted");
      qc.invalidateQueries({ queryKey: ["submissions", milestoneId] });
      onDone();
    },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <DialogContent>
      <DialogHeader><DialogTitle>New submission</DialogTitle></DialogHeader>
      <form onSubmit={form.handleSubmit((v) => mut.mutate(v))} className="space-y-3">
        <div className="space-y-1.5"><Label>GitHub link</Label><Input {...form.register("github_link")} placeholder="https://github.com/…" /></div>
        <div className="space-y-1.5"><Label>Drive link</Label><Input {...form.register("drive_link")} placeholder="https://drive.google.com/…" /></div>
        <div className="space-y-1.5"><Label>Notes</Label><Textarea rows={3} {...form.register("notes")} /></div>
        <DialogFooter><Button type="submit" disabled={mut.isPending}>Submit</Button></DialogFooter>
      </form>
    </DialogContent>
  );
}

function ReviewSubmissionDialog({ submission, onDone }: { submission: SubmissionResponse; onDone: () => void }) {
  const qc = useQueryClient();
  const form = useForm<{ status: string; marks: number; feedback: string }>({
    defaultValues: { status: submission.status, marks: submission.marks ?? 0, feedback: submission.feedback ?? "" },
  });
  const mut = useMutation({
    mutationFn: (v: { status: string; marks: number; feedback: string }) =>
      submissionsService.update(submission.id, {
        status: v.status,
        marks: Number(v.marks) || null,
        feedback: v.feedback || null,
      }),
    onSuccess: () => {
      toast.success("Review saved");
      qc.invalidateQueries({ queryKey: ["submissions", submission.milestone_id] });
      onDone();
    },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <DialogContent>
      <DialogHeader><DialogTitle>Review submission</DialogTitle></DialogHeader>
      <form onSubmit={form.handleSubmit((v) => mut.mutate(v))} className="space-y-3">
        <div className="space-y-1.5">
          <Label>Status</Label>
          <Select defaultValue={submission.status} onValueChange={(v) => form.setValue("status", v)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              {STATUSES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-1.5"><Label>Marks</Label><Input type="number" {...form.register("marks", { valueAsNumber: true })} /></div>
        <div className="space-y-1.5"><Label>Feedback</Label><Textarea rows={3} {...form.register("feedback")} /></div>
        <DialogFooter><Button type="submit" disabled={mut.isPending}>Save</Button></DialogFooter>
      </form>
    </DialogContent>
  );
}
