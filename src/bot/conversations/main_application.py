from telegram import ChatPermissions, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import key, state
from bot.constants.info.menu import ALL_MENU
from bot.constants.info.text import (
    COMPLETE_MESSAGE,
    START_MESSAGE,
    STOP_MESSAGE,
    WELCOME_MESSAGE,
)
from bot.conversations.menu_application import menu
from bot.utils import send_message


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Send a welcome message to the user."""
    user = update.effective_user
    message = START_MESSAGE.format(name=user.full_name)

    if context.user_data.get(key.FORM, {}).get(key.COMPLETE):
        return await send_message(update, message + COMPLETE_MESSAGE)

    await send_message(update, message)

    return await main_menu(update, context)


async def stop(update: Update, _) -> int:
    """Stops the conversation and replies with the given message."""
    await update.message.reply_text(STOP_MESSAGE)
    return ConversationHandler.END


async def main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data[key.MENU] = ALL_MENU[f"{key.MENU}_MAIN"]
    await menu(update, context)
    return state.MAIN_MENU


async def greet_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Greeting a new member of the group."""
    new_members = update.message.new_chat_members

    for member in new_members:
        welcome_message = WELCOME_MESSAGE.format(
            nickname=member.name,
            full_name=member.full_name,
            bot_link=context.bot.link
        )
        await update.effective_chat.send_message(
            welcome_message,
            parse_mode=ParseMode.HTML
        )
        await mute_member(context, member.id, update.effective_chat.id)


async def mute_member(
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int, chat_id: int
):
    """Mute a new member of the chat."""
    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
        ),
    )


async def unmute_member(
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int, chat_id: int
):
    """Unmute a new member of the chat."""
    await context.bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
        ),
    )
