from vkinder import VKbot
from BD.func_BD import check_database, check_table


if __name__ == "__main__":
    check_database()
    check_table()
    with open('token.txt', 'r', encoding='utf-8') as file:
        vk_token = file.read()
    with open('token_vk.txt', 'r', encoding='utf-8') as file:
        vk_token_user = file.read()
    token = vk_token
    token_user = vk_token_user
    bot = VKbot(token, token_user)
    bot.run()