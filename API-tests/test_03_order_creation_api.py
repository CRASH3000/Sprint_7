import requests
import allure
from data.url_data import Url

from data.order_test_data import (
    order_data_black,
    order_data_grey,
    order_data_both_colors,
    order_data_no_color,
)


@allure.suite("3. Создание заказа")
@allure.story("Создание заказа с разными цветами")
class TestOrderCreation:

    @allure.title("1. Можно создать заказ с черным цветом")
    @allure.description(
        "Отправляем POST-запрос на создание заказа. "
        "Проверяем, что заказ можно создать с черным цветом"
    )
    def test_create_order_with_black_color(self):
        response = requests.post(f"{Url.BASE_URL}/orders", json=order_data_black)

        assert response.status_code == 201, "Код ответа не 201"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит track"

    @allure.title("2. Можно создать заказ с серым цветом")
    @allure.description(
        "Отправляем POST-запрос на создание заказа. "
        "Проверяем, что заказ можно создать с серым цветом"
    )
    def test_create_order_with_grey_color(self):
        response = requests.post(f"{Url.BASE_URL}/orders", json=order_data_grey)

        assert response.status_code == 201, "Код ответа не 201"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит track"

    @allure.title("3. Можно создать заказ с черным и серым цветами")
    @allure.description(
        "Отправляем POST-запрос на создание заказа. "
        "Проверяем, что заказ можно создать с черным и серым цветами"
    )
    def test_create_order_with_both_colors(self):
        response = requests.post(f"{Url.BASE_URL}/orders", json=order_data_both_colors)

        assert response.status_code == 201, "Код ответа не 201"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит track"

    @allure.title("4. Можно создать заказ без указания цвета")
    @allure.description(
        "Отправляем POST-запрос на создание заказа. "
        "Проверяем, что заказ можно создать без указания цвета"
    )
    def test_create_order_without_color(self):
        response = requests.post(f"{Url.BASE_URL}/orders", json=order_data_no_color)

        assert response.status_code == 201, "Код ответа не 201"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит track"
