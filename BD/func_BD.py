import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists

from models_BD import Base
from key_BD import username, password, name_bd


engine = create_engine(f'postgresql+psycopg2://{username}:{password}@localhost:5432/{name_bd}')


"""
Проверяем, существует ли база данных и если нет, то создаем
"""


def check_database():
    if not database_exists(engine.url):
        Base.metadata.create_all(engine)
        print(f"Создание базы данных прошло успешно")
    else:
        print(f"База данных уже существует")


"""
Проверяем, существует ли таблицы в базе данных
"""


def check_table():

    name_table = ["users", "applicants", "favorites"]

    for table in name_table:
            check_tables = sqlalchemy.inspect(engine).has_table(f"{table}", schema="public")
            if check_tables == True:
                print(f"{table} существует в базе данных")
            else:
                print(f"{table} не существует в базе данных")


if __name__ == "__main__":
    check_database()
    check_table()