from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
# from bot.constants.info.menu import ALL_MENU
# uncomment after adding the menu manager
from bot.constants.info.text import START_MESSAGE, STOP_MESSAGE, WELCOME_MESSAGE
from bot.conversations.menu_application import menu

from bot.constants import key
from bot.constants.info.menu import ALL_MENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message to the user."""
    await update.message.reply_text(START_MESSAGE)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[key.MENU] = ALL_MENU[f"{key.MENU}_MAIN"]
    await menu(update, context)
    return state.MAIN_MENU


async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greeting a new member of the group."""
    user_first_name = update.effective_user.full_name
    welcome_message = WELCOME_MESSAGE.format(user_first_name)

    await update.effective_chat.send_message(welcome_message, parse_mode=ParseMode.HTML)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stops the conversation and replies with the given message."""
    await update.message.reply_text(STOP_MESSAGE)
    return ConversationHandler.END
