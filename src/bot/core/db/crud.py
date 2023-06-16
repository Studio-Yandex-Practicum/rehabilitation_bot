from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Message

from bot.core.db.models import MessageData, MessageFilterData


class CRUDBase:
    """CRUD Base class for database operations."""

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_first(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().first()


class CRUDMessageData(CRUDBase):
    """CRUD operations for MessageData objects."""

    async def get_message_data_by_id(
        self, message_id: int, session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == message_id)
        )
        return db_obj.scalars().first()

    async def update_message_data_attrib(
        self, object: MessageData, message: Message, session: AsyncSession
    ):
        object.text = getattr(message, "text", None)
        object.sticker = getattr(message.sticker, "emoji", None)
        object.timestamp = message.date
        session.add(object)
        await session.commit()
        await session.refresh(object)
        await session.close()


class CRUDMessageFilterData(CRUDBase):
    """CRUD operations for MessageFilterData objects."""

    async def get_message_filter_data_by_user_id(
        self, user_id: int, session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return db_obj.scalars().first()


message_data_crud = CRUDMessageData(MessageData)
message_filter_data_crud = CRUDMessageFilterData(MessageFilterData)
