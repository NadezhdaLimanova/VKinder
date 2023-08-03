from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
from datetime import date


class VKbot:
    def __init__(self, token):
        # авторизация
        self.token = token
        self.vk = vk_api.VkApi(token=self.token)
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
                user = self.session_api.users.get(user_ids=user_id, fields="bdate, city, sex") # получение информации о пользователе
                first_name = user[0]['first_name']
                bdate = user[0]['bdate']
                sex = user[0]['sex']
                city = user[0]['city']['title']
                if len(bdate) == 9:  # проверка указан ли возраст
                    bdate_year = bdate[-4:]
                    now = date.today()
                    year = now.year
                    age = year - int(bdate_year)
                else:
                    age = None
            if event.to_me:
                    request = event.text
                    if request == 'Начать' or request.lower() == 'привет':
                        message = f"Привет, {first_name}! Здесь мы поможем тебе найти свою половинку! Нажми на кнопку ниже"
                        self.write_msg(user_id, 1, message)
                    elif request == 'Вернуться':
                        message = 'Нажми кнопку ниже'
                        self.write_msg(user_id, 1, message)
                    elif request == "Показать анкеты":
                        user_id_from_bd = self.session_api.users.get(user_ids=user_id, fields="bdate, city, sex")
                        bdate_bd = user[0]['bdate']
                        sex_bd = user[0]['sex']
                        city_bd = user[0]['city']['title']
                        if len(bdate_bd) == 9:  # проверка указан ли возраст
                            bdate_year = bdate_bd[-4:]
                            now = date.today()
                            year = now.year
                            age_bd = year - int(bdate_year)
                        else:
                            age_bd = None
                        if age is not None or age_bd is not None:
                            if age + 5 > age_bd > age - 5 and city == city_from_bd and sex != sex_from_bd: # проверка на совпадение данных пользователя с профилем из базы данных
                            # информация из базы данных:
                                name_from_bd = name
                                profile_link = link
                                photo_1 = photo_1
                                photo_2 = photo_2
                                photo_3 = photo_3
                                message = "Вот несколько фотографий и имя пользователя, если вам интересен этот человек, то добавьте его в избранное или нажмите пропустить", name_from_bd, profile_link, photo_1, photo_2, photo_3
                                self.write_msg(user_id, 2, message)
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
                    elif request == 'Пока' or request == 'пока':
                        message = 'До свидания!'
                        self.write_msg(user_id, 4, message)
                    else:
                        message = "Не поняла Вашего ответа...Напишите 'привет'"
                        self.write_msg(user_id, 4, message)



if __name__ == "__main__":
    with open('token.txt', 'r', encoding='utf-8') as file:
        vk_token = file.read()
    token = vk_token
    bot = VKbot(token)
    bot.run()