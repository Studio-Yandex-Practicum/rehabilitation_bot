from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

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
