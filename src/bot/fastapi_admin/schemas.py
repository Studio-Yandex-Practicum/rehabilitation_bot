from pydantic import BaseModel


class AddQuestionSchema(BaseModel):
    question: str


class QuestionSchema(AddQuestionSchema):
    id: int


class AnswerSchema(BaseModel):
    user_id: int
    name: str
    question: str
    answer: str


class AddUserSchema(BaseModel):
    full_name: str
    speciality: str
    job: str
    experience: str


class UserSchema(AddUserSchema):
    id: int
