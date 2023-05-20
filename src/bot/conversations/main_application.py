from telegram import Update
from telegram.constants import ParseMode
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


async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greeting a new member of the group."""
    user_first_name = update.effective_user.full_name
    welcome_message = WELCOME_MESSAGE.format(user_first_name)

    await update.effective_chat.send_message(welcome_message, parse_mode=ParseMode.HTML)

