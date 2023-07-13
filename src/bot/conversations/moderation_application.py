import re
import string
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.filter import FLOOD_WARNING_MESSAGE, OBSCENE_WARNING_MESSAGE
from bot.core.db.models import ObsceneWordData
from bot.utils import (
    check_message_limit,
    create_community_member,
    fuzzy_string_matching,
    get_community_member_from_db,
    get_multiple_records_from_db,
    preformatted_text,
    update_community_member_data,
)


async def moderate_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Moderates a conversation by checking for various conditions
    such as message frequency, obscene words, and flood.
    """
    current_message = update.message
    current_message_text = current_message.text
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
                text=FLOOD_WARNING_MESSAGE.format(user_first_name)
            )
        return

    if current_message_text:
        text_no_digital = re.sub("[0-9]", "", current_message_text)
        forbidden_objs = await get_multiple_records_from_db(ObsceneWordData)
        forbidden_words = [obj.word for obj in forbidden_objs]

        if any(
            word.lower().translate(str.maketrans("", "", string.punctuation))
            in forbidden_words
            for word in text_no_digital.split(" ")
        ):
            await update.effective_chat.send_message(
                text=OBSCENE_WARNING_MESSAGE.format(user_first_name)
            )
            await current_message.delete()
            return

    if last_message.text and current_message_text:
        current_text, previous_text = preformatted_text(
            current_message_text, last_message.text
        )

        if fuzzy_string_matching(current_text, previous_text):
            await current_message.reply_text(
                text=FLOOD_WARNING_MESSAGE.format(user_first_name)
            )

    await update_community_member_data(community_member, current_message)
