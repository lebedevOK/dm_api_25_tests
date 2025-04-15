import requests


def test_put_v1_account_password():
    # Подготовка данных
    json_data = {
        'login': 'test_user',
        'token': 'reset-token',  # Токен из письма после сброса пароля
        'oldPassword': 'old_password',
        'newPassword': 'new_password'
    }
    headers = {
        'X-Dm-Auth-Token': 'auth-token'  # Токен авторизации
    }

    # Выполнение запроса
    response = requests.put(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/password',
        json=json_data,
        headers=headers
    )

    # Проверка ответа
    assert response.status_code == 200


def test_put_v1_account_password_wrong_old():
    # Подготовка данных с неверным старым паролем
    json_data = {
        'login': 'test_user',
        'oldPassword': 'wrong_password',
        'newPassword': 'new_password'
    }
    headers = {
        'X-Dm-Auth-Token': 'auth-token'
    }

    # Выполнение запроса
    response = requests.put(
        url='[http://5.63.153.31](http://5.63.153.31):5051/v1/account/password',
        json=json_data,
        headers=headers
    )

    # Проверка ответа
    assert response.status_code == 400
    assert response.json()['message'] == 'Password is incorrect'