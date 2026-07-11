from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import (
    RecommendationResponse,
    AITextResponse,
    IdeaGeneratorRequest,
    ProposalGeneratorRequest,
    VivaGeneratorRequest,
    WeeklyReportRequest,
    MeetingMinutesRequest,
    DocumentationRequest,
)

from app.ai.service import AIService

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

# =====================================================
# AI RECOMMENDATIONS
# =====================================================

@router.get(
    "/recommendations",
    response_model=RecommendationResponse,
)
async def recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return await service.recommend(current_user)


# =====================================================
# SMART IDEA GENERATOR
# =====================================================

@router.post(
    "/generate-idea",
    response_model=AITextResponse,
)
async def generate_idea(
    data: IdeaGeneratorRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return {
        "result": await service.generate_ideas(
            domain=data.domain,
            technologies=data.technologies,
            difficulty=data.difficulty,
            total=data.total,
        )
    }


# =====================================================
# PROPOSAL GENERATOR
# =====================================================

@router.post(
    "/generate-proposal",
    response_model=AITextResponse,
)
async def generate_proposal(
    data: ProposalGeneratorRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return {
        "result": await service.generate_proposal(
            title=data.title,
            description=data.description,
        )
    }


# =====================================================
# DOCUMENTATION GENERATOR
# =====================================================

@router.post(
    "/generate-documentation",
    response_model=AITextResponse,
)
async def generate_documentation(
    data: DocumentationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return {
        "result": await service.generate_documentation(
            title=data.title,
            description=data.description,
        )
    }


# =====================================================
# VIVA QUESTION GENERATOR
# =====================================================

@router.post(
    "/generate-viva",
    response_model=AITextResponse,
)
async def generate_viva(
    data: VivaGeneratorRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return {
        "result": await service.generate_viva(
            title=data.title,
            description=data.description,
        )
    }


# =====================================================
# WEEKLY REPORT
# =====================================================

@router.post(
    "/generate-weekly-report",
    response_model=AITextResponse,
)
async def weekly_report(
    data: WeeklyReportRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return {
        "result": await service.generate_weekly_report(
            title=data.title,
            completed=data.completed,
            pending=data.pending,
            issues=data.issues,
        )
    }


# =====================================================
# MEETING MINUTES
# =====================================================

@router.post(
    "/generate-meeting-minutes",
    response_model=AITextResponse,
)
async def meeting_minutes(
    data: MeetingMinutesRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return {
        "result": await service.generate_meeting_minutes(
            notes=data.notes,
        )
    }


# =====================================================
# PROJECT DOCUMENTATION
# =====================================================

@router.post(
    "/documentation",
    response_model=AITextResponse,
)
async def documentation(
    data: DocumentationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return {
        "result": await service.generate_documentation(
            title=data.title,
            description=data.description,
        )
    }


# =====================================================
# PROJECT SUMMARY
# =====================================================

@router.get(
    "/project-summary",
    response_model=AITextResponse,
)
async def project_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.project_summary(
            current_user
        )
    }


# =====================================================
# PROJECT TIMELINE
# =====================================================

@router.post(
    "/project-timeline",
    response_model=AITextResponse,
)
async def project_timeline(
    data: DocumentationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.generate_project_timeline(
            title=data.title,
            description=data.description,
        )
    }


# =====================================================
# PROJECT CHAT
# =====================================================

@router.post(
    "/project-chat",
    response_model=AITextResponse,
)
async def project_chat(
    question: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.project_chat(
            current_user=current_user,
            question=question,
        )
    }


# =====================================================
# ROADMAP GENERATOR
# =====================================================

@router.post(
    "/roadmap",
    response_model=AITextResponse,
)
async def roadmap(
    data: DocumentationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.roadmap(
            title=data.title,
            description=data.description,
        )
    }


# =====================================================
# SPRINT PLANNER
# =====================================================

@router.post(
    "/sprint-plan",
    response_model=AITextResponse,
)
async def sprint_plan(
    data: DocumentationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.sprint_plan(
            title=data.title,
            description=data.description,
            duration=2,
        )
    }


# =====================================================
# DASHBOARD AI
# =====================================================

@router.get(
    "/dashboard-ai",
    response_model=AITextResponse,
)
async def dashboard_ai(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.dashboard_ai()
    }

# =====================================================
# PROPOSAL REVIEW
# =====================================================

@router.post(
    "/review-proposal",
    response_model=AITextResponse,
)
async def review_proposal(
    data: ProposalGeneratorRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.review_proposal(
            title=data.title,
            abstract=data.description,
            objectives=data.description,
        )
    }


# =====================================================
# MILESTONE REVIEW
# =====================================================

@router.post(
    "/review-milestone",
    response_model=AITextResponse,
)
async def review_milestone(
    milestone: str,
    submission: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.review_milestone(
            milestone=milestone,
            submission=submission,
        )
    }


# =====================================================
# SUBMISSION EVALUATION
# =====================================================

@router.post(
    "/evaluate-submission",
    response_model=AITextResponse,
)
async def evaluate_submission(
    data: DocumentationRequest,
    submission: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.evaluate_submission(
            title=data.title,
            description=data.description,
            submission=submission,
        )
    }


# =====================================================
# CODE REVIEW
# =====================================================

@router.post(
    "/review-code",
    response_model=AITextResponse,
)
async def review_code(
    language: str,
    code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.review_code(
            language=language,
            code=code,
        )
    }


# =====================================================
# PROJECT PROGRESS ANALYSIS
# =====================================================

@router.get(
    "/progress-analysis",
    response_model=AITextResponse,
)
async def progress_analysis(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.analyze_progress(
            current_user
        )
    }


# =====================================================
# RISK PREDICTION
# =====================================================

@router.get(
    "/predict-risks",
    response_model=AITextResponse,
)
async def predict_risks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.predict_risks(
            current_user
        )
    }


# =====================================================
# SUPERVISOR AI ASSISTANT
# =====================================================

@router.get(
    "/supervisor-assistant",
    response_model=AITextResponse,
)
async def supervisor_assistant(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.supervisor_assistant(
            current_user
        )
    }


# =====================================================
# TEAM PERFORMANCE ANALYSIS
# =====================================================

@router.get(
    "/team-analysis",
    response_model=AITextResponse,
)
async def team_analysis(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = AIService(db)

    return {
        "result": await service.team_analysis(
            current_user
        )
    }