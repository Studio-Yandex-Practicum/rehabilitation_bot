from typing import Optional

from email_validate import validate_or_fail
from pydantic import BaseModel, EmailStr, Field, validator

from bot.constants.info.text import (
    REGEX_FULL_NAME,
    REGEX_NON_LATIN,
    REGEX_PHONE,
)


class FormBase(BaseModel):
    full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    phone: str = Field(None, regex=REGEX_PHONE)
    email: Optional[EmailStr]
    city: str = Field(None, regex=REGEX_NON_LATIN, max_length=100)

    @validator("email")
    def validator_email(cls, email):
        validate_or_fail(
            email_address=email,
            check_blacklist=False,
            check_smtp=False,
        )
        return email

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096
        validate_assignment = True
        anystr_strip_whitespace = True
