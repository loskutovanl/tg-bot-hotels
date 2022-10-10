from telebot.types import BotCommand


def set_commands(bot) -> None:
    """
    Функция, определяющая команды, на которые реагирует бот, и их краткие описания.
    :param bot: бот
    :return: None
    """

    bot.set_my_commands(
        commands=[
            BotCommand(command="helloworld", description="приветствие"),
            BotCommand(command="help", description="помощь по командам бота"),
            BotCommand(command="lowprice", description="топ самых дешевых отелей в городе"),
            BotCommand(command="highprice", description="топ самых дорогих отелей в городе"),
            BotCommand(command="bestdeal", description="топ отелей, наиболее подходящих по цене и расположению"),
            BotCommand(command="history", description="история поиска отелей")
        ],
    )
