import pytest
import requests
import allure
from data.courier_generator_data import generate_random_courier_data
from data.url_data import Url
from data.expected_responses import expected_responses


@allure.suite("1. Создание курьера")
@allure.story("Тестирование функционала создания курьера")
@pytest.mark.usefixtures("create_courier")
class TestCourierAPI:

    @allure.title("1. Создание курьера")
    @allure.description(
        "Проверка, что курьера можно создать и ответом приходит код 201 и 'ok': True"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера с сгенерированными данными в Json файле"
    )
    def test_create_courier(self, create_courier):
        courier_data, response_data = create_courier

        assert (
            response_data == expected_responses["courier"]["create_success"]
        ), "Первичный запрос на создание курьера вернул некорректный ответ"

    @allure.title("2. Нельзя создать двух одинаковых курьеров")
    @allure.description(
        "Проверка, что нельзя создать двух одинаковых курьеров и ответом приходит "
        "код 409 и сообщение об ошибке'Этот логин уже используется'"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера с ранее сгенерированными данными снова"
    )
    def test_create_duplicate_courier(self, create_courier):
        courier_data, _ = create_courier
        response = requests.post(f"{Url.BASE_URL}/courier", json=courier_data)

        assert response.status_code == 409, "Код ответа не 409 для повторного логина"
        assert (
            response.json() == expected_responses["courier"]["duplicate_error"]
        ), "Сообщение об ошибке не совпадает"

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    @allure.title("3. Если одного из полей нет, запрос возвращает ошибку 400")
    @allure.description(
        "Проверка, что создание курьера без одного из обязательных полей приводит к ошибке 400 и сообщению "
        "'Недостаточно данных для создания учетной записи'"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера с сгенерированными данными в Json файле без одного из полей"
    )
    def test_create_courier_missing_field(self, missing_field, create_courier):
        courier_data, _ = create_courier
        invalid_data = courier_data.copy()
        del invalid_data[missing_field]

        response = requests.post(f"{Url.BASE_URL}/courier", json=invalid_data)

        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии обязательного поля"
        assert (
            response.json() == expected_responses["courier"]["missing_field_error"]
        ), "Сообщение об ошибке не совпадает"

    @allure.title(
        "4. Чтобы создать курьера, нужно передать в ручку все обязательные поля"
    )
    @allure.description(
        "Проверка, что создание курьера без обязательного поля приводит к ошибке 400 "
        "с сообщением 'Недостаточно данных для создания учетной записи"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера и пробуем создать курьера только с логином и паролем"
    )
    def test_create_courier_partial_data(self, create_courier):
        courier_data, _ = create_courier
        partial_data = {
            "login": courier_data["login"],
            "password": courier_data["password"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)

        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии поля 'firstName'"

        # Пробуем создать курьера только с паролем и именем
        partial_data = {
            "password": courier_data["password"],
            "firstName": courier_data["firstName"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)

        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии поля 'login'"

        # Пробуем создать курьера только с логином и именем
        partial_data = {
            "login": courier_data["login"],
            "firstName": courier_data["firstName"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)

        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии поля 'password'"

    @allure.title(
        "5. Если создать пользователя с логином, который уже есть, возвращается ошибка."
    )
    @allure.description(
        "Проверка, что создание пользователя с существующим логином вызывает ошибку 409 "
        "с сообщением 'Этот логин уже используется'"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера с сгенерированными данными в Json файле, но с логином, который уже есть"
    )
    def test_create_courier_with_existing_login(self, create_courier):
        courier_data, _ = create_courier
        # Генерируем новый пароль и имя, но используем старый логин
        new_data = generate_random_courier_data()
        new_data["login"] = courier_data["login"]  # Используем старый логин

        response = requests.post(f"{Url.BASE_URL}/courier", json=new_data)

        assert (
            response.status_code == 409
        ), "Код ответа не 409 для логина, который уже используется"
        assert (
            response.json() == expected_responses["courier"]["duplicate_error"]
        ), "Сообщение об ошибке не совпадает"
