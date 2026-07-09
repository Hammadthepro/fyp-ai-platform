import json

from google import genai
from google.genai.types import GenerateContentConfig
from sqlalchemy.ext.asyncio import AsyncSession

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

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

class AIService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AIRepository(db)

    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.5,
    ) -> str:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=temperature,
            ),
        )

        return response.text       

    async def recommend(self, current_user):

        student = await self.repo.get_student(current_user.id)

        ideas = await self.repo.get_all_ideas()

        student_payload = {
            "semester": student.semester,
            "department": student.department,
            "skills": [
                s.skill.name
                for s in student.skills
            ],
            "domains": [
                d.domain.name
                for d in student.domains
            ],
        }

        ideas_payload = []

        for idea in ideas:

            ideas_payload.append(
                {
                    "idea_id": str(idea.id),
                    "title": idea.title,
                    "description": idea.description,
                    "difficulty": idea.difficulty,
                    "domain": idea.domain.name,
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
            }
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        return json.loads(response.text)


    async def generate_ideas(
        self,
        data,
    ):
        prompt = IDEA_GENERATOR_PROMPT.format(
            domain=data.domain,
            technologies=", ".join(data.technologies),
            difficulty=data.difficulty,
            total=data.total,
        )

        return {
            "result": self.generate_text(prompt)
        }

    async def generate_proposal(
        self,
        data,
    ):
        prompt = PROPOSAL_GENERATOR_PROMPT.format(
            title=data.title,
            description=data.description,
        )

        return {
            "result": self.generate_text(prompt)
        }

    async def generate_viva(
        self,
        data,
    ):
        prompt = VIVA_GENERATOR_PROMPT.format(
            title=data.title,
            description=data.description,
        )

        return {
            "result": self.generate_text(prompt)
        }

    async def generate_weekly_report(
        self,
        data,
    ):
        prompt = WEEKLY_REPORT_PROMPT.format(
            title=data.title,
            completed=data.completed,
            pending=data.pending,
            issues=data.issues,
        )

        return {
            "result": self.generate_text(prompt)
        }

    async def generate_minutes(
        self,
        data,
    ):
        prompt = MEETING_MINUTES_PROMPT.format(
            notes=data.notes,
        )

        return {
            "result": self.generate_text(prompt)
        }

    async def generate_documentation(
        self,
        data,
    ):
        prompt = DOCUMENTATION_PROMPT.format(
            title=data.title,
            description=data.description,
        )

        return {
            "result": self.generate_text(prompt)
        }