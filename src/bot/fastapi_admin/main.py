import asyncio

import typer
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.fastapi_admin.config import settings
from src.bot.fastapi_admin.db.base import get_session, init_models
from src.bot.fastapi_admin.schemas import (
    AddUserSchema,
    AnswerSchema,
    QuestionSchema,
    UserSchema,
)
from src.bot.fastapi_admin.tasks import (
    add_new_user,
    add_question,
    get_answers,
    get_questions,
    get_users,
)


app = FastAPI(title=settings.app_title, description=settings.app_description)
cli = typer.Typer()


@app.post(
    "/question/",
    tags=["Вопросы"],
    name="Добавить новый вопрос",
)
async def add_new_question(
    question: QuestionSchema, session: AsyncSession = Depends(get_session)
):
    question = add_question(session, question.question)
    try:
        await session.commit()
        return question
    except Exception:
        await session.rollback()
        raise Exception("Failed to add new question")


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


@app.get(
    "/questions/",
    response_model=list[QuestionSchema],
    tags=["Вопросы"],
    name="Получить список всех добавленных вопросов",
)
async def get_all_questions(session: AsyncSession = Depends(get_session)):
    questions = await get_questions(session)
    return [QuestionSchema(**q.__dict__) for q in questions]


@app.get(
    "/answers/",
    response_model=list[AnswerSchema],
    tags=["Ответы"],
    name="Получить список всех записанных ответов",
)
async def get_all_answers(session: AsyncSession = Depends(get_session)):
    answers = await get_answers(session)
    return [AnswerSchema(**a.__dict__) for a in answers]


@app.post(
    "/users/",
    tags=["Пользователи"],
    name="Добавить нового пользователя",
)
async def add_user(
    user: AddUserSchema,
    session: AsyncSession = Depends(get_session)
):
    user = await add_new_user(session, user=user)
    try:
        await session.commit()
        return user
    except Exception:
        await session.rollback()
        raise Exception("Не получилось добавить нового пользователя")


@app.get(
    "/users/",
    tags=["Пользователи"],
    name="Получить список всех пользователей",
)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await get_users(session)
    return [UserSchema(**u.__dict__) for u in users]


if __name__ == "__main__":
    cli()
