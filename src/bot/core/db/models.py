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


class CustomMessage(Base):
    __tablename__ = 'message_table'

    text = Column(String, default=None)
    sticker = Column(String, default=None)
    date = Column(DateTime, default=datetime.datetime.now())


class UserFilteredData(Base):
    __tablename__ = 'filter_table'

    user_id = Column(Integer, unique=True, nullable=False)
    sticker_count = Column(Integer(), nullable=False)
    previous_message = relationship("CustomMessage", lazy="subquery")
    previous_message_id = Column(Integer, ForeignKey('message_table.id'))

    def __repr__(self):
        return f"{self.user_id}, {self.sticker_count}, {self.previous_message}"
