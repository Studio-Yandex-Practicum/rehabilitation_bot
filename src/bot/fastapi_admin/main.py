import asyncio

import typer
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.fastapi_admin.db.base import get_session
from src.bot.fastapi_admin.schemas import QuestionSchema
from src.bot.fastapi_admin.tasks import (
    add_question,
    get_questions,
    init_models,
)


app = FastAPI()
cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


@app.get(
    "/questions/",
    response_model=list[QuestionSchema],
)
async def get_all_questions(session: AsyncSession = Depends(get_session)):
    questions = await get_questions(session)
    return [QuestionSchema(question=q.question) for q in questions]


@app.post(
    "/question/",
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

if __name__ == "__main__":
    cli()
