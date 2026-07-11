import { createFileRoute } from "@tanstack/react-router";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import { Check, Users, X } from "lucide-react";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { EmptyState } from "@/components/common/EmptyState";
import { groupsService } from "@/services/groups.service";
import { extractApiError } from "@/lib/api";
import type { GroupResponse } from "@/types/api";

export const Route = createFileRoute("/_app/groups")({ component: GroupsPage });

function GroupsPage() {
  const [group, setGroup] = useState<GroupResponse | null>(null);
  const [studentId, setStudentId] = useState("");
  const [invitationId, setInvitationId] = useState("");
  const form = useForm<{ name: string }>();

  const createMut = useMutation({
    mutationFn: (name: string) => groupsService.create(name),
    onSuccess: (g) => { setGroup(g); toast.success("Group created"); },
    onError: (e) => toast.error(extractApiError(e)),
  });

  const inviteMut = useMutation({
    mutationFn: () => groupsService.invite(group!.id, studentId),
    onSuccess: () => { toast.success("Invitation sent"); setStudentId(""); },
    onError: (e) => toast.error(extractApiError(e)),
  });

  const respondMut = useMutation({
    mutationFn: (action: "accept" | "reject") => groupsService.respond(invitationId, action),
    onSuccess: (_r, action) => { toast.success(`Invitation ${action}ed`); setInvitationId(""); },
    onError: (e) => toast.error(extractApiError(e)),
  });

  return (
    <div>
      <PageHeader title="Groups" description="Create your project group and invite teammates." />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {!group ? (
          <Card className="border-border/60">
            <CardHeader><CardTitle className="text-sm">Create a new group</CardTitle></CardHeader>
            <CardContent>
              <form onSubmit={form.handleSubmit((v) => createMut.mutate(v.name))} className="space-y-3">
                <div className="space-y-1.5">
                  <Label>Group name</Label>
                  <Input {...form.register("name", { required: true, minLength: 3 })} />
                </div>
                <Button type="submit" disabled={createMut.isPending}>Create</Button>
              </form>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4 lg:col-span-2">
            <Card className="border-border/60">
              <CardHeader><CardTitle className="text-sm">{group.name}</CardTitle></CardHeader>
              <CardContent>
                <p className="mb-3 text-xs text-muted-foreground">Members</p>
                {group.members.length === 0 ? (
                  <EmptyState icon={Users} title="No members yet" description="Invite a teammate by student ID." />
                ) : (
                  <ul className="space-y-1">
                    {group.members.map((m) => (
                      <li key={m.student.id} className="rounded-md border border-border/60 p-2 text-sm">
                        {m.student.registration_number} · Semester {m.student.semester}
                      </li>
                    ))}
                  </ul>
                )}
              </CardContent>
            </Card>
            <Card className="max-w-md border-border/60">
              <CardHeader><CardTitle className="text-sm">Invite student</CardTitle></CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-1.5">
                  <Label>Student ID (UUID)</Label>
                  <Input value={studentId} onChange={(e) => setStudentId(e.target.value)} />
                </div>
                <Button disabled={inviteMut.isPending || !studentId} onClick={() => inviteMut.mutate()}>Send invite</Button>
              </CardContent>
            </Card>
          </div>
        )}

        <Card className="border-border/60">
          <CardHeader><CardTitle className="text-sm">Respond to invitation</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-1.5">
              <Label>Invitation ID (UUID)</Label>
              <Input value={invitationId} onChange={(e) => setInvitationId(e.target.value)} />
            </div>
            <div className="flex gap-2">
              <Button size="sm" disabled={!invitationId || respondMut.isPending} onClick={() => respondMut.mutate("accept")}>
                <Check className="mr-1 h-4 w-4" /> Accept
              </Button>
              <Button size="sm" variant="outline" disabled={!invitationId || respondMut.isPending} onClick={() => respondMut.mutate("reject")}>
                <X className="mr-1 h-4 w-4" /> Reject
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
