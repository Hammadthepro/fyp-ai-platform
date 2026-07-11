from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# ==========================================================
# COMMON
# ==========================================================

class DashboardStat(BaseModel):
    title: str
    value: int


class NotificationItem(BaseModel):
    id: UUID
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime


class MilestoneItem(BaseModel):
    id: UUID
    title: str
    due_date: datetime
    status: str


class SubmissionItem(BaseModel):
    id: UUID
    milestone: str
    submitted_at: datetime | None = None
    status: str | None = None


class ProposalItem(BaseModel):
    id: UUID
    title: str
    status: str
    professor: str | None = None


class GroupMemberItem(BaseModel):
    id: UUID
    name: str


# ==========================================================
# STUDENT DASHBOARD
# ==========================================================

class StudentDashboardResponse(BaseModel):

    student_name: str

    department: str

    semester: int

    group_name: str | None = None

    progress: float

    completed_milestones: int

    total_milestones: int

    proposal: ProposalItem | None = None

    milestones: list[MilestoneItem] = []

    notifications: list[NotificationItem] = []


# ==========================================================
# PROFESSOR DASHBOARD
# ==========================================================

class ProfessorProposalItem(BaseModel):

    id: UUID

    title: str

    group_name: str | None = None

    status: str


class ProfessorDashboardResponse(BaseModel):

    professor_name: str

    total_groups: int

    total_proposals: int

    pending_proposals: int

    approved_proposals: int

    rejected_proposals: int

    proposals: list[ProfessorProposalItem] = []


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

class AdminDashboardResponse(BaseModel):

    students: int

    professors: int

    groups: int

    ideas: int

    proposals: int

    approved: int

    pending: int

    rejected: int

    milestones: int

    submissions: int


# ==========================================================
# RECENT ACTIVITY
# ==========================================================

class RecentUser(BaseModel):

    id: UUID

    name: str

    email: str

    role: str


class RecentProposal(BaseModel):

    id: UUID

    title: str

    status: str


class RecentSubmission(BaseModel):

    id: UUID

    student: str

    milestone: str


class RecentGroup(BaseModel):

    id: UUID

    name: str


class AdminAnalyticsResponse(BaseModel):

    dashboard: AdminDashboardResponse

    recent_users: list[RecentUser] = []

    recent_groups: list[RecentGroup] = []

    recent_proposals: list[RecentProposal] = []

    recent_submissions: list[RecentSubmission] = []