import requests


def test_post_v1_account_login():
    # Подготовка данных
    json_data = {
        'login': 'test_user',
        'password': 'password',
        'rememberMe': True
    }

    # Выполнение запроса
    response = requests.post(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/login',
        json=json_data
    )

    # Проверка ответа
    assert response.status_code == 200
    assert 'token' in response.json()


def test_post_v1_account_login_wrong_password():
    # Подготовка данных с неверным паролем
    json_data = {
        'login': 'test_user',
        'password': 'wrong_password',
        'rememberMe': False
    }

    # Выполнение запроса
    response = requests.post(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/login',
        json=json_data
    )

    # Проверка ответа
    assert response.status_code == 400
    assert response.json()['message'] == 'Invalid login or password'