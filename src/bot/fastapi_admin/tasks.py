from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.core.db.models import Answer, Question, User
from src.bot.fastapi_admin.schemas import AddUserSchema


PATH = "/questions.sqlite3"


async def get_questions(session: AsyncSession) -> list[Question]:
    result = await session.execute(select(Question))
    return result.scalars().all()


async def get_answers(session: AsyncSession) -> list[User]:
    result = await session.execute(select(Answer).group_by(Answer.user_id))
    return result.scalars().all()


async def get_users(session: AsyncSession) -> list[Question]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def add_new_user(session: AsyncSession, user: AddUserSchema):
    new_user = User(
        full_name=user.full_name,
        speciality=user.speciality,
        job=user.job,
        experience=user.experience,
    )
    session.add(new_user)
    return new_user


def add_question(session: AsyncSession, question: str):
    new_question = Question(question=question)
    session.add(new_question)
    return new_question
