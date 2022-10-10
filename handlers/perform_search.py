from loader import bot
from rapidAPI import hotels_list, hotel_photos, hotels_list_bestdeal
from users import users
from keyboards.inline import commands_keyboard
from logging import info, warning


def perform_search(chat_id: int) -> None:
    """
    Функция, производящая поиск отелей по заданным пользователем параметрам. По id места назначения запрашивает отели
    (get_hotels или get_bestdeal_hotels). Если требуется, для каждого отеля запрашивает фотографии (get_hotel_photos).
    Всю полученную информацию выводит пользователю сообщениями. При неудачном поиске сообщает об ошибке.
    :param chat_id: уникальный id пользователя
    :return: None
    :raises StopIteration: когда количество найденных отелей меньше желаемого пользователем
    """

    info(f"User {chat_id} doing func perform_search")
    user = users.Users.get_user(user_id=chat_id)

    destination_id = user.destination_id
    destination_name = user.city

    bot.send_message(chat_id=chat_id,
                     text=f"Выгружаю результаты для {destination_name}:")

    if user.sort_order == "PRICE" or user.sort_order == "PRICE_HIGHEST_FIRST":
        hotels_info = hotels_list.get_hotels(destination_id=str(destination_id),
                                             chat_id=chat_id)
    else:
        hotels_info = hotels_list_bestdeal.get_bestdeal_hotels(destination_id=str(destination_id),
                                                               chat_id=chat_id)

    if hotels_info:

        try:
            for i in range(user.hotels_amount):
                i_hotel_id, i_hotel_info = next(hotels_info)
                bot.send_message(chat_id=chat_id,
                                 text=i_hotel_info)

                if user.photos:
                    i_hotel_photos = hotel_photos.get_hotel_photos(hotel_id=str(i_hotel_id),
                                                                   photos_amount=user.photos)
                    for j in range(user.photos):
                        j_photo_url = next(i_hotel_photos)
                        bot.send_photo(chat_id=chat_id,
                                       photo=j_photo_url)

            bot.send_message(chat_id=chat_id,
                             text="Готово! Что делаем дальше?",
                             reply_markup=commands_keyboard.commands_keyboard())

        except StopIteration:
            warning(f"StopIteration Error raised. Reason: less hotels are available"
                    f" than requested by user {chat_id}")
            bot.send_message(chat_id=chat_id,
                             text="Больше отелей не найдено! Что делаем дальше?",
                             reply_markup=commands_keyboard.commands_keyboard())

    else:
        warning(f"Search unsuccessful by user {chat_id}")
        bot.send_message(chat_id=chat_id,
                         text=f"Упс, похоже в городе {user.city} ничего не найдено :(\n"
                              f"Что делаем дальше?",
                         reply_markup=commands_keyboard.commands_keyboard())
