import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import toast from "react-hot-toast";
import { Plus } from "lucide-react";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { masterService } from "@/services/master.service";
import { extractApiError } from "@/lib/api";
import type { NamedEntity } from "@/types/api";

export const Route = createFileRoute("/_app/master")({ component: MasterPage });

function MasterPage() {
  return (
    <div>
      <PageHeader title="Master Data" description="Manage skills, domains and technologies." />
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <MasterList
          title="Skills"
          queryKey="skills"
          list={masterService.listSkills}
          create={masterService.createSkill}
        />
        <MasterList
          title="Domains"
          queryKey="domains"
          list={masterService.listDomains}
          create={masterService.createDomain}
        />
        <MasterList
          title="Technologies"
          queryKey="technologies"
          list={masterService.listTechnologies}
          create={masterService.createTechnology}
        />
      </div>
    </div>
  );
}

function MasterList({
  title,
  queryKey,
  list,
  create,
}: {
  title: string;
  queryKey: string;
  list: () => Promise<NamedEntity[]>;
  create: (name: string) => Promise<NamedEntity>;
}) {
  const qc = useQueryClient();
  const [name, setName] = useState("");
  const { data } = useQuery({ queryKey: [queryKey], queryFn: list });
  const mut = useMutation({
    mutationFn: (n: string) => create(n),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: [queryKey] });
      setName("");
      toast.success(`${title.slice(0, -1)} added`);
    },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <Card className="border-border/60">
      <CardHeader><CardTitle className="text-sm">{title}</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <div className="flex gap-2">
          <Input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder={`Add ${title.slice(0, -1).toLowerCase()}`}
          />
          <Button size="sm" disabled={!name || mut.isPending} onClick={() => mut.mutate(name)}>
            <Plus className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex flex-wrap gap-1">
          {(data ?? []).map((e) => (
            <Badge key={e.id} variant="secondary">{e.name}</Badge>
          ))}
          {(data ?? []).length === 0 && (
            <p className="text-xs text-muted-foreground">None yet.</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
