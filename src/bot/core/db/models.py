from sqlalchemy import Column, ForeignKey, Integer, String

from src.bot.fastapi_admin.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(256), unique=True, index=True)
    speciality = Column(String(256), unique=True, index=True)
    job = Column(String(256), unique=True, index=True)
    experience = Column(String(256), unique=True, index=True)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(256), unique=True, index=True)

    def __init__(self, question):
        self.question = question


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, ForeignKey("users.full_name"))
    question = Column(String, index=True)
    answer = Column(String(256), unique=True, index=True)
