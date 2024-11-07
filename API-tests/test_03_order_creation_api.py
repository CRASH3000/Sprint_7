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

    @allure.description(
        "Отправляем POST-запрос на создание заказа с разными цветами и проверяем, что заказ создан"
    )
    @pytest.mark.parametrize(
        "test_number, order_data, color_description",
        [
            (1, order_data_black, "черным цветом"),
            (2, order_data_grey, "серым цветом"),
            (3, order_data_both_colors, "черным и серым цветами"),
            (4, order_data_no_color, "без указания цвета"),
        ],
    )
    def test_create_order_with_various_colors(
        self, test_number, order_data, color_description
    ):
        response = requests.post(f"{Url.BASE_URL}/orders", json=order_data)

        allure.dynamic.title(
            f"{test_number}: Можно создать заказ с {color_description}"
        )

        assert response.status_code == 201, "Код ответа не 201"
        response_data = response.json()
        assert "track" in response_data, "Ответ не содержит track"
