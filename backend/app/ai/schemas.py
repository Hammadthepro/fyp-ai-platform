from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ==========================================================
# Generic Response
# ==========================================================

class AITextResponse(BaseModel):
    result: str


# ==========================================================
# Recommendation
# ==========================================================

class Recommendation(BaseModel):
    idea_id: UUID
    title: str
    match_score: int
    reason: str
    missing_skills: list[str]


class RecommendationResponse(BaseModel):
    recommendations: list[Recommendation]


# ==========================================================
# Smart Idea Generator
# ==========================================================

class IdeaGeneratorRequest(BaseModel):
    domain: str
    technologies: list[str]
    difficulty: str
    total: int = 5


# ==========================================================
# Proposal Generator
# ==========================================================

class ProposalGeneratorRequest(BaseModel):
    title: str
    description: str


# ==========================================================
# SRS Generator
# ==========================================================

class SRSGeneratorRequest(BaseModel):
    title: str
    description: str


# ==========================================================
# Documentation Generator
# ==========================================================

class DocumentationRequest(BaseModel):
    title: str
    description: str


# ==========================================================
# Weekly Report
# ==========================================================

class WeeklyReportRequest(BaseModel):
    week: int
    completed: str
    pending: str
    issues: str


# ==========================================================
# Meeting Minutes
# ==========================================================

class MeetingMinutesRequest(BaseModel):
    meeting_title: str
    notes: str


# ==========================================================
# Viva Generator
# ==========================================================

class VivaGeneratorRequest(BaseModel):
    title: str
    description: str


# ==========================================================
# Final Report
# ==========================================================

class FinalReportRequest(BaseModel):
    title: str
    description: str


# ==========================================================
# Presentation Generator
# ==========================================================

class PresentationRequest(BaseModel):
    title: str
    description: str


# ==========================================================
# Demo Script
# ==========================================================

class DemoScriptRequest(BaseModel):
    title: str
    description: str


# ==========================================================
# AI Supervisor Chat
# ==========================================================

class SupervisorChatRequest(BaseModel):
    message: str


# ==========================================================
# GitHub Review
# ==========================================================

class GitHubReviewRequest(BaseModel):
    github_url: str


# ==========================================================
# Architecture Review
# ==========================================================

class ArchitectureReviewRequest(BaseModel):
    architecture: str


# ==========================================================
# UML Generator
# ==========================================================

class UMLRequest(BaseModel):
    description: str


# ==========================================================
# ERD Generator
# ==========================================================

class ERDRequest(BaseModel):
    description: str


# ==========================================================
# Database Design
# ==========================================================

class DatabaseDesignRequest(BaseModel):
    description: str


# ==========================================================
# API Documentation
# ==========================================================

class APIDocumentationRequest(BaseModel):
    endpoints: str


# ==========================================================
# Test Case Generator
# ==========================================================

class TestCaseRequest(BaseModel):
    feature: str


# ==========================================================
# Sprint Planner
# ==========================================================

class SprintPlannerRequest(BaseModel):
    project_description: str
    duration_weeks: int = Field(default=2)


# ==========================================================
# Milestone Planner
# ==========================================================

class MilestonePlannerRequest(BaseModel):
    project_title: str
    duration_months: int


# ==========================================================
# Progress Analysis
# ==========================================================

class ProgressAnalysisRequest(BaseModel):
    completed_work: str
    remaining_work: str


# ==========================================================
# Risk Analysis
# ==========================================================

class RiskAnalysisRequest(BaseModel):
    project_description: str


# ==========================================================
# Professor Assistant
# ==========================================================

class ProfessorAssistantRequest(BaseModel):
    question: str


# ==========================================================
# Admin Analytics
# ==========================================================

class AdminAnalyticsRequest(BaseModel):
    query: str


# ==========================================================
# Universal AI Chat (Future)
# ==========================================================

class AIChatRequest(BaseModel):
    message: str
    context: Optional[str] = None