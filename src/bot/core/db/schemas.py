from datetime import datetime

from pydantic import BaseModel, Field

from bot.constants.info.text import REGEX_FULL_NAME, REGEX_NON_LATIN


class FormBase(BaseModel):
    full_name: str = Field(None, regex=REGEX_FULL_NAME)
    speciality: str = Field(None, regex=REGEX_NON_LATIN)
    job: str = Field(None, regex=REGEX_NON_LATIN)
    experience: str = Field(None, regex=REGEX_NON_LATIN)

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096
        anystr_strip_whitespace = True


class MessageBase(BaseModel):
    text: str | None = Field(None, min_length=1, max_length=4096)
    sticker: str | None = None
    timestamp: datetime

    class Config:
        orm_mode = True


class MessageFilterBase(BaseModel):
    user_id: int
    sticker_count: int
    last_message: MessageBase
    last_message_id: int

    class Config:
        orm_mode = True
