import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import toast from "react-hot-toast";
import { BookOpen, Pencil, Plus, Search, Sparkles, Trash2 } from "lucide-react";

import { PageHeader } from "@/components/common/PageHeader";
import { EmptyState } from "@/components/common/EmptyState";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MultiSelect } from "@/components/common/MultiSelect";
import { ideasService } from "@/services/ideas.service";
import { masterService } from "@/services/master.service";
import { aiService } from "@/services/ai.service";
import { useAuth } from "@/contexts/AuthContext";
import { extractApiError } from "@/lib/api";
import type { IdeaResponse } from "@/types/api";

export const Route = createFileRoute("/_app/ideas")({ component: IdeasPage });

const createSchema = z.object({
  title: z.string().min(5),
  description: z.string().min(20),
  domain_id: z.string().uuid(),
  difficulty: z.string().min(1),
  max_students: z.number().int().min(1).max(5),
});
type CreateForm = z.infer<typeof createSchema>;

function IdeasPage() {
  const { role } = useAuth();
  const [keyword, setKeyword] = useState("");
  const [tab, setTab] = useState<"all" | "mine">("all");
  const [open, setOpen] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ["ideas", { keyword, tab }],
    queryFn: () => (tab === "mine" ? ideasService.mine() : ideasService.list({ keyword: keyword || undefined })),
  });

  return (
    <div>
      <PageHeader
        title="Ideas"
        description="Browse and manage FYP ideas."
        actions={
          role === "professor" && (
            <Dialog open={open} onOpenChange={setOpen}>
              <DialogTrigger asChild><Button><Plus className="mr-2 h-4 w-4" /> New idea</Button></DialogTrigger>
              <IdeaFormDialog mode="create" onDone={() => setOpen(false)} />
            </Dialog>
          )
        }
      />

      {role === "student" && <RecommendationsPanel />}

      <div className="mb-4 flex flex-wrap items-center gap-2">
        {role === "professor" && (
          <Tabs value={tab} onValueChange={(v) => setTab(v as "all" | "mine")}>
            <TabsList>
              <TabsTrigger value="all">All ideas</TabsTrigger>
              <TabsTrigger value="mine">My ideas</TabsTrigger>
            </TabsList>
          </Tabs>
        )}
        {tab === "all" && (
          <div className="relative max-w-md flex-1">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input className="pl-8" placeholder="Search ideas…" value={keyword} onChange={(e) => setKeyword(e.target.value)} />
          </div>
        )}
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => <Skeleton key={i} className="h-40" />)}
        </div>
      ) : !data || data.length === 0 ? (
        <EmptyState icon={BookOpen} title="No ideas found" description="Try adjusting your search." />
      ) : (
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
          {data.map((idea) => <IdeaCard key={idea.id} idea={idea} canManage={role === "professor" && tab === "mine"} />)}
        </div>
      )}
    </div>
  );
}

function IdeaCard({ idea, canManage }: { idea: IdeaResponse; canManage: boolean }) {
  const qc = useQueryClient();
  const [editOpen, setEditOpen] = useState(false);
  const remove = useMutation({
    mutationFn: () => ideasService.remove(idea.id),
    onSuccess: () => { toast.success("Idea deleted"); qc.invalidateQueries({ queryKey: ["ideas"] }); },
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <Card className="border-border/60">
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-base">{idea.title}</CardTitle>
          {canManage && (
            <div className="flex gap-1">
              <Dialog open={editOpen} onOpenChange={setEditOpen}>
                <DialogTrigger asChild><Button size="icon" variant="ghost"><Pencil className="h-3.5 w-3.5" /></Button></DialogTrigger>
                <IdeaFormDialog mode="edit" idea={idea} onDone={() => setEditOpen(false)} />
              </Dialog>
              <Button size="icon" variant="ghost" onClick={() => remove.mutate()}><Trash2 className="h-3.5 w-3.5" /></Button>
            </div>
          )}
        </div>
        <div className="mt-1 flex flex-wrap gap-1">
          <Badge variant="secondary">{idea.domain.name}</Badge>
          <Badge variant="outline">{idea.difficulty}</Badge>
          <Badge variant="outline">Max {idea.max_students}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="line-clamp-3 text-sm text-muted-foreground">{idea.description}</p>
        <div className="mt-3 flex flex-wrap gap-1">
          {idea.technologies.slice(0, 4).map((t) => (
            <Badge key={t.technology.id} variant="outline" className="text-xs">{t.technology.name}</Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function RecommendationsPanel() {
  const { data, isLoading } = useQuery({ queryKey: ["ai", "recommendations"], queryFn: aiService.recommendations });
  if (isLoading) return <Skeleton className="mb-4 h-24" />;
  if (!data || data.recommendations.length === 0) return null;
  return (
    <Card className="mb-4 border-border/60 bg-gradient-to-br from-primary/5 to-transparent">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-sm">
          <Sparkles className="h-4 w-4 text-primary" /> Recommended for you
        </CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-1 gap-2 md:grid-cols-3">
        {data.recommendations.slice(0, 3).map((r) => (
          <div key={r.idea_id} className="rounded-md border border-border/60 p-3">
            <p className="text-sm font-medium">{r.title}</p>
            <p className="mt-1 text-xs text-muted-foreground">{r.reason}</p>
            <div className="mt-2 flex items-center justify-between">
              <Badge variant="secondary">{Math.round(r.match_score * 100)}% match</Badge>
              {r.missing_skills.length > 0 && (
                <span className="text-[10px] text-muted-foreground">Missing: {r.missing_skills.slice(0, 2).join(", ")}</span>
              )}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

function IdeaFormDialog({ mode, idea, onDone }: { mode: "create" | "edit"; idea?: IdeaResponse; onDone: () => void }) {
  const qc = useQueryClient();
  const { data: domains } = useQuery({ queryKey: ["domains"], queryFn: masterService.listDomains });
  const { data: skills } = useQuery({ queryKey: ["skills"], queryFn: masterService.listSkills });
  const { data: techs } = useQuery({ queryKey: ["technologies"], queryFn: masterService.listTechnologies });

  const [skillIds, setSkillIds] = useState<string[]>(idea?.skills.map((s) => s.skill.id) ?? []);
  const [techIds, setTechIds] = useState<string[]>(idea?.technologies.map((t) => t.technology.id) ?? []);

  const form = useForm<CreateForm>({
    resolver: zodResolver(createSchema),
    defaultValues: {
      title: idea?.title ?? "",
      description: idea?.description ?? "",
      domain_id: idea?.domain.id ?? "",
      difficulty: idea?.difficulty ?? "Intermediate",
      max_students: idea?.max_students ?? 3,
    },
  });

  const mutation = useMutation({
    mutationFn: (v: CreateForm) =>
      mode === "create"
        ? ideasService.create({ ...v, technology_ids: techIds, skill_ids: skillIds })
        : ideasService.update(idea!.id, { ...v, technology_ids: techIds, skill_ids: skillIds }),
    onSuccess: () => {
      toast.success(mode === "create" ? "Idea created" : "Idea updated");
      qc.invalidateQueries({ queryKey: ["ideas"] });
      onDone();
    },
    onError: (e) => toast.error(extractApiError(e)),
  });

  return (
    <DialogContent className="max-w-lg">
      <DialogHeader><DialogTitle>{mode === "create" ? "New idea" : "Edit idea"}</DialogTitle></DialogHeader>
      <form onSubmit={form.handleSubmit((v) => mutation.mutate(v))} className="space-y-3">
        <div className="space-y-1.5"><Label>Title</Label><Input {...form.register("title")} /></div>
        <div className="space-y-1.5"><Label>Description</Label><Textarea rows={4} {...form.register("description")} /></div>
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1.5">
            <Label>Domain</Label>
            <Select defaultValue={idea?.domain.id} onValueChange={(v) => form.setValue("domain_id", v)}>
              <SelectTrigger><SelectValue placeholder="Select" /></SelectTrigger>
              <SelectContent>
                {(domains ?? []).map((d) => <SelectItem key={d.id} value={d.id}>{d.name}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-1.5">
            <Label>Difficulty</Label>
            <Select defaultValue={idea?.difficulty ?? "Intermediate"} onValueChange={(v) => form.setValue("difficulty", v)}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="Beginner">Beginner</SelectItem>
                <SelectItem value="Intermediate">Intermediate</SelectItem>
                <SelectItem value="Advanced">Advanced</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
        <div className="space-y-1.5">
          <Label>Max students</Label>
          <Input type="number" min={1} max={5} {...form.register("max_students", { valueAsNumber: true })} />
        </div>
        <div className="space-y-1.5">
          <Label>Technologies</Label>
          <MultiSelect options={(techs ?? []).map((t) => ({ value: t.id, label: t.name }))} value={techIds} onChange={setTechIds} placeholder="Select technologies" />
        </div>
        <div className="space-y-1.5">
          <Label>Required skills</Label>
          <MultiSelect options={(skills ?? []).map((s) => ({ value: s.id, label: s.name }))} value={skillIds} onChange={setSkillIds} placeholder="Select skills" />
        </div>
        <DialogFooter>
          <Button type="submit" disabled={mutation.isPending}>{mode === "create" ? "Create" : "Save"}</Button>
        </DialogFooter>
      </form>
    </DialogContent>
  );
}
