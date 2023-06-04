import datetime

from sqlalchemy import (  # create_engine,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from bot.core.database import Base


# engine = create_engine('sqlite:///sqlite3.db')
# engine.connect()

meta = MetaData()

obscene_language = Table(
    'Obscene_language', meta,
    Column('id', Integer, primary_key=True),
    Column('The_forbidden_word', String(50), unique=True)
)


class MessageData(Base):
    __tablename__ = 'message_data'

    text = Column(String, default=None)
    sticker = Column(String, default=None)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())


class MessageFilterData(Base):
    __tablename__ = 'message_filter_data'

    user_id = Column(Integer, unique=True, nullable=False)
    sticker_count = Column(Integer(), nullable=False)
    last_message = relationship("MessageData", lazy="subquery")
    last_message_id = Column(Integer, ForeignKey('message_data.id'))

    def __repr__(self):
        return f"{self.user_id}, {self.sticker_count}, {self.last_message}"
