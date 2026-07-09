from uuid import UUID

from pydantic import BaseModel


# -------------------------
# Recommendation
# -------------------------

class Recommendation(BaseModel):
    idea_id: UUID
    title: str
    match_score: int
    reason: str
    missing_skills: list[str]


class RecommendationResponse(BaseModel):
    recommendations: list[Recommendation]


# -------------------------
# AI Idea Generator
# -------------------------

class IdeaGeneratorRequest(BaseModel):
    domain: str
    technologies: list[str]
    difficulty: str
    total: int = 5


class AITextResponse(BaseModel):
    result: str


# -------------------------
# Proposal Generator
# -------------------------

class ProposalGeneratorRequest(BaseModel):
    title: str
    description: str


# -------------------------
# Viva Generator
# -------------------------

class VivaGeneratorRequest(BaseModel):
    title: str
    description: str


# -------------------------
# Weekly Report
# -------------------------

class WeeklyReportRequest(BaseModel):
    title: str
    completed: str
    pending: str
    issues: str


# -------------------------
# Meeting Minutes
# -------------------------

class MeetingMinutesRequest(BaseModel):
    notes: str


# -------------------------
# Documentation
# -------------------------

class DocumentationRequest(BaseModel):
    title: str
    description: str