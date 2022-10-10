import datetime
from peewee import SqliteDatabase, IntegerField, CharField, DateTimeField, Model, ForeignKeyField


# SQL база данных для хранения команд пользователей
db = SqliteDatabase('database/commands.db')


# базовый класс
class BaseModel(Model):
    class Meta:
        database = db


# Класс-таблица команд Command для хранения идентификатора команды id, идентификатора пользователя (user_id = chat_id),
# названия команды name, даты и времени введения команды date, инфо о команде details (город поиска, даты заезда/выезда)
class Command(BaseModel):
    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    name = CharField()
    date = DateTimeField(default=datetime.datetime.now)
    details = CharField()


# Класс-таблица отелей Hotel для хранения идентификатора отеля id, названия отеля name, веб-сайта отеля web_site
class Hotel(BaseModel):
    id = IntegerField(unique=True)
    name = CharField()
    web_site = CharField()


# Класс-таблица Command2Hotel, хранящая связи идентификатор команды command_id - идентификатор найденного отеля hotel_id
class Command2Hotel(BaseModel):
    command_id = ForeignKeyField(Command)
    hotel_id = ForeignKeyField(Hotel)


db.create_tables([Command, Hotel, Command2Hotel])
