// Types mirror FastAPI backend schemas exactly.
// Do NOT invent fields — every field maps to a Pydantic model in the backend.

export type UUID = string;
export type ISODateString = string;

export type UserRole = "student" | "professor" | "admin";

// ---------- Auth ----------
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: UUID;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
}

export interface StudentRegisterPayload {
  email: string;
  password: string;
  full_name: string;
  registration_number: string;
  department: string;
  semester: number;
  phone?: string | null;
}

export interface ProfessorRegisterPayload {
  email: string;
  password: string;
  full_name: string;
  employee_id: string;
  designation: string;
  office?: string | null;
  bio?: string | null;
  research_interests?: string | null;
  max_groups?: number;
}

// ---------- Profile ----------
export interface StudentProfileResponse {
  id: UUID;
  registration_number: string;
  department: string;
  semester: number;
  phone: string | null;
  github: string | null;
  linkedin: string | null;
  portfolio: string | null;
}

export interface StudentProfileUpdate {
  phone?: string | null;
  github?: string | null;
  linkedin?: string | null;
  portfolio?: string | null;
  skill_ids?: UUID[];
  domain_ids?: UUID[];
}

export interface ProfessorProfileResponse {
  id: UUID;
  employee_id: string;
  designation: string;
  office: string | null;
  bio: string | null;
  research_interests: string | null;
  available_slots: number;
}

export interface ProfessorProfileUpdate {
  office?: string | null;
  bio?: string | null;
  research_interests?: string | null;
  available_slots?: number | null;
  skill_ids?: UUID[];
  domain_ids?: UUID[];
}

// ---------- Master ----------
export interface NamedEntity {
  id: UUID;
  name: string;
}
export type SkillResponse = NamedEntity;
export type DomainResponse = NamedEntity;
export type TechnologyResponse = NamedEntity;

// ---------- Ideas ----------
export interface IdeaSkill {
  skill: NamedEntity;
}
export interface IdeaTechnology {
  technology: NamedEntity;
}
export interface IdeaResponse {
  id: UUID;
  title: string;
  description: string;
  difficulty: string;
  max_students: number;
  is_active: boolean;
  created_at: ISODateString;
  domain: NamedEntity;
  skills: IdeaSkill[];
  technologies: IdeaTechnology[];
}
export interface IdeaCreate {
  title: string;
  description: string;
  domain_id: UUID;
  difficulty?: string;
  max_students?: number;
  technology_ids?: UUID[];
  skill_ids?: UUID[];
}
export interface IdeaUpdate {
  title?: string;
  description?: string;
  domain_id?: UUID;
  difficulty?: string;
  max_students?: number;
  technology_ids?: UUID[];
  skill_ids?: UUID[];
  is_active?: boolean;
}
export interface IdeaListParams {
  keyword?: string;
  domain_id?: UUID;
  difficulty?: string;
  technology_id?: UUID;
  skill_id?: UUID;
  professor?: string;
  newest?: boolean;
}

// ---------- Groups ----------
export interface StudentSimple {
  id: UUID;
  registration_number: string;
  semester: number;
}
export interface GroupMemberResponse {
  student: StudentSimple;
}
export interface GroupResponse {
  id: UUID;
  name: string;
  created_at: ISODateString;
  members: GroupMemberResponse[];
}
export interface InvitationResponse {
  id: UUID;
  group_id: UUID;
  student_id: UUID;
  status: string;
}

// ---------- Proposals ----------
export interface ProposalCreate {
  professor_id: UUID;
  title: string;
  abstract: string;
  objectives: string;
}
export interface ProposalResponse {
  id: UUID;
  group_id: UUID;
  professor_id: UUID;
  title: string;
  abstract: string;
  objectives: string;
  status: string;
  feedback: string | null;
  created_at: ISODateString;
}

// ---------- Milestones ----------
export interface MilestoneCreate {
  title: string;
  description: string;
  due_date: ISODateString;
}
export interface MilestoneUpdate {
  title?: string;
  description?: string;
  due_date?: ISODateString;
  status?: string;
  feedback?: string;
}
export interface MilestoneResponse {
  id: UUID;
  group_id: UUID;
  title: string;
  description: string;
  due_date: ISODateString;
  status: string;
  feedback: string | null;
  created_at: ISODateString;
}

// ---------- Submissions ----------
export interface SubmissionCreate {
  milestone_id: UUID;
  github_link?: string | null;
  drive_link?: string | null;
  notes?: string | null;
}
export interface SubmissionUpdate {
  status: string;
  feedback?: string | null;
  marks?: number | null;
}
export interface SubmissionResponse {
  id: UUID;
  milestone_id: UUID;
  submitted_by: UUID;
  github_link: string | null;
  drive_link: string | null;
  notes: string | null;
  feedback: string | null;
  marks: number | null;
  status: string;
  created_at: ISODateString;
  updated_at: ISODateString;
}

// ---------- Dashboard ----------
export interface StudentDashboardResponse {
  student_name: string;
  department: string;
  semester: number;
  group_name: string | null;
  progress: number;
  completed_milestones: number;
  total_milestones: number;
  proposal: {
    id: UUID;
    title: string;
    status: string;
    professor: string | null;
  } | null;
  milestones: Array<{
    id: UUID;
    title: string;
    due_date: ISODateString;
    status: string;
  }>;
  notifications: Array<{
    id: UUID;
    title: string;
    message: string;
    type: string;
    is_read: boolean;
    created_at: ISODateString;
  }>;
}

export interface ProfessorDashboardResponse {
  professor_name: string;
  total_groups: number;
  total_proposals: number;
  pending_proposals: number;
  approved_proposals: number;
  rejected_proposals: number;
  proposals: Array<{
    id: UUID;
    title: string;
    group_name: string | null;
    status: string;
  }>;
}

export interface AdminDashboardResponse {
  students: number;
  professors: number;
  groups: number;
  ideas: number;
  proposals: number;
  approved: number;
  pending: number;
  rejected: number;
  milestones: number;
  submissions: number;
}

export interface AdminAnalyticsResponse {
  dashboard: AdminDashboardResponse;
  recent_users: Array<{ id: UUID; name: string; email: string; role: string }>;
  recent_groups: Array<{ id: UUID; name: string }>;
  recent_proposals: Array<{ id: UUID; title: string; status: string }>;
  recent_submissions: Array<{ id: UUID; student: string; milestone: string }>;
}

// ---------- Notifications ----------
export interface NotificationResponse {
  id: UUID;
  title: string;
  message: string;
  type: string;
  is_read: boolean;
  created_at: ISODateString;
}

// ---------- Calendar ----------
export interface CalendarEventResponse {
  id: UUID;
  title: string;
  description: string | null;
  event_type: string;
  start_date: ISODateString;
  end_date: ISODateString | null;
  is_all_day: boolean;
  group_id: UUID | null;
  created_by: UUID;
  created_at: ISODateString;
}
export interface CalendarEventCreate {
  title: string;
  description?: string | null;
  event_type?: string;
  start_date: ISODateString;
  end_date?: ISODateString | null;
  group_id?: UUID | null;
  is_all_day?: boolean;
}
export interface CalendarEventUpdate {
  title?: string | null;
  description?: string | null;
  event_type?: string | null;
  start_date?: ISODateString | null;
  end_date?: ISODateString | null;
  is_all_day?: boolean | null;
}

// ---------- Chat ----------
export interface ChatRoomResponse {
  id: UUID;
  group_id: UUID;
  name: string;
  created_at: ISODateString;
}
export interface ChatMessageResponse {
  id: UUID;
  room_id: UUID;
  sender_id: UUID;
  message: string;
  is_ai: boolean;
  created_at: ISODateString;
}
export interface ChatRoomCreate {
  group_id: UUID;
  name: string;
}
export interface ChatMessageCreate {
  room_id: UUID;
  message: string;
}
export interface WSChatMessage {
  id: string;
  room_id: string;
  sender_id: string;
  sender_name: string;
  message: string;
  created_at: string;
}

// ---------- AI ----------
export interface AITextResponse {
  result: string;
}
export interface Recommendation {
  idea_id: UUID;
  title: string;
  match_score: number;
  reason: string;
  missing_skills: string[];
}
export interface RecommendationResponse {
  recommendations: Recommendation[];
}
export interface IdeaGeneratorRequest {
  domain: string;
  technologies: string[];
  difficulty: string;
  total?: number;
}
export interface DocumentationRequest {
  title: string;
  description: string;
}
export interface ProposalGeneratorRequest {
  title: string;
  description: string;
}
export interface VivaGeneratorRequest {
  title: string;
  description: string;
}
export interface WeeklyReportRequest {
  week: number;
  completed: string;
  pending: string;
  issues: string;
}
export interface MeetingMinutesRequest {
  meeting_title: string;
  notes: string;
}
