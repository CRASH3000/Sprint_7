import requests
import allure
from data.url_data import Url


@allure.suite("4. Список заказов")
@allure.story("Тестирование функционала получения списка заказов")
class TestGetOrders:

    @allure.title("Можно получить список всех заказов")
    @allure.description(
        "Отправляем GET-запрос на получение списка заказов."
        "Проверяем, что в тело ответа возвращается список заказов."
    )
    def test_get_orders_list(self):
        response = requests.get(f"{Url.BASE_URL}/orders")

        assert response.status_code == 200, "Код ответа не 200"
        response_data = response.json()

        assert "orders" in response_data, "Ответ не содержит ключ 'orders'"
        assert isinstance(
            response_data["orders"], list
        ), "Ключ 'orders' не является списком"
        assert len(response_data["orders"]) > 0, "Список заказов пуст"
