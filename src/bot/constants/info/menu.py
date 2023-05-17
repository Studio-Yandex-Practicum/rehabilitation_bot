from bot.constants import key


MAIN_MENU = {
    f"{key.MENU}_MAIN": {
        key.NAME: "Главное меню",
        key.DESCRIPTION: (
            "Чтобы вступить в сообщество необходимо заполнить краткую анкету."
        ),
        key.MENU: [
            f"{key.MENU}_SUB",
        ],
    }
}

SUBMENU = {
    f"{key.MENU}_SUB": {
        key.NAME: "ФИО пользователя",
        key.DESCRIPTION: "Укажите Вашу фамилию, имя и отчество",
        key.PARENT: f"{key.MENU}_MAIN",
        key.MENU: [
            f"{key.MENU}_SUB2",
        ],
    },
    f"{key.MENU}_SUB2": {
        key.NAME: "Ваша специальность",
        key.DESCRIPTION: "Выберите вашу специальность",
        key.PARENT: f"{key.MENU}_SUB",
    },
}

ALL_MENU = {
    **MAIN_MENU,
    **SUBMENU,
}
