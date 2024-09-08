import pytest
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

        courier_id = response.json().get("id")
        if courier_id:
            delete_courier.append(courier_id)

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

    @allure.description(
        "Отправляем POST-запрос на создание курьера с различными комбинациями неполных данных, и проверяем что:"
        "Если переданы обязательные поля (логин) и (пароль), курьер создается успешно, в противном случаи возвращается "
        "ошибка"
    )
    @pytest.mark.parametrize(
        "test_number, courier_data_source, partial_data, data_combination, expected_response",
        [
            (
                3,
                "generate_random_courier_data",
                {"login": "login", "password": "password"},
                "имени",
                "create_success",
            ),
            (
                4,
                "create_courier",
                {"password": "password", "firstName": "firstName"},
                "логина",
                "missing_field_error",
            ),
            (
                5,
                "create_courier",
                {"login": "login", "firstName": "firstName"},
                "пароля",
                "missing_field_error",
            ),
        ],
    )
    def test_create_courier_with_incomplete_data(
        self,
        request,
        delete_courier,
        test_number,
        courier_data_source,
        partial_data,
        data_combination,
        expected_response,
    ):

        # Генерация курьера или использование фикстуры в зависимости от параметров
        if courier_data_source == "generate_random_courier_data":
            courier_data = generate_random_courier_data()
        else:
            courier_data = request.getfixturevalue(courier_data_source)

        # Динамический заголовок для Allure
        allure.dynamic.title(f"{test_number}. Создания курьера без {data_combination}")

        for key, value in partial_data.items():
            partial_data[key] = courier_data.get(key, value)

        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)

        assert response.json() == expected_responses["courier"][expected_response]

        if expected_response == "create_success":
            courier_id = response.json().get("id")
            if courier_id:
                delete_courier.append(courier_id)

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
