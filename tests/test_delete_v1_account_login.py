import requests


def test_delete_v1_account_login():
    # Подготовка данных
    headers = {
        'X-Dm-Auth-Token': 'auth-token'
    }

    # Выполнение запроса
    response = requests.delete(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/login',
        headers=headers
    )

    # Проверка ответа
    assert response.status_code == 204


def test_delete_v1_account_login_no_auth():
    # Выполнение запроса без токена авторизации
    response = requests.delete(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/login'
    )

    # Проверка ответа
    assert response.status_code == 401
    assert response.json()['message'] == 'Auth token not found'