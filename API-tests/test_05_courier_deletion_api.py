import requests
import allure
from data.url_data import Url
from data.expected_responses import expected_responses
from data.account_test_data import incorrect_id


@allure.suite("5. Удалить курьера")
@allure.story("Тестирование функционала удаления курьера")
class TestCourierDeletionAPI:

    @allure.title("1. Удаление курьера")
    @allure.description(
        "Отправляем DELETE-запрос на удаление курьера с ID."
        "Проверяем, что курьера можно удалить и ответом приходит код 200 и 'ok': True"
    )
    def test_delete_courier(self, courier_id_for_deletion):
        response = requests.delete(f"{Url.BASE_URL}/courier/{courier_id_for_deletion}")

        assert response.status_code == 200, "Курьер не был успешно удален"
        assert response.json() == {
            "ok": True
        }, "Ответ не соответствует ожидаемому после удаления"

    @allure.title("2. Если отправить запрос без id, вернётся ошибка")
    @allure.description(
        "Отправляем DELETE-запрос без ID. " "Проверяем, что система вернёт ошибку 400"
    )
    def test_delete_courier_with_id(self):
        response = requests.delete(f"{Url.BASE_URL}/courier/")

        assert (
            response.json() == expected_responses["delete_courier"]["without_id_error"]
        )

    @allure.title("3. Если отправить запрос с несуществующим id, вернётся ошибка.")
    @allure.description(
        "Отправляем DELETE-запрос на удаление курьера с несуществующим ID."
        "Проверяем, что система вернёт ошибку 404"
    )
    def test_delete_courier_with_nonexistent_id(self):
        courier_id = incorrect_id["id"]
        response = requests.delete(f"{Url.BASE_URL}/courier/{courier_id}")

        assert (
            response.json()
            == expected_responses["delete_courier"]["nonexistent_id_error"]
        )
