import json
from typing import Any

from google import genai
from google.genai.types import GenerateContentConfig

from groq import Groq

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app.ai.prompt import (
    SYSTEM_PROMPT,
    IDEA_GENERATOR_PROMPT,
    PROPOSAL_GENERATOR_PROMPT,
    VIVA_GENERATOR_PROMPT,
    WEEKLY_REPORT_PROMPT,
    MEETING_MINUTES_PROMPT,
    DOCUMENTATION_PROMPT,
)

from app.ai.repository import AIRepository
from app.core.config import settings


# --------------------------------------------------------
# Gemini
# --------------------------------------------------------

gemini = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# --------------------------------------------------------
# Groq
# --------------------------------------------------------

groq = Groq(
    api_key=settings.GROQ_API_KEY
)


class AIService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = AIRepository(db)

    # =====================================================
    # GEMINI
    # =====================================================

    def call_gemini(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.4,
        json_output: bool = False,
    ) -> str:

        config = GenerateContentConfig(
            temperature=temperature,
        )

        if system_prompt:
            config.system_instruction = system_prompt

        if json_output:
            config.response_mime_type = "application/json"

        response = gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        return response.text

    # =====================================================
    # GROQ
    # =====================================================

    def call_groq(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.4,
    ) -> str:

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature,
        )

        return response.choices[0].message.content

    # =====================================================
    # FALLBACK ENGINE
    # =====================================================

    def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.4,
    ) -> str:

        try:

            return self.call_gemini(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
            )

        except Exception:

            try:

                return self.call_groq(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                )

            except Exception as e:

                raise HTTPException(
                    status_code=503,
                    detail=f"AI service unavailable.\n{str(e)}",
                )

    # =====================================================
    # JSON GENERATOR
    # =====================================================

    def generate_json(
        self,
        prompt: str,
        system_prompt: str,
    ) -> Any:

        try:

            response = self.call_gemini(
                prompt=prompt,
                system_prompt=system_prompt,
                json_output=True,
                temperature=0.2,
            )

            return json.loads(response)

        except Exception:

            try:

                response = self.call_groq(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=0.2,
                )

                return json.loads(response)

            except Exception:

                raise HTTPException(
                    status_code=500,
                    detail="AI returned invalid JSON.",
                )

        # =====================================================
    # AI RECOMMENDATIONS
    # =====================================================

    async def recommend(
        self,
        current_user,
    ):

        student = await self.repo.get_student(
            current_user.id
        )

        if not student:
            raise HTTPException(
                status_code=403,
                detail="Only students can use recommendations.",
            )

        ideas = await self.repo.get_all_ideas()

        if not ideas:
            return {
                "recommendations": []
            }

        student_payload = {
            "name": student.user.full_name,
            "department": student.department,
            "semester": student.semester,
            "skills": [
                s.skill.name
                for s in student.skills
            ],
            "domains": [
                d.domain.name
                for d in student.domains
            ],
            "github": student.github,
            "portfolio": student.portfolio,
        }

        ideas_payload = []

        for idea in ideas:

            ideas_payload.append(
                {
                    "idea_id": str(idea.id),
                    "title": idea.title,
                    "description": idea.description,
                    "difficulty": idea.difficulty,
                    "domain": (
                        idea.domain.name
                        if idea.domain
                        else ""
                    ),
                    "skills": [
                        s.skill.name
                        for s in idea.skills
                    ],
                    "technologies": [
                        t.technology.name
                        for t in idea.technologies
                    ],
                }
            )

        prompt = json.dumps(
            {
                "student": student_payload,
                "ideas": ideas_payload,
            },
            indent=2,
        )

        result = self.generate_json(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
        )

        recommendations = result.get(
            "recommendations",
            [],
        )

        cleaned = []

        valid_ids = {
            str(i.id)
            for i in ideas
        }

        for rec in recommendations:

            if rec.get("idea_id") not in valid_ids:
                continue

            cleaned.append(
                {
                    "idea_id": rec["idea_id"],
                    "title": rec["title"],
                    "match_score": int(
                        rec.get(
                            "match_score",
                            0,
                        )
                    ),
                    "reason": rec.get(
                        "reason",
                        "",
                    ),
                    "missing_skills": rec.get(
                        "missing_skills",
                        [],
                    ),
                }
            )

        cleaned.sort(
            key=lambda x: x["match_score"],
            reverse=True,
        )

        return {
            "recommendations": cleaned
        }

    # =====================================================
    # SMART IDEA GENERATOR
    # =====================================================

    async def generate_ideas(
        self,
        domain: str,
        technologies: list[str],
        difficulty: str,
        total: int,
    ):

        prompt = f"""
Domain:
{domain}

Difficulty:
{difficulty}

Technologies:
{", ".join(technologies)}

Generate exactly {total} Final Year Project ideas.

Each idea should contain:

1. Title

2. Problem Statement

3. Features

4. AI Features

5. Tech Stack

6. Difficulty

7. Estimated Timeline

8. Innovation Score (/10)

9. Commercial Potential

10. Future Scope
"""

        return self.generate_text(
            prompt=prompt,
            system_prompt=IDEA_GENERATOR_PROMPT,
            temperature=0.7,
        )



        # =====================================================
    # PROPOSAL GENERATOR
    # =====================================================

    async def generate_proposal(
        self,
        title: str,
        description: str,
    ):

        prompt = f"""
Project Title

{title}


Project Description

{description}


Generate a complete Final Year Project proposal.

Include:

1. Abstract

2. Problem Statement

3. Objectives

4. Scope

5. Functional Requirements

6. Non Functional Requirements

7. Technologies

8. Methodology

9. Deliverables

10. Future Enhancements

11. Expected Outcomes

12. References
"""

        return self.generate_text(
            prompt=prompt,
            system_prompt=PROPOSAL_GENERATOR_PROMPT,
            temperature=0.5,
        )

    # =====================================================
    # DOCUMENTATION GENERATOR
    # =====================================================

    async def generate_documentation(
        self,
        title: str,
        description: str,
    ):

        prompt = f"""
Project

{title}


Description

{description}


Generate professional project documentation.

Include:

1. Introduction

2. Existing System

3. Proposed System

4. Objectives

5. Scope

6. Functional Requirements

7. Non Functional Requirements

8. System Architecture

9. Database Design

10. Modules

11. Technologies Used

12. Testing Strategy

13. Future Work

14. Conclusion

Write in university report style.
"""

        return self.generate_text(
            prompt=prompt,
            system_prompt=DOCUMENTATION_PROMPT,
            temperature=0.4,
        )

    # =====================================================
    # PROJECT SUMMARY
    # =====================================================

    async def project_summary(
        self,
        current_user,
    ):

        context = await self.repo.build_project_context(
            current_user.id
        )

        if not context:
            raise HTTPException(
                status_code=404,
                detail="Project not found.",
            )

        proposal = context["proposal"]

        milestones = context["milestones"]

        submissions = context["submissions"]

        prompt = f"""
Project Title

{proposal.title if proposal else ""}


Abstract

{proposal.abstract if proposal else ""}


Objectives

{proposal.objectives if proposal else ""}


Milestones

{len(milestones)}


Submissions

{len(submissions)}


Write a concise executive summary of the project.

Mention:

Current progress

Completed work

Pending work

Risks

Overall completion percentage

Next milestone
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.4,
        )


        # =====================================================
    # VIVA QUESTION GENERATOR
    # =====================================================

    async def generate_viva(
        self,
        title: str,
        description: str,
    ):

        prompt = f"""
Project Title

{title}

Project Description

{description}

Generate a complete Final Year Project viva preparation guide.

Include:

1. 30 Technical Questions

2. 10 Beginner Questions

3. 10 Advanced Questions

4. Database Questions

5. AI Questions

6. API Questions

7. Security Questions

8. Deployment Questions

9. Difficult Cross Questions

10. Sample Ideal Answers

11. Tips to Impress Examiner
"""

        return self.generate_text(
            prompt=prompt,
            system_prompt=VIVA_GENERATOR_PROMPT,
            temperature=0.5,
        )

    # =====================================================
    # WEEKLY REPORT
    # =====================================================

    async def generate_weekly_report(
        self,
        title: str,
        completed: str,
        pending: str,
        issues: str,
    ):

        prompt = f"""
Project

{title}

Completed Work

{completed}

Pending Work

{pending}

Issues

{issues}

Generate a professional university weekly progress report.

Include:

Week Summary

Completed Tasks

Pending Tasks

Challenges

Solutions

Plan For Next Week

Supervisor Notes

Overall Progress
"""

        return self.generate_text(
            prompt=prompt,
            system_prompt=WEEKLY_REPORT_PROMPT,
            temperature=0.4,
        )

    # =====================================================
    # MEETING MINUTES
    # =====================================================

    async def generate_meeting_minutes(
        self,
        notes: str,
    ):

        prompt = f"""
Convert the following raw notes into professional meeting minutes.

Raw Notes

{notes}

Include:

Meeting Title

Meeting Date

Participants

Agenda

Discussion

Decisions

Action Items

Deadline

Next Meeting
"""

        return self.generate_text(
            prompt=prompt,
            system_prompt=MEETING_MINUTES_PROMPT,
            temperature=0.3,
        )

    # =====================================================
    # PROJECT TIMELINE
    # =====================================================

    async def generate_project_timeline(
        self,
        title: str,
        description: str,
    ):

        prompt = f"""
Project

{title}

Description

{description}

Generate a complete 16-week Final Year Project timeline.

For each week provide:

Week Number

Goal

Tasks

Deliverables

Expected Output

Risk

Estimated Completion %
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.5,
        )


        # =====================================================
    # PROPOSAL REVIEWER
    # =====================================================

    async def review_proposal(
        self,
        title: str,
        abstract: str,
        objectives: str,
    ):

        prompt = f"""
Review this Final Year Project proposal.

Title
{title}

Abstract
{abstract}

Objectives
{objectives}

Act as an experienced university supervisor.

Evaluate:

1. Originality (/10)

2. Technical Difficulty (/10)

3. Research Value (/10)

4. Commercial Potential (/10)

5. Strengths

6. Weaknesses

7. Missing Sections

8. Risks

9. Suggestions for Improvement

10. Final Recommendation
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.3,
        )

    # =====================================================
    # MILESTONE REVIEWER
    # =====================================================

    async def review_milestone(
        self,
        milestone: str,
        submission: str,
    ):

        prompt = f"""
Milestone

{milestone}

Student Submission

{submission}

Review this milestone like a university supervisor.

Return

Completion %

Quality Score (/10)

Missing Tasks

Positive Points

Weak Areas

Suggestions

Supervisor Feedback
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.3,
        )

    # =====================================================
    # SUBMISSION EVALUATOR
    # =====================================================

    async def evaluate_submission(
        self,
        title: str,
        description: str,
        submission: str,
    ):

        prompt = f"""
Project

{title}

Description

{description}

Submission

{submission}

Evaluate this submission.

Return

Marks (/100)

Implementation Quality

Documentation Quality

Innovation

Code Structure

Research Quality

Pros

Cons

Final Feedback
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.25,
        )

    # =====================================================
    # CODE REVIEW
    # =====================================================

    async def review_code(
        self,
        language: str,
        code: str,
    ):

        prompt = f"""
Programming Language

{language}

Code

{code}

Review this code.

Return

Bugs

Security Issues

Performance Issues

Best Practices

Code Smells

Suggested Improvements

Optimized Version
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.2,
        )

    # =====================================================
    # PROJECT PROGRESS ANALYZER
    # =====================================================

    async def analyze_progress(
        self,
        current_user,
    ):

        context = await self.repo.build_project_context(
            current_user.id
        )

        if not context:

            raise HTTPException(
                status_code=404,
                detail="Project not found.",
            )

        proposal = context["proposal"]

        milestones = context["milestones"]

        submissions = context["submissions"]

        completed = len(
            [
                m
                for m in milestones
                if m.status == "Completed"
            ]
        )

        prompt = f"""
Project

{proposal.title if proposal else ""}

Milestones

{len(milestones)}

Completed

{completed}

Submissions

{len(submissions)}

Analyze project progress.

Return

Overall Progress %

Current Phase

Expected Completion Date

Current Risks

Missing Deliverables

Productivity Rating

Supervisor Advice

Next Recommended Tasks
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.3,
        )


        # =====================================================
    # PROJECT CHAT
    # =====================================================

    async def project_chat(
        self,
        current_user,
        question: str,
    ):

        context = await self.repo.build_project_context(
            current_user.id
        )

        if not context:
            raise HTTPException(
                status_code=404,
                detail="Project not found.",
            )

        proposal = context["proposal"]

        milestones = context["milestones"]

        submissions = context["submissions"]

        project_context = f"""
Project Title:
{proposal.title if proposal else "N/A"}

Abstract:
{proposal.abstract if proposal else ""}

Objectives:
{proposal.objectives if proposal else ""}

Milestones:
{len(milestones)}

Submissions:
{len(submissions)}
"""

        prompt = f"""
You are the AI assistant of this Final Year Project.

Project Context

{project_context}

Student Question

{question}

Answer only using the project context whenever possible.
If additional knowledge is needed, clearly distinguish it from the stored project information.
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.3,
        )

    # =====================================================
    # SUPERVISOR ASSISTANT
    # =====================================================

    async def supervisor_assistant(
        self,
        current_user,
    ):

        context = await self.repo.professor_context(
            current_user.id
        )

        if not context:

            raise HTTPException(
                status_code=403,
                detail="Only professors can use this feature.",
            )

        professor = context["professor"]

        proposals = context["proposals"]

        summary = []

        for proposal in proposals:

            summary.append(
                {
                    "title": proposal.title,
                    "status": proposal.status,
                    "group": proposal.group.name,
                }
            )

        prompt = f"""
Professor

{professor.user.full_name}

Assigned Projects

{json.dumps(summary, indent=2)}

Generate:

Overall supervision summary

Students needing attention

Pending approvals

Suggestions for meetings

Project risks

Recommended next actions
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.3,
        )

    # =====================================================
    # TEAM PERFORMANCE
    # =====================================================

    async def team_analysis(
        self,
        current_user,
    ):

        context = await self.repo.build_project_context(
            current_user.id
        )

        if not context:
            raise HTTPException(
                status_code=404,
                detail="Project not found.",
            )

        group = context["group"]

        submissions = context["submissions"]

        prompt = f"""
Team Members

{len(group.members) if group else 0}

Submissions

{len(submissions)}

Analyze team performance.

Include

Participation

Team collaboration

Workload balance

Risk factors

Recommendations

Overall Team Score
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.3,
        )

    # =====================================================
    # DASHBOARD INSIGHTS
    # =====================================================

    async def dashboard_ai(
        self,
    ):

        stats = await self.repo.dashboard_stats()

        prompt = f"""
Platform Statistics

{json.dumps(stats, indent=2)}

Generate an executive dashboard summary.

Mention

Platform health

Growth

Usage

Possible issues

Recommendations

Future improvements
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.3,
        )

    # =====================================================
    # ROADMAP GENERATOR
    # =====================================================

    async def roadmap(
        self,
        title: str,
        description: str,
    ):

        prompt = f"""
Project

{title}

Description

{description}

Generate a roadmap from project idea to deployment.

Include

Planning

Research

Design

Development

Testing

Deployment

Documentation

Presentation

Timeline

Expected Deliverables
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.4,
        )

    # =====================================================
    # RISK PREDICTION
    # =====================================================

    async def predict_risks(
        self,
        current_user,
    ):

        context = await self.repo.build_project_context(
            current_user.id
        )

        if not context:

            raise HTTPException(
                status_code=404,
                detail="Project not found.",
            )

        proposal = context["proposal"]

        milestones = context["milestones"]

        prompt = f"""
Project

{proposal.title if proposal else ""}

Milestones

{len(milestones)}

Predict possible project risks.

Include

Technical Risks

Research Risks

Time Risks

Team Risks

Deployment Risks

Severity

Mitigation Plan
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.3,
        )

    # =====================================================
    # AI SPRINT PLANNER
    # =====================================================

    async def sprint_plan(
        self,
        title: str,
        description: str,
        duration: int = 2,
    ):

        prompt = f"""
Project

{title}

Description

{description}

Create a {duration}-week sprint.

Include

Sprint Goal

User Stories

Tasks

Priority

Estimated Hours

Deliverables

Definition of Done
"""

        return self.generate_text(
            prompt=prompt,
            temperature=0.4,
        )