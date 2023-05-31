from datetime import datetime, timedelta, timezone

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
# from bot.constants.info.menu import ALL_MENU
# uncomment after adding the menu manager
from bot.constants.info.text import (
    MAX_MESSAGES,
    START_MESSAGE,
    STOP_MESSAGE,
    WELCOME_MESSAGE,
)
from bot.conversations.menu_application import menu


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


user_data = {}


async def handle_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Handle all incoming messages.
    """
    current_message = update.message
    user_id = current_message.from_user.id
    current_time = datetime.now(timezone.utc)
    username = current_message.from_user.first_name

    if user_id not in user_data:
        user_data[user_id] = {
            "stickers_count": 1,
            "previous_message": current_message,
        }
        return

    print(user_data)

    # sticker flood checker
    if current_message.sticker:
        previous_time = user_data[user_id]["previous_message"].date
        time_diff = current_time - previous_time

        if time_diff < timedelta(seconds=30):
            user_data[user_id]["stickers_count"] += 1
        else:
            user_data[user_id]["stickers_count"] = 0

        user_data[user_id]["previous_message"] = current_message

        if user_data[user_id]["stickers_count"] >= MAX_MESSAGES:
            await update.effective_chat.send_message(
                text=f"Воу-воу, палегче, {username}!"
            )
        return
    else:
        user_data[user_id]["stickers_count"] = 0
        user_data[user_id]["previous_message"] = current_message

    # text flood checker
    # if current_message.text:
    #     previous_message_text = user_data[user_id][""]
