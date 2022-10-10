from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def help_keyboard() -> InlineKeyboardMarkup:
    """
    Функция, которая генерирует инлайн-клавиатуру с командой help в ответ на нечитаемый запрос пользователя.
    :return InlineKeyboardMarkup:
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=" /help - помощь по командам бота ", callback_data="help"))
    return keyboard
