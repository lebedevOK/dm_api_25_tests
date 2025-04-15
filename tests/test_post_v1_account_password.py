import requests


def test_post_v1_account_password():
    # Подготовка данных
    json_data = {
        'login': 'test_user',
        'email': 'test@test.com'
    }

    # Выполнение запроса
    response = requests.post(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/password',
        json=json_data
    )

    # Проверка ответа
    assert response.status_code == 200


def test_post_v1_account_password_invalid_email():
    # Подготовка данных
    json_data = {
        'login': 'test_user',
        'email': 'invalid-email'
    }

    # Выполнение запроса
    response = requests.post(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/password',
        json=json_data
    )

    # Проверка ответа
    assert response.status_code == 400