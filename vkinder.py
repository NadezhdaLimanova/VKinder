from random import randrange
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
import datetime
from pprint import pprint
# from BD.func_BD import add_user_database, add_applicant_database, add_favorite_database, favorites_output
import re




class VKbot:
    def __init__(self, token, token_user):

    # """авторизация"""

        self.token = token
        self.token_user = token_user
        self.vk = vk_api.VkApi(token=self.token)
        self.vk_user = vk_api.VkApi(token=self.token_user)
        self.longpoll = VkLongPoll(self.vk)
        self.upload = VkUpload(self.vk)
        self.session_api = self.vk.get_api()
        self.vk_user_get = self.vk_user.get_api()

    # """установка клавиатуры и кнопок"""

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

        self.keyboard_4 = VkKeyboard(one_time=True)
        self.keyboard_4.add_button('Начать заново', color=VkKeyboardColor.SECONDARY)

    # """функция для определения в каком виде будет сообщение бота пользователю"""

    def write_msg(self, user_id, i, message,
                  attachment=None):  #
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
                                             'attachment': attachment,
                                             'random_id': randrange(10 ** 7),
                                             'keyboard': self.keyboard_2.get_keyboard()})
        if self.i == 3:
            self.vk.method('messages.send', {'user_id': user_id, 'message': self.message,
                                             'random_id': randrange(10 ** 7),
                                             'attachment': attachment,
                                             'keyboard': self.keyboard_3.get_keyboard()})
        if self.i == 4:
            self.vk.method('messages.send', {'user_id': user_id, 'message': self.message,
                                             'random_id': randrange(10 ** 7)})

        if self.i == 5:
            self.vk.method('messages.send', {'user_id': user_id, 'message': self.message,
                                             'random_id': randrange(10 ** 7),
                                             'keyboard': self.keyboard_4.get_keyboard()})


    # """функция для получения и распознавания сообщений от пользователя"""

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                user_id = event.user_id
                if event.to_me:
                    request = event.text
                    return request

    # """функция для получения общей информации о пользователе из Вконтакте"""

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

    # """функция для получения информации о дате рождения пользователя"""

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

    # """функция для получения информации о городе пользователя"""

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

    """Поиск потенциальных кандидатов для пользователя по определенным параметрам"""

    def user_search(self, user_info):
        resp = self.vk_user.method('users.search', {
            'age_from': user_info['age'] - 5,
            'age_to': user_info['age'] + 5,
            'hometown': user_info['city'],
            'sex': 3 - user_info['sex'],
            'relation': 6,
            'status': 1,
            'has_photo': 1,
            'count': 1000,
            'v': 5.131})
        if resp:
            if resp.get('items'):
                return resp.get('items')

    # """отсеивание закрытых аккаунтов потенциальных кандидатов"""

    def get_users_list(self, users_data, user_id):
        not_private_list = []
        if users_data:
            for person_dict in users_data:
                if person_dict.get('is_closed') == False:
                    not_private_list.append(
                        {'first_name': person_dict.get('first_name'), 'last_name': person_dict.get('last_name'),
                         'id': person_dict.get('id'), 'vk_link': 'vk.com/id' + str(person_dict.get('id')),
                         'is_closed': person_dict.get('is_closed')
                         })
                else:
                    continue
            return not_private_list

    """Выбор случайного  из списка потенциальных кандидатов"""

    def get_random_user(self, users_data, user_id):
        if users_data:
            return random.choice(users_data)

    """Получение фотографий потенциального кандидата из VK"""

    def get_photos(self, vk_id):

        resp = self.vk_user.method('photos.getAll', {
            'owner_id': vk_id,
            'album_id': 'profile',
            'extended': 'likes',
            'count': 25
        })
        if resp:
            if resp.get('items'):
                return resp.get('items')

    # """сортировка фотографий по количеству лайков"""

    def sort_by_likes(self, photos_dict):
        photos_by_likes_list = []
        for photos in photos_dict:
            likes = photos.get('likes')
            photos_by_likes_list.append([photos.get('owner_id'), photos.get('id'), likes.get('count')])
        photos_by_likes_list = sorted(photos_by_likes_list, key=lambda x: x[2], reverse=True)
        return photos_by_likes_list

    """Получение 3 фотографий с самым большим количеством лайков"""

    def get_photos_list(self, sort_list):
        photos_list = []
        count = 0
        if len(sort_list) == 1 or len(sort_list) == 2:
            message = 'У этого пользователя слишком мало фотографий'
            self.write_msg(self.user_id, 4, message)
        else:
            for photos in sort_list:
                photos_list.append('photo' + str(photos[0]) + '_' + str(photos[1]))
                count += 1
                if count == 3:
                    return photos_list

    # """функция, запускающая бота"""

    def run(self):
        applicants_list = []
        counter = 0
        counter_1 = 0
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                user_id = event.user_id
                if event.to_me:
                    request = event.text
                    first_name = self.get_user_data(user_id)['first_name']
                    if request == 'Начать' or request.lower() == 'привет':
                        message = f"Привет, {first_name}! Здесь мы поможем тебе найти свою половинку!  Нажми на кнопку ниже"
                        self.write_msg(user_id, 1, message)

                    elif request == 'Показать избранное':
                        if counter == 0:
                            message = "Пока вы ничего не добавили в избранное"
                            self.write_msg(user_id, 3, message)
                        else:
                            # favorites_list = favorites_output(user_info)
                            favorites_list = [{'id_link_favorites': 'https://vk.com/id231613868', 'first_name': 'Р”РјРёС‚СЂРёР№', 'last_name': 'Р�РІР°РЅРѕРІ', 'photo_1': 'photo231613868_457267795', 'photo_2': 'photo231613868_457254237', 'photo_3': 'photo231613868_457267089'}, {'id_link_favorites': 'https://vk.com/id324868454', 'first_name': 'РџР°РІРµР»', 'last_name': 'Р–СѓРєРѕРІ', 'photo_1': 'photo324868454_456240157', 'photo_2': 'photo324868454_456239364', 'photo_3': 'photo324868454_456239205'}]
                            # favorites_list = ['https://vk.com/id231613868', 'Р”РјРёС‚СЂРёР№', 'Р�РІР°РЅРѕРІ', 'photo231613868_457267795', 'photo231613868_457254237', 'photo231613868_457267089'}, {'id_link_favorites': 'https://vk.com/id324868454', 'first_name': 'РџР°РІРµР»', 'last_name': 'Р–СѓРєРѕРІ', 'photo_1': 'photo324868454_456240157', 'photo_2': 'photo324868454_456239364', 'photo_3': 'photo324868454_456239205'}]

                            message = "Ваш выбранные профили: "
                            self.write_msg(user_id, 3, message)
                            for i in favorites_list:
                                print(i)
                                self.write_msg(user_id, 3, {
                                    i['first_name'] + ' ' + i[
                                        'last_name'] + '\n' + 'Ссылка на профиль: ' +
                                    i['id_link_favorites']}, {','.join([i['photo_1'], i['photo_2'], i['photo_3']])})



                    elif request == 'Вернуться':
                        message = 'Нажми кнопку ниже'
                        self.write_msg(user_id, 1, message)

                    elif request in ["Показать анкеты", 'Пропустить', 'Начать заново']:
                        if counter_1 == 0:
                            user_info = self.get_user_data(user_id)
                            age = self.check_bdate(user_info, user_id)
                            city = self.check_city(user_info, user_id)
                            if 'bdate' in user_info:
                                del user_info['bdate']
                                user_info['age'] = age
                            else:
                                user_info['age'] = age
                            if 'city' not in user_info:
                                user_info['city'] = city
                        counter_1 += 1
                        # add_user_database(user_info)
                        try:
                            users_data = self.user_search(user_info)
                            list = self.get_users_list(users_data, user_id)
                            get_vk_id = self.get_random_user(list, user_id)
                            sort_list = self.get_photos_list(self.sort_by_likes(self.get_photos(get_vk_id['id'])))

                            if get_vk_id['id'] not in applicants_list:
                                self.write_msg(user_id, 2, {
                                    get_vk_id['first_name'] + ' ' + get_vk_id['last_name'] + '\n' + 'Ссылка на профиль: ' +
                                    get_vk_id['vk_link']}, {','.join(sort_list)})
                                applicants_list.append(get_vk_id)
                                # add_applicant_database(get_vk_id, user_info, sort_list)
                        except TypeError:
                            message = 'Ошибка, попробуйте заново'
                            self.write_msg(user_id, 5, message)
                            counter_1 -= 1


                    elif request == 'Добавить в избранное':
                        # add_favorite_database(get_vk_id, user_info, sort_list)

                        message = "Профиль добавлен в избранное"
                        self.write_msg(user_id, 1, message)
                        counter += 1

                    elif request.lower() == 'пока':
                        message = 'До свидания!'
                        self.write_msg(user_id, 4, message)

                    else:
                        message = "Не поняла Вашего ответа...Напишите 'привет'"
                        self.write_msg(user_id, 4, message)



