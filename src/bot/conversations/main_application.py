from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.info.text import START_MESSAGE


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MESSAGE)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...
