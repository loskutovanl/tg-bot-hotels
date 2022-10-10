import requests
from logging import error, info
from typing import Dict, Any


def request_to_api(url: str, headers: Dict[str, str], querystring: Dict[str, str]) -> Any:
    """
    Универсальная функция, которая делает запрос к rapidAPI и возвращает найденные данные в формате JSON либо None,
    если произошла ошибка.
    :param str url: url-адрес rapidAPI
    :param Dict[str, str] headers: уникальные ключи для доступа к rapidAPI
    :param Dict[str, str] querystring: фильтры, по которым происходит поиск на rapidAPI
    :return Optional[json]: информация по городу/отелям/фотографиям.
    :raises Timeout: в случае если ответ от сервера ожидается дольше 20 сек.
    """

    info("Doing func request_to_api")

    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=20)

        if response.status_code == requests.codes.ok:
            return response
    except requests.exceptions.Timeout as exc:
        error(f"Timeout error occurred while doing func request_to_api. Details: {exc}")
        return None
