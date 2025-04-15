import requests


def test_get_v1_account():
    # Подготовка данных
    token = 'token'  # Нужно получить токен из метода логина
    headers = {
        'X-Dm-Auth-Token': token
    }

    # Выполнение запроса
    response = requests.get(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account',
        headers=headers
    )

    # Проверка ответа
    assert response.status_code == 200


def test_get_v1_account_no_token():
    # Выполнение запроса без токена
    response = requests.get(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account'
    )

    # Проверка ответа
    assert response.status_code == 400
    assert response.json()['message'] == 'Auth token not found'