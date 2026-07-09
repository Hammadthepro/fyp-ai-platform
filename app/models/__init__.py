from .user import User
from .student import Student
from .professor import Professor
from .fyp_idea import FYPIdea
from .technology import Technology
from .skill import Skill
from .domain import Domain
from app.models.idea_skill import IdeaSkill
from app.models.idea_technology import IdeaTechnology
from .student_skill import StudentSkill
from .student_domain import StudentDomain
from .professor_skill import ProfessorSkill
from .professor_domain import ProfessorDomain
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.group_invitation import GroupInvitation
from app.models.proposal import Proposal
from app.models.milestone import Milestone
from app.models.submission import Submission
from app.models.notification import Notification

__all__ = [
    "User",
    "Student",
    "Professor",
]