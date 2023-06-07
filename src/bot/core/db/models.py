from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from bot.core.database import Base


class MessageData(Base):
    """Store data from user messages."""

    __tablename__ = "message_data"

    text = Column(String, default=None)
    sticker = Column(String, default=None)
    timestamp = Column(DateTime(timezone=True))


class MessageFilterData(Base):
    """Store data for flood filter including sticker count and last message."""

    __tablename__ = "message_filter_data"

    user_id = Column(BigInteger, unique=True, nullable=False)
    sticker_count = Column(Integer(), nullable=False)
    last_message = relationship("MessageData", lazy="subquery")
    last_message_id = Column(Integer, ForeignKey("message_data.id"))

    def __repr__(self):
        return f"{self.user_id}, {self.sticker_count}, {self.last_message}"


class ObsceneWordData(Base):
    """Store obscene words for filtering."""

    __tablename__ = "obscene_words"

    word: str = Column(String(25), unique=True)

    def __repr__(self):
        return f"id={self.id} word={self.word}"
