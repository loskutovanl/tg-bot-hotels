from telebot.types import Message, CallbackQuery
from keyboards.inline import help_keyboard
from loader import bot
from logging import info


@bot.message_handler(commands=['helloworld'])
def helloworld_executor(message: Message) -> None:
    """
    Хендлер, обрабатывающий команду helloworld.
    :param Message message: /helloworld
    :return: None
    """

    info(f"User {message.chat.id} doing func helloworld_executor")
    bot.send_message(chat_id=message.chat.id,
                     parse_mode="Markdown",
                     text=f"Привет, {message.from_user.username}! \U0001F609 Давай знакомиться. Я твой бот из агентства "
                          f"*Too Easy Travel* \U00002708 и я помогу тебе найти "
                          f"отель твоей мечты ;) Чтобы узнать, что я могу, введи команду /help!",
                     reply_markup=help_keyboard.help_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == "helloworld")
def callback_query(call: CallbackQuery) -> None:
    """
    Колбек, обрабатывающий нажатие helloworld на всплывающих инлайн-клавиатурах.
    :param CallbackQuery call: helloworld
    :return: None
    """

    info(f"Callback helloworld working for user {call.message.chat.id}")
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    helloworld_executor(call.message)
