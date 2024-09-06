import requests
import allure
from data.url_data import Url
from data.expected_responses import expected_responses
from data.account_test_data import incorrect_credentials


@allure.suite("2. Логин курьера")
@allure.story("Тестирование авторизации курьера")
class TestCourierLoginAPI:

    @allure.title("1. Авторизация курьера")
    @allure.description(
        "Отправляем POST-запрос на авторизацию курьера с логином и паролем, которые мы получили при создании курьера "
        "Проверяем, что курьер может авторизоваться и успешный запрос возвращает id."
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

    @allure.title("2. Авторизация без логина")
    @allure.description(
        "Отправляем POST-запрос на авторизацию курьера с логином и паролем, которые мы получили при создании курьера."
        "Проверяем, что нужно передать все обязательные поля и система вернёт ошибку, если нет логина"
    )
    def test_login_missing_login(self):
        invalid_data = incorrect_credentials.copy()
        del invalid_data["login"]

        response = requests.post(f"{Url.BASE_URL}/courier/login", json=invalid_data)

        assert response.json() == expected_responses["courier_login"]["missing_error"]

    @allure.title("3. Авторизация без пароля")
    @allure.description(
        "Отправляем POST-запрос на авторизацию курьера с логином и паролем, которые мы получили при создании курьера."
        "Проверяем, что нужно передать все обязательные поля и система вернёт ошибку, если нет логина"
    )
    def test_login_missing_password(self):
        invalid_data = incorrect_credentials.copy()
        del invalid_data["password"]

        response = requests.post(f"{Url.BASE_URL}/courier/login", json=invalid_data)

        assert response.json() == expected_responses["courier_login"]["missing_error"]

    @allure.title("4. Система вернёт ошибку, если неправильно указать логин или пароль")
    @allure.description(
        "Отправляем POST-запрос на авторизацию курьера с неправильными данными. "
        "Проверяем, что система вернёт ошибку, если неправильно указать логин или пароль"
    )
    def test_login_with_incorrect_credentials(self):
        invalid_data = incorrect_credentials

        response = requests.post(f"{Url.BASE_URL}/courier/login", json=invalid_data)

        assert response.json() == expected_responses["courier_login"]["login_error"]
