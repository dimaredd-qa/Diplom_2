import allure
from data.data import DataBurger
from helpers.api_requests import login_user, create_order

@allure.feature("Создание заказа")
@allure.story("Тестирование создания заказа в различных сценариях")
class TestCreateOrder:
    @allure.title("Тест создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_authorized_with_ingredients(self, for_auth_delete_user):
        with allure.step("Запрос на вход пользователя"):
            auth_response = login_user(for_auth_delete_user["email"], for_auth_delete_user["password"])
            token = auth_response.json().get("accessToken")
            headers = {"Authorization": token}
        with allure.step("Запрос создания заказа"):
            order_data = {"ingredients": DataBurger.burger_four_ingre}
            response = create_order(order_data, headers)
        with allure.step("Проверить успешный ответ"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "name" in response_data
            assert "order" in response_data
            assert "number" in response_data["order"]

    @allure.title("Тест создание заказа без авторизации")
    def test_create_order_unauthorized(self, for_reg_delete_user):
        with allure.step("Запрос на новый заказ без авторизации"):
            order_data = {"ingredients": DataBurger.burger_four_ingre}
            response = create_order(order_data)
        with allure.step("Проверить успешный ответ и тело ответа"):
            assert response.status_code == 200
            assert response.json().get("success") is True

    @allure.title("Тест создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, for_auth_delete_user):
        with allure.step("Запрос на вход пользователя"):
            auth_response = login_user(for_auth_delete_user["email"], for_auth_delete_user["password"])
            token = auth_response.json().get("accessToken")
            headers = {"Authorization": token}
        with allure.step("Попытка создать заказ без ингредиентов"):
            order_data = {"ingredients": []}
            response = create_order(order_data, headers)
        with allure.step("Проверить код и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Тест создание заказа с невалидным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self, for_auth_delete_user):
        with allure.step("Запрос на вход пользователя"):
            auth_response = login_user(for_auth_delete_user["email"], for_auth_delete_user["password"])
            token = auth_response.json().get("accessToken")
            headers = {"Authorization": token}
        with allure.step("Пытаться создать заказ с невалидным хешем ингредиента"):
            order_data = {"ingredients": ["invalid_hash_123", "another_invalid_hash"]}
            response = create_order(order_data, headers)
        with allure.step("Проверить код ошибки 500"):
            assert response.status_code == 500