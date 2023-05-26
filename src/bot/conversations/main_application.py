from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from thefuzz import fuzz, utils

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
    find_obscene_words_in_a_message,
    increment_message_count,
    pending_messages,
    replace_emoji_with_symbols,
    send_message_to_the_conversation,
    set_dict_key_to_zero,
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


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stops the conversation and replies with the given message."""
    await update.message.reply_text(STOP_MESSAGE)
    return ConversationHandler.END


async def welcome_new_user_in_group(
        update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Welcomes a new user when they join a group.
    """
    user = update.effective_user
    chat = update.effective_chat
    user_first_name = user.first_name
    welcome_message = WELCOME_MESSAGE.format(user_first_name)

    set_dict_key_to_zero(user.id)

    await send_message_to_the_conversation(chat, welcome_message)


async def handle_messages_from_new_user(
        update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming messages from a new user.
    """
    user = update.message.from_user

    if user.is_bot or user.id not in pending_messages:
        return

    message_count = increment_message_count(user.id)

    if check_message_limit(message_count):
        pending_messages.pop(user.id)
        return

    await update.message.reply_text("spam detected")


async def handle_all_messages(
        update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle all incoming messages.
    """
    current_message = update.message

    if current_message is None or current_message.photo:
        return

    current_message_text = current_message.text
    user = current_message.from_user
    # user_first_name = user.first_name
    chat = update.effective_chat

    if user.is_bot:
        return

    if current_message.sticker:
        message_count = increment_message_count("sticker")

        if check_message_limit(message_count):
            set_dict_key_to_zero("sticker")
            await send_message_to_the_conversation(
                chat, text="more than 3 stickers")
            return
        return

    if utils.full_process(current_message_text):
        matching = find_obscene_words_in_a_message(
            current_message_text.split())

        if matching is not None:
            await send_message_to_the_conversation(
                # chat, text=f"Здесь не матерятся, {user_first_name}!")
                chat, text=f"found '{matching[0]}'. matching {matching[1]}")
            return

    if chat.id in pending_messages:
        previous_message_text = pending_messages[chat.id].text

        current, previous = replace_emoji_with_symbols(
            current_message_text,
            previous_message_text
        )

        matching = fuzz.WRatio(current, previous)

        if matching is not None and matching >= 89:
            await send_message_to_the_conversation(
                chat, text=f"matching is {matching}")

    pending_messages[chat.id] = current_message
    set_dict_key_to_zero("sticker")
