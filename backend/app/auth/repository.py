from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.student import Student
from app.models.professor import Professor


class AuthRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(
        self,
        email: str,
    ):
        result = await self.db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def get_user_by_id(
        self,
        user_id: str,
    ):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def create_user(
        self,
        user: User,
    ):
        self.db.add(user)
        await self.db.flush()
        return user

    async def create_student(
        self,
        student: Student,
    ):
        self.db.add(student)
        await self.db.flush()
        return student

    async def create_professor(
        self,
        professor: Professor,
    ):
        self.db.add(professor)
        await self.db.flush()
        return professor

    async def update_user(
        self,
        user: User,
    ):
        await self.db.flush()
        return user

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()