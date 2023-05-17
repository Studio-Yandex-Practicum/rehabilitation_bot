from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import key, state
from bot.constants.info.menu import ALL_MENU
from bot.constants.info.text import START_MESSAGE
from bot.conversations.menu_application import menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message to the user."""
    await update.message.reply_text(START_MESSAGE)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[key.MENU] = ALL_MENU[f"{key.MENU}_MAIN"]
    await menu(update, context)
    return state.MAIN_MENU
