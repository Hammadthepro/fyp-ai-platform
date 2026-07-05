import json

from google import genai
from google.genai.types import GenerateContentConfig
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.prompt import SYSTEM_PROMPT
from app.ai.repository import AIRepository

from app.core.config import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

class AIService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AIRepository(db)

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