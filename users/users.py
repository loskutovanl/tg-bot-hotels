from typing import Optional, List
from datetime import datetime


class Users:
    """
    Класс пользователей, в котором для каждого конкретного пользователя (user_id=chat_id в словаре all_users) хранятся
    данные последнего введенного запроса: команда боту command, тип сортировки для rapidAPI sort_order, даты заезда и
    выезда check_in & check_out, город назначения city, id места назначения destination_id, список информации обо
    всех подходящих мечтах назначения locations, кол-во отелей для вывода hotels_amount, кол-во фотографий для вывода
    photos, диапазон цен min_price & max_price и растояний min_distance & max_distance (для команды bestdeal).
    """

    all_users = dict()

    def __init__(self, user_id: int) -> None:
        self.command: Optional[str] = None
        self.sort_order: Optional[str] = None
        self.check_in: Optional[datetime] = None
        self.check_out: Optional[datetime] = None
        self.city: Optional[str] = None
        self.destination_id: Optional[int] = None
        self.locations: Optional[List[dict]] = None
        self.hotels_amount: Optional[int] = None
        self.photos: Optional[int] = None
        self.min_price: Optional[int] = None
        self.max_price: Optional[int] = None
        self.min_distance: Optional[float] = None
        self.max_distance: Optional[float] = None
        Users.add_user(user_id, self)

    @classmethod
    def get_user(cls, user_id: int) -> 'Users':
        """Геттер для получения пользователя (объекта класса) по его id, если пользователь уже существует или
        создания и возвращения нового пользователя"""
        if Users.all_users.get(user_id) is None:
            new_user = Users(user_id)
            return new_user
        return Users.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id: int, user: 'Users') -> None:
        """Функция добавляет нового пользователя"""
        cls.all_users[user_id] = user

    @staticmethod
    def get_check_in(user_id: int) -> datetime:
        """Геттер для даты заезда"""
        user = Users.all_users[user_id]
        return user.check_in

    @staticmethod
    def get_check_out(user_id: int) -> datetime:
        """Геттер для даты выезда"""
        user = Users.all_users[user_id]
        return user.check_out

    @staticmethod
    def get_command(user_id: int) -> str:
        """Геттер для команды пользователя"""
        user = Users.all_users[user_id]
        return user.command

    @staticmethod
    def get_city(user_id: int) -> str:
        """Геттер для названия места назначения"""
        user = Users.all_users[user_id]
        return user.city

    @staticmethod
    def get_destination_id(user_id: int) -> int:
        """Геттер для id места назначения"""
        user = Users.all_users[user_id]
        return user.destination_id

    @staticmethod
    def get_photos(user_id: int) -> int:
        """Геттер для получения кол-ва фотографий"""
        user = Users.all_users[user_id]
        return user.photos

    @staticmethod
    def get_hotels_amount(user_id: int) -> int:
        """Геттер для получения кол-ва отелей"""
        user = Users.all_users[user_id]
        return user.hotels_amount

    @staticmethod
    def get_min_price(user_id: int) -> int:
        """Геттер для минимальной цены за ночь"""
        user = Users.all_users[user_id]
        return user.min_price

    @staticmethod
    def get_max_price(user_id: int) -> int:
        """Геттер для максимальной цены за ночь"""
        user = Users.all_users[user_id]
        return user.max_price

    @staticmethod
    def get_min_distance(user_id: int) -> float:
        """Геттер для минимального расстояния от центра"""
        user = Users.all_users[user_id]
        return user.min_distance

    @staticmethod
    def get_max_distance(user_id: int) -> float:
        """Геттер для максимального расстояния от центра"""
        user = Users.all_users[user_id]
        return user.max_distance
