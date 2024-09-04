import pytest
import requests
from data.courier_generator_data import generate_random_courier_data
from data.url_data import Url

@pytest.fixture(scope="class")
def create_courier():
    courier_data = generate_random_courier_data()
    response = requests.post(f"{Url.BASE_URL}/courier", json=courier_data)
    assert response.status_code == 201, "Не удалось создать курьера в фикстуре"
    return courier_data, response.json()

@pytest.fixture(scope="class")
def courier_for_login(create_courier):
    courier_data, _ = create_courier
    response = requests.post(f"{Url.BASE_URL}/courier/login", json=courier_data)
    assert response.status_code == 200, "Не удалось авторизовать курьера в фикстуре"
    courier_data['id'] = response.json().get("id")
    return courier_data

@pytest.fixture(scope="class")
def courier_id_for_deletion(courier_for_login):
    return courier_for_login['id']
