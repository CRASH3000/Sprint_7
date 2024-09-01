import random
import string

def generate_random_courier_data():
    """Генерирует случайные данные для курьера"""

    def generate_random_string(length):
        characters = string.ascii_letters + string.digits  # Используем и буквы, и цифры
        return ''.join(random.choice(characters) for _ in range(length))

    # Генерируем случайные логин, пароль и имя
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # Формируем и возвращаем словарь с данными Json
    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }