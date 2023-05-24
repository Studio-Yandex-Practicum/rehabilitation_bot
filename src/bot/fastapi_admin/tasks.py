import os.path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.fastapi_admin.db.base import init_models
from src.bot.fastapi_admin.models_db import Question


path = '/questions.sqlite3'


async def get_questions(session: AsyncSession) -> list[Question]:
    result = await session.execute(select(Question))
    return result.scalars().all()


def add_question(session: AsyncSession, question: str):
    new_question = Question(question=question)
    session.add(new_question)
    return new_question


async def check_if_db_exists():
    if not os.path.isfile(path):
        await init_models()
    print('Done')
