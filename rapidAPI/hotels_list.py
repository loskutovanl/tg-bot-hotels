from typing import Iterator, Tuple
import json
from peewee import IntegrityError
from config_data import config
from datetime import datetime
from . import request_to_api
from users import users
from database import database
from logging import info, warning


def get_hotels(destination_id: str, chat_id: int) -> Iterator[Tuple[int, str]]:
    """
    Генератор для команд lowprice и highprice, который по id места назначения делает запрос к rapidAPI через
    request_to_api, получает JSON и извлекает из него всю необходимую пользователю информацию об отеле. С помощью
    id пользователя записывает историю его поиска в реляционную базу данных db.
    :param str destination_id: id места назначения
    :param int chat_id: уникальный id пользователя
    :return Iterator[Tuple[int, str]]: генерирует и возвращает кортеж id отеля / строковое представление всей информации
    об отеле. Если ничего не найдено, возвращает None.
    :raises IntegrityError: если найденный отель уже существует в базе данных, чтобы не было дупликатов записей.
    """

    info(f"User {chat_id} doing func get_hotels")

    user = users.Users.get_user(user_id=chat_id)

    with database.db:
        command = database.Command.create(user_id=chat_id, name=user.command,
                                          details=f"{user.city}; с {user.check_in} по {user.check_out}")

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": destination_id, "pageNumber": "1", "pageSize": str(user.hotels_amount),
                   "checkIn": datetime.strftime(user.check_in, "%Y-%m-%d"),
                   "checkOut": datetime.strftime(user.check_out, "%Y-%m-%d"), "adults1": "1",
                   "sortOrder": user.sort_order, "locale": "ru_RU", "currency": "RUB"}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.RAPID_API_KEY
    }

    response = request_to_api.request_to_api(url=url, headers=headers, querystring=querystring)

    if response:
        data = json.loads(response.text)
        info(f'Response get_hotels: : {data}')

        hotels = data["data"]["body"]["searchResults"].get("results", 0)

        if hotels:
            for i_hotel in hotels:
                hotel_remoteness = i_hotel["landmarks"][0].get("distance", 0)
                hotel_id = i_hotel.get("id", 0)
                hotel_name = i_hotel.get("name", 0)
                hotel_address = i_hotel["address"].get("streetAddress", 0)
                hotel_price = i_hotel["ratePlan"]["price"].get("current", 0)
                nights = (user.check_out - user.check_in).days
                hotel_total_price = round(i_hotel["ratePlan"]["price"].get("exactCurrent", 0) * nights, 2)
                hotel_url = f"www.hotels.com/ho{hotel_id}"

                hotel_info = f"Название отеля: {hotel_name}\nАдрес: {hotel_address}\n" \
                             f"Удаленность от центра: {hotel_remoteness}\n" \
                             f"Цена за ночь: {hotel_price}\nЦена за {nights} ночей: {hotel_total_price} RUB\n" \
                             f"Сайт отеля: {hotel_url}\n"

                with database.db:
                    database.Command2Hotel.create(command_id=command.id, hotel_id=hotel_id)

                    try:
                        database.Hotel.create(id=hotel_id, name=hotel_name, web_site=hotel_url)
                    except IntegrityError as exc:
                        warning(f"peewee IntegrityError occurred. Details: {exc}")
                        pass

                yield hotel_id, hotel_info

        else:
            return None

    else:
        return None
