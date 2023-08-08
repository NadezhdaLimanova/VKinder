from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
from datetime import date
from VK_info import Vk_info_data
from BD.func_BD import check_database, check_table, add_user_database
import re

class VKbot:
    def __init__(self, token, token_user):
        # авторизация
        self.token = token
        self.token_user = token_user
        self.vk = vk_api.VkApi(token=self.token)
        self.vk_user = vk_api.VkApi(token=token_user)
        self.longpoll = VkLongPoll(self.vk)
        self.upload = VkUpload(self.vk)
        self.session_api = self.vk.get_api()

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


    def run(self):  # функция для алгоритма общения с пользователем и вывода информации
        counter = 0
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                user_id = event.user_id
                if event.to_me:
                    request = event.text
                    info = Vk_info_data(user_id, token).get_user_data()
                    first_name = Vk_info_data(user_id, token).get_user_data()['first_name']   # Использование сторонних классов

                    if request == 'Начать' or request.lower() == 'привет':
                        message = f"Привет, {first_name}! Здесь мы поможем тебе найти свою половинку!  Нажми на кнопку ниже"
                        self.write_msg(user_id, 1, message)
                        add_user_database(Vk_info_data.get_user_data(self))
                    elif request == 'Вернуться':
                        message = 'Нажми кнопку ниже'
                        self.write_msg(user_id, 1, message)
                    elif request == "Показать анкеты":
                        res = Vk_info_data(user_id, token).check_bdate()     # Использование сторонних классов
                        if len(res) > 10:
                            self.write_msg(user_id, 4, res)
                        else:
                            bdate = res
                            print(bdate)
                    elif re.match(r'\d\d\.\d\d.\d\d\d\d', request):
                            bdate = request
                            print(bdate)

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