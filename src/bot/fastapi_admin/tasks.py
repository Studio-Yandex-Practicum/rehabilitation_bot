from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.core.db.models import Answer, Question, User


PATH = "/questions.sqlite3"


async def get_questions(session: AsyncSession) -> list[Question]:
    result = await session.execute(select(Question))
    return result.scalars().all()


async def get_answers(session: AsyncSession) -> list[User]:
    result = await session.execute(select(Answer))
    return result.scalars().all()


async def get_users(session: AsyncSession) -> list[Question]:
    result = await session.execute(select(User))
    return result.scalars().all()


def add_question(session: AsyncSession, question: str):
    new_question = Question(question=question)
    session.add(new_question)
    return new_question
