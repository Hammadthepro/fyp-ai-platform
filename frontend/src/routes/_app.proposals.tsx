import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { FileText, Plus } from "lucide-react";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/common/EmptyState";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { proposalsService } from "@/services/proposals.service";
import { useAuth } from "@/contexts/AuthContext";
import { extractApiError } from "@/lib/api";
import type { ProposalResponse } from "@/types/api";

export const Route = createFileRoute("/_app/proposals")({ component: ProposalsPage });

function ProposalsPage() {
  const { role } = useAuth();
  const qc = useQueryClient();
  const [createOpen, setCreateOpen] = useState(false);

  const { data, isLoading } = useQuery({ queryKey: ["proposals", "pending"], queryFn: proposalsService.pending });

  const approve = useMutation({
    mutationFn: proposalsService.approve,
    onSuccess: () => { toast.success("Approved"); qc.invalidateQueries({ queryKey: ["proposals", "pending"] }); },
    onError: (e) => toast.error(extractApiError(e)),
  });

  return (
    <div>
      <PageHeader
        title="Proposals"
        description={role === "professor" ? "Review pending proposals from your groups." : "Submit and track your project proposal."}
        actions={
          role === "student" ? (
            <Dialog open={createOpen} onOpenChange={setCreateOpen}>
              <DialogTrigger asChild><Button><Plus className="mr-2 h-4 w-4" /> New proposal</Button></DialogTrigger>
              <CreateProposalDialog onDone={() => setCreateOpen(false)} />
            </Dialog>
          ) : null
        }
      />
      {isLoading ? (
        <div className="grid gap-3">
          {Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-24" />)}
        </div>
      ) : !data || data.length === 0 ? (
        <EmptyState icon={FileText} title="No pending proposals" />
      ) : (
        <div className="grid gap-3">
          {data.map((p) => (
            <ProposalCard key={p.id} proposal={p} canReview={role === "professor"} onApprove={() => approve.mutate(p.id)} />
          ))}
        </div>
      )}
    </div>
  );
}

function ProposalCard({ proposal: p, canReview, onApprove }: { proposal: ProposalResponse; canReview: boolean; onApprove: () => void }) {
  const [rejectOpen, setRejectOpen] = useState(false);
  return (
    <Card className="border-border/60">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <div className="flex-1">
          <CardTitle className="text-base">{p.title}</CardTitle>
          <p className="mt-1 text-xs text-muted-foreground">{p.abstract}</p>
          {p.objectives && <p className="mt-1 text-xs">Objectives: {p.objectives}</p>}
          {p.feedback && <p className="mt-2 rounded-md bg-muted px-2 py-1 text-xs">Feedback: {p.feedback}</p>}
        </div>
        <Badge variant="secondary">{p.status}</Badge>
      </CardHeader>
      {canReview && p.status === "pending" && (
        <CardContent className="flex gap-2">
          <Button size="sm" onClick={onApprove}>Approve</Button>
          <Dialog open={rejectOpen} onOpenChange={setRejectOpen}>
            <DialogTrigger asChild><Button size="sm" variant="outline">Reject</Button></DialogTrigger>
            <RejectDialog proposalId={p.id} onDone={() => setRejectOpen(false)} />
          </Dialog>
        </CardContent>
      )}
    </Card>
  );
}

function CreateProposalDialog({ onDone }: { onDone: () => void }) {
  const qc = useQueryClient();
  const form = useForm<{ group_id: string; professor_id: string; title: string; abstract: string; objectives: string }>();
  const mut = useMutation({
    mutationFn: (v: { group_id: string; professor_id: string; title: string; abstract: string; objectives: string }) =>
      proposalsService.create(v.group_id, {
        professor_id: v.professor_id,
        title: v.title,
        abstract: v.abstract,
        objectives: v.objectives,
      }),
    onSuccess: () => {
      toast.success("Proposal submitted");
      qc.invalidateQueries({ queryKey: ["proposals", "pending"] });
      onDone();
    },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <DialogContent>
      <DialogHeader><DialogTitle>Submit proposal</DialogTitle></DialogHeader>
      <form onSubmit={form.handleSubmit((v) => mut.mutate(v))} className="space-y-3">
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1.5"><Label>Group ID</Label><Input {...form.register("group_id", { required: true })} /></div>
          <div className="space-y-1.5"><Label>Professor ID</Label><Input {...form.register("professor_id", { required: true })} /></div>
        </div>
        <div className="space-y-1.5"><Label>Title</Label><Input {...form.register("title", { required: true, minLength: 5 })} /></div>
        <div className="space-y-1.5"><Label>Abstract</Label><Textarea rows={4} {...form.register("abstract", { required: true, minLength: 20 })} /></div>
        <div className="space-y-1.5"><Label>Objectives</Label><Textarea rows={3} {...form.register("objectives", { required: true })} /></div>
        <DialogFooter><Button type="submit" disabled={mut.isPending}>Submit</Button></DialogFooter>
      </form>
    </DialogContent>
  );
}

function RejectDialog({ proposalId, onDone }: { proposalId: string; onDone: () => void }) {
  const qc = useQueryClient();
  const form = useForm<{ feedback: string }>();
  const mut = useMutation({
    mutationFn: (v: { feedback: string }) => proposalsService.reject(proposalId, v.feedback),
    onSuccess: () => {
      toast.success("Rejected");
      qc.invalidateQueries({ queryKey: ["proposals", "pending"] });
      onDone();
    },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <DialogContent>
      <DialogHeader><DialogTitle>Reject proposal</DialogTitle></DialogHeader>
      <form onSubmit={form.handleSubmit((v) => mut.mutate(v))} className="space-y-3">
        <div className="space-y-1.5"><Label>Feedback</Label><Textarea rows={4} {...form.register("feedback", { required: true, minLength: 5 })} /></div>
        <DialogFooter><Button type="submit" variant="destructive" disabled={mut.isPending}>Reject</Button></DialogFooter>
      </form>
    </DialogContent>
  );
}
