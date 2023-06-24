from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException
from typing import Optional

from telegram import InlineKeyboardMarkup, Update

from bot.constants.info.text import MESSAGE_MARKDOWN
from bot.core.settings import settings


async def send_message(
    update: Update,
    text: str,
    keyboard: Optional[InlineKeyboardMarkup] = None,
    link_preview: bool = False
):
    """Send a message with optional inline keyboard and link preview."""
    message_args = {
        'text': text,
        'reply_markup': keyboard,
        'parse_mode': MESSAGE_MARKDOWN,
        'disable_web_page_preview': not link_preview,
    }
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.edit_text(**message_args)
    else:
        await update.message.reply_text(**message_args)


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
