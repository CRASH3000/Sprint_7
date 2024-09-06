import requests
import allure
from data.courier_generator_data import generate_random_courier_data
from data.url_data import Url
from data.expected_responses import expected_responses


@allure.suite("1. Создание курьера")
@allure.story("Тестирование функционала создания курьера")
class TestCourierAPI:

    @allure.title("1. Создание курьера")
    @allure.description(
        "Проверка, что курьера можно создать и ответом приходит код 201 и 'ok': True"
    )
    def test_create_courier(self, delete_courier):
        courier_data = generate_random_courier_data()

        response = requests.post(f"{Url.BASE_URL}/courier", json=courier_data)

        assert response.status_code == 201
        assert response.json() == expected_responses["courier"]["create_success"]

    @allure.title("2. Нельзя создать двух одинаковых курьеров")
    @allure.description(
        "Проверка, что нельзя создать двух одинаковых курьеров и ответом приходит "
        "код 409 и сообщение об ошибке'Этот логин уже используется'"
    )
    def test_create_duplicate_courier(self, create_courier):
        courier_data = create_courier

        # Повторная попытка создать того же курьера
        duplicate_response = requests.post(f"{Url.BASE_URL}/courier", json=courier_data)

        assert (
            duplicate_response.json()
            == expected_responses["courier"]["duplicate_error"]
        )

    @allure.title("3. Создание курьера без имени")
    @allure.description(
        "Проверка, что можно создать курьера без имени, но с логином и паролем"
    )
    def test_create_courier_with_login_and_password(self, create_courier):
        courier_data = create_courier

        partial_data = {
            "login": courier_data["login"],
            "password": courier_data["password"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)

        assert response.json() == expected_responses["courier"]["duplicate_error"]

    @allure.title("4. Создание курьера без логина")
    @allure.description(
        "Проверка, что создание курьера только с паролем и именем приводит к ошибке 400 "
        "с сообщением 'Недостаточно данных для создания учетной записи'"
    )
    def test_create_courier_with_password_and_firstname(
        self, create_courier
    ):
        courier_data = create_courier

        partial_data = {
            "password": courier_data["password"],
            "firstName": courier_data["firstName"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)

        assert response.json() == expected_responses["courier"]["missing_field_error"]

    @allure.title("5. Создание курьера без пароля")
    @allure.description(
        "Проверка, что создание курьера только с логином и именем приводит к ошибке 400 "
        "с сообщением 'Недостаточно данных для создания учетной записи'"
    )
    def test_create_courier_with_login_and_firstname(self, create_courier):
        courier_data = create_courier

        partial_data = {
            "login": courier_data["login"],
            "firstName": courier_data["firstName"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)

        assert response.json() == expected_responses["courier"]["missing_field_error"]

    @allure.title(
        "6. Если создать пользователя с логином, который уже есть, возвращается ошибка."
    )
    @allure.description(
        "Проверка, что создание пользователя с существующим логином вызывает ошибку 409 "
        "с сообщением 'Этот логин уже используется'"
    )
    def test_create_courier_with_existing_login(self, create_courier):
        courier_data = create_courier
        # Генерируем новый пароль и имя, но используем старый логин
        new_data = generate_random_courier_data()
        new_data["login"] = courier_data["login"]  # Используем старый логин

        response = requests.post(f"{Url.BASE_URL}/courier", json=new_data)

        assert response.json() == expected_responses["courier"]["duplicate_error"]
