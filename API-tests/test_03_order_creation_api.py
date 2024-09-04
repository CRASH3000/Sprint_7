import pytest
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

    @allure.title("1. Можно создать заказ с разными цветами")
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

        assert response.status_code == 201, "Код ответа не 201"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит track"
