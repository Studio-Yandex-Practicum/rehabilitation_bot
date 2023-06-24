from telegram import InlineKeyboardButton as Button

from bot.constants import callback
from bot.constants.info import text


# FORM
SEND_DATA = Button(text.SEND_FORM, callback_data=callback.SEND_DATA)
EDIT_MENU = Button(text.EDIT_FORM, callback_data=callback.EDIT_MENU)
SHOW_DATA = Button(text.BACK, callback_data=callback.SHOW_DATA)
MENU_BACK = Button(text.BACK, callback_data=callback.MENU_BACK)
BACK = Button(text.BACK, callback_data=callback.BACK)
