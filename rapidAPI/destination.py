from typing import Optional
import json
from config_data import config
from . import request_to_api
from logging import info


def get_destination_id(city: str) -> Optional[list]:
    """
    Функция, которая по введенному пользователем названию города делает запрос к rapidAPI через request_to_api, получает
    JSON и извлекает из него список подходящих локаций с наилучшим совпадением.
    :param str city: введенный пользователем город
    :return Optional[Tuple[int, str]]: кортеж id города / наименование города. Если ничего не найдено, возвращает None
    """

    info("Doing func get_destination_id")

    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}

    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.RAPID_API_KEY
    }

    response = request_to_api.request_to_api(url=url, headers=headers, querystring=querystring)

    if response:
        data = json.loads(response.text)

        if data["suggestions"][0]["entities"]:
            return data["suggestions"][0]["entities"]

        else:
            return None

    else:
        return None
