import requests
from uuid import uuid4


def test_put_v1_account_token():
    # Подготовка данных
    token = str(uuid4())

    # Выполнение запроса
    response = requests.put(
        url=f'[http://5.63.153.31](http://5.63.153.31):5051/v1/account/{token}'
    )

    # Проверка ответа
    assert response.status_code == 200


def test_put_v1_account_token_invalid():
    # Подготовка данных
    token = 'invalid-token'

    # Выполнение запроса
    response = requests.put(
        url=f'[http://5.63.153.31](http://5.63.153.31):5051/v1/account/{token}'
    )

    # Проверка ответа
    assert response.status_code == 400