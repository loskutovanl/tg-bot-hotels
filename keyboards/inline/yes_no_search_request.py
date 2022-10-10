from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_no_keyboard() -> InlineKeyboardMarkup:
    """
    Функция, которая генерирует инлайн-клавиатуру "да-нет" для подтверждения запроса пользователя на поиск отелей.
    :return InlineKeyboardMarkup:
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="да", callback_data="yes_search_request"),
                 InlineKeyboardButton(text="нет", callback_data="no_search_request"))
    return keyboard
