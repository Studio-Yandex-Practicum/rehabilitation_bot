from pydantic import BaseModel


class QuestionSchema(BaseModel):
    question: str
