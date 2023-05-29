from pydantic import BaseModel


class QuestionSchema(BaseModel):
    id: int
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


class AddUserSchema(BaseModel):
    full_name: str
    speciality: str
    job: str
    experience: str
