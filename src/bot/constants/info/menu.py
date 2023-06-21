from bot.constants import key
from bot.core.db.schemas import FormBase


MAIN_MENU = {
    f"{key.MENU}_MAIN": {
        key.NAME: "Главное Меню",
        key.DESCRIPTION: (
            "Чтобы принять участие в нашем сообществе и получить "
            "доступ ко всем возможностям бота, "
            "пожалуйста, зарегистрируйтесь."
        ),
        key.CHILD: [
            f"{key.FORM}_BASE",
        ],
    }
}

SUBMENU = {
    f"{key.FORM}_BASE": {
        key.NAME: "Регистрация",
        key.MODEL: FormBase,
        key.PARENT: f"{key.MENU}_MAIN",
    },
}

ALL_MENU = {
    **MAIN_MENU,
    **SUBMENU,
}
