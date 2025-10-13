import allure
from helpers.api_requests import login_user
from data.data import ExistingUser

@allure.feature("Авторизация пользователя")
@allure.story("Тестирование авторизации пользователя в различных сценариях")
class TestUserLogin:
    @allure.title("Тест успешный вход под существующим пользователем")
    def test_successful_login(self):
        with allure.step("Отправить запрос на авторизацию"):
            response = login_user(ExistingUser.existing_user["email"], ExistingUser.existing_user["password"])
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, (
                f"Ожидался статус код 200, получен {response.status_code}. "
                f"Response: {response.text}"
            )
        with allure.step("Проверить тело ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
            assert "refreshToken" in response_data, "Refresh токен отсутствует в ответе"
            assert response_data["user"]["email"] == ExistingUser.existing_user["email"], "Email не совпадает"

    @allure.title("Тест вход с неверным паролем")
    def test_login_with_wrong_password(self, for_auth_delete_user):
        email = for_auth_delete_user["email"]
        wrong_password = "wrong_" + for_auth_delete_user["password"]
        with allure.step("Попытка авторизации с неверным паролем"):
            response = login_user(email, wrong_password)
        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
            assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"