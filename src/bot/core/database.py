from contextlib import asynccontextmanager

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, declared_attr

from bot.core.settings import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_engine)


def async_session_generator():
    return async_sessionmaker(engine, class_=AsyncSession)


@asynccontextmanager
async def async_session():
    try:
        get_async_session = async_session_generator()

        async with get_async_session() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
