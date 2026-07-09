from pydantic import BaseModel


class StudentDashboardResponse(BaseModel):
    student_name: str
    group_name: str | None = None
    proposal_status: str | None = None
    supervisor: str | None = None

    total_milestones: int
    completed_milestones: int
    pending_milestones: int

    total_submissions: int

    progress: int


class ProfessorDashboardResponse(BaseModel):
    professor_name: str

    total_groups: int
    total_students: int

    pending_proposals: int
    pending_submissions: int

    total_milestones: int