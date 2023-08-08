import random
from random import randrange
import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload




class Vk_info_data:

    def __init__(self, user_id, token=None, token_user=None):
        self.user_id = user_id
        self.token = token
        self.token_user = token_user
        self.vk_user = vk_api.VkApi(token=token_user)
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk)
        self.upload = VkUpload(self.vk)
        self.session_api = self.vk.get_api()



    """Получение пользовательских данных"""

    def get_user_data(self):
        self.user_data = {}
        resp = self.vk.method('users.get', {'user_id': self.user_id,
                                            'v': 5.131,
                                            'fields': 'first name, last name, bdate, sex, city'})
        if resp:
            for key, value in resp[0].items():
                if key == 'city':
                    self.user_data[key] = value['title']
                else:
                    self.user_data[key] = value
            return self.user_data





