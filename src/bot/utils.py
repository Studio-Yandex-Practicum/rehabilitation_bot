from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

import emoji
from sqlalchemy import select
from telegram import Message
from thefuzz import fuzz

from bot.constants.info.text import MAX_MESSAGES, RATIO_LIMIT
from bot.core.database import async_session
from bot.core.db.models import CustomMessage, UserFilteredData
from bot.core.settings import settings


user_data = {}


def send_email_message(message: str, subject: str, recipient: str) -> bool:
    """Send email message to the specified curator email-address."""
    msg = MIMEMultipart()
    msg['From'] = settings.smtp_server_bot_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))
    try:
        with SMTP_SSL(
            settings.smtp_server_address,
            settings.smtp_server_port,
        ) as mailserver:
            if settings.debug:
                mailserver.set_debuglevel(True)

            mailserver.login(
                settings.smtp_server_bot_email,
                settings.smtp_server_bot_password,
            )

            mailserver.send_message(msg)
        return True
    except SMTPException:
        return False


def remove_emoji_from_text(current: str, previous: str) -> tuple[str, str]:
    current_text = emoji.replace_emoji(current, replace="")
    previous_text = emoji.replace_emoji(previous, replace="")
    return current_text, previous_text


def fuzzy_string_matching(current_text: str, previous_text: str) -> bool:
    ratio = fuzz.ratio(current_text, previous_text)
    return ratio >= RATIO_LIMIT


def preformatted_text(
    current_text: str, previous_text: str
) -> tuple[str, str]:
    current_message_text = current_text.lower()
    previous_message_text = previous_text.lower()
    return remove_emoji_from_text(current_message_text, previous_message_text)


async def create_community_member(
            user_id: int,
            message: Message,
):
    custom_message = CustomMessage(
        text=getattr(message, 'text', None),
        sticker=getattr(message.sticker, 'emoji', None),
        date=message.date
    )
    print(message)
    async with async_session() as session:
        community_member = UserFilteredData(
            user_id=user_id,
            previous_message=custom_message,
            sticker_count=0)
        session.add(community_member)
        await session.commit()
        await session.refresh(community_member)
        return community_member


async def get_all():
    async with async_session() as session:
        db_objs = await session.execute(select(UserFilteredData))
        return db_objs.scalars().all()


async def get_by_user_id(user_id: int):
    async with async_session() as session:
        db_obj = await session.execute(
            select(UserFilteredData).where(
                UserFilteredData.user_id == user_id
            )
        )
        return db_obj.scalars().first()


async def get_message_by_id(message_id: int):
    async with async_session() as session:
        db_obj = await session.execute(
            select(CustomMessage).where(
                CustomMessage.id == message_id
            )
        )
        return db_obj.scalars().first()


async def change_message_attrib(object, message: Message):
    async with async_session() as session:
        object.text = getattr(message, 'text', None)
        object.sticker = getattr(message.sticker, 'emoji', None)
        object.date = message.date
        session.add(object)
        await session.commit()
        await session.refresh(object)


def check_message_limit(stickers_count: int) -> bool:
    return stickers_count >= MAX_MESSAGES


async def update_user_data(
        community_member: UserFilteredData,
        message: Message,
        time_diff: bool = False
):
    message_id = community_member.previous_message_id
    filter_data = await get_message_by_id(message_id)

    await change_message_attrib(filter_data, message)

    sticker_count = community_member.sticker_count

    if time_diff:
        sticker_count += 1
    else:
        sticker_count = 0

    community_member.sticker_count = sticker_count

    async with async_session() as session:
        session.add(community_member)
        await session.commit()
        await session.refresh(community_member)
        return sticker_count
