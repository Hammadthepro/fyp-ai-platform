import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { Users, FolderKanban, FileText, ClipboardList } from "lucide-react";

import { ProtectedRoute } from "@/components/common/ProtectedRoute";
import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { dashboardService } from "@/services/dashboard.service";

export const Route = createFileRoute("/_app/admin")({
  component: () => (
    <ProtectedRoute roles={["admin"]}><AdminPage /></ProtectedRoute>
  ),
});

function AdminPage() {
  const { data, isLoading } = useQuery({ queryKey: ["admin", "analytics"], queryFn: dashboardService.analytics });

  return (
    <div>
      <PageHeader title="Admin" description="Platform-wide analytics and recent activity." />
      {isLoading || !data ? (
        <div className="grid gap-3 md:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-24" />)}
        </div>
      ) : (
        <>
          <div className="mb-4 grid grid-cols-2 gap-3 md:grid-cols-4">
            <StatCard label="Students" value={data.dashboard.students} icon={Users} />
            <StatCard label="Professors" value={data.dashboard.professors} icon={Users} />
            <StatCard label="Groups" value={data.dashboard.groups} icon={FolderKanban} />
            <StatCard label="Ideas" value={data.dashboard.ideas} icon={FileText} />
            <StatCard label="Proposals" value={data.dashboard.proposals} icon={FileText} />
            <StatCard label="Approved" value={data.dashboard.approved} icon={FileText} />
            <StatCard label="Milestones" value={data.dashboard.milestones} icon={ClipboardList} />
            <StatCard label="Submissions" value={data.dashboard.submissions} icon={ClipboardList} />
          </div>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <Card className="border-border/60">
              <CardHeader><CardTitle className="text-sm">Recent users</CardTitle></CardHeader>
              <CardContent className="space-y-2">
                {data.recent_users.map((u) => (
                  <div key={u.id} className="flex items-center justify-between rounded-md border border-border/60 p-2 text-sm">
                    <div>
                      <p className="font-medium">{u.name}</p>
                      <p className="text-xs text-muted-foreground">{u.email}</p>
                    </div>
                    <Badge variant="secondary">{u.role}</Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
            <Card className="border-border/60">
              <CardHeader><CardTitle className="text-sm">Recent proposals</CardTitle></CardHeader>
              <CardContent className="space-y-2">
                {data.recent_proposals.map((p) => (
                  <div key={p.id} className="flex items-center justify-between rounded-md border border-border/60 p-2 text-sm">
                    <p className="font-medium">{p.title}</p>
                    <Badge variant="secondary">{p.status}</Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
            <Card className="border-border/60">
              <CardHeader><CardTitle className="text-sm">Recent groups</CardTitle></CardHeader>
              <CardContent className="space-y-2">
                {data.recent_groups.map((g) => (
                  <div key={g.id} className="rounded-md border border-border/60 p-2 text-sm font-medium">{g.name}</div>
                ))}
              </CardContent>
            </Card>
            <Card className="border-border/60">
              <CardHeader><CardTitle className="text-sm">Recent submissions</CardTitle></CardHeader>
              <CardContent className="space-y-2">
                {data.recent_submissions.map((s) => (
                  <div key={s.id} className="rounded-md border border-border/60 p-2 text-sm">
                    <p className="font-medium">{s.student}</p>
                    <p className="text-xs text-muted-foreground">{s.milestone}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}

function StatCard({ label, value, icon: Icon }: { label: string; value: number; icon: React.ComponentType<{ className?: string }> }) {
  return (
    <Card className="border-border/60">
      <CardContent className="flex items-center justify-between p-4">
        <div>
          <p className="text-xs text-muted-foreground">{label}</p>
          <p className="mt-1 text-2xl font-semibold">{value}</p>
        </div>
        <Icon className="h-5 w-5 text-muted-foreground" />
      </CardContent>
    </Card>
  );
}
