import time

from telegram import ChatMember, Update
from telegram.ext import ContextTypes, ConversationHandler
from thefuzz import fuzz, utils

from bot.constants import state
# from bot.constants.info.menu import ALL_MENU
# uncomment after adding the menu manager
from bot.constants.info.text import (
    MUTE_TIME,
    START_MESSAGE,
    STOP_MESSAGE,
    WELCOME_MESSAGE,
)
from bot.conversations.menu_application import menu
from bot.utils import (
    check_message_limit,
    find_obscene_words_in_a_message,
    increment_message_count,
    initalize_user,
    pending_messages,
    processed_users,
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
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Welcomes a new user when they join a group.
    """
    user = update.effective_user
    chat = update.effective_chat
    user_first_name = user.first_name
    welcome_message = WELCOME_MESSAGE.format(user_first_name)

    # set_dict_key_to_zero(user.id)
    initalize_user(user.id, True)

    await send_message_to_the_conversation(chat, welcome_message)


# async def handle_messages_from_new_user(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ):
#     """
#     Handle incoming messages from a new user.
#     """
#     user = update.message.from_user

#     if user.is_bot or user.id not in pending_messages:
#         return

#     message_count = increment_message_count(user.id)

#     if check_message_limit(message_count):
#         pending_messages.pop(user.id)
#         return

#     await update.message.reply_text("spam detected")


async def handle_all_messages(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Handle all incoming messages.
    """
    current_message = update.message

    if current_message is None:
        return

    current_message_text = current_message.text
    user = current_message.from_user
    # user_first_name = user.first_name
    chat = update.effective_chat

    if user.is_bot:
        return

    if not processed_users.get(user.id):
        initalize_user(user.id)

    # stickers flood checker
    if current_message.sticker:
        message_count = increment_message_count(user.id, "sticker")

        if check_message_limit(message_count):
            set_dict_key_to_zero(user.id, "sticker")
            await send_message_to_the_conversation(
                chat, text="more than 3 stickers"
            )
            return
        return

    # emojis flood checker
    # if is_message_contains_only_emojis(current_message_text):
    #     user_emoji_count = increment_message_count(user_id)

    #     if check_message_limit(user_emoji_count):
    #         set_dict_key_to_zero(user_id)
    #         await send_message_to_the_conversation(
    #             chat, text="more than 3 only emojis message"
    #         )
    #         return
    #     return

    # obscene vocabulary checker
    if utils.full_process(current_message_text):
        matching, execution_time = find_obscene_words_in_a_message(
            current_message_text.lower().split()
        )

        if matching is not None:
            chat_id = current_message.chat_id
            message_id = current_message.message_id
            permissions = ChatMember(user, status="restricted")

            await context.bot.delete_message(chat_id, message_id)
            await context.bot.restrict_chat_member(
                chat_id,
                user.id,
                permissions,
                until_date=time.time() + MUTE_TIME,
            )
            await send_message_to_the_conversation(
                # chat, text=f"Здесь не матерятся, {user_first_name}!")
                chat,
                text=(
                    f"found '{matching[0]}'. matching {matching[1]}\n"
                    f"message id={message_id} deleted\n"
                    f"execution time is {round(execution_time, 5)} sec"
                ),
            )
            return

    # text flood checker
    if chat.id in pending_messages:
        previous_message_text = pending_messages[chat.id].text

        current, previous = replace_emoji_with_symbols(
            current_message_text, previous_message_text
        )

        matching = fuzz.WRatio(current, previous)

        if matching is not None and matching >= 89:
            await send_message_to_the_conversation(
                chat, text=f"matching is {matching}"
            )

    pending_messages[chat.id] = current_message
    set_dict_key_to_zero("sticker")
