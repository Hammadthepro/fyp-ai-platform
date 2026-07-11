import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { BellRing, CheckCheck, Trash, Trash2 } from "lucide-react";
import { formatDistanceToNow } from "date-fns";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/common/EmptyState";
import { Skeleton } from "@/components/ui/skeleton";
import { notificationsService } from "@/services/notifications.service";
import { extractApiError } from "@/lib/api";

export const Route = createFileRoute("/_app/notifications")({ component: NotificationsPage });

function NotificationsPage() {
  const qc = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ["notifications"],
    queryFn: notificationsService.list,
  });

  const markRead = useMutation({
    mutationFn: notificationsService.markRead,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notifications"] }),
    onError: (e) => toast.error(extractApiError(e)),
  });
  const markAll = useMutation({
    mutationFn: notificationsService.markAllRead,
    onSuccess: () => {
      toast.success("All read");
      qc.invalidateQueries({ queryKey: ["notifications"] });
    },
  });
  const remove = useMutation({
    mutationFn: notificationsService.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notifications"] }),
  });
  const removeAll = useMutation({
    mutationFn: notificationsService.removeAll,
    onSuccess: () => { toast.success("Cleared"); qc.invalidateQueries({ queryKey: ["notifications"] }); },
  });

  return (
    <div>
      <PageHeader
        title="Notifications"
        description="Stay on top of activity across your projects."
        actions={
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={() => markAll.mutate()}>
              <CheckCheck className="mr-2 h-4 w-4" /> Mark all read
            </Button>
            <Button size="sm" variant="ghost" onClick={() => removeAll.mutate()}>
              <Trash className="mr-2 h-4 w-4" /> Clear all
            </Button>
          </div>
        }
      />
      {isLoading ? (
        <div className="grid gap-2">{Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-16" />)}</div>
      ) : !data || data.length === 0 ? (
        <EmptyState icon={BellRing} title="You're all caught up" />
      ) : (
        <div className="grid gap-2">
          {data.map((n) => (
            <Card key={n.id} className={"border-border/60 " + (!n.is_read ? "bg-primary/5" : "")}>
              <CardContent className="flex items-start justify-between gap-3 p-3">
                <div className="min-w-0">
                  <p className="text-sm font-medium">{n.title}</p>
                  <p className="text-xs text-muted-foreground">{n.message}</p>
                  <p className="mt-1 text-[10px] uppercase tracking-wide text-muted-foreground">
                    {n.type} · {formatDistanceToNow(new Date(n.created_at), { addSuffix: true })}
                  </p>
                </div>
                <div className="flex gap-1">
                  {!n.is_read && (
                    <Button size="sm" variant="ghost" onClick={() => markRead.mutate(n.id)}>
                      <CheckCheck className="h-4 w-4" />
                    </Button>
                  )}
                  <Button size="sm" variant="ghost" onClick={() => remove.mutate(n.id)}>
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
