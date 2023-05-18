from telegram import Update
from telegram.ext import ContextTypes

from src.bot.constants import state
from src.bot.constants.info.text import START_MESSAGE, WELCOME_MESSAGE
from src.bot.conversations.menu_application import menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message to the user."""
    await update.message.reply_text(START_MESSAGE)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.user_data[key.MENU] = ALL_MENU[f"{key.MENU}_MAIN"]
    # uncomment after adding the menu manager
    await menu(update, context)
    return state.MAIN_MENU


async def welcome_new_user_in_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Welcomes a new user when they join a group.
    """
    chat_id = update.effective_chat.id
    user_first_name = update.effective_user.first_name
    welcome_message = WELCOME_MESSAGE.format(user_first_name)

    await context.bot.send_message(chat_id, welcome_message)

