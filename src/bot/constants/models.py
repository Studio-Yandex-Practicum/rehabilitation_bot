from pydantic import BaseModel, Field


FULL_NAME_REGEX = r"^([А-Яа-яЁё\-]+\b {,3}){2,}$"


class BaseFormModel(BaseModel):
    class Config:
        min_anystr_length = 1
        max_anystr_length = 2048
        validate_assignment = True
        anystr_strip_whitespace = True


class WelcomeFormModel(BaseFormModel):
    full_name: str = Field(..., regex=FULL_NAME_REGEX, max_length=100)


class SpecialtyFormModel(BaseFormModel):
    specialty: str = Field(..., max_length=100)
