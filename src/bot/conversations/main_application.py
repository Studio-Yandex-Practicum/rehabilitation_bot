from datetime import datetime, timedelta

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import state
# from bot.constants.info.menu import ALL_MENU
# uncomment after adding the menu manager
from bot.constants.info.text import (
    FLOOD_MESSAGE,
    START_MESSAGE,
    STOP_MESSAGE,
    WELCOME_MESSAGE,
)
from bot.conversations.menu_application import menu
from bot.utils import (
    check_message_limit,
    create_community_member,
    fuzzy_string_matching,
    get_community_member_from_db,
    preformatted_text,
    update_community_member_data,
    update_obscene_words_db_table,
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


async def manage_message_flooding(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Monitoring and managing message flooding and sticker usage by comparing
    text similarity and tracking the number of stickers sent by each user.
    """
    current_message = update.message
    user_id = current_message.from_user.id
    current_time = datetime.now().replace(microsecond=0)
    user_first_name = current_message.from_user.first_name

    community_member = await get_community_member_from_db(user_id)

    if not community_member:
        await create_community_member(user_id, current_message)
        return

    last_message = community_member.last_message

    if last_message.sticker and current_message.sticker:
        previous_time = last_message.timestamp
        elapsed_time = current_time - previous_time
        time_diff = elapsed_time < timedelta(seconds=30)

        message_count = await update_community_member_data(
            community_member, current_message, time_diff
        )

        if check_message_limit(message_count):
            await current_message.reply_text(
                text=FLOOD_MESSAGE.format(user_first_name)
            )
        return

    if last_message.text and current_message.text:
        current_text, previous_text = preformatted_text(
            current_message.text, last_message.text
        )

        if fuzzy_string_matching(current_text, previous_text):
            await current_message.reply_text(
                text=FLOOD_MESSAGE.format(user_first_name)
            )

    await update_community_member_data(community_member, current_message)


async def update_obscene(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update_obscene_words_db_table()
    await update.effective_chat.send_message("obscene values updated")
