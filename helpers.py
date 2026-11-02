import random
import string

import allure
import requests

from routes import Routes


def random_text(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def make_account_data():
    return {
        "email": "qa_ui_" + random_text(15) + "@example.com",
        "password": random_text(15),
        "name": "Test",
    }


@allure.step("Создать тестового пользователя")
def create_account(account_payload):
    response = requests.post(Routes.REGISTER_API, json=account_payload, timeout=30)
    response.raise_for_status()
    return response.json()["accessToken"]


@allure.step("Удалить тестового пользователя")
def remove_account(token):
    response = requests.delete(
        Routes.USER_API, headers={"Authorization": token}, timeout=30
    )
    response.raise_for_status()
