import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";
import toast from "react-hot-toast";
import { motion } from "framer-motion";
import { Loader2, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { authService } from "@/services/auth.service";
import { useAuth } from "@/contexts/AuthContext";
import { extractApiError } from "@/lib/api";

const studentSchema = z.object({
  full_name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8, "Min 8 characters"),
  registration_number: z.string().min(2),
  department: z.string().min(2),
  semester: z.number().int().min(1).max(12),
  phone: z.string().optional().or(z.literal("")),
});
type StudentForm = z.infer<typeof studentSchema>;

const professorSchema = z.object({
  full_name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8),
  employee_id: z.string().min(2),
  designation: z.string().min(2),
  office: z.string().optional().or(z.literal("")),
  bio: z.string().optional().or(z.literal("")),
  research_interests: z.string().optional().or(z.literal("")),
  max_groups: z.number().int().min(1).max(50),
});
type ProfessorForm = z.infer<typeof professorSchema>;

export const Route = createFileRoute("/register")({ component: RegisterPage });

function RegisterPage() {
  const [tab, setTab] = useState<"student" | "professor">("student");
  const navigate = useNavigate();
  const { setToken } = useAuth();
  const [submitting, setSubmitting] = useState(false);

  const student = useForm<StudentForm>({ resolver: zodResolver(studentSchema) });
  const professor = useForm<ProfessorForm>({
    resolver: zodResolver(professorSchema),
    defaultValues: { max_groups: 10 },
  });

  async function onStudent(data: StudentForm) {
    setSubmitting(true);
    try {
      const res = await authService.registerStudent({
        ...data,
        phone: data.phone || null,
      });
      await setToken(res.access_token);
      toast.success("Account created");
      void navigate({ to: "/dashboard" });
    } catch (err) {
      toast.error(extractApiError(err, "Registration failed"));
    } finally {
      setSubmitting(false);
    }
  }

  async function onProfessor(data: ProfessorForm) {
    setSubmitting(true);
    try {
      const res = await authService.registerProfessor({
        ...data,
        office: data.office || null,
        bio: data.bio || null,
        research_interests: data.research_interests || null,
      });
      await setToken(res.access_token);
      toast.success("Account created");
      void navigate({ to: "/dashboard" });
    } catch (err) {
      toast.error(extractApiError(err, "Registration failed"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background px-4 py-10">
      <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_20%_10%,rgba(99,102,241,0.15),transparent_40%),radial-gradient(circle_at_80%_90%,rgba(168,85,247,0.15),transparent_40%)]" />
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-xl">
        <Card className="border-border/60 bg-card/60 backdrop-blur">
          <CardHeader className="text-center">
            <div className="mx-auto mb-2 flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 text-white shadow">
              <Sparkles className="h-5 w-5" />
            </div>
            <CardTitle className="text-2xl">Create your account</CardTitle>
            <CardDescription>Join the FYP Platform</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={tab} onValueChange={(v) => setTab(v as "student" | "professor")}>
              <TabsList className="grid grid-cols-2">
                <TabsTrigger value="student">Student</TabsTrigger>
                <TabsTrigger value="professor">Professor</TabsTrigger>
              </TabsList>
              <TabsContent value="student" className="pt-4">
                <form onSubmit={student.handleSubmit(onStudent)} className="grid grid-cols-1 gap-3 md:grid-cols-2">
                  <Field label="Full name" error={student.formState.errors.full_name?.message}>
                    <Input {...student.register("full_name")} />
                  </Field>
                  <Field label="Email" error={student.formState.errors.email?.message}>
                    <Input type="email" {...student.register("email")} />
                  </Field>
                  <Field label="Password" error={student.formState.errors.password?.message}>
                    <Input type="password" {...student.register("password")} />
                  </Field>
                  <Field label="Registration #" error={student.formState.errors.registration_number?.message}>
                    <Input {...student.register("registration_number")} />
                  </Field>
                  <Field label="Department" error={student.formState.errors.department?.message}>
                    <Input {...student.register("department")} />
                  </Field>
                  <Field label="Semester" error={student.formState.errors.semester?.message}>
                    <Input type="number" {...student.register("semester", { valueAsNumber: true })} />
                  </Field>
                  <Field label="Phone (optional)">
                    <Input {...student.register("phone")} />
                  </Field>
                  <div className="md:col-span-2">
                    <Button className="w-full" type="submit" disabled={submitting}>
                      {submitting ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                      Create student account
                    </Button>
                  </div>
                </form>
              </TabsContent>
              <TabsContent value="professor" className="pt-4">
                <form onSubmit={professor.handleSubmit(onProfessor)} className="grid grid-cols-1 gap-3 md:grid-cols-2">
                  <Field label="Full name" error={professor.formState.errors.full_name?.message}>
                    <Input {...professor.register("full_name")} />
                  </Field>
                  <Field label="Email" error={professor.formState.errors.email?.message}>
                    <Input type="email" {...professor.register("email")} />
                  </Field>
                  <Field label="Password" error={professor.formState.errors.password?.message}>
                    <Input type="password" {...professor.register("password")} />
                  </Field>
                  <Field label="Employee ID" error={professor.formState.errors.employee_id?.message}>
                    <Input {...professor.register("employee_id")} />
                  </Field>
                  <Field label="Designation" error={professor.formState.errors.designation?.message}>
                    <Input {...professor.register("designation")} />
                  </Field>
                  <Field label="Office">
                    <Input {...professor.register("office")} />
                  </Field>
                  <Field label="Max groups">
                    <Input type="number" {...professor.register("max_groups", { valueAsNumber: true })} />
                  </Field>
                  <Field label="Research interests" className="md:col-span-2">
                    <Input {...professor.register("research_interests")} />
                  </Field>
                  <Field label="Bio" className="md:col-span-2">
                    <Input {...professor.register("bio")} />
                  </Field>
                  <div className="md:col-span-2">
                    <Button className="w-full" type="submit" disabled={submitting}>
                      {submitting ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
                      Create professor account
                    </Button>
                  </div>
                </form>
              </TabsContent>
            </Tabs>
            <p className="mt-4 text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link to="/login" className="text-primary underline-offset-4 hover:underline">
                Sign in
              </Link>
            </p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}

function Field({
  label,
  error,
  className,
  children,
}: {
  label: string;
  error?: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div className={"space-y-1.5 " + (className ?? "")}>
      <Label className="text-xs uppercase tracking-wide text-muted-foreground">{label}</Label>
      {children}
      {error && <p className="text-xs text-destructive">{error}</p>}
    </div>
  );
}
