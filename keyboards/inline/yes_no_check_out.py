from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_no_keyboard() -> InlineKeyboardMarkup:
    """
    Функция, которая генерирует инлайн-клавиатуру "да-нет" для даты выезда.
    :return InlineKeyboardMarkup:
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="да", callback_data="yes_check_out"),
                 InlineKeyboardButton(text="нет", callback_data="no_check_out"))
    return keyboard
