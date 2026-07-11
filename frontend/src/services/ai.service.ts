import { api } from "@/lib/api";
import type {
  AITextResponse,
  DocumentationRequest,
  IdeaGeneratorRequest,
  MeetingMinutesRequest,
  ProposalGeneratorRequest,
  RecommendationResponse,
  VivaGeneratorRequest,
  WeeklyReportRequest,
} from "@/types/api";

const post = async <T>(path: string, body?: unknown, params?: Record<string, unknown>) =>
  (await api.post<T>(path, body, { params })).data;
const get = async <T>(path: string) => (await api.get<T>(path)).data;

export const aiService = {
  recommendations: () => get<RecommendationResponse>("/ai/recommendations"),
  generateIdea: (payload: IdeaGeneratorRequest) =>
    post<AITextResponse>("/ai/generate-idea", payload),
  generateProposal: (payload: ProposalGeneratorRequest) =>
    post<AITextResponse>("/ai/generate-proposal", payload),
  generateDocumentation: (payload: DocumentationRequest) =>
    post<AITextResponse>("/ai/generate-documentation", payload),
  generateViva: (payload: VivaGeneratorRequest) =>
    post<AITextResponse>("/ai/generate-viva", payload),
  weeklyReport: (payload: WeeklyReportRequest) =>
    post<AITextResponse>("/ai/generate-weekly-report", payload),
  meetingMinutes: (payload: MeetingMinutesRequest) =>
    post<AITextResponse>("/ai/generate-meeting-minutes", payload),
  documentation: (payload: DocumentationRequest) =>
    post<AITextResponse>("/ai/documentation", payload),
  projectSummary: () => get<AITextResponse>("/ai/project-summary"),
  projectTimeline: (payload: DocumentationRequest) =>
    post<AITextResponse>("/ai/project-timeline", payload),
  // NOTE: backend defines `project-chat` with `question` as a raw query param
  projectChat: (question: string) =>
    post<AITextResponse>("/ai/project-chat", undefined, { question }),
  roadmap: (payload: DocumentationRequest) => post<AITextResponse>("/ai/roadmap", payload),
  sprintPlan: (payload: DocumentationRequest) => post<AITextResponse>("/ai/sprint-plan", payload),
  dashboardAi: () => get<AITextResponse>("/ai/dashboard-ai"),
  reviewProposal: (payload: ProposalGeneratorRequest) =>
    post<AITextResponse>("/ai/review-proposal", payload),
  reviewMilestone: (milestone: string, submission: string) =>
    post<AITextResponse>("/ai/review-milestone", undefined, { milestone, submission }),
  evaluateSubmission: (payload: DocumentationRequest, submission: string) =>
    post<AITextResponse>("/ai/evaluate-submission", payload, { submission }),
  reviewCode: (language: string, code: string) =>
    post<AITextResponse>("/ai/review-code", undefined, { language, code }),
  progressAnalysis: () => get<AITextResponse>("/ai/progress-analysis"),
  predictRisks: () => get<AITextResponse>("/ai/predict-risks"),
  supervisorAssistant: () => get<AITextResponse>("/ai/supervisor-assistant"),
  teamAnalysis: () => get<AITextResponse>("/ai/team-analysis"),
};
