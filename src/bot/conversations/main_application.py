from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import key, state
from bot.constants.info.menu import ALL_MENU
from bot.constants.info.text import START_MESSAGE, STOP_MESSAGE
from bot.conversations.menu_application import menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MESSAGE)
    return await main_menu(update, context)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[key.MENU] = ALL_MENU[f"{key.MENU}_MAIN"]
    await menu(update, context)
    return state.MAIN_MENU


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stops the conversation and replies with the given message."""
    await update.message.reply_text(STOP_MESSAGE)
    return ConversationHandler.END
