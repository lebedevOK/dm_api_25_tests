import requests


def test_put_v1_account_email():
    # Подготовка данных
    json_data = {
        'login': 'test_user',
        'password': 'password',
        'email': 'new_email@test.com'
    }
    headers = {
        'X-Dm-Auth-Token': 'auth-token'
    }

    # Выполнение запроса
    response = requests.put(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/email',
        json=json_data,
        headers=headers
    )

    # Проверка ответа
    assert response.status_code == 200


def test_put_v1_account_email_invalid():
    # Подготовка данных с неверным форматом email
    json_data = {
        'login': 'test_user',
        'password': 'password',
        'email': 'invalid-email'
    }
    headers = {
        'X-Dm-Auth-Token': 'auth-token'
    }

    # Выполнение запроса
    response = requests.put(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/email',
        json=json_data,
        headers=headers
    )

    # Проверка ответа
    assert response.status_code == 400
    assert response.json()['message'] == 'Invalid email format'