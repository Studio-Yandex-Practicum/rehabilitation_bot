from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

import emoji
from thefuzz import fuzz

from bot.constants.info.text import MAX_MESSAGES
from bot.core.settings import settings


user_data = {}


def send_email_message(message: str, subject: str, recipient: str) -> bool:
    """Send email message to the specified curator email-address."""
    msg = MIMEMultipart()
    msg["From"] = settings.smtp_server_bot_email
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))
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


def remove_emoji_from_text(current, previous):
    current_text = emoji.replace_emoji(current, replace="")
    previous_text = emoji.replace_emoji(previous, replace="")
    return current_text, previous_text


def fuzzy_string_matching(current_text, previous_text, limit):
    ratio = fuzz.ratio(current_text, previous_text)
    return ratio >= limit


def check_message_limit(user_id):
    return user_data[user_id]["stickers_count"] >= MAX_MESSAGES


def preformatted_text(current_text, previous_text):
    current_message_text = current_text.lower()
    previous_message_text = previous_text.lower()
    return remove_emoji_from_text(current_message_text, previous_message_text)


def update_user_data(user_id, current_message, condition=False):
    user_data[user_id]["previous_message"] = current_message
    if condition:
        user_data[user_id]["stickers_count"] += 1
    else:
        user_data[user_id]["stickers_count"] = 0
