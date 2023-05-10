from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import callback, key, state
from bot.constants.info.menu import ALL_MENU
from bot.utils import send_message


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the selected menu or sub-menu to the user."""

    query = update.callback_query
    user_data = context.user_data

    if not query or query.data == callback.MENU_BACK:
        menu = user_data[key.MENU]
        if parent_menu := menu.get(key.PARENT):
            menu = ALL_MENU[parent_menu]
    else:
        menu = ALL_MENU[query.data]
        user_data[key.MENU] = menu

    buttons = [
        [Button(text=ALL_MENU[menu][key.NAME], callback_data=menu)]
        for menu in menu.get(key.MENU, [])
    ]
    if parent_menu := menu.get(key.PARENT):
        buttons.append(
            [Button(text=ALL_MENU[parent_menu][key.NAME],
                    callback_data=parent_menu)]
        )
    menu_keyboard = Keyboard(buttons)

    await send_message(update, menu[key.DESCRIPTION], keyboard=menu_keyboard)

    return state.MAIN_MENU
