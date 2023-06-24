from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import callback, key, state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.utils import send_message


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the selected menu or sub-menu to the user."""

    query = update.callback_query
    user_data = context.user_data

    if query and query.data and query.data.startswith(key.MENU):
        menu_name = query.data
        if query.data == callback.MENU_BACK:
            menu_name = user_data[key.MENU][key.PARENT]
        menu = ALL_MENU[menu_name]
        user_data[key.MENU] = menu
    else:
        menu = user_data[key.MENU]

    buttons = [
        [Button(text=ALL_MENU[menu_name][key.NAME], callback_data=menu_name)]
        for menu_name in menu.get(key.CHILD, [])
    ]
    if parent_menu := menu.get(key.PARENT):
        buttons.append([Button(text=text.BACK, callback_data=parent_menu)])

    await send_message(
        update, menu[key.DESCRIPTION],
        keyboard=Keyboard(buttons)
    )

    return state.MAIN_MENU
