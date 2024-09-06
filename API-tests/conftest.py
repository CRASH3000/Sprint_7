import pytest
import requests
from data.courier_generator_data import generate_random_courier_data
from data.url_data import Url


@pytest.fixture(scope="function")
def create_courier():
    courier_data = generate_random_courier_data()

    response = requests.post(f"{Url.BASE_URL}/courier", json=courier_data)
    if response.status_code != 201:
        raise RuntimeError(f"Не удалось создать курьера: {response.status_code}, {response.json()}")

    return courier_data

@pytest.fixture(scope="function")
def append_courier_id_for_delete(delete_courier, create_courier):
    courier_data = create_courier()

    courier_id = courier_data.get("id")

    if courier_id:
        courier_data.append(delete_courier)  # Добавляем ID курьера для последующего удаления

    return courier_data  # Возвращаем данные курьера для дальнейшего использования

@pytest.fixture(scope="function")
def delete_courier():
    created_courier_ids = []

    yield created_courier_ids  # Возвращаем список для записи ID созданных курьеров

    # Удаление всех созданных курьеров после завершения теста
    for courier_id in created_courier_ids:
        delete_response = requests.delete(f"{Url.BASE_URL}/courier/{courier_id}")
        if delete_response.status_code != 200:
            raise RuntimeError(f"Не удалось удалить курьера с ID {courier_id}: {delete_response.status_code}, {delete_response.json()}")

@pytest.fixture(scope="function")
def courier_for_login(create_courier):
    courier_data = create_courier
    response = requests.post(f"{Url.BASE_URL}/courier/login", json=courier_data)

    courier_data['id'] = response.json().get("id")
    return courier_data

@pytest.fixture(scope="function")
def courier_id_for_deletion(courier_for_login):
    return courier_for_login['id']
