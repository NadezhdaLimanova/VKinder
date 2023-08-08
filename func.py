import random
from random import randrange
import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy_utils import database_exists, create_database
from bot_db import create_tables, drop_tables, User, UserData, WhiteList, BlackList
from sqlalchemy.exc import IntegrityError, InvalidRequestError, PendingRollbackError

url_object = URL.create(
    'postgresql',
    username='postgres',
    password='',
    host='localhost',
    database='VKinder',
)


"""Создание движка"""
engine = create_engine(url_object)


"""Создание ДБ, а также удаление (если есть) и создание таблиц в ней"""
if not database_exists(engine.url):
    create_database(engine.url)

drop_tables(engine)
create_tables(engine)

Session = sessionmaker(bind=engine)


session = Session()


"""vk_tokens"""
with open('bot_token.txt', 'r') as file:
    bot_token = file.readline()
with open('user_token.txt', 'r') as file:
    user_token = file.readline()

vk_bot = vk_api.VkApi(token=bot_token)
vk_user = vk_api.VkApi(token=user_token)
longpoll = VkLongPoll(vk_bot)


"""Обеспечение отправки сообщений пользователю"""


def write_msg(user_id, message, attachment):
    vk_bot.method('messages.send',
              {'user_id': user_id, 'message': message, 'attachment': attachment,  'random_id': randrange(10 ** 7)})


"""Получение пользовательских данных"""


def get_user_data(user_id):
    user_data = {}
    resp = vk_bot.method('users.get', {'user_id': user_id,
                                   'v': 5.131,
                                   'fields': 'first name, last name, bdate, sex, city'})
    if resp:
        for key, value in resp[0].items():
            if key == 'city':
                user_data[key] = value['id']
            else:
                user_data[key] = value
    else:
        write_msg(user_id, 'Ошибка', None)
        return False
    return user_data



"""Проверка наличия даты рождения. Если её нет - ввести"""


def check_bdate(user_data, user_id):
    if user_data:
        for item_dict in [user_data]:
            if len(item_dict['bdate'].split('.')) != 3:
                write_msg(user_id, f'Введите дату рождения в формате "ДД.ММ.ГГГГ:"', None)
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        user_data['bdate'] = event.text
                        return user_data
            else:
                return user_data
    write_msg(user_data['id'], 'Ошибка в дате рождения', None)
    return False


"""Проверка по городу"""


def check_city(user_data, user_id):
    if user_data:
        for item_dict in [user_data]:
            if item_dict['city'] == '':
                write_msg(user_id, f'Введите город:', None)
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        user_data['city'] = city_id(event.text)[0]['id']
                        return user_data
            else:
                return user_data
    write_msg(user_data['id'], 'Введите название города корректно', None)
    return False

"""Название города в id города"""


def city_id(city_name):
    resp = vk_user.method('database.getCities', {
                    'country_id': 1,
                    'q': f'{city_name}',
                    'need_all': 0,
                    'count': 1000,
                    'v': 5.131})
    if resp:
        if resp.get('items'):
            return resp.get('items')
        write_msg(city_name, 'Ошибка, проверьте город', None)
        return False





"""Подсчёт возраста пользователей"""


def get_age(user_data):
    if user_data:
        for key, value in user_data:
            user_data['age'] = datetime.datetime.now().year - int(user_data['bdate'][-4:])
            return user_data
    write_msg(user_data['id'], 'Ошибка', None)
    return False

"""Поиск пары по параметрам"""

def user_search(user_data):
    resp = vk_user.method('users.search', {
                                'age_from': user_data['age'] - 5,
                                'age_to': user_data['age'] + 5,
                                'city': user_data['city'],
                                'sex': 3 - user_data['sex'],
                                'relation': 6,
                                'status': 1,
                                'has_photo': 1,
                                'count': 1000,
                                'v': 5.131})
    if resp:
        if resp.get('items'):
            return resp.get('items')
        write_msg(user_data['id'], 'Ошибка, попробуйте ещё раз', None)
        return False


"""Отсеивание закрытых аккаунтов"""


def get_users_list(users_data, user_id):
    not_private_list = []
    if users_data:
        for person_dict in users_data:
            if person_dict.get('is_closed') == False:
                not_private_list.append(
                                {'first_name': person_dict.get('first_name'), 'last_name': person_dict.get('last_name'),
                                 'id': person_dict.get('id'), 'vk_link':   'vk.com/id'+str(person_dict.get('id')),
                                 'is_closed': person_dict.get('is_closed')
                                 })
            else:
                continue
        return not_private_list
    write_msg(user_id, 'Ошибка', None)
    return False


"""Объединение пользовательских данных"""


def combine_user_data(user_id):
    user_data = [get_age(check_city(check_bdate(get_user_data(user_id), user_id), user_id))]
    if user_data:
        return user_data
    write_msg(user_id, 'Ошибка', None)
    return False

"""Объединение пользовательских данных по поиску"""


def combine_users_data(user_id):
    users_data = get_users_list(
        user_search(get_age(check_city(check_bdate(get_user_data(user_id), user_id), user_id))), user_id)
    if users_data:
        return users_data
    write_msg(user_id, 'Ошибка', None)
    return False



"""Выбор случайного аккаунта"""


def get_random_user(users_data, user_id):
    if users_data:
        return random.choice(users_data)
    write_msg(user_id, 'Ошибка', None)
    return False


"""Получение фотографий из VK"""


def get_photos(vk_id):

    resp = vk_user.method('photos.getAll', {
            'owner_id': vk_id,
            'album_id': 'profile',
            'extended': 'likes',
            'count': 25
        })
    if resp:
        if resp.get('items'):
            return resp.get('items')
        write_msg(vk_id, 'Ошибка', None)
        return False


"""Сортировка фотографий по лайкам"""


def sort_by_likes(photos_dict):
    photos_by_likes_list = []

    for photos in photos_dict:
        likes = photos.get('likes')
        photos_by_likes_list.append([photos.get('owner_id'), photos.get('id'), likes.get('count')])
    photos_by_likes_list = sorted(photos_by_likes_list, key=lambda x: x[2], reverse=True)
    return photos_by_likes_list


"""Получение 3 лучших фотографий на основе лайков"""


def get_photos_list(sort_list):
    photos_list = []
    count = 0
    for photos in sort_list:
        photos_list.append('photo'+str(photos[0])+'_'+str(photos[1]))
        count += 1
        if count == 3:
            return photos_list


"""Заполнение таблицы пользователя"""


def fill_user_table(user_data):
    if user_data:
        for item in user_data:
            user_record = session.query(User).filter_by(id=item['id']).scalar()
            if not user_record:
                user_record = User(id=item['id'])
            session.add(user_record)
            session.commit()
        return True
    write_msg(user_data['id'], 'Ошибка', None)
    return False


"""Заполнение таблицы поиска"""


def fill_user_search_table(users_data, user_id):
    try:
        for item in users_data:
            users_record = session.query(UserData).filter_by(id=item['id']).scalar()
            if not users_record:
                users_record = UserData(id=item['id'])
            session.add(users_record)
            session.commit()
        return True
    except (IntegrityError, InvalidRequestError, PendingRollbackError, TypeError):
        session.rollback()
        write_msg(user_id, 'Ошибка', None)
        return False


"""Заполнение белого списка - ИЗБРАННЫЕ"""


def fill_white_list(random_choice):
    for item in random_choice:
        random_user_record = session.query(WhiteList).filter_by(id=item['id']).scalar()
        if not random_user_record:
            random_user_record = WhiteList(id=item['id'], first_name=item['first_name'], last_name=item['last_name'],
                                            vk_link=item['vk_link']
                                            )
        session.add(random_user_record)
    return session.commit()


"""Заполнение чёрного списка"""


def fill_black_list(random_choice):
    for item in random_choice:
        random_user_record = session.query(BlackList).filter_by(id=item['id']).scalar()
        if not random_user_record:
            random_user_record = BlackList(id=item['id'])
        session.add(random_user_record)
    return session.commit()


"""Получение избранных"""


def check_db_favorites(user_id):
    db_favorites = session.query(WhiteList).order_by(WhiteList.user_id).all()
    all_users = []
    if db_favorites:
        for item in db_favorites:
            all_users.append([item.user_id, 'id:'+str(item.id), item.first_name+' '+item.last_name, item.vk_link+' '])
        return all_users
    write_msg(user_id, 'Ошибка', None)
    return False

"""Ожидание бота"""


def loop_bot():
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text




