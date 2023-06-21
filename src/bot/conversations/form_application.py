import logging
from datetime import date

from email_validate.exceptions import Error as EmailValidationError
from pydantic.error_wrappers import ValidationError
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import button, callback, key, state
from bot.constants.info import text
from bot.constants.info.menu import ALL_MENU
from bot.constants.info.question import ALL_QUESTIONS
from bot.core.settings import settings
from bot.utils import send_email_message, send_message


async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initializes the user's form data and asks for input."""
    query = update.callback_query
    user_data = context.user_data
    menu = ALL_MENU[query.data]
    user_data[key.MENU] = menu

    model = menu.get(key.MODEL)

    user_data[key.FORM] = {
        key.DATA: model(),
        key.FIELDS: list(model().dict()),
        key.FIELD_INDEX: 0,
        key.FIELD_EDIT: False,
        key.COMPLETE: False,
    }

    return await ask_data(update, context)


async def ask_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask the user for input related to the current form field."""
    query = update.callback_query
    user_data = context.user_data
    form = user_data[key.FORM]
    fields = form[key.FIELDS]

    if query and query.data.startswith(callback.ASK_DATA):
        form[key.FIELD_EDIT] = query.data.replace(
            f"{callback.ASK_DATA}_", ""
        ).lower()

    field = form.get(key.FIELD_EDIT)
    if not field:
        field = fields[form[key.FIELD_INDEX]]

    question = ALL_QUESTIONS[field.upper()]
    await send_message(update, question[key.TEXT])

    return state.FORM_INPUT


async def save_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the user's input for the current form field."""
    user_data = context.user_data
    form = user_data[key.FORM]
    fields = form[key.FIELDS]
    input = update.message.text.strip()

    field = form.get(key.FIELD_EDIT)
    if not field:
        field = fields[form[key.FIELD_INDEX]]
    try:
        setattr(form[key.DATA], field, input)
    except (ValidationError, EmailValidationError) as error:
        error_message = text.VALIDATION_ERROR.format(
            field=field,
            form=user_data[key.FORM][key.DATA].__class__.__name__,
            error=error.errors()[0]["msg"],
        ) if type(error) is ValidationError else error
        logging.info(error_message)
        question_hint = ALL_QUESTIONS[field.upper()][key.HINT]
        error_message = text.INPUT_ERROR_TEMPLATE.format(hint=question_hint)
        await send_message(update, error_message)
        return await ask_data(update, context)

    if (form[key.FIELD_INDEX] + 1) >= len(fields):
        return await show_data(update, context)

    form[key.FIELD_INDEX] = form[key.FIELD_INDEX] + 1

    return await ask_data(update, context)


async def edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the edit menu to the user."""
    user_data = context.user_data
    fields = user_data[key.FORM][key.FIELDS]

    edit_buttons = []
    for field in fields:
        question = ALL_QUESTIONS[field.upper()]
        btn_callback = f'{callback.ASK_DATA}_{field.upper()}'
        edit_buttons.append(
            [Button(text=question[key.TITLE], callback_data=btn_callback)]
        )
    edit_buttons.append([button.SHOW_DATA])

    await send_message(
        update,
        text.SELECT_EDIT,
        keyboard=Keyboard(edit_buttons)
    )

    return state.FORM_INPUT


async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the completed form data to the user."""
    user_data = context.user_data
    form = user_data[key.FORM]

    message = f"<b>{text.FORM}:</b>\n\n"

    for name, value in form[key.DATA]:
        question = ALL_QUESTIONS[name.upper()]
        message += text.SHOW_DATA_TEMPLATE.format(
            title=question[key.TITLE],
            value=value,
        )

    message += text.SHOW_DATA_TEMPLATE.format(
        title=text.APPLICATION_DATE,
        value=date.today().strftime(text.DATE_TEMPLATE),
    )
    form[key.SHOW_DATA] = message

    keyboard = Keyboard(
        [[button.SEND_DATA], [button.EDIT_MENU, button.MENU_BACK]]
    )
    await send_message(update, message, keyboard=keyboard)

    return state.FORM_SUBMISSION


async def send_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send form data to the specified curator email-address."""
    user_data = context.user_data
    form = user_data[key.FORM]
    data = form[key.DATA]
    message = form[key.SHOW_DATA].replace("\n", "<br>")

    subject = f"{text.FORM} {data.full_name}"

    curators = settings.email_curator.split(',')
    if all(
        send_email_message(message, subject, curator) for curator in curators
    ):
        response_message = text.MAIL_SEND_OK_MESSAGE
        user_data[key.FORM][key.COMPLETE] = True
    else:
        response_message = text.MAIL_SEND_ERROR_MESSAGE

    await send_message(
        update,
        response_message,
        keyboard=Keyboard([[button.START_BACK]]),
    )

    return state.MAIN_MENU
