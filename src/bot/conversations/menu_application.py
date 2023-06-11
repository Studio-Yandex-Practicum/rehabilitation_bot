from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from src.bot.constants.info.menu import ALL_MENU, MAIN_MENU


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # Получаем текущее меню пользователя из контекста
    current_menu = context.user_data.get('current_menu', 'MENU_MAIN')

    # Получаем информацию о текущем меню
    menu_info = ALL_MENU.get(current_menu)

    # Формируем сообщение
    message_text = menu_info['DESCRIPTION']

    # Создаем кнопки на основе дочерних меню
    keyboard = []
    for child_menu in menu_info['MENU']:
        child_menu_info = ALL_MENU.get(child_menu)
        button = KeyboardButton(child_menu_info[key.NAME])
        keyboard.append([button])

    # Добавляем кнопку "Назад" на основе родительского меню
    parent_menu = menu_info.get('PARENT')
    if parent_menu:
        parent_menu_info = ALL_MENU.get(parent_menu)
        back_button = KeyboardButton("Назад")
        keyboard.append([back_button])

    # Формируем и отправляем сообщение с кнопками
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat_id,
        text=message_text,
        reply_markup=reply_markup
    )