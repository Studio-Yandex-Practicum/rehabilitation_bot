# MAIN MENU
START_MESSAGE = (
    "Добро пожаловать <b>{name}</b>,"
    " в сообщество реабилитологов Фонда Хабенского!\n\n"
    "👋 Приветствуем тебя в нашем телеграм-боте!\n"
    "Здесь ты сможешь присоединиться"
    " к нашему замечательному сообществу реабилитологов. 🌟"
)
WELCOME_MESSAGE = (
    "Добро пожаловать {full_name} ({nickname}), в группу по реабилитации "
    "<a href='https://rsmu.ru/index.php?id=1313'>РНИМУ</a>"
    " и благотворительного фонда "
    "<a href='https://bfkh.ru/'>Фонд Хабенского</a>,"
    " посвященное реабилитации!"
    "\n\nЗдесь вы найдете единомышленников,"
    " которые также заинтересованы в помощи детям, молодым и взрослым с "
    "онкологическими и другими серьезными заболеваниями"
    " головного и спинного мозга. "
    "\n\nЧтобы принять участие в нашем сообществе и получить "
    "доступ ко всем возможностям бота, "
    "пожалуйста, зарегистрируйтесь в боте:\n"
    "{bot_link}"
)
COMPLETE_MESSAGE = (
    "\n\nВаша заявка отправлена. Координатор Фонда свяжется "
    "с Вами в течение 7 рабочих дней."
)
STOP_MESSAGE = "Работа приложения остановлена."

# REGEXP
REGEX_PHONE = r"^(?:\+)?[0-9]\d{10,14}$"
REGEX_FULL_NAME = r"^([А-Яа-яЁё\-]+\b {,3}){2,}$"
REGEX_NON_LATIN = r"^[^a-zA-Z]*$"

# SHOW FORM
FORM = "Анкета"
APPLICATION_DATE = "Дата заявки"
SELECT_EDIT = "Выберите поле для редактирования:"
MESSAGE_MARKDOWN = "HTML"
SHOW_DATA_TEMPLATE = "<b><u>{title}</u></b>\n{value}\n\n"
INPUT_ERROR_TEMPLATE = "<b>Некорректно введены данные!</b>\n\n{hint}"
DATE_TEMPLATE = "%d.%m.%Y"

# Validation error template
VALIDATION_ERROR = "Validation Error in {field} of {form}: {error}"

# MAIN BUTTONS
BACK = "Назад"
START_FORM = "Заполнить анкету"
SEND_FORM = "Отправить"
EDIT_FORM = "Редактировать"

# MAIL CONSTANTS
MAIL_SEND_OK_MESSAGE = "Ваша заявка успешно отправлена!"
MAIL_SEND_ERROR_MESSAGE = "Ошибка: Невозможно отправить заявку!"
