from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def commands_keyboard() -> InlineKeyboardMarkup:
    """
    Функция, которая генерирует инлайн-клавиатуру со всеми существующими у бота командами.
    :return InlineKeyboardMarkup:
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(InlineKeyboardButton(text=" /helloworld - приветствие ", callback_data="helloworld"),
                 InlineKeyboardButton(text=" /lowprice - топ самых дешевых отелей в городе ",
                                      callback_data="lowprice"),
                 InlineKeyboardButton(text=" /highprice - топ самых дорогих отелей в городе ",
                                      callback_data="highprice"),
                 InlineKeyboardButton(text=" /bestdeal - топ отелей, наиболее подходящих по цене и расположению ",
                                      callback_data="bestdeal"),
                 InlineKeyboardButton(text=" /history - история поиска отелей ", callback_data="history"))
    return keyboard
