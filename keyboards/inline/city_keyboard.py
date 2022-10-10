from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def city_keyboard(destinations: list) -> InlineKeyboardMarkup:
    """
    Функция, которая генерирует инлайн-клавиатуру с самыми подходящими местами назначения (не больше 6).
    :param list destinations: список возможных мест назначения, подгруженный из rapidAPI
    :return InlineKeyboardMarkup:
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1

    for i in range(len(destinations)):
        destination_name = destinations[i].get("name", 0)
        keyboard.add(InlineKeyboardButton(text=f"{destination_name}", callback_data=f"{i}"))
        if i == 6:
            break

    return keyboard
