import sqlalchemy as sq
from sqlalchemy.orm import declarative_base

Data = declarative_base()

"""Создание классов"""


class User(Data):
    __tablename__ = 'Пользователь'

    user_id = sq.Column(sq.Integer, primary_key=True)
    id = sq.Column(sq.Integer, unique=True)

    def __str__(self):
        return f'User {self.id}: {self.user_id}'


class UserData(Data):

    __tablename__ = 'Все данные'

    user_id = sq.Column(sq.Integer, primary_key=True)
    id = sq.Column(sq.Integer, unique=True)

    def __str__(self):
        return f'User_search_data {self.id}: {self.user_id}'


class WhiteList(Data):

    __tablename__ = 'Избранные'

    user_id = sq.Column(sq.Integer, primary_key=True)
    id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String, nullable=False)
    last_name = sq.Column(sq.String, nullable=False)
    vk_link = sq.Column(sq.String, unique=True, nullable=False)

    def __str__(self):
        return f'WhiteList {self.id}: {self.user_id}, {self.first_name},' \
               f'{self.last_name}, {self.vk_link}'


class BlackList(Data):
    __tablename__ = 'Чёрный список'

    user_id = sq.Column(sq.Integer, primary_key=True)
    id = sq.Column(sq.Integer, unique=True)

    def __str__(self):
        return f'BlackList {self.id}: {self.user_id}'


"""Создание таблиц"""


def create_tables(engine):
    Data.metadata.create_all(engine)


"""Удаление таблиц"""


def drop_tables(engine):
    Data.metadata.drop_all(engine)