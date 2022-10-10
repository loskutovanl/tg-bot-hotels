from telebot.types import Message, CallbackQuery
from keyboards.inline import commands_keyboard
from loader import bot
from logging import info


@bot.message_handler(commands=['help'])
def help_executor(message: Message) -> None:
    """
    Хендлер, обрабатывающий команду help.
    :param Message message: /help
    :return: None
    """

    info(f"User {message.chat.id} doing func help")
    bot.send_message(chat_id=message.chat.id,
                     text="Вот что я умею:",
                     reply_markup=commands_keyboard.commands_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "help")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывающий нажатие help на всплывающих инлайн-клавиатурах.
    :param CallbackQuery call: help
    :return: None
    """

    info(f"Callback help working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    help_executor(call.message)
