import { createFileRoute } from "@tanstack/react-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { useState, useEffect } from "react";
import toast from "react-hot-toast";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { MultiSelect } from "@/components/common/MultiSelect";
import { useAuth } from "@/contexts/AuthContext";
import { profileService } from "@/services/profile.service";
import { masterService } from "@/services/master.service";
import { extractApiError } from "@/lib/api";

export const Route = createFileRoute("/_app/profile")({ component: ProfilePage });

function ProfilePage() {
  const { role } = useAuth();
  return (
    <div>
      <PageHeader title="Profile" description="Manage your account details." />
      {role === "student" && <StudentProfileForm />}
      {role === "professor" && <ProfessorProfileForm />}
      {role === "admin" && (
        <p className="text-sm text-muted-foreground">Admin has no editable profile.</p>
      )}
    </div>
  );
}

function useMasterOptions() {
  const { data: skills } = useQuery({ queryKey: ["skills"], queryFn: masterService.listSkills });
  const { data: domains } = useQuery({ queryKey: ["domains"], queryFn: masterService.listDomains });
  return {
    skillOptions: (skills ?? []).map((s) => ({ value: s.id, label: s.name })),
    domainOptions: (domains ?? []).map((d) => ({ value: d.id, label: d.name })),
  };
}

function StudentProfileForm() {
  const qc = useQueryClient();
  const { skillOptions, domainOptions } = useMasterOptions();
  const { data, isLoading } = useQuery({ queryKey: ["profile", "student"], queryFn: profileService.getStudent });
  const [skillIds, setSkillIds] = useState<string[]>([]);
  const [domainIds, setDomainIds] = useState<string[]>([]);
  const form = useForm({
    values: {
      phone: data?.phone ?? "",
      github: data?.github ?? "",
      linkedin: data?.linkedin ?? "",
      portfolio: data?.portfolio ?? "",
    },
  });

  if (isLoading || !data) return <Skeleton className="h-64" />;

  return (
    <Card className="border-border/60">
      <CardHeader>
        <CardTitle className="text-sm">
          {data.registration_number} · {data.department} · Semester {data.semester}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form
          onSubmit={form.handleSubmit(async (values) => {
            try {
              await profileService.updateStudent({
                phone: values.phone || null,
                github: values.github || null,
                linkedin: values.linkedin || null,
                portfolio: values.portfolio || null,
                skill_ids: skillIds,
                domain_ids: domainIds,
              });
              toast.success("Profile updated");
              qc.invalidateQueries({ queryKey: ["profile", "student"] });
            } catch (e) {
              toast.error(extractApiError(e));
            }
          })}
          className="grid grid-cols-1 gap-3 md:grid-cols-2"
        >
          <FormField label="Phone"><Input {...form.register("phone")} /></FormField>
          <FormField label="GitHub"><Input placeholder="https://github.com/…" {...form.register("github")} /></FormField>
          <FormField label="LinkedIn"><Input placeholder="https://linkedin.com/in/…" {...form.register("linkedin")} /></FormField>
          <FormField label="Portfolio"><Input placeholder="https://…" {...form.register("portfolio")} /></FormField>
          <FormField label="Skills" className="md:col-span-2">
            <MultiSelect options={skillOptions} value={skillIds} onChange={setSkillIds} placeholder="Add skills" />
          </FormField>
          <FormField label="Domains" className="md:col-span-2">
            <MultiSelect options={domainOptions} value={domainIds} onChange={setDomainIds} placeholder="Add domains" />
          </FormField>
          <div className="md:col-span-2"><Button type="submit">Save changes</Button></div>
        </form>
      </CardContent>
    </Card>
  );
}

function ProfessorProfileForm() {
  const qc = useQueryClient();
  const { skillOptions, domainOptions } = useMasterOptions();
  const { data, isLoading } = useQuery({ queryKey: ["profile", "professor"], queryFn: profileService.getProfessor });
  const [skillIds, setSkillIds] = useState<string[]>([]);
  const [domainIds, setDomainIds] = useState<string[]>([]);
  const form = useForm({
    values: {
      office: data?.office ?? "",
      bio: data?.bio ?? "",
      research_interests: data?.research_interests ?? "",
      available_slots: data?.available_slots ?? 0,
    },
  });

  useEffect(() => { /* keep hooks stable */ }, [data]);

  if (isLoading || !data) return <Skeleton className="h-64" />;

  return (
    <Card className="border-border/60">
      <CardHeader>
        <CardTitle className="text-sm">{data.employee_id} · {data.designation}</CardTitle>
      </CardHeader>
      <CardContent>
        <form
          onSubmit={form.handleSubmit(async (values) => {
            try {
              await profileService.updateProfessor({
                office: values.office || null,
                bio: values.bio || null,
                research_interests: values.research_interests || null,
                available_slots: Number(values.available_slots) || 0,
                skill_ids: skillIds,
                domain_ids: domainIds,
              });
              toast.success("Profile updated");
              qc.invalidateQueries({ queryKey: ["profile", "professor"] });
            } catch (e) {
              toast.error(extractApiError(e));
            }
          })}
          className="grid grid-cols-1 gap-3 md:grid-cols-2"
        >
          <FormField label="Office"><Input {...form.register("office")} /></FormField>
          <FormField label="Available slots">
            <Input type="number" {...form.register("available_slots", { valueAsNumber: true })} />
          </FormField>
          <FormField label="Research interests" className="md:col-span-2"><Input {...form.register("research_interests")} /></FormField>
          <FormField label="Bio" className="md:col-span-2"><Input {...form.register("bio")} /></FormField>
          <FormField label="Skills" className="md:col-span-2">
            <MultiSelect options={skillOptions} value={skillIds} onChange={setSkillIds} placeholder="Add skills" />
          </FormField>
          <FormField label="Domains" className="md:col-span-2">
            <MultiSelect options={domainOptions} value={domainIds} onChange={setDomainIds} placeholder="Add domains" />
          </FormField>
          <div className="md:col-span-2"><Button type="submit">Save changes</Button></div>
        </form>
      </CardContent>
    </Card>
  );
}

function FormField({ label, className, children }: { label: string; className?: string; children: React.ReactNode }) {
  return (
    <div className={"space-y-1.5 " + (className ?? "")}>
      <Label className="text-xs uppercase tracking-wide text-muted-foreground">{label}</Label>
      {children}
    </div>
  );
}
