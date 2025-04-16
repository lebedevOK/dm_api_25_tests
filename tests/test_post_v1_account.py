import requests
from random import randint
import time
import json
import os


def test_post_v1_account():
    # Регистрация пользователя
    login = f'al{randint(1, 9999)}'
    password = '123456789'
    email = f"{login}@qw.ru"
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account',
        json=json_data
    )
    print(response.status_code)
    assert response.status_code == 201, f'Статус код ответа должен быть 201, но получен {response.status_code}'

    # Ждем 3 секунды
    time.sleep(3)

    # Получаем список писем
    response = requests.get(
        url='http://5.63.153.31:5025/api/v2/messages',
        params={'limit': 50}
    )
    assert response.status_code == 200
    print(response.status_code)
    print(response.json())

    # Ищем письмо с нашим логином и получаем токен
    for item in response.json()['items']:
        user_data = json.loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            break
    
    assert token, f'Не найдено письмо для логина {login}'
    print(f'Activation token: {token}')

    # Активация пользователя
    response = requests.put(
        url=f'http://5.63.153.31:5051/v1/account/{token}'
    )
    assert response.status_code == 200, f'Статус код ответа должен быть 200, но получен {response.status_code}'
    print(response.status_code)

    # Авторизация пользователя
    login_data = {
        'login': login,
        'password': password
    }
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account/login',
        json=login_data
    )
    assert response.status_code == 200, f'Статус код ответа должен быть 200, но получен {response.status_code}'
    print(response.status_code)
    print(email)
    print(password)

    # Записываем email пользователя в файл
    users_list_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utilities', 'users_list.txt')
    with open(users_list_path, 'a', encoding='utf-8') as f:
        f.write(f'{email}\n')


def test_post_v1_account_empty_login():
    # Подготовка данных с пустым логином
    json_data = {
        'login': '',
        'email': 'test@test.ru',
        'password': '123456789'
    }

    # Выполнение запроса
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account',
        json=json_data
    )

    # Проверка ответа
    assert response.status_code == 400, f'Статус код ответа должен быть 400, но получен {response.status_code}'
    assert response.json()['message'] == 'Login is required'


def test_post_v1_account_empty_email():
    # Подготовка данных с пустым email
    json_data = {
        'login': f'al{randint(1, 999)}',
        'email': '',
        'password': '123456789'
    }

    # Выполнение запроса
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account',
        json=json_data
    )

    # Проверка ответа
    assert response.status_code == 400, f'Статус код ответа должен быть 400, но получен {response.status_code}'
    assert response.json()['message'] == 'Email is required'


def test_post_v1_account_empty_password():
    # Подготовка данных с пустым паролем
    json_data = {
        'login': f'al{randint(1, 999)}',
        'email': 'test@test.ru',
        'password': ''
    }

    # Выполнение запроса
    response = requests.post(
        url='http://5.63.153.31:5051/v1/account',
        json=json_data
    )

    # Проверка ответа
    assert response.status_code == 400, f'Статус код ответа должен быть 400, но получен {response.status_code}'
    assert response.json()['message'] == 'Password is required'
