import requests
import vk_authorization
import gcp_authorization
from random import randint
from vk_api.longpoll import VkLongPoll, VkEventType
import analyze_image


vk_session = vk_authorization.authorization()  # Авторизация в вк
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


gcp_authorization.gcp_authorization()  # Создаем локальную переменную для атовризации на gcp


def find_last_img_url_in_dialog():  # Функция которая находит последнее сообщение, содержащие изображение
    messages = vk.messages.getHistory(user_id=event.user_id)
    msg_num = len(messages['items'])
    img_url = False
    i = 0
    while i < msg_num and img_url == False:
        if len(messages['items'][i]['fwd_messages']) == 0:
            if messages['items'][i]['text'] == '':
                if messages['items'][i]['attachments'][0]['type'] == 'photo':
                    img_url = messages['items'][i]['attachments'][0]['photo']['sizes'][2]['url']
        i += 1
    return img_url


def download_img(url):  # Функция которая загружает изображение на сервер
    r = requests.get(url, allow_redirects=True)
    open('img.jpg', 'wb').write(r.content)


def send_error_msg(error_text):
    vk.messages.send(user_id=event.user_id, message=error_text, random_id=randint(1, 2000))


def send_greeting_msg():
    msg = 'Привет! Я использую обученную нейронную сеть, чтобы анализировать изображения. ' \
          'Пришли мне изображение, а затем выбери нужное действие из панели управления.'
    vk.messages.send(user_id=event.user_id, message=msg, random_id=randint(1, 2000))


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:
        img_url = find_last_img_url_in_dialog()  # Проверка на наличие изображения в сообщении
        if img_url:
            download_img(img_url)  # Загрузка изображения на сервер
            analyze_image.analyze_image(vk, event.user_id)  # Функция по обнаружению объектов на изображении
        elif event.text == 'Начать':
            send_greeting_msg()  # Отправка приветствия новому пользователю
        else:
            error_text = 'Пришлите изображение.'
            send_error_msg(error_text)
