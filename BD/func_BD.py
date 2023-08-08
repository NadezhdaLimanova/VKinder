import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models_BD import Base, users_table, applicants_table, favorites_table
from key_BD import username, password, name_bd


engine = create_engine(f'postgresql+psycopg2://{username}:{password}@localhost:5432/{name_bd}')
Session = sessionmaker(bind=engine)
session = Session()


def check_database():
    """
    Проверяем, существует ли база данных и если нет, то создаем
    """
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
        print(f"Создание базы данных прошло успешно")
    else:
        print(f"База данных уже существует")


def check_table():
    """
    Проверяем, существует ли таблицы в базе данных
    """
    name_table = ["users", "applicants", "favorites"]

    for table in name_table:
        check_tables = sqlalchemy.inspect(engine).has_table(f"{table}", schema="public")
        if check_tables == True:
            print(f"{table} существует в базе данных")
        else:
            print(f"{table} не существует в базе данных")


def add_user_database(users_data: dict):
    if check_users(users_data['id']) is None:
        try:
            session.add(users_table(id_vk_users=users_data['id'], sex=users_data['sex'], age=users_data['bdate'], city=1))
            session.commit()
            return True
        except(IntegrityError, InvalidRequestError):
            return False


def check_users(user_data: str):
    """
    Проверяем, существуют ли пользователь с таким ID
    """
    current_user_id = session.query(users_table).filter_by(id_vk_users=user_data).first()
    return current_user_id


def add_applicant_database():
    pass