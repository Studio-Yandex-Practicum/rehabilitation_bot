from telegram import BotCommand
from telegram import InlineKeyboardButton as Button

from bot.constants import callback


MENU_COMMAND = BotCommand('/menu', 'Меню')

START_FORM = Button(
    text='Начать', callback_data=callback.START_FORM
)
EDIT_DATA = Button(
    text='Редактировать данные', callback_data=callback.EDIT_DATA
)
SAVE_DATA = Button(
    text='Сохранить данные', callback_data=callback.SAVE_DATA
)
SEND_DATA = Button(
    text='Отправить данные', callback_data=callback.SEND_DATA
)
EDIT_MENU = Button(
    text='Редактировать меню', callback_data=callback.EDIT_MENU
)
SHOW_DATA = Button(
    text='Показать данные', callback_data=callback.SHOW_DATA
)
MAIN_MENU = Button(
    text='Главное меню', callback_data=callback.MAIN_MENU
)
