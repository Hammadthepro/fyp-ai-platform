from uuid import UUID

from pydantic import BaseModel


class Recommendation(BaseModel):
    idea_id: UUID
    title: str
    match_score: int
    reason: str
    missing_skills: list[str]


class RecommendationResponse(BaseModel):
    recommendations: list[Recommendation]