import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import {
  Activity,
  CheckCircle2,
  ClipboardList,
  FileText,
  FolderKanban,
  GraduationCap,
  Layers,
  Users,
} from "lucide-react";

import { useAuth } from "@/contexts/AuthContext";
import { dashboardService } from "@/services/dashboard.service";
import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { formatDistanceToNow } from "date-fns";

export const Route = createFileRoute("/_app/dashboard")({ component: DashboardPage });

function DashboardPage() {
  const { role, user } = useAuth();
  return (
    <div>
      <PageHeader
        title={`Hello, ${user?.full_name ?? ""}`}
        description="Your workspace at a glance."
      />
      {role === "student" && <StudentDashboard />}
      {role === "professor" && <ProfessorDashboard />}
      {role === "admin" && <AdminDashboard />}
    </div>
  );
}

function StatCard({
  title,
  value,
  icon: Icon,
}: {
  title: string;
  value: string | number;
  icon: React.ElementType;
}) {
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
      <Card className="border-border/60">
        <CardContent className="flex items-center justify-between p-4">
          <div>
            <p className="text-xs uppercase tracking-wide text-muted-foreground">{title}</p>
            <p className="mt-1 text-2xl font-semibold">{value}</p>
          </div>
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-muted text-muted-foreground">
            <Icon className="h-4 w-4" />
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

function LoadingStats() {
  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <Skeleton key={i} className="h-20" />
      ))}
    </div>
  );
}

function StudentDashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ["dashboard", "student"],
    queryFn: dashboardService.student,
  });
  if (isLoading || !data) return <LoadingStats />;
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <StatCard title="Semester" value={data.semester} icon={GraduationCap} />
        <StatCard title="Group" value={data.group_name ?? "—"} icon={Users} />
        <StatCard title="Milestones" value={`${data.completed_milestones}/${data.total_milestones}`} icon={CheckCircle2} />
        <StatCard title="Progress" value={`${Math.round(data.progress)}%`} icon={Activity} />
      </div>

      <Card className="border-border/60">
        <CardHeader>
          <CardTitle className="text-sm">Overall progress</CardTitle>
        </CardHeader>
        <CardContent>
          <Progress value={data.progress} />
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card className="border-border/60">
          <CardHeader>
            <CardTitle className="text-sm">Milestones</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {data.milestones.length === 0 && (
              <p className="text-sm text-muted-foreground">No milestones yet.</p>
            )}
            {data.milestones.map((m) => (
              <div key={m.id} className="flex items-center justify-between rounded-md border border-border/60 p-3">
                <div>
                  <p className="text-sm font-medium">{m.title}</p>
                  <p className="text-xs text-muted-foreground">
                    Due {formatDistanceToNow(new Date(m.due_date), { addSuffix: true })}
                  </p>
                </div>
                <Badge variant="secondary">{m.status}</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
        <Card className="border-border/60">
          <CardHeader>
            <CardTitle className="text-sm">Recent notifications</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {data.notifications.length === 0 && (
              <p className="text-sm text-muted-foreground">No notifications.</p>
            )}
            {data.notifications.slice(0, 5).map((n) => (
              <div key={n.id} className="rounded-md border border-border/60 p-3">
                <p className="text-sm font-medium">{n.title}</p>
                <p className="text-xs text-muted-foreground">{n.message}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function ProfessorDashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ["dashboard", "professor"],
    queryFn: dashboardService.professor,
  });
  if (isLoading || !data) return <LoadingStats />;
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <StatCard title="Groups" value={data.total_groups} icon={Users} />
        <StatCard title="Proposals" value={data.total_proposals} icon={FileText} />
        <StatCard title="Approved" value={data.approved_proposals} icon={CheckCircle2} />
        <StatCard title="Pending" value={data.pending_proposals} icon={ClipboardList} />
      </div>
      <Card className="border-border/60">
        <CardHeader>
          <CardTitle className="text-sm">Recent proposals</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {data.proposals.length === 0 && (
            <p className="text-sm text-muted-foreground">No proposals yet.</p>
          )}
          {data.proposals.map((p) => (
            <div key={p.id} className="flex items-center justify-between rounded-md border border-border/60 p-3">
              <div>
                <p className="text-sm font-medium">{p.title}</p>
                <p className="text-xs text-muted-foreground">{p.group_name ?? "—"}</p>
              </div>
              <Badge variant="secondary">{p.status}</Badge>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}

function AdminDashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ["dashboard", "admin"],
    queryFn: dashboardService.admin,
  });
  if (isLoading || !data) return <LoadingStats />;
  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
      <StatCard title="Students" value={data.students} icon={GraduationCap} />
      <StatCard title="Professors" value={data.professors} icon={Users} />
      <StatCard title="Groups" value={data.groups} icon={FolderKanban} />
      <StatCard title="Ideas" value={data.ideas} icon={Layers} />
      <StatCard title="Proposals" value={data.proposals} icon={FileText} />
      <StatCard title="Approved" value={data.approved} icon={CheckCircle2} />
      <StatCard title="Milestones" value={data.milestones} icon={ClipboardList} />
      <StatCard title="Submissions" value={data.submissions} icon={Activity} />
    </div>
  );
}
