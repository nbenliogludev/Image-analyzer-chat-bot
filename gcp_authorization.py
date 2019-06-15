import os


# Создание локальной переменной в которой хранится ключ. Необходимо для работы с gcp
def gcp_authorization():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
