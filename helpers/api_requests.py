import allure
import requests

from data.data import Endpoint

@allure.step("Создание пользователя")
def create_user(data_user):
    response = requests.post(Endpoint.create_user_url, json=data_user)
    return response

@allure.step("Авторизация пользователя")
def login_user(email, password):
    response = requests.post(Endpoint.login_user_url, json={"email": email, "password": password})
    return response

@allure.step("Создание заказа")
def create_order(order_data, headers=None):
    response = requests.post(Endpoint.order_create_url, json=order_data, headers=headers)
    return response

@allure.step("Удаление пользователя")
def delete_user(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(Endpoint.profile_user_url, headers=headers)
    return response

@allure.step("Получение токена авторизации")
def get_auth_token(email, password):
    login_data = {"email": email, "password": password}
    response = requests.post(Endpoint.login_user_url, json=login_data)
    if response.status_code == 200:
        return response.json().get("accessToken")
    return None