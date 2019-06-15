import requests
import translator
import img_labels
import get_objects
from random import randint


def send_response(img_description, detected_objects, saved_img_info, vk, user_id):  # Отправка ответа пользователю
    if detected_objects:
        response = 'Описание: ' + img_description + '\n Обнаруженные объекты: ' + detected_objects
        vk.messages.send(user_id=user_id,
                        attachment='photo%s_%s' % (saved_img_info[0]['owner_id'], saved_img_info[0]['id']),
                        message=response, random_id=randint(1, 2000))
    elif img_description == '':
        response = 'Не удалось обнаружить объекты на изображении.'
        vk.messages.send(user_id=user_id, message=response, random_id=randint(1, 2000))
    else:
        response = 'Описание: ' + img_description
        vk.messages.send(user_id=user_id, message=response, random_id=randint(1, 2000))


def upload_img(vk, user_id):  # Функция которая загружает изображение на сервер вк
    upload_info = vk.photos.getMessagesUploadServer(peer_id=user_id)
    upload_url = upload_info['upload_url']
    uploaded_img = requests.post(upload_url, files={'photo': open('img.jpg', 'rb')}).json()
    saved_img_info = vk.photos.saveMessagesPhoto(server=uploaded_img['server'], photo=uploaded_img['photo'], hash=uploaded_img['hash'])
    return saved_img_info


def analyze_image(vk, user_id):
    labels = img_labels.get_img_labels()  # Получение описания изображения
    labels_arr = []
    for label in labels:
        labels_arr.append(label.description)
    img_description = translator.translate_text(labels_arr)  # Перевод описания изображения на русский

    detected_objects = get_objects.detect_objects_on_img()  # Получение списка объектов на изображении
    if detected_objects:
        detected_objects = translator.translate_text(detected_objects)  # Перевод названия объектов на русский

    saved_img_info = upload_img(vk, user_id)  # Загружаем изображение на сервер вк
    send_response(img_description, detected_objects, saved_img_info, vk, user_id)
