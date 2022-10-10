from telebot.types import Message, CallbackQuery
from loader import bot
from keyboards.inline import city_keyboard, commands_keyboard
from users import users
from logging import info, warning
from rapidAPI import destination
from . import bestdeal, search_request


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def search_commands(message: Message) -> None:
    """
    Хендлер, обрабатывающий команды lowprice, highprice, bestdeal.
    :param Message message: /lowprice, /highprice, /bestdeal
    :return: None
    """

    info(f"User {message.chat.id} doing func search_commands")
    user = users.Users.get_user(message.chat.id)

    if message.text == "/lowprice":
        user.command = "/lowprice"
        user.sort_order = "PRICE"
    elif message.text == "/highprice":
        user.command = "/highprice"
        user.sort_order = "PRICE_HIGHEST_FIRST"
    elif message.text == "/bestdeal":
        user.command = "/bestdeal"
        user.sort_order = "DISTANCE_FROM_LANDMARK"

    msg = bot.send_message(chat_id=message.chat.id,
                           text=f"Вы выбрали {users.Users.get_command(user_id=message.chat.id)}\n"
                                f"В каком городе ищем?")
    bot.register_next_step_handler(msg, process_city_name)


@bot.callback_query_handler(func=lambda call: call.data == "lowprice")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывающий нажатие lowprice на всплывающих инлайн-клавиатурах.
    :param CallbackQuery call: lowprice
    :return: None
    """

    info(f"Callback lowprice working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    user = users.Users.get_user(call.message.chat.id)
    user.command = "/lowprice"
    user.sort_order = "PRICE"
    search_commands(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "highprice")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывающий нажатие highprice на всплывающих инлайн-клавиатурах.
    :param CallbackQuery call: highprice
    :return: None
    """

    info(f"Callback highprice working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    user = users.Users.get_user(call.message.chat.id)
    user.command = "/highprice"
    user.sort_order = "PRICE_HIGHEST_FIRST"
    search_commands(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "bestdeal")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывающий нажатие bestdeal на всплывающих инлайн-клавиатурах.
    :param CallbackQuery call: bestdeal
    :return: None
    """

    info(f"Callback bestdeal working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    user = users.Users.get_user(call.message.chat.id)
    user.command = "/bestdeal"
    user.sort_order = "DISTANCE_FROM_LANDMARK"
    search_commands(call.message)


def process_city_name(message: Message) -> None:
    """
    Фунция, обрабатывающая и регистрирующая введенное пользователем место назначения с помощью инлайн клавиатуры.
    :param Message message: сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func process_city_name")
    user = users.Users.get_user(message.chat.id)
    user.city = message.text

    destinations_list = destination.get_destination_id(city=user.city)

    if destinations_list:
        user.locations = destinations_list
        bot.send_message(chat_id=message.chat.id,
                         text="Уточните место назначения, пожалуйста:",
                         reply_markup=city_keyboard.city_keyboard(destinations_list))

    else:
        warning(f"Search unsuccessful by user {message.chat.id}")
        bot.send_message(chat_id=message.chat.id,
                         text=f"Упс, похоже города {user.city} в нашей базе нет :(\n"
                              f"Что делаем дальше?",
                         reply_markup=commands_keyboard.commands_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "0" or call.data == "1" or call.data == "2"
                            or call.data == "3" or call.data == "4" or call.data == "5")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, который обрабатывает уточненное пользователем место назначения. Запоминает выбранное id локации и название.
    Далее направляет на обработчик process_hotels_amount (команды lowprice, highprice) или process_min_price (команда
    bestdeal).
    :param CallbackQuery call: от 0 до 5
    :return: None
    """

    info(f"Callback specify_city working for user {call.message.chat.id}")

    user = users.Users.get_user(user_id=call.message.chat.id)
    user.destination_id = user.locations[int(call.data)].get("destinationId", 0)
    user.city = user.locations[int(call.data)].get("name", 0)
    user.locations = None

    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)

    if user.command == "/bestdeal":
        msg = bot.send_message(chat_id=call.message.chat.id,
                                    text=f"Отлично, я запомнил!\n"
                                         f"Теперь определим диапозон цен отеля.\n"
                                         f"Какая минимальная цена за ночь (RUB)?")
        bot.register_next_step_handler(msg, bestdeal.process_min_price)

    else:
        msg = bot.send_message(chat_id=call.message.chat.id,
                               text="Отлично, я запомнил!\nСколько отелей выводим?")
        bot.register_next_step_handler(msg, process_hotels_amount)


def process_hotels_amount(message: Message) -> None:
    """
    Фунция, обрабатывающая и регистрирующая введенное пользователем кол-во отелей. Оно должно быть
    int числом, больше нуля и меньше 25. При выполнении этих требований перенаправляет пользователя на обработчик
    process_photos.
    :param Message message: сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func process_hotels_amount")
    max_hotels_amount = 25
    user = users.Users.get_user(message.chat.id)

    if message.text.isdigit():
        user.hotels_amount = int(message.text)

        if user.hotels_amount > max_hotels_amount or user.hotels_amount < 1:
            msg = bot.send_message(chat_id=message.chat.id,
                                   text="Не могу показать меньше 1 и больше 25 отелей за раз...\n"
                                        "Сколько отелей выводим?")
            info(f"User {message.chat.id} typed unsupported value")
            bot.register_next_step_handler(msg, process_hotels_amount)
            return

    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Цифрами, пожалуйста...\nСколько отелей выводим?")
        info(f"User {message.chat.id} typed unsupported value type")
        bot.register_next_step_handler(msg, process_hotels_amount)
        return

    msg = bot.send_message(chat_id=message.chat.id,
                           text="Мне показать фотографии для каждого отеля? (Да/нет)")
    bot.register_next_step_handler(msg, process_photos)


def process_photos(message: Message) -> None:
    """
    Фунция, обрабатывающая, нужно ли показывать фотографии отелей. Ответ должен быть "да" или "нет" (нечувствительно
    к регистру). При выполнении этих требований перенаправляет пользователя на обработчик process_photos_amount ("да")
    или на обработчик process_check_in ("нет").
    :param Message message: сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func process_photos")

    if message.text.isalpha():
        reply = message.text.lower()

        if reply == "да":
            msg = bot.send_message(chat_id=message.chat.id,
                                   text="Сколько фотографий показать?")
            bot.register_next_step_handler(msg, process_photos_amount)

        elif reply == "нет":
            user = users.Users.get_user(message.chat.id)
            user.photos = 0
            search_request.process_check_in(chat_id=message.chat.id)

        else:
            msg = bot.send_message(chat_id=message.chat.id,
                                   parse_mode="Markdown",
                                   text="Скажите _да_ или _нет_, пожалуйста...\n"
                                        "Мне показать фотографии для каждого отеля? (Да/нет)")
            info(f"User {message.chat.id} typed unsupported value")
            bot.register_next_step_handler(msg, process_photos)
            return

    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Буквами, пожалуйста...\n"
                                    "Мне показать фотографии для каждого отеля? (Да/нет)")
        info(f"User {message.chat.id} typed unsupported value type")
        bot.register_next_step_handler(msg, process_photos)


def process_photos_amount(message: Message) -> None:
    """
    Фунция, обрабатывающая, какое кол-во фотографий отелей нужно показать. Это должно быть int число, больше 0 и
    меньше 20. При выполнении этих требований направляет на обработчик process_check_in.
    :param Message message: сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func process_photos_amount")
    user = users.Users.get_user(message.chat.id)
    max_photos = 20

    if message.text.isdigit():
        user.photos = int(message.text)

        if user.photos > max_photos or user.photos < 1:
            msg = bot.send_message(chat_id=message.chat.id,
                                   text="Не могу показать меньше 1 и больше 20 фотографий отеля...\n"
                                        "Сколько фотографий показать?")
            info(f"User {message.chat.id} typed unsupported value")
            bot.register_next_step_handler(msg, process_photos_amount)
            return

    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text="Цифрами, пожалуйста...\nСколько фотографий показать?")
        info(f"User {message.chat.id} typed unsupported value type")
        bot.register_next_step_handler(msg, process_photos_amount)
        return

    search_request.process_check_in(chat_id=message.chat.id)

