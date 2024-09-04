import pytest
import requests
import allure
from data.url_data import Url
from data.expected_responses import expected_responses


@allure.suite("5. Удалить курьера")
@allure.story("Тестирование функционала удаления курьера")
@pytest.mark.usefixtures("create_courier")
class TestCourierDeletionAPI:

    @allure.title("1. Удаление курьера")
    @allure.description(
        "Проверка, что курьера можно удалить и ответом приходит код 200 и 'ok': True"
    )
    @allure.step(
        "Отправляем DELETE-запрос на удаление курьера с ID, который мы получили во время авторизации"
    )
    def test_delete_courier(self, courier_id_for_deletion):
        response = requests.delete(f"{Url.BASE_URL}/courier/{courier_id_for_deletion}")
        assert response.status_code == 200, "Курьер не был успешно удален"
        assert response.json() == {
            "ok": True
        }, "Ответ не соответствует ожидаемому после удаления"

    @allure.title("2. Если отправить запрос без id, вернётся ошибка")
    @allure.description(
        "Проверка, что система вернёт ошибку, если не указать ID курьера"
    )
    @allure.step("Отправляем DELETE-запрос на удаление курьера без ID")
    def test_delete_courier_without_id(self):
        response = requests.delete(f"{Url.BASE_URL}/courier/")
        assert response.status_code == 400, "Код ответа не 400 при отсутствии ID"
        assert (
            response.json() == expected_responses["delete_courier"]["without_id_error"]
        ), "Сообщение об ошибке не совпадает"

    @allure.title("3. Если отправить запрос с несуществующим id, вернётся ошибка.")
    @allure.description(
        "Проверка, что система вернёт ошибку, если указать несуществующий ID курьера"
    )
    @allure.step("Отправляем DELETE-запрос на удаление курьера с несуществующим ID")
    def test_delete_courier_with_nonexistent_id(self, courier_id_for_deletion):
        response = requests.delete(f"{Url.BASE_URL}/courier/{courier_id_for_deletion}")
        assert (
            response.status_code == 404
        ), "Код ответа не 404 при удалении несуществующего ID"
        assert (
            response.json()
            == expected_responses["delete_courier"]["nonexistent_id_error"]
        ), "Сообщение об ошибке не совпадает"
