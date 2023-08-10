import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from BD.models_BD import Base, users_table, applicants_table, favorites_table
from BD.key_BD import username, password, name_bd


engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/{name_bd}')
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


def add_user_database(user_data: dict):
    if check_users(user_data) is None:
        try:
            session.add(users_table(id_vk_users=user_data['id'], sex=user_data['sex'], age=user_data['age'], city=user_data['city']))
            session.commit()
            return True
        except(IntegrityError, InvalidRequestError):
            return False


def check_users(user_id: str):
    """
    Проверяем, существуют ли пользователь с таким ID
    """
    current_user_id = session.query(users_table).filter_by(id_vk_users=user_id['id']).first()
    return current_user_id


def add_applicant_database(applicant_data: dict, user_data: dict):
    list_id_applicants = []
    for i in session.query(users_table).filter(users_table.id_vk_users == user_data['id']):
        id_user = i.id
    for applicants in session.query(applicants_table).filter_by(id_user=id_user):
        list_id_applicants.append(applicants.id_vk_applicant)
    if applicant_data['id'] not in list_id_applicants:
        session.add(applicants_table(id_user=id_user,
                                     id_vk_applicant=applicant_data['id'],
                                     first_name=applicant_data['first_name'],
                                     last_name=applicant_data['last_name'],
                                     id_link_applicant=f"https://{applicant_data['vk_link']}",
                                     photo_1='s',
                                     photo_2='s',
                                     photo_3='s'))
        session.commit()
        return True
    else:
        return False


def add_favorite_database(applicant_data: dict, user_data: dict):
    list_id_favorite = []
    for i in session.query(users_table).filter(users_table.id_vk_users == user_data['id']):
        id_user = i.id
    for favorite in session.query(favorites_table).filter_by(id_user=id_user):
        list_id_favorite.append(favorite.id_vk_favorite)
    if applicant_data['id'] not in list_id_favorite:
        session.add(favorites_table(id_user=id_user,
                                     id_vk_favorite=applicant_data['id'],
                                     first_name=applicant_data['first_name'],
                                     last_name=applicant_data['last_name'],
                                     id_link_favorite=f"https://{applicant_data['vk_link']}",
                                     photo_1='s',
                                     photo_2='s',
                                     photo_3='s'))
        session.commit()
        return True
    else:
        return False