from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
import datetime
from BD.func_BD import check_database, check_table, add_user_database
import re

class VKbot:
    def __init__(self, token, token_user):
        # авторизация
        self.token = token
        self.token_user = token_user
        self.vk = vk_api.VkApi(token=self.token)
        self.vk_user = vk_api.VkApi(token=self.token_user)
        self.longpoll = VkLongPoll(self.vk)
        self.upload = VkUpload(self.vk)
        self.session_api = self.vk.get_api()
        self.vk_user_get = self.vk_user.get_api()

        # установка клавиатуры и кнопок
        self.keyboard_1 = VkKeyboard(one_time=True)
        self.keyboard_1.add_button('Показать анкеты', color=VkKeyboardColor.POSITIVE)
        self.keyboard_1.add_button('Показать избранное', color=VkKeyboardColor.PRIMARY)

        self.keyboard_2 = VkKeyboard(one_time=True)
        self.keyboard_2.add_button('Добавить в избранное', color=VkKeyboardColor.POSITIVE)
        self.keyboard_2.add_line()
        self.keyboard_2.add_button('Пропустить', color=VkKeyboardColor.SECONDARY)
        self.keyboard_2.add_line()
        self.keyboard_2.add_button('Показать избранное', color=VkKeyboardColor.PRIMARY)

        self.keyboard_3 = VkKeyboard(one_time=True)
        self.keyboard_3.add_button('Вернуться', color=VkKeyboardColor.SECONDARY)


    def write_msg(self, user_id, i, message): # функция для определения в каком виде будет сообщение бота пользователю
        self.user_id = user_id
        self.i = i
        self.message = message
        if self.i == 1:
            self.vk.method('messages.send', {'user_id': user_id,
                                             'message': self.message,
                                             'random_id': randrange(10 ** 7),
                                             'keyboard': self.keyboard_1.get_keyboard()})
        if self.i == 2:
            self.vk.method('messages.send', {'user_id': user_id,
                                             'message': self.message,
                                             'random_id': randrange(10 ** 7),
                                             'keyboard': self.keyboard_2.get_keyboard()})
        if self.i == 3:
            self.vk.method('messages.send', {'user_id': user_id, 'message': self.message,
                                                                'random_id': randrange(10 ** 7),
                                                                'keyboard': self.keyboard_3.get_keyboard()})
        if self.i == 4:
            self.vk.method('messages.send', {'user_id': user_id, 'message': self.message,
                                             'random_id': randrange(10 ** 7)})


    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                user_id = event.user_id
                if event.to_me:
                    request = event.text
                    return request

    def get_user_data(self, user_id):
        self.user_data = {}
        resp = self.vk.method('users.get', {'user_id': user_id,
                                            'v': 5.131,
                                            'fields': 'first name, last name, bdate, sex, city'})
        if resp:
            for key, value in resp[0].items():
                if key == 'city':
                    self.user_data[key] = value['title']
                else:
                    self.user_data[key] = value
            return self.user_data

    """Поиск пары по параметрам"""

    # def user_search(self, user_info):
    #
    #     resp = self.vk_user.method('users.search', {
    #         'age_from': self.user_info['age'] - 5,
    #         'age_to': self.user_info['age'] + 5,
    #         'city': self.user_info['city'],
    #         'sex': 3 - self.user_info['sex'],
    #         'relation': 6,
    #         'status': 1,
    #         'has_photo': 1,
    #         'count': 1000,
    #         'v': 5.131})
    #     print(resp)
    #     if resp:
    #         if resp.get('items'):
    #             return resp.get('items')


    def check_bdate(self, user_info, user_id):
        if user_info:
            for item_dict in [user_info]:
                try:
                    if len(item_dict['bdate'].split('.')) == 3:
                        bdate = item_dict['bdate']
                        age = datetime.datetime.now().year - int(bdate[-4:])
                        return age
                    else:
                        bot_message = 'Введите дату рождения в формате "ДД.ММ.ГГГГ:"'
                        self.write_msg(user_id, 4, bot_message)
                        request = self.listen()
                        if re.match(r'\d\d\.\d\d.\d\d\d\d', request):
                            bdate = request
                            age = datetime.datetime.now().year - int(bdate[-4:])
                            return age
                except KeyError:
                    bot_message = 'Введите дату рождения в формате "ДД.ММ.ГГГГ:"'
                    self.write_msg(user_id, 4, bot_message)
                    request = self.listen()
                    if re.match(r'\d\d\.\d\d.\d\d\d\d', request):
                        bdate = request
                        age = datetime.datetime.now().year - int(bdate[-4:])
                        return age

    def check_city(self, user_info, user_id):
        if user_info:
            for item_dict in [user_info]:
                try:
                    if 'city' != None:
                        return item_dict['city']
                except KeyError:
                    bot_message = 'Введите корректно название Вашего города. Пример: Москва'
                    self.write_msg(user_id, 4, bot_message)
                    city = self.listen()
                    return city


    def run(self):  # функция для алгоритма общения с пользователем и вывода информации
        counter = 0
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                user_id = event.user_id
                if event.to_me:
                    request = event.text
                    # info = self.get_user_data()
                    first_name = self.get_user_data(user_id)['first_name']   # Использование сторонних классов
                    if request == 'Начать' or request.lower() == 'привет':
                        message = f"Привет, {first_name}! Здесь мы поможем тебе найти свою половинку!  Нажми на кнопку ниже"
                        self.write_msg(user_id, 1, message)

                    elif request == 'Вернуться':
                        message = 'Нажми кнопку ниже'
                        self.write_msg(user_id, 1, message)
                    elif request == "Показать анкеты":
                        user_info = self.get_user_data(user_id)
                        print(user_info)
                        age = self.check_bdate(user_info, user_id)
                        print(age)
                        city = self.check_city(user_info, user_id)
                        print(city)
                        if 'bdate' in user_info:
                            del user_info['bdate']
                            user_info['age'] = age
                        else:
                            user_info['age'] = age
                        print(user_info)
                        if 'city' not in user_info:
                            user_info['city'] = city
                        print(user_info)
                        add_user_database(user_info)
                        # profile_link = link
                        # photo_1 = photo_1
                        # photo_2 = photo_2
                        # photo_3 = photo_3

                        # user_id_from_bd = self.session_api.users.get(user_ids=user_id, fields="bdate, city, sex")
                        # bdate_bd = user[0]['bdate']
                        # sex_bd = user[0]['sex']
                        # city_bd = user[0]['city']['title']
                        # if len(bdate_bd) == 9:  # проверка указан ли возраст
                        #     bdate_year = bdate_bd[-4:]
                        #     now = date.today()
                        #     year = now.year
                        #     age_bd = year - int(bdate_year)
                        # else:
                        #     age_bd = None
                        # if age is not None or age_bd is not None:
                        #     if age + 5 > age_bd > age - 5 and city == city_from_bd and sex != sex_from_bd: # проверка на совпадение данных пользователя с профилем из базы данных
                        #     # информация из базы данных:
                        #
                        # message = "Вот несколько фотографий и имя пользователя, если вам интересен этот человек, то добавьте его в избранное или нажмите пропустить", name_from_bd, profile_link, photo_1, photo_2, photo_3
                        # self.write_msg(user_id, 2, message)
                    elif request == 'Показать избранное':
                        if counter == 0:
                            message = "Пока вы ничего не добавили в избранное"
                            self.write_msg(user_id, 3, message)
                        else:
                            # информация из базы данных
                            fav_name_from_bd = name
                            fav_profile_link = link
                            fav_photo_1 = photo_1
                            fav_photo_2 = photo_2
                            fav_photo_3 = photo_3
                            message = "Ваш выбранные профили: ", fav_name_from_bd,  fav_profile_link, fav_photo_1, fav_photo_2, fav_photo_3
                            self.write_msg(user_id, 3, message)
                    elif request == 'Пропустить':
                        if age is not None or age_bd is not None:
                            if age + 5 > age_bd > age - 5 and city == city_from_bd and sex != sex_from_bd:
                                name_from_bd = name
                                profile_link = link
                                photo_1 = photo_1
                                photo_2 = photo_2
                                photo_3 = photo_3
                                message = "Вот несколько фотографий и имя пользователя, если вам интересен этот человек, то добавьте его в избранное или нажмите пропустить", name_from_bd, profile_link, photo_1, photo_2, photo_3
                                self.write_msg(user_id, 2, message)
                    elif request == 'Добавить в избранное':  # добавить избранный профиль в таблицу базы данных
                        message = "Профиль добавлен в избранное"
                        self.write_msg(user_id, 1, message)
                        counter += 1
                    elif request.lower() == 'пока':
                        message = 'До свидания!'
                        self.write_msg(user_id, 4, message)
                    else:
                        message = "Не поняла Вашего ответа...Напишите 'привет'"
                        self.write_msg(user_id, 4, message)










if __name__ == "__main__":
    check_database()
    check_table()
    with open('token.txt', 'r', encoding='utf-8') as file:
        vk_token = file.read()
    with open('token.txt', 'r', encoding='utf-8') as file:
        vk_token_user = file.read()
    token = vk_token
    token_user = vk_token_user
    bot = VKbot(token, token_user)
    bot.run()