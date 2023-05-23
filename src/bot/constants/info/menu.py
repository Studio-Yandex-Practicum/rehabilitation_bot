from bot.constants import key


MAIN_MENU = {
    f"{key.MENU}_MAIN": {
        key.NAME: "Главное меню Кнопка",
        key.DESCRIPTION: "Временное описание кнопки главного меню",
        key.MENU: [
            f"{key.MENU}_SUB",
        ],
    }
}

SUBMENU = {
    f"{key.MENU}_SUB": {
        key.NAME: "Кнопка 1",
        key.DESCRIPTION: "Описание 1",
        key.PARENT: f"{key.MENU}_MAIN",
        key.MENU: [
            f"{key.MENU}_SUB2",
        ],
    },
    f"{key.MENU}_SUB2": {
        key.NAME: "Кнопка 2",
        key.DESCRIPTION: "Описание 2",
        key.PARENT: f"{key.MENU}_SUB",
    },
}

ALL_MENU = {
    **MAIN_MENU,
    **SUBMENU,
}
