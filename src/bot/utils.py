import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

import emoji
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Message
from thefuzz import fuzz

from bot.constants.info.text import MAX_MESSAGES, RATIO_LIMIT
from bot.core.database import async_session
from bot.core.db.crud import (
    CRUDBase,
    message_data_crud,
    message_filter_data_crud,
)
from bot.core.db.models import MessageData, MessageFilterData, ObsceneWordData
from bot.core.settings import settings


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
    """Remove emojis from text."""
    current_text = emoji.replace_emoji(current, replace="")
    previous_text = emoji.replace_emoji(previous, replace="")
    return current_text, previous_text


def fuzzy_string_matching(current_text: str, previous_text: str) -> bool:
    """Perform fuzzy string matching."""
    ratio = fuzz.ratio(current_text, previous_text)
    return ratio >= RATIO_LIMIT


def check_message_limit(stickers_count: int) -> bool:
    """Check if the sticker count exceeds the maximum message limit."""
    return stickers_count >= MAX_MESSAGES


def preformatted_text(
    current_text: str, previous_text: str
) -> tuple[str, str]:
    """Preformat text by converting it to lowercase and removing emojis."""
    current_message_text = current_text.lower()
    previous_message_text = previous_text.lower()
    return remove_emoji_from_text(current_message_text, previous_message_text)


async def get_community_member_from_db(user_id: int) -> MessageFilterData:
    """Retrieve community member object from database."""
    async with async_session() as session:
        community_member = (
            await message_filter_data_crud.get_message_filter_data_by_user_id(
                user_id, session
            )
        )
        return community_member


async def create_community_member(
    user_id: int, message: Message
) -> MessageFilterData:
    """Creates a new community member and saves their last post data."""
    async with async_session() as session:
        message_data = MessageData()

        await message_data_crud.update_message_data_attrib(
            message_data, message, session
        )

        community_member = MessageFilterData(
            user_id=user_id, last_message=message_data, sticker_count=0
        )

        session.add(community_member)
        await session.commit()
        await session.refresh(community_member)
        return community_member


async def update_community_member_data(
    community_member: MessageFilterData,
    message: Message,
    time_diff: bool = False,
) -> int:
    """Update community member data."""
    async with async_session() as session:
        message_id = community_member.last_message_id
        message_data = await message_data_crud.get_message_data_by_id(
            message_id, session
        )

        await message_data_crud.update_message_data_attrib(
            message_data, message, session
        )

        sticker_count = community_member.sticker_count

        if time_diff:
            sticker_count += 1
        else:
            sticker_count = 0

        community_member.sticker_count = sticker_count

        session.add(community_member)
        await session.commit()
        await session.refresh(community_member)
        return sticker_count


async def check_existing_records(
    obscene_list: list, session: AsyncSession
) -> list[str]:
    """Check existing records for obscene wordlist."""
    objects = await CRUDBase(ObsceneWordData).get_multi(session)
    wordlist = [obj.word for obj in objects]
    new_list = [word for word in obscene_list if word not in wordlist]
    return new_list


async def update_obscene_words_db_table() -> None:
    """Update obscene words database table."""
    async with async_session() as session:
        with open(settings.obscene_json, "r") as json_file:
            obscene_list = json.load(json_file)
            updated_list = await check_existing_records(obscene_list, session)
            unique_list = []
            [
                unique_list.append(word)
                for word in updated_list
                if word not in unique_list
            ]
            objects = [ObsceneWordData(word=object) for object in unique_list]
            session.add_all(objects)
            await session.commit()
            await session.close()
