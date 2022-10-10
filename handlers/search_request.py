from telebot.types import CallbackQuery
from loader import bot
from keyboards.inline import commands_keyboard, yes_no_check_in, yes_no_check_out, yes_no_search_request
from datetime import datetime
from . import perform_search
from users import users
from logging import info
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date, timedelta


def process_check_in(chat_id: int) -> None:
    """
    Фунция, обрабатывающая и регистрирующая выбранную пользователем дату заезда на инлайн календаре.
    :param int chat_id: уникальный id пользователя
    :return: None
    """

    info(f"User {chat_id} doing func process_check_in")
    calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                              current_date=date.today(),
                                              min_date=date.today(),
                                              max_date=date.today() + timedelta(days=365),
                                              locale="ru").build()
    bot.send_message(chat_id=chat_id,
                     text="Выберите дату заезда:",
                     reply_markup=calendar)


def process_check_out(chat_id: int) -> None:
    """
    Фунция, обрабатывающая и регистрирующая выбранную пользователем дату выезда на инлайн календаре.
    :param int chat_id: уникальный id пользователя
    :return: None
    """

    info(f"User {chat_id} doing func process_check_out")
    calendar, step = DetailedTelegramCalendar(calendar_id=2,
                                              current_date=date.today(),
                                              min_date=date.today() + timedelta(days=1),
                                              max_date=date.today() + timedelta(days=365),
                                              locale="ru").build()
    bot.send_message(chat_id=chat_id,
                     text="Выберите дату выезда:",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывайщий и запрашивающий подтверждение правильности ввода даты заезда на всплывающем инлайн-календаре.
    :param CallbackQuery call: дата заезда
    :return: None
    """

    info(f"Callback calendar_1 working for user {call.message.chat.id}")
    result, key, step = DetailedTelegramCalendar(calendar_id=1,
                                                 current_date=date.today(),
                                                 min_date=date.today(),
                                                 max_date=date.today() + timedelta(days=365),
                                                 locale="ru").process(call.data)
    user = users.Users.get_user(call.message.chat.id)

    if not result and key:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Выберите дату заезда:",
                              reply_markup=key)

    elif result:
        user.check_in = result
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f"Вы выбрали дату заезда {result}. Правильно?",
                              reply_markup=yes_no_check_in.yes_no_keyboard())


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывайщий и запрашивающий подтверждение правильности ввода даты выезда на всплывающем инлайн-календаре.
    :param CallbackQuery call: дата выезда
    :return: None
    """

    info(f"Callback calendar_2 working for user {call.message.chat.id}")
    result, key, step = DetailedTelegramCalendar(calendar_id=2,
                                                 current_date=date.today(),
                                                 min_date=date.today() + timedelta(days=1),
                                                 max_date=date.today() + timedelta(days=365),
                                                 locale="ru").process(call.data)
    user = users.Users.get_user(call.message.chat.id)

    if not result and key:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f"Выберите дату выезда:",
                              reply_markup=key)

    elif result <= user.check_in:
        info(f"User {call.message.chat.id} chose unsupported value")
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"Ошибка! Дата выезда должна быть позже даты заезда :(\n"
                              f"Давайте попробуем еще раз...")
        process_check_out(call.message.chat.id)

    elif result:
        user.check_out = result
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f"Вы выбрали дату выезда {result}. Правильно?",
                              reply_markup=yes_no_check_out.yes_no_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "yes_check_in")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывайщий подтверждение правильного ввода даты заезда на инлайн-календаре. Перенправляет на
    обработчик process_check_out.
    :param CallbackQuery call: yes_check_in
    :return: None
    """

    info(f"Callback yes_check_in working for user {call.message.chat.id}")
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f"Отлично! Я запомнил, что дата заезда "
                               f"{users.Users.get_check_in(user_id=call.message.chat.id)} ;)")
    process_check_out(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "no_check_in")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывайщий НЕправильную дату заезда на инлайн-календаре.
    :param CallbackQuery call: no_check_in
    :return: None
    """

    info(f"Callback no_check_in working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id,
                     text=f"Давайте попробуем еще раз...")
    process_check_in(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "yes_check_out")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывайщий подтверждение правильного ввода даты выезда на инлайн-календаре.
    При выполнении этих требований запрашивает проверку всех введенных параметров поиска (всё инфо получено
    через функцию summarize_request).
    :param CallbackQuery call: yes_check_out
    :return: None
    """

    info(f"Callback yes_check_out working for user {call.message.chat.id}")

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f"Отлично! Я запомнил, что дата выезда "
                               f"{users.Users.get_check_out(user_id=call.message.chat.id)} ;)")
    text = summarize_request(chat_id=call.message.chat.id)
    bot.send_message(chat_id=call.message.chat.id,
                     text=text)
    bot.send_message(chat_id=call.message.chat.id,
                     text="Все правильно?",
                     reply_markup=yes_no_search_request.yes_no_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "no_check_out")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывайщий НЕправильную дату выезда на инлайн-календаре.
    :param CallbackQuery call: no_check_out
    :return: None
    """

    info(f"Callback no_check_out working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id,
                     text=f"Давайте попробуем еще раз...")
    process_check_out(call.message.chat.id)


def summarize_request(chat_id: int) -> str:
    """
    Функция, которая по id пользователя выводит все введенные им данные по поиску отелей и переспрашивает их
    корректность.
    :param chat_id: уникальный id пользователя
    :return str: все введенные пользователем данные по поиску отелей
    """

    info(f"User {chat_id} doing func summarize_request")

    user = users.Users.get_user(user_id=chat_id)
    days = (user.check_out - user.check_in).days
    check_in = datetime.strftime(user.check_in, "%Y-%m-%d")
    check_out = datetime.strftime(user.check_out, "%Y-%m-%d")
    price_distance_range = ""

    if user.photos == 0:
        photos_text = "(без фотографий)"
    else:
        photos_text = f"(с {user.photos} фотографиями)"

    if user.sort_order == "PRICE":
        choice = "Вы выбрали поиск топ дешевых отелей"
    elif user.sort_order == "PRICE_HIGHEST_FIRST":
        choice = "Вы выбрали поиск топ дорогих отелей"
    else:
        choice = "Вы выбрали топ отелей, наиболее подходящих по цене и расположению от центра"
        price_distance_range = "\n".join((f"Диапазон цен за ночь: {user.min_price} - {user.max_price} RUB.",
                                          f"Диапазон расстояния от центра: {user.min_distance} - {user.max_distance} км."))

    result = "\n".join((choice, f"в городе: {user.city}",
                        f"с {check_in} по {check_out} ({days} ночей)", f"показать {user.hotels_amount} отелей",
                        photos_text, price_distance_range))
    return result


@bot.callback_query_handler(func=lambda call: call.data == "yes_search_request")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, который запускает поиск отелей по заданным параметрам, если пользователь подтверждает корректность
    ввода своих данных в инлайн клавиатуре. Перенаправляет на обработчик perform_search.
    :param CallbackQuery call: yes_search_request
    :return: None
    """

    info(f"Callback yes_search_request working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id,
                     text="Отлично! Подождите секунду, ищу отели...")
    perform_search.perform_search(chat_id=call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == "no_search_request")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, который сбрасывает введенную пользователем информацию и уточняет следующее действие.
    :param CallbackQuery call: no_search_request
    :return: None
    """

    info(f"Callback no_search_request working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id,
                     text="Давайте попробуем еще раз...\nВведите нужную команду!",
                     reply_markup=commands_keyboard.commands_keyboard())
