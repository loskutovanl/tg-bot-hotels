from typing import Iterator
import json
from config_data import config
from re import sub
from . import request_to_api
from logging import info


def get_hotel_photos(hotel_id: str, photos_amount: int) -> Iterator[str]:
    """
    Генератор, который по id отеля и нужному пользователю кол-ву фотографий делает запрос к rapidAPI через
    request_to_api, получает JSON и извлекает из него url фотографий отеля. Генерирует и возвращает ссылки на фото.
    :param str hotel_id: уникальный id отеля
    :param int photos_amount: нужное пользователю кол-во фото
    :return Iterator[str]: генератор url-ссылок на фото
    """

    info("Doing func get_hotel_photos")

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel_id}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.RAPID_API_KEY
    }

    response = request_to_api.request_to_api(url=url, headers=headers, querystring=querystring)

    data = json.loads(response.text)

    for i in range(photos_amount):
        base_url = data["hotelImages"][i].get("baseUrl", 0)
        size = data["hotelImages"][i]["sizes"][0].get("suffix")
        i_photo_url = sub(pattern=r"{size}", repl=size, string=base_url)

        yield i_photo_url
