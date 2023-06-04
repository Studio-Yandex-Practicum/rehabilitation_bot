from datetime import datetime

from pydantic import BaseModel, Field

from bot.constants.info.text import REGEX_FULL_NAME, REGEX_NON_LATIN
from bot.core.db.models import MessageData


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
    date: datetime

    class Config:
        orm_mode = True


class MessageFilterBase(BaseModel):
    user_id: int
    sticker_count: int
    last_message: MessageData
    # last_message_id = Column(Integer, ForeignKey('message_data.id'))

    class Config:
        orm_mode = True
