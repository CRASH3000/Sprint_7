import pytest
import requests
import allure
from data.url_data import Url
from data.expected_responses import expected_responses


@allure.suite("2. Логин курьера")
@allure.story("Тестирование авторизации курьера")
@pytest.mark.usefixtures("courier_for_login")
class TestCourierLoginAPI:

    @allure.title("1. Авторизация курьера")
    @allure.description(
        "Проверка, что курьер может авторизоваться и успешный запрос возвращает id"
    )
    @allure.step(
        "Отправляем POST-запрос на авторизацию курьера с логином и паролем, которые мы получили при создании курьера"
    )
    def test_courier_can_login(self, courier_for_login):

        response = requests.post(
            f"{Url.BASE_URL}/courier/login",
            json={
                "login": courier_for_login["login"],
                "password": courier_for_login["password"],
            },
        )
        assert response.status_code == 200, "Код ответа не 200 при успешной авторизации"
        assert "id" in response.json(), "Ответ не содержит id"

        # Сохранение ID курьера
        self.__class__.courier_id = response.json()["id"]

    @allure.title("2. Для авторизации нужно передать все обязательные поля")
    @allure.description("Проверка, что система вернёт ошибку, если какого-то поля нет")
    @allure.step(
        "Отправляем POST-запрос на авторизацию курьера с логином и паролем, которые мы получили при создании курьера"
    )
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field, courier_for_login):
        invalid_data = courier_for_login.copy()
        del invalid_data[missing_field]

        response = requests.post(f"{Url.BASE_URL}/courier/login", json=invalid_data)
        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии обязательного поля"
        assert (
            response.json() == expected_responses["courier_login"]["missing_error"]
        ), "Сообщение об ошибке не совпадает"

    @allure.title("3. Система вернёт ошибку, если неправильно указать логин или пароль")
    @allure.description(
        "Проверка, что система вернёт ошибку, если неправильно указать логин или пароль"
    )
    @allure.step(
        "Отправляем POST-запрос на авторизацию курьера с неправильными данными"
    )
    def test_login_with_incorrect_credentials(self):
        invalid_data = {"login": "wrong_login", "password": "wrong_password"}

        response = requests.post(f"{Url.BASE_URL}/courier/login", json=invalid_data)
        assert (
            response.status_code == 404
        ), "Код ответа не 404 при неправильных учетных данных"
        assert (
            response.json() == expected_responses["courier_login"]["login_error"]
        ), "Сообщение об ошибке не совпадает"

    @allure.title(
        "4. Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку"
    )
    @allure.description(
        "Проверка, что система вернёт ошибку при попытке авторизации под несуществующим пользователем"
    )
    @allure.step(
        "Отправляем POST-запрос на авторизацию курьера с логином и паролем, которые не существуют"
    )
    def test_login_nonexistent_user(self):
        nonexistent_data = {
            "login": "nonexistent_user",
            "password": "nonexistent_password",
        }

        response = requests.post(f"{Url.BASE_URL}/courier/login", json=nonexistent_data)

        assert (
            response.status_code == 404
        ), "Код ответа не 404 при попытке авторизации несуществующего пользователя"
        assert (
            response.json() == expected_responses["courier_login"]["login_error"]
        ), "Сообщение об ошибке не совпадает"
