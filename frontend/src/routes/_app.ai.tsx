import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { Copy, Loader2, Sparkles } from "lucide-react";
import toast from "react-hot-toast";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { aiService } from "@/services/ai.service";
import { extractApiError } from "@/lib/api";
import type { AITextResponse } from "@/types/api";

export const Route = createFileRoute("/_app/ai")({ component: AIStudio });

function AIStudio() {
  return (
    <div>
      <PageHeader
        title="AI Studio"
        description="Generate ideas, proposals, docs, reviews and more — powered by your backend AI."
      />
      <Tabs defaultValue="generators" className="w-full">
        <TabsList className="flex flex-wrap">
          <TabsTrigger value="generators">Generators</TabsTrigger>
          <TabsTrigger value="reviews">Reviews</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
        </TabsList>
        <TabsContent value="generators" className="grid grid-cols-1 gap-4 pt-4 md:grid-cols-2">
          <IdeaGenerator />
          <ProposalGenerator />
          <DocGenerator title="Documentation" fn={aiService.generateDocumentation} />
          <DocGenerator title="Viva questions" fn={aiService.generateViva} />
          <DocGenerator title="Project timeline" fn={aiService.projectTimeline} />
          <DocGenerator title="Roadmap" fn={aiService.roadmap} />
          <DocGenerator title="Sprint plan" fn={aiService.sprintPlan} />
          <WeeklyReport />
          <MeetingMinutes />
        </TabsContent>
        <TabsContent value="reviews" className="grid grid-cols-1 gap-4 pt-4 md:grid-cols-2">
          <ReviewProposal />
          <ReviewMilestone />
          <EvaluateSubmission />
          <ReviewCode />
        </TabsContent>
        <TabsContent value="insights" className="grid grid-cols-1 gap-4 pt-4 md:grid-cols-2">
          <Insight title="Recommendations" fn={async () => {
            const r = await aiService.recommendations();
            return { result: r.recommendations.map((x) => `• ${x.title} (${x.match_score}%) — ${x.reason}`).join("\n") };
          }} />
          <Insight title="Project summary" fn={aiService.projectSummary} />
          <Insight title="Progress analysis" fn={aiService.progressAnalysis} />
          <Insight title="Risk prediction" fn={aiService.predictRisks} />
          <Insight title="Supervisor assistant" fn={aiService.supervisorAssistant} />
          <Insight title="Team analysis" fn={aiService.teamAnalysis} />
          <Insight title="Dashboard AI" fn={aiService.dashboardAi} />
          <ProjectChat />
        </TabsContent>
      </Tabs>
    </div>
  );
}

function ResultBlock({ text }: { text: string }) {
  return (
    <div className="mt-3 rounded-md border border-border/60 bg-muted/40 p-3">
      <div className="flex items-center justify-between">
        <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Result</p>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => {
            navigator.clipboard.writeText(text);
            toast.success("Copied");
          }}
        >
          <Copy className="h-3 w-3" />
        </Button>
      </div>
      <pre className="mt-2 max-h-64 overflow-auto whitespace-pre-wrap text-xs">{text}</pre>
    </div>
  );
}

function AICard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <Card className="border-border/60">
      <CardHeader className="flex flex-row items-center gap-2 pb-3">
        <Sparkles className="h-4 w-4 text-primary" />
        <CardTitle className="text-sm">{title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">{children}</CardContent>
    </Card>
  );
}

function IdeaGenerator() {
  const [domain, setDomain] = useState("");
  const [technologies, setTechnologies] = useState("");
  const [difficulty, setDifficulty] = useState("Intermediate");
  const [total, setTotal] = useState(5);
  const mut = useMutation({
    mutationFn: () =>
      aiService.generateIdea({
        domain,
        technologies: technologies.split(",").map((t) => t.trim()).filter(Boolean),
        difficulty,
        total,
      }),
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <AICard title="Idea generator">
      <Label className="text-xs">Domain</Label>
      <Input value={domain} onChange={(e) => setDomain(e.target.value)} />
      <Label className="text-xs">Technologies (comma-separated)</Label>
      <Input value={technologies} onChange={(e) => setTechnologies(e.target.value)} />
      <div className="grid grid-cols-2 gap-2">
        <div>
          <Label className="text-xs">Difficulty</Label>
          <Select value={difficulty} onValueChange={setDifficulty}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="Beginner">Beginner</SelectItem>
              <SelectItem value="Intermediate">Intermediate</SelectItem>
              <SelectItem value="Advanced">Advanced</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div>
          <Label className="text-xs">Total</Label>
          <Input type="number" value={total} onChange={(e) => setTotal(Number(e.target.value))} />
        </div>
      </div>
      <Button size="sm" disabled={!domain || mut.isPending} onClick={() => mut.mutate()}>
        {mut.isPending && <Loader2 className="mr-2 h-3 w-3 animate-spin" />} Generate
      </Button>
      {mut.data && <ResultBlock text={mut.data.result} />}
    </AICard>
  );
}

function TitleDescForm({
  title,
  fn,
}: {
  title: string;
  fn: (p: { title: string; description: string }) => Promise<AITextResponse>;
}) {
  const [t, setT] = useState("");
  const [d, setD] = useState("");
  const mut = useMutation({
    mutationFn: () => fn({ title: t, description: d }),
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <AICard title={title}>
      <Label className="text-xs">Title</Label>
      <Input value={t} onChange={(e) => setT(e.target.value)} />
      <Label className="text-xs">Description</Label>
      <Textarea rows={3} value={d} onChange={(e) => setD(e.target.value)} />
      <Button size="sm" disabled={!t || !d || mut.isPending} onClick={() => mut.mutate()}>
        {mut.isPending && <Loader2 className="mr-2 h-3 w-3 animate-spin" />} Generate
      </Button>
      {mut.data && <ResultBlock text={mut.data.result} />}
    </AICard>
  );
}

const ProposalGenerator = () => <TitleDescForm title="Proposal generator" fn={aiService.generateProposal} />;
const DocGenerator = ({ title, fn }: { title: string; fn: (p: { title: string; description: string }) => Promise<AITextResponse> }) =>
  <TitleDescForm title={title} fn={fn} />;
const ReviewProposal = () => <TitleDescForm title="Review proposal" fn={aiService.reviewProposal} />;

function WeeklyReport() {
  const [w, setW] = useState(1);
  const [c, setC] = useState("");
  const [p, setP] = useState("");
  const [i, setI] = useState("");
  const mut = useMutation({
    mutationFn: () => aiService.weeklyReport({ week: w, completed: c, pending: p, issues: i }),
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <AICard title="Weekly report">
      <Label className="text-xs">Week</Label>
      <Input type="number" value={w} onChange={(e) => setW(Number(e.target.value))} />
      <Label className="text-xs">Completed</Label>
      <Textarea rows={2} value={c} onChange={(e) => setC(e.target.value)} />
      <Label className="text-xs">Pending</Label>
      <Textarea rows={2} value={p} onChange={(e) => setP(e.target.value)} />
      <Label className="text-xs">Issues</Label>
      <Textarea rows={2} value={i} onChange={(e) => setI(e.target.value)} />
      <Button size="sm" disabled={mut.isPending} onClick={() => mut.mutate()}>Generate</Button>
      {mut.data && <ResultBlock text={mut.data.result} />}
    </AICard>
  );
}

function MeetingMinutes() {
  const [t, setT] = useState("");
  const [n, setN] = useState("");
  const mut = useMutation({
    mutationFn: () => aiService.meetingMinutes({ meeting_title: t, notes: n }),
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <AICard title="Meeting minutes">
      <Label className="text-xs">Meeting title</Label>
      <Input value={t} onChange={(e) => setT(e.target.value)} />
      <Label className="text-xs">Notes</Label>
      <Textarea rows={4} value={n} onChange={(e) => setN(e.target.value)} />
      <Button size="sm" disabled={mut.isPending} onClick={() => mut.mutate()}>Generate</Button>
      {mut.data && <ResultBlock text={mut.data.result} />}
    </AICard>
  );
}

function ReviewMilestone() {
  const [m, setM] = useState("");
  const [s, setS] = useState("");
  const mut = useMutation({
    mutationFn: () => aiService.reviewMilestone(m, s),
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <AICard title="Review milestone">
      <Label className="text-xs">Milestone</Label>
      <Textarea rows={2} value={m} onChange={(e) => setM(e.target.value)} />
      <Label className="text-xs">Submission</Label>
      <Textarea rows={2} value={s} onChange={(e) => setS(e.target.value)} />
      <Button size="sm" disabled={mut.isPending} onClick={() => mut.mutate()}>Review</Button>
      {mut.data && <ResultBlock text={mut.data.result} />}
    </AICard>
  );
}

function EvaluateSubmission() {
  const [t, setT] = useState("");
  const [d, setD] = useState("");
  const [s, setS] = useState("");
  const mut = useMutation({
    mutationFn: () => aiService.evaluateSubmission({ title: t, description: d }, s),
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <AICard title="Evaluate submission">
      <Label className="text-xs">Title</Label>
      <Input value={t} onChange={(e) => setT(e.target.value)} />
      <Label className="text-xs">Description</Label>
      <Textarea rows={2} value={d} onChange={(e) => setD(e.target.value)} />
      <Label className="text-xs">Submission</Label>
      <Textarea rows={2} value={s} onChange={(e) => setS(e.target.value)} />
      <Button size="sm" disabled={mut.isPending} onClick={() => mut.mutate()}>Evaluate</Button>
      {mut.data && <ResultBlock text={mut.data.result} />}
    </AICard>
  );
}

function ReviewCode() {
  const [lang, setLang] = useState("python");
  const [code, setCode] = useState("");
  const mut = useMutation({
    mutationFn: () => aiService.reviewCode(lang, code),
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <AICard title="Code review">
      <Label className="text-xs">Language</Label>
      <Input value={lang} onChange={(e) => setLang(e.target.value)} />
      <Label className="text-xs">Code</Label>
      <Textarea rows={6} value={code} onChange={(e) => setCode(e.target.value)} className="font-mono text-xs" />
      <Button size="sm" disabled={!code || mut.isPending} onClick={() => mut.mutate()}>Review</Button>
      {mut.data && <ResultBlock text={mut.data.result} />}
    </AICard>
  );
}

function Insight({ title, fn }: { title: string; fn: () => Promise<AITextResponse> }) {
  const q = useQuery({ queryKey: ["ai-insight", title], queryFn: fn, enabled: false });
  return (
    <AICard title={title}>
      <Button size="sm" onClick={() => q.refetch()} disabled={q.isFetching}>
        {q.isFetching && <Loader2 className="mr-2 h-3 w-3 animate-spin" />} Run
      </Button>
      {q.data && <ResultBlock text={q.data.result} />}
    </AICard>
  );
}

function ProjectChat() {
  const [q, setQ] = useState("");
  const mut = useMutation({
    mutationFn: () => aiService.projectChat(q),
    onError: (e) => toast.error(extractApiError(e)),
  });
  return (
    <AICard title="Project chat">
      <Label className="text-xs">Question</Label>
      <Textarea rows={3} value={q} onChange={(e) => setQ(e.target.value)} />
      <Button size="sm" disabled={!q || mut.isPending} onClick={() => mut.mutate()}>Ask</Button>
      {mut.data && <ResultBlock text={mut.data.result} />}
    </AICard>
  );
}
