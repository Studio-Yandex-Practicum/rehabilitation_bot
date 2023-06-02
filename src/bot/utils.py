from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

import emoji
from telegram import Message
from thefuzz import fuzz

from bot.constants.info.text import MAX_MESSAGES, RATIO_LIMIT
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


def check_message_limit(user_id: int) -> bool:
    return user_data[user_id]["stickers_count"] >= MAX_MESSAGES


def preformatted_text(
    current_text: str, previous_text: str
) -> tuple[str, str]:
    current_message_text = current_text.lower()
    previous_message_text = previous_text.lower()
    return remove_emoji_from_text(current_message_text, previous_message_text)


def update_user_data(
    user_id: int, current_message: Message, condition: bool = False
) -> None:
    user_data[user_id]["previous_message"] = current_message
    if condition:
        user_data[user_id]["stickers_count"] += 1
    else:
        user_data[user_id]["stickers_count"] = 0
