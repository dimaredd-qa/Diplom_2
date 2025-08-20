import pytest
import allure
from helpers.api_requests import create_user
from data.data import ExistingUser

@allure.feature("Создание пользователя")
@allure.story("Тестирование создания пользователя в различных сценариях")
class TestCreateUser:
    @allure.title("Тест создание пользователя")
    def test_create_user(self, for_delete_user):
        data_user = for_delete_user
        response = create_user(data_user)
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        with allure.step("Проверить тело ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
            assert "refreshToken" in response_data, "Refresh токен отсутствует в ответе"
            assert response_data["user"]["email"] == for_delete_user["email"], "Email не совпадает"
            assert response_data["user"]["name"] == for_delete_user["name"], "Name не совпадает"

    @allure.title("Тест регистрация с уже существующим email")
    def test_registration_with_existing_email(self):
        response = create_user(ExistingUser.existing_user)
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == "User already exists", "Неверное сообщение об ошибке"

    @pytest.mark.parametrize("field", ["email", "password", "name"])
    @allure.title("Тест регистрация с отсутствующим обязательным полем {field}")
    def test_registration_with_missing_field(self, for_delete_user, field):
        data_user = for_delete_user.copy()
        del data_user[field]
        response = create_user(data_user)
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        with allure.step("Проверить сообщение об ошибке"):
            assert "required fields" in response.json()["message"], "Неверное сообщение об ошибке"

    @allure.title("Тест регистрация с невалидным email")
    def test_registration_with_invalid_email(self, for_delete_user):
        data_user = for_delete_user
        data_user["email"] = "invalid_email"
        response = create_user(data_user)
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        with allure.step("Проверить сообщение об ошибке"):
            assert "required fields" in response.json()["message"], "Неверное сообщение об ошибке"