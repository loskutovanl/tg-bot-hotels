from telebot.types import Message, CallbackQuery
from loader import bot
from database.database import Command, Command2Hotel, Hotel
from keyboards.inline import commands_keyboard
from logging import info


@bot.message_handler(commands=['history'])
def history_executor(message: Message) -> None:
    """
    Хендлер, обрабатывающий команду history.
    :param Message message: /history
    :return: None
    """

    info(f"User {message.chat.id} doing func history")
    bot.send_message(chat_id=message.chat.id,
                     text="Минутку, загружаю историю ваших последних 15 запросов...")

    command_query = Command.select().where(Command.user_id == message.chat.id)

    if len(command_query) > 15:
        command_query = command_query[len(command_query) - 15:]

    for command in command_query:
        command_date = command.date.strftime("%H:%M %m/%d/%Y")
        command_text = f"{command_date} {command.name} {command.details}"

        hotel_query = (Hotel
                       .select()
                       .join(Command2Hotel, on=(Hotel.id == Command2Hotel.hotel_id))
                       .where(Command2Hotel.command_id == command.id))

        for hotel in hotel_query:

            command_text = f"{command_text}\n\n    {hotel.name}: {hotel.web_site};"

        bot.send_message(chat_id=message.chat.id,
                         text=command_text)

    bot.send_message(chat_id=message.chat.id,
                     text="Готово! Что делаем дальше?",
                     reply_markup=commands_keyboard.commands_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "history")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывающий нажатие history на всплывающих инлайн-клавиатурах.
    :param CallbackQuery call: history
    :return: None
    """

    info(f"Callback history working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    history_executor(call.message)
