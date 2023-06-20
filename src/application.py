from telegram import (  # BotCommandScopeChat,
    BotCommand,
    BotCommandScopeChatAdministrators,
)
from telegram.ext import Application

from bot.core import logger  # noqa
from bot.core.settings import settings
from bot.handlers import (
    greet_new_member_handler,
    main_handler,
    moderate_conversation_handler,
)


admin_commands = [
    BotCommand("upd_mod_db", "update moderation database"),
]

user_commands = [
    BotCommand("start", "start"),
    BotCommand("stop", "stop"),
]


async def post_init(application: Application) -> None:
    """
    Sets up bot commands after application has initialized.
    """
    bot = application.bot
    all_commands = user_commands.copy()
    all_commands.extend(admin_commands)

    # await bot.set_my_commands(
    #     user_commands,
    #     scope=BotCommandScopeChat(chat_id=settings.chat_id),
    # )

    await bot.set_my_commands(
        all_commands,
        scope=BotCommandScopeChatAdministrators(chat_id=settings.chat_id),
    )


def main() -> None:
    """Initialize a Telegram bot application with a main handler."""
    application = (
        Application.builder()
        .token(settings.telegram_token)
        .post_init(post_init)
        .build()
    )
    application.add_handlers(
        [
            main_handler,
            greet_new_member_handler,
            moderate_conversation_handler,
        ]
    )
    application.run_polling()


if __name__ == "__main__":
    main()
