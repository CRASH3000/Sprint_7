import pytest
import requests
import allure
from data.courier_generator_data import generate_random_courier_data
from data.url_data import Url

from data.order_test_data import (
    order_data_black,
    order_data_grey,
    order_data_both_colors,
    order_data_no_color,
)


class TestCourierAPI:

    @classmethod
    def setup_class(cls):
        """Метод, который выполняется один раз перед запуском всех тестов в классе"""
        cls.courier_data = generate_random_courier_data()

    @allure.feature("Создание курьера")
    @allure.story("1. Создание курьера")
    @allure.description(
        "Проверка, что курьера можно создать и ответом приходит код 201 и 'ok': True"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера с генирированными данными в Json файле"
    )
    def test_create_courier(self):
        response = requests.post(f"{Url.BASE_URL}/courier", json=self.courier_data)
        print(f"Статус после создания курьера в setup_class: {response.status_code}")

        assert response.status_code == 201, "Не удалось создать курьера в setup_class"
        assert response.json() == {
            "ok": True
        }, "Первичный запрос на создание курьера вернул некорректный ответ"
        print(f"Курьер создан: {self.courier_data}")

    @allure.feature("Создание курьера")
    @allure.story("2. Нельзя создать двух одинаковых курьеров")
    @allure.description(
        "Проверка, что нельзя создать двух одинаковых курьеров и ответом приходит "
        "код 409 и сообщение об ошибке'Этот логин уже используется'"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера с ранее сгенерированными данными снова"
    )
    def test_create_duplicate_courier(self):
        response = requests.post(f"{Url.BASE_URL}/courier", json=self.courier_data)
        print(
            f"Статус после попытки создания дубликата курьера: {response.status_code}"
        )

        assert response.status_code == 409, "Код ответа не 409 для повторного логина"
        assert (
            response.json().get("message") == "Этот логин уже используется"
        ), "Сообщение об ошибке не совпадает"

    @pytest.mark.parametrize("missing_field", [("login"), ("password"), ("firstName")])
    @allure.feature("Создание курьера")
    @allure.story(
        "3. Чтобы создать курьера, нужно передать в ручку все обязательные поля"
    )
    @allure.description(
        "Проверка, что создание курьера без обязательного поля приводит к ошибке 400 "
        "с сообщением 'Недостаточно данных для создания учетной записи"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера с генирированными данными в Json файле без одного из полей"
    )
    def test_create_courier_missing_field(self, missing_field):
        invalid_data = self.courier_data.copy()
        del invalid_data[missing_field]

        response = requests.post(f"{Url.BASE_URL}/courier", json=invalid_data)
        print(
            f"Статус после попытки создания курьера с отсутствующим полем '{missing_field}': {response.status_code}"
        )

        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии обязательного поля"
        assert (
            response.json().get("message")
            == "Недостаточно данных для создания учетной записи"
        ), "Сообщение об ошибке не совпадает"

    @allure.feature("Создание курьера")
    @allure.story(
        "4. Чтобы создать курьера, нужно передать в ручку все обязательные поля"
    )
    @allure.description(
        "Проверка, что создание курьера без обязательного поля приводит к ошибке 400 "
        "с сообщением 'Недостаточно данных для создания учетной записи"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера и пробуем создать курьера только с логином и паролем"
    )
    def test_create_courier_partial_data(self):
        partial_data = {
            "login": self.courier_data["login"],
            "password": self.courier_data["password"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)
        print(
            f"Статус после попытки создания курьера без 'firstName': {response.status_code}"
        )
        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии поля 'firstName'"

        # Пробуем создать курьера только с паролем и именем
        partial_data = {
            "password": self.courier_data["password"],
            "firstName": self.courier_data["firstName"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)
        print(
            f"Статус после попытки создания курьера без 'login': {response.status_code}"
        )
        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии поля 'login'"

        # Пробуем создать курьера только с логином и именем
        partial_data = {
            "login": self.courier_data["login"],
            "firstName": self.courier_data["firstName"],
        }
        response = requests.post(f"{Url.BASE_URL}/courier", json=partial_data)
        print(
            f"Статус после попытки создания курьера без 'password': {response.status_code}"
        )
        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии поля 'password'"

    @allure.feature("Создание курьера")
    @allure.story(
        "5. Если создать пользователя с логином, который уже есть, возвращается ошибка."
    )
    @allure.description(
        "Проверка, что создание пользователя с существующим логином вызывает ошибку 409 "
        "с сообщением 'Этот логин уже используется'"
    )
    @allure.step(
        "Отправляем POST-запрос на создание курьера с генирированными данными в Json файле, но с логином, который уже есть"
    )
    def test_create_courier_with_existing_login(self):
        # Генерируем новый пароль и имя, но используем старый логин
        new_data = generate_random_courier_data()
        new_data["login"] = self.courier_data["login"]  # Используем старый логин

        response = requests.post(f"{Url.BASE_URL}/courier", json=new_data)
        print(
            f"Статус после попытки создания курьера с существующим логином: {response.status_code}"
        )

        assert (
            response.status_code == 409
        ), "Код ответа не 409 для логина, который уже используется"
        assert (
            response.json().get("message") == "Этот логин уже используется"
        ), "Сообщение об ошибке не совпадает"


class TestCourierLoginAPI:

    @classmethod
    def setup_class(cls):
        """Используем данные из TestCourierAPI"""
        # Убедимся, что курьер был создан
        TestCourierAPI.setup_class()  # Явно вызываем setup_class из TestCourierAPI

        # Выводим данные созданного курьера
        print(f"Данные курьера для авторизации: {TestCourierAPI.courier_data}")

        # Проверяем, что курьер действительно был создан
        response = requests.post(
            f"{Url.BASE_URL}/courier", json=TestCourierAPI.courier_data
        )
        if response.status_code != 201:
            print("Курьер уже существует или не может быть создан снова.")

        cls.courier_data = TestCourierAPI.courier_data

    @allure.feature("Логин курьера")
    @allure.story("1. Курьер может авторизоваться")
    @allure.description(
        "Проверка, что курьер может авторизоваться и успешный запрос возвращает id"
    )
    @allure.step(
        "Отправляем POST-запрос на авторизацию курьера с логином и паролем, которые мы получили при создании курьера"
    )
    def test_courier_can_login(self):

        response = requests.post(
            f"{Url.BASE_URL}/courier/login",
            json={
                "login": self.courier_data["login"],
                "password": self.courier_data["password"],
            },
        )
        print(f"Статус после авторизации курьера: {response.status_code}")
        assert response.status_code == 200, "Код ответа не 200 при успешной авторизации"
        assert "id" in response.json(), "Ответ не содержит id"

        # Сохранение ID курьера
        self.__class__.courier_id = response.json()["id"]

    @allure.feature("Логин курьера")
    @allure.story("2. Для авторизации нужно передать все обязательные поля")
    @allure.description("Проверка, что система вернёт ошибку, если какого-то поля нет")
    @allure.step(
        "Отправляем POST-запрос на авторизацию курьера с логином и паролем, которые мы получили при создании курьера"
    )
    @pytest.mark.parametrize("missing_field", [("login"), ("password")])
    def test_login_missing_field(self, missing_field):
        invalid_data = self.courier_data.copy()
        del invalid_data[missing_field]

        response = requests.post(f"{Url.BASE_URL}/courier/login", json=invalid_data)
        print(
            f"Статус после попытки авторизации без поля '{missing_field}': {response.status_code}"
        )
        assert (
            response.status_code == 400
        ), "Код ответа не 400 при отсутствии обязательного поля"
        assert (
            response.json().get("message") == "Недостаточно данных для входа"
        ), "Сообщение об ошибке не совпадает"

    @allure.feature("Логин курьера")
    @allure.story("3. Система вернёт ошибку, если неправильно указать логин или пароль")
    @allure.description(
        "Проверка, что система вернёт ошибку, если неправильно указать логин или пароль"
    )
    @allure.step(
        "Отправляем POST-запрос на авторизацию курьера с неправильными данными"
    )
    def test_login_with_incorrect_credentials(self):
        invalid_data = {"login": "wrong_login", "password": "wrong_password"}

        response = requests.post(f"{Url.BASE_URL}/courier/login", json=invalid_data)
        print(
            f"Статус после попытки авторизации с неправильными данными: {response.status_code}"
        )
        assert (
            response.status_code == 404
        ), "Код ответа не 404 при неправильных учетных данных"
        assert (
            response.json().get("message") == "Учетная запись не найдена"
        ), "Сообщение об ошибке не совпадает"

    @allure.feature("Логин курьера")
    @allure.story(
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
        print(
            f"Статус после попытки авторизации под несуществующим пользователем: {response.status_code}"
        )
        assert (
            response.status_code == 404
        ), "Код ответа не 404 при попытке авторизации несуществующего пользователя"
        assert (
            response.json().get("message") == "Учетная запись не найдена"
        ), "Сообщение об ошибке не совпадает"


class TestCourierDeletionAPI:

    @classmethod
    def setup_class(cls):
        """Получаем courier_id из TestCourierLoginAPI"""
        cls.courier_id = TestCourierLoginAPI.courier_id

    @allure.feature("Удалить курьера")
    @allure.story("1. Удаление курьера")
    @allure.description(
        "Проверка, что курьера можно удалить и ответом приходит код 200 и 'ok': True"
    )
    @allure.step(
        "Отправляем DELETE-запрос на удаление курьера с ID, который мы получили во время авторизации"
    )
    def test_delete_courier(self):
        response = requests.delete(f"{Url.BASE_URL}/courier/{self.courier_id}")
        print(f"Статус после удаления курьера: {response.status_code}")
        assert response.status_code == 200, "Курьер не был успешно удален"
        assert response.json() == {
            "ok": True
        }, "Ответ не соответствует ожидаемому после удаления"

    @allure.feature("Удалить курьера")
    @allure.story("2. Если отправить запрос без id, вернётся ошибка")
    @allure.description(
        "Проверка, что система вернёт ошибку, если не указать ID курьера"
    )
    @allure.step("Отправляем DELETE-запрос на удаление курьера без ID")
    def test_delete_courier_without_id(self):
        response = requests.delete(f"{Url.BASE_URL}/courier/")
        print(f"Статус после попытки удаления без ID: {response.status_code}")
        assert response.status_code == 400, "Код ответа не 400 при отсутствии ID"
        assert (
            response.json().get("message") == "Недостаточно данных для удаления курьера"
        ), "Сообщение об ошибке не совпадает"

    @allure.feature("Удалить курьера")
    @allure.story("2. Если отправить запрос с несуществующим id, вернётся ошибка.")
    @allure.description(
        "Проверка, что система вернёт ошибку, если указать несуществующий ID курьера"
    )
    @allure.step("Отправляем DELETE-запрос на удаление курьера с несуществующим ID")
    def test_delete_courier_with_nonexistent_id(self):
        response = requests.delete(f"{Url.BASE_URL}/courier/{self.courier_id}")
        print(
            f"Статус после попытки удаления несуществующего курьера: {response.status_code}"
        )
        assert (
            response.status_code == 404
        ), "Код ответа не 404 при удалении несуществующего ID"
        assert (
            response.json().get("message") == "Курьера с таким id нет"
        ), "Сообщение об ошибке не совпадает"


class TestOrderCreation:

    @allure.feature("Создание заказа")
    @allure.story("1. Можно создать заказ с разными цветами")
    @allure.description("Проверка, что заказ можно создать с разными цветами")
    @allure.step(
        "Отправляем DELETE-запрос на удаление курьера с ID, который мы получили во время авторизации"
    )
    @pytest.mark.parametrize(
        "order_data",
        [
            order_data_black,
            order_data_grey,
            order_data_both_colors,
            order_data_no_color,
        ],
    )
    def test_create_order_with_various_colors(self, order_data):
        response = requests.post(f"{Url.BASE_URL}/orders", json=order_data)

        print(f"Request Data: {order_data}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        assert response.status_code == 201, "Код ответа не 201"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит track"


class TestGetOrders:

    @allure.feature("Список заказов")
    @allure.story("1. Можно получить список всех заказов")
    @allure.description("Проверь, что в тело ответа возвращается список заказов.")
    @allure.step("Отправляем GET-запрос на получение списка заказов")
    def test_get_orders_list(self):
        response = requests.get(f"{Url.BASE_URL}/orders")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")

        assert response.status_code == 200, "Код ответа не 200"
        response_data = response.json()

        assert "orders" in response_data, "Ответ не содержит ключ 'orders'"
        assert isinstance(
            response_data["orders"], list
        ), "Ключ 'orders' не является списком"
        assert len(response_data["orders"]) > 0, "Список заказов пуст"
