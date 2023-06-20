from telegram import ChatPermissions, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
from bot.constants.filter import DB_UPDATE_PERMISSION_USERS, DB_UPDATED_MESSAGE
# from bot.constants.info.menu import ALL_MENU
# uncomment after adding the menu manager
from bot.constants.info.text import (
    START_MESSAGE,
    STOP_MESSAGE,
    WELCOME_MESSAGE,
)
from bot.conversations.menu_application import menu
from bot.utils import update_obscene_words_db_table


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message to the user."""
    await update.message.reply_text(START_MESSAGE)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.user_data[key.MENU] = ALL_MENU[f"{key.MENU}_MAIN"]
    # uncomment after adding the menu manager
    await menu(update, context)
    return state.MAIN_MENU


async def greet_new_member(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Greeting a new member of the group."""
    user_first_name = update.effective_user.full_name
    welcome_message = WELCOME_MESSAGE.format(user_first_name)

    await update.effective_chat.send_message(
        welcome_message, parse_mode=ParseMode.HTML
    )
    await mute_new_member(update, context)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stops the conversation and replies with the given message."""
    await update.message.reply_text(STOP_MESSAGE)
    return ConversationHandler.END


async def mute_new_member(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Mute a new member of the chat."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
        ),
    )
    message = (
        "Для получения возможности отправлять "
        "сообщения пройдите анкетирование."
    )
    await update.effective_chat.send_message(message)


async def unmute_new_member(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Unmute a new member of the chat."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
        ),
    )
    message = (
        f"Уважаемый {update.effective_user.full_name}, "
        "права доступа обновлены."
    )
    await update.effective_chat.send_message(message)


async def update_moderation_db(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_member = await context.bot.get_chat_member(chat_id, user_id)

    if chat_member.status not in DB_UPDATE_PERMISSION_USERS:
        return

    await update_obscene_words_db_table()
    await update.message.reply_text(DB_UPDATED_MESSAGE)
