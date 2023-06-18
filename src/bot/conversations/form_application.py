from datetime import date
from typing import List

from pydantic import ValidationError
from telegram import BotCommandScopeChat
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import button, key, state
from bot.constants.info.question import QUESTIONS
from bot.core import settings
from bot.utils import send_email_message, send_message


# from bot.utils import send_message


async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    chat_id = update.effective_chat.id
    await context.bot.set_my_commands(
        [button.MENU_COMMAND], scope=BotCommandScopeChat(chat_id)
    )

    option = user_data.get(key.OPTION, {})
    model = option.get(key.MODEL) or user_data[key.MENU][key.MODEL]

    user_data[key.FORM] = {
        key.DATA: model(),
        key.FIELD: list(model().dict()),
        key.FIELD_INDEX: 0,
        key.EDIT: False,
    }

    return await ask_input(update, context)


async def ask_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    user_data = context.user_data
    form = user_data[key.FORM]
    fields = form[key.FIELDS]

    if callback and callback.data.startswith(key.ASK):
        form[key.EDIT] = callback.data.replace(f"{key.ASK}_", "").lower()

    field = form.get(key.EDIT)
    if not field:
        field = fields[form[key.FIELD_INDEX]]

    question = QUESTIONS[field.upper()]
    await send_email_message(update, question[key.TEXT])

    return state.FORM_INPUT


async def edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    form_fields = user_data[key.FORM][key.FIELDS]
    edit_buttons = [
        [Button(
            text=QUESTIONS[field.upper()][key.TITLE],
            callback_data=f'{key.ASK}_{field.upper()}'
        )]
        for field in form_fields
    ]
    edit_buttons.append([button.SHOW_DATA])

    await send_edit_menu(update, edit_buttons)

    return state.FORM_INPUT


async def send_edit_menu(update: Update, buttons: List[List[Button]]):
    await send_message(
        update, "Выберите что редактировать", keyboard=Keyboard(buttons)
    )


async def send_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    form_data = user_data[key.FORM]
    menu_data = user_data[key.MENU]
    message = form_data[key.SHOW_DATA]
    options = user_data.get(key.OPTION)
    subject = f"Анкета_{menu_data.get(key.NAME)}"

    if options:
        subject += f"_{options.get(key.BUTTON_TEXT)}"
    curators = settings.email_curator.split(',')
    success = all(
        send_email_message(message, subject, curator) for curator in curators
    )

    if success:
        response_message = menu_data.get(
            key.RESPONSE, 'Письмо успешно отправлено.'
        )
    else:
        response_message = 'Ошибка отправки письма. Попробуйте еще раз.'

    keyboard = Keyboard([[button.MAIN_MENU]])
    await send_message(update, response_message, keyboard=keyboard)
    return state.MAIN_MENU


async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    form = user_data[key.FORM]
    data = user_data[key.MENU]

    message = f"{form}, {data}"
    if menu_options := user_data.get(key.OPTION):
        message += f"\n{menu_options}"
    message += f"\n{date.today.strftime('%d %B %Y')}"

    for name, value in form[key.DATA]:
        question = QUESTIONS[name.upper()]
        message += f"\n{question[key.TITLE]}: {value}"
    form[key.SHOW_DATA] = message

    keyboard = Keyboard(
        [[button.SEND_DATA], [button.MAIN_MENU], [button.EDIT_MENU]],
    )
    await send_message(update, message, keyboard=keyboard)
    return state.FORM_SUBMISSION


async def edit_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


async def save_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    form_data = user_data[key.FORM]
    fields = form_data[key.FIELDS]
    input_text = update.message.text.split(' ', 1)[1]

    current_field = form_data.get(key.EDIT)
    if not current_field:
        current_field = fields[form_data[key.FIELD_INDEX]]

    try:
        setattr(form_data[key.DATA], current_field, input_text)
    except ValidationError as error:
        error_message = error
        await send_message(update, error_message)
        return await ask_input(update, context)

    if form_data[key.FIELD_INDEX] + 1 >= len(fields):
        return await show_data(update, context)

    form_data[key.FIELD_INDEX] += 1
    return await ask_input(update, context)
