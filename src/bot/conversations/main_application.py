from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.info.text import START_MESSAGE, STOP_MESSAGE


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MESSAGE)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...


async def stop(update: Update,
               context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stops the conversation and replies with the given message."""
    await update.message.reply_text(STOP_MESSAGE)
    return ConversationHandler.END
