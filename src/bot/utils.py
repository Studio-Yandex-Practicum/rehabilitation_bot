from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

import emoji
from telegram import Message
from thefuzz import fuzz

from bot.constants.info.text import MAX_MESSAGES, RATIO_LIMIT
from bot.core.database import async_session
from bot.core.db.crud import message_data_crud, message_filter_data_crud
from bot.core.db.schemas import MessageBase, MessageFilterBase
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
    current_text = emoji.replace_emoji(current, replace="")
    previous_text = emoji.replace_emoji(previous, replace="")
    return current_text, previous_text


def fuzzy_string_matching(current_text: str, previous_text: str) -> bool:
    ratio = fuzz.ratio(current_text, previous_text)
    return ratio >= RATIO_LIMIT


def check_message_limit(stickers_count: int) -> bool:
    return stickers_count >= MAX_MESSAGES


def preformatted_text(
    current_text: str, previous_text: str
) -> tuple[str, str]:
    current_message_text = current_text.lower()
    previous_message_text = previous_text.lower()
    return remove_emoji_from_text(current_message_text, previous_message_text)


async def get_community_member_from_db(user_id: int):
    async with async_session() as session:
        community_member = (
            await message_filter_data_crud.get_message_filter_data_by_user_id(
                user_id, session
            )
        )
        return community_member


async def create_community_member(
    user_id: int,
    message: Message,
):
    async with async_session() as session:
        message_data = MessageBase()

        await message_data_crud.update_message_data_attrib(
            message_data, message, session
        )

        community_member = MessageFilterBase(
            user_id=user_id, last_message=message_data, sticker_count=0
        )

        session.add(community_member)
        await session.commit()
        await session.refresh(community_member)
        return community_member


async def update_community_member_data(
    community_member: MessageFilterBase,
    message: Message,
    time_diff: bool = False,
):
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
