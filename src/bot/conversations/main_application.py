from datetime import datetime, timedelta, timezone

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
# from bot.constants.info.menu import ALL_MENU
# uncomment after adding the menu manager
from bot.constants.info.text import (
    START_MESSAGE,
    STOP_MESSAGE,
    WELCOME_MESSAGE,
)
from bot.conversations.menu_application import menu
from bot.utils import (
    check_message_limit,
    fuzzy_string_matching,
    preformatted_text,
    update_user_data,
    user_data,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message to the user."""
    await update.message.reply_text(START_MESSAGE)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.user_data[key.MENU] = ALL_MENU[f"{key.MENU}_MAIN"]
    # uncomment after adding the menu manager
    await menu(update, context)
    return state.MAIN_MENU


async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greeting a new member of the group."""
    user_first_name = update.effective_user.full_name
    welcome_message = WELCOME_MESSAGE.format(user_first_name)

    await update.effective_chat.send_message(
        welcome_message, parse_mode=ParseMode.HTML
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stops the conversation and replies with the given message."""
    await update.message.reply_text(STOP_MESSAGE)
    return ConversationHandler.END


async def handle_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Handle all incoming messages.
    """
    current_message = update.message
    user_id = current_message.from_user.id
    current_time = datetime.now(timezone.utc).replace(microsecond=0)
    username = current_message.from_user.first_name

    if user_id not in user_data:
        user_data[user_id] = {
            "stickers_count": 0,
            "previous_message": current_message,
        }
        return

    previous_message = user_data.get(user_id).get("previous_message")

    # sticker flood checker
    if previous_message.sticker and current_message.sticker:
        previous_time = previous_message.date
        elapsed_time = current_time - previous_time
        time_diff = elapsed_time < timedelta(seconds=30)

        update_user_data(user_id, current_message, time_diff)

        if check_message_limit(user_id):
            await current_message.reply_text(
                text=f"Воу-воу, палехче, {username}!"
            )
        return

    # text flood checker
    if previous_message.text and current_message.text:
        current_text, previous_text = preformatted_text(
            current_message.text, previous_message.text
        )

        matching = fuzzy_string_matching(current_text, previous_text)

        if matching:
            await update.effective_chat.send_message(
                text=f"matching is {matching}"
            )

    update_user_data(user_id, current_message)
