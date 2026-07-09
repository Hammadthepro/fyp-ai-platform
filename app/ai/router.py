from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import (
    RecommendationResponse,
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


# ----------------------------------------------------
# AI Recommendation
# ----------------------------------------------------

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


# ----------------------------------------------------
# AI Idea Generator
# ----------------------------------------------------

@router.post("/generate-idea")
async def generate_idea(
    data: IdeaGeneratorRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    prompt = (
        f"{data.domain}\n"
        f"{data.skills}\n"
        f"{data.technologies}"
    )

    return {
        "result": service.generate_text(
            prompt=prompt,
            temperature=0.8,
        )
    }


# ----------------------------------------------------
# AI Proposal Generator
# ----------------------------------------------------

@router.post("/generate-proposal")
async def generate_proposal(
    data: ProposalGeneratorRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    prompt = (
        f"Title: {data.title}\n"
        f"Description: {data.description}"
    )

    return {
        "result": service.generate_text(
            prompt=prompt,
            temperature=0.4,
        )
    }


# ----------------------------------------------------
# AI Viva Questions
# ----------------------------------------------------

@router.post("/generate-viva")
async def generate_viva(
    data: VivaGeneratorRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    prompt = (
        f"Project Title: {data.title}\n"
        f"Description: {data.description}"
    )

    return {
        "result": service.generate_text(
            prompt=prompt,
            temperature=0.5,
        )
    }


# ----------------------------------------------------
# Weekly Report Generator
# ----------------------------------------------------

@router.post("/weekly-report")
async def weekly_report(
    data: WeeklyReportRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    prompt = (
        f"Project: {data.project}\n"
        f"Completed Work:\n{data.completed_work}\n"
        f"Next Week:\n{data.next_plan}"
    )

    return {
        "result": service.generate_text(
            prompt=prompt,
            temperature=0.4,
        )
    }


# ----------------------------------------------------
# Meeting Minutes Generator
# ----------------------------------------------------

@router.post("/meeting-minutes")
async def meeting_minutes(
    data: MeetingMinutesRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    return {
        "result": service.generate_text(
            prompt=data.transcript,
            temperature=0.3,
        )
    }


# ----------------------------------------------------
# Documentation Generator
# ----------------------------------------------------

@router.post("/documentation")
async def documentation(
    data: DocumentationRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)

    prompt = (
        f"Project Title: {data.title}\n"
        f"Description:\n{data.description}"
    )

    return {
        "result": service.generate_text(
            prompt=prompt,
            temperature=0.3,
        )
    }