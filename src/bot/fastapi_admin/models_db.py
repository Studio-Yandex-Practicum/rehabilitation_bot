from sqlalchemy import Column, Integer, String

from src.bot.fastapi_admin.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(256), unique=True, index=True)

    def __init__(self, question):
        self.question = question
