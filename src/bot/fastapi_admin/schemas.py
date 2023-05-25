from pydantic import BaseModel


class QuestionSchema(BaseModel):
    question: str


class AnswerSchema(BaseModel):
    user_id: int
    name: str
    question: str
    answer: str


class UserSchema(BaseModel):
    id: int
    full_name: str
    speciality: str
    job: str
    experience: str
