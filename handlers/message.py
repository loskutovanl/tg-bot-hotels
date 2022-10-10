from telebot.types import Message
from keyboards.inline import helloworld_keyboard
from handlers import history, lowprice_highprice_bestdeal, help, helloworld
from loader import bot
from logging import info


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message) -> None:
    """
    Хендлер, обрабатывающийлюбое введенное пользователем сообщение и перенапрвляющий его на соответствующие обработчики
    или выдающий ошибку на нечленораздельные команды.
    :param Message message: любое сообщение пользователя
    :return: None
    """

    info(f"User {message.chat.id} doing func get_text_messages")
    if message.text.lower() == "привет" or message.text == "/helloworld":
        helloworld.helloworld_executor(message)
    elif message.text == "/help":
        help.help_executor(message)
    elif message.text == "/lowprice" or message.text == "/highprice" or message.text == "/bestdeal":
        lowprice_highprice_bestdeal.search_commands(message)
    elif message.text == "/history":
        history.history_executor(message)
    else:
        bot.send_message(chat_id=message.chat.id,
                         parse_mode="Markdown",
                         text="Я вас не понимаю. Чтобы начать, напишите _Привет_ или введи команду /helloworld ;)",
                         reply_markup=helloworld_keyboard.helloworld_keyboard())
