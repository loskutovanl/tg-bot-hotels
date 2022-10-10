from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def helloworld_keyboard() -> InlineKeyboardMarkup:
    """
    Функция, которая генерирует приветственную инлайн-клавиатуру.
    :return InlineKeyboardMarkup:
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=" /helloworld - приветствие ", callback_data="helloworld"))
    return keyboard
