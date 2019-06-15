from random import randint
from PIL import Image, ImageDraw
from google.cloud import vision


def detect_objects_on_img():
    img = Image.open("img.jpg")
    img_width = img.width
    img_height = img.height

    client = vision.ImageAnnotatorClient()
    with open('img.jpg', 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    if len(objects) != 0:
        objects_name = []
        for object_ in objects:
            objects_name.append(object_.name)
            obj_coordinates = []

            # Получение и добавления в массив координат объекта
            # Используем переменную i, чтобы достать координаты только двух точек
            # Так как для постороения прямоугольника необходимо лишь две точки

            i = 0
            for vertex in object_.bounding_poly.normalized_vertices:
                if i == 0 or i == 2:
                    obj_coordinates.append(vertex.x * img_width)
                    obj_coordinates.append(vertex.y * img_height)
                i += 2
            draw = ImageDraw.Draw(img)  # Выделение объектов на изображении по заданным координатам
            draw.rectangle(obj_coordinates, width=3, outline=(randint(1, 255), randint(1, 255), randint(1, 255)))
        img.save('img.jpg')  # Заменяем старое изображение на отредактированное
        return objects_name  # Возвращаем названия объектов
    else:
        return False
