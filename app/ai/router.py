from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import RecommendationResponse
from app.ai.service import AIService

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


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