from telebot.types import Message
from loader import bot
from . import lowprice_highprice_bestdeal
from users import users
from math import floor
from logging import info


def process_min_price(message: Message) -> None:
    """
    Фунция, обрабатывающая и регистрирующая введенную пользователем минимальную цену за ночь. Цена должна быть
    int или float числом, больше нуля. При выполнении этих требований перенаправляет пользователя на обработчик
    process_max_price.
    :param Message message: сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func process_min_price")
    user = users.Users.get_user(message.chat.id)

    if message.text.isdigit():
        user.min_price = int(message.text)
    elif message.text.count(".") == 1 and message.text.index(".") > 0:
        user.min_price = floor(float(message.text))
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Цифрами, пожалуйста...\nКакая минимальная цена за ночь (RUB)?")
        info(f"User {message.chat.id} typed unsupported value type")
        bot.register_next_step_handler(msg, process_min_price)
        return

    if user.min_price <= 0:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Цена должна быть положительным числом...\n"
                                    "Какая минимальная цена за ночь (RUB)?")
        info(f"User {message.chat.id} typed unsupported value")
        bot.register_next_step_handler(msg, process_min_price)
        return

    msg = bot.send_message(chat_id=message.chat.id,
                           text="Отлично, я запомнил!\nКакая максимальная цена за ночь (RUB)?")
    bot.register_next_step_handler(msg, process_max_price)


def process_max_price(message: Message) -> None:
    """
    Фунция, обрабатывающая и регистрирующая введенную пользователем максимальную цену за ночь. Цена должна быть
    int или float числом, больше минимальной цены. При выполнении этих требований перенаправляет пользователя на
    обработчик process_min_distance.
    :param Message message: сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func process_max_price")
    user = users.Users.get_user(message.chat.id)

    if message.text.isdigit():
        user.max_price = int(message.text)
    elif message.text.count(".") == 1 and message.text.index(".") > 0:
        user.max_price = floor(float(message.text))
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Цифрами, пожалуйста...\nКакая максимальная цена за ночь (RUB)?")
        info(f"User {message.chat.id} typed unsupported value type")
        bot.register_next_step_handler(msg, process_max_price)
        return

    if user.max_price <= user.min_price:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Максимальная цена должна быть больше минимальной...\n"
                                    "Какая максимальная цена за ночь (RUB)?")
        info(f"User {message.chat.id} typed unsupported value")
        bot.register_next_step_handler(msg, process_max_price)
        return

    msg = bot.send_message(chat_id=message.chat.id,
                           text="Отлично, я запомнил! Теперь определим диапазон расстояния отеля от центра.\n"
                                "Какое минимальное расстояние (км)?")
    bot.register_next_step_handler(msg, process_min_distance)


def process_min_distance(message: Message) -> None:
    """
    Фунция, обрабатывающая и регистрирующая введенное пользователем минимальное расстояние до центра. Оно должно
    быть int или float числом, больше нуля. При выполнении этих требований перенаправляет пользователя на
    обработчик process_max_distance.
    :param Message message: сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func process_min_distance")
    user = users.Users.get_user(message.chat.id)

    if message.text.isdigit():
        user.min_distance = int(message.text)
    elif message.text.count(".") == 1 and message.text.index(".") > 0:
        user.min_distance = float(message.text)
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Цифрами, пожалуйста...\nКакое минимальное расстояние (км)?")
        info(f"User {message.chat.id} typed unsupported value type")
        bot.register_next_step_handler(msg, process_min_distance)
        return

    if user.min_distance <= 0:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Расстояние должно быть положительным числом...\n"
                                    "Какое минимальное расстояние (км)?")
        info(f"User {message.chat.id} typed unsupported value")
        bot.register_next_step_handler(msg, process_min_distance)
        return

    msg = bot.send_message(chat_id=message.chat.id,
                           text="Отлично, я запомнил!\nКакое максимальное расстояние (км)?")
    bot.register_next_step_handler(msg, process_max_distance)


def process_max_distance(message: Message) -> None:
    """
    Фунция, обрабатывающая и регистрирующая введенное пользователем максимальное расстояние до центра. Оно должно
    быть int или float числом, больше минимального расстояния. При выполнении этих требований перенаправляет
    пользователя на обработчик process_hotels_amount.
    :param Message message: сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func process_max_distance")
    user = users.Users.get_user(message.chat.id)

    if message.text.isdigit():
        user.max_distance = int(message.text)
    elif message.text.count(".") == 1 and message.text.index(".") > 0:
        user.max_distance = float(message.text)
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Цифрами, пожалуйста...\nКакое максимальное расстояние (км)?")
        info(f"User {message.chat.id} typed unsupported value type")
        bot.register_next_step_handler(msg, process_max_distance)
        return

    if user.max_distance <= user.min_distance:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Максимальное расстояние должно быть больше минимального...\n"
                                    "Какое максимальное расстояние (км)?")
        info(f"User {message.chat.id} typed unsupported value")
        bot.register_next_step_handler(msg, process_max_distance)
        return

    msg = bot.send_message(chat_id=message.chat.id,
                           text="Отлично, я запомнил!\nСколько отелей выводим?")
    bot.register_next_step_handler(msg, lowprice_highprice_bestdeal.process_hotels_amount)
